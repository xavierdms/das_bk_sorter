import os
import subprocess
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET
import shutil
import sys
from PySide2 import QtWidgets, QtGui, QtCore

class App(QtWidgets.QWidget):

    def write_settings(self):
        settings = QtCore.QSettings("DAS Sorter")

        settings.setValue("saves_path", self.saves_path)
        settings.setValue("editor_path", self.editor_path)
        settings.setValue("bk_path", self.bk_path)

    def read_settings(self):
        settings = QtCore.QSettings("DAS Sorter")

        self.saves_path = settings.value("saves_path")
        self.editor_path = settings.value("editor_path")
        self.bk_path = settings.value("bk_path")

    def browse_saves(self):
        saves_path = QtWidgets.QFileDialog.getExistingDirectory(None, caption="Saves path:")
        self.saves_line.setText(saves_path)
        self.saves_path = saves_path

    def browse_editor(self):
        editor_path = QtWidgets.QFileDialog.getOpenFileName(self, caption="das_editor.exe file:", filter="Executable files (*.exe)")
        self.editor_line.setText(str(editor_path[0]))
        self.editor_path = str(editor_path[0])

    def browse_bk(self):
        bk_path = QtWidgets.QFileDialog.getExistingDirectory(None, caption="Backup path:")
        self.bk_line.setText(bk_path)
        self.bk_path = bk_path

    def __init__(self):
        super().__init__()
        
        # gui window setup
        self.setMinimumSize(QtCore.QSize(450,320))
        self.setMaximumWidth(450)
        self.setWindowTitle("DAS Sorter") 

        settings = QtCore.QSettings("DAS Sorter")
        self.read_settings()

        # saves path
        self.saves_loc_text = QtWidgets.QLabel(self)
        self.saves_loc_text.setText("DAI saves folder:")
        self.saves_loc_text.move(22,20)
        
        self.saves_line = QtWidgets.QLineEdit(self)
        self.saves_line.resize(300,30)
        self.saves_line.move(22,45)
        self.saves_line.setText(settings.value("saves_path"))

        self.saves_button = QtWidgets.QPushButton("Browse",self)
        self.saves_button.clicked.connect(self.browse_saves)
        self.saves_button.resize(100,31)
        self.saves_button.move(330,45)

        # das_editor path
        self.editor_loc_text = QtWidgets.QLabel(self)
        self.editor_loc_text.setText("das_editor.exe file:")
        self.editor_loc_text.move(22,100)

        self.editor_line = QtWidgets.QLineEdit(self)
        self.editor_line.resize(300,30)
        self.editor_line.move(22,125)
        self.editor_line.setText(settings.value("editor_path"))

        self.editor_button = QtWidgets.QPushButton("Browse",self)
        self.editor_button.clicked.connect(self.browse_editor)
        self.editor_button.resize(100,31)
        self.editor_button.move(330,125)

        # backup path
        self.bk_loc_text = QtWidgets.QLabel(self)
        self.bk_loc_text.setText("Choose where to back up your sorted saves:")
        self.bk_loc_text.move(22,180)
        
        self.bk_line = QtWidgets.QLineEdit(self)
        self.bk_line.resize(300,30)
        self.bk_line.move(22,205)
        self.bk_line.setText(settings.value("bk_path"))

        self.bk_button = QtWidgets.QPushButton("Browse",self)
        self.bk_button.clicked.connect(self.browse_bk)
        self.bk_button.resize(100,31)
        self.bk_button.move(330,205)

        # run app button
        self.bk_button = QtWidgets.QPushButton("Sort save files", self)
        self.bk_button.clicked.connect(self.run_sorter)
        self.bk_button.resize(410,40)
        self.bk_button.move(20,260)
        
        # progress text area
        self.progress = QtWidgets.QTextEdit(self)
        self.progress.setReadOnly(True)
        self.progress_height = 0
        self.progress.resize(410, self.progress_height)
        self.progress.move(20,320)

    def run_sorter(self):

        das_path = self.saves_path                                      # DAI saves path
        daseditor_dir = self.editor_path                                # das_editor.exe path
        das_bk_dir = self.bk_path                                       # Saves backup path

        self.write_settings()                                           # save app settings

        save_lists = defaultdict(list)                                  # define and populate dict of save lists

        for filename in os.listdir(das_path):
            if filename.endswith(".DAS"):
                save_char = (os.path.join(das_path, filename))
                save_char_code_temp = (save_char[-12:])
                save_char_code = (save_char_code_temp[:8])
                save_lists[save_char_code].append(save_char)
        
        self.progress.append("Running sorter... \n")
        self.setMinimumHeight(420)

        for k, v in save_lists.items():
            curr_char = save_lists[k][0]                                # grab first save on a list
            p = subprocess.Popen([daseditor_dir, curr_char],            # open with das_editor.exe
                stdout=subprocess.PIPE, 
                stdin=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
            p.communicate(input=b'4')[0]                                # create xml file

            root = ET.parse('xml_file01.xml').getroot()                 # parse xml file for character name
            for type_tag in root.findall('charinfo'):
                chara_name = type_tag.get('name')
                self.progress.append("Sorting saves for: " + chara_name)
                self.progress_height = self.progress_height + 30
                self.progress.resize(410, self.progress_height)
                
            das_bk_dir_chara = os.path.join(das_bk_dir, chara_name)     # update bk path with character name folder
            Path(das_bk_dir_chara).mkdir(parents=True, exist_ok=True)   # create folder

            for item in save_lists[k]:
                shutil.copy(item, das_bk_dir_chara)

            os.remove('xml_file01.xml')                                 # remove file, needed to generate new for next chara

        os.remove('xml_file02.xml')                                     # remove extra file

        self.progress.append("\nDone.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = App()
    mainWin.show()
    
    sys.exit( app.exec_() )