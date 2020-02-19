import os
import subprocess
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET
import shutil

# DAI saves path
das_path = os.getlogin() + "/Documents/BioWare/Dragon Age Inquisition/Save"
das_path = os.path.join('C:/Users/', das_path)

# das_editor.exe path
daseditor_dir = "D://Modding//DAITools//DAISaveGameEditor//das_editor"

# Saves backup path
das_bk_dir = os.getlogin() + "//Documents//Google Drive//⭐️//Game BKs"
das_bk_dir = os.path.join('C://Users//', das_bk_dir)

#define and populate dict of save lists
save_lists = defaultdict(list)

for filename in os.listdir(das_path):
    if filename.endswith(".DAS"):
        save_char = (os.path.join(das_path, filename))
        testfile = save_char
        save_char_code_temp = (save_char[-12:])
        save_char_code = (save_char_code_temp[:8])
        save_lists[save_char_code].append(save_char)


#for every k,v pair in savelists
for k, v in save_lists.items():
    #grab first save on a list
    curr_char = save_lists[k][0]
    # open that save with das_editor.exe and create xml file
    p = subprocess.Popen([daseditor_dir, curr_char], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.communicate(input=b'4')[0]

    #parse xml file for character name
    root = ET.parse('xml_file01.xml').getroot()
    for type_tag in root.findall('charinfo'):
        chara_name = type_tag.get('name')
        print("Sorting saves for: " + chara_name)
        
    # update bk path with character name folder
    das_bk_dir_chara = os.path.join(das_bk_dir, chara_name)

    # create folder with character name
    Path(das_bk_dir_chara).mkdir(parents=True, exist_ok=True)

    for item in save_lists[k]:
        shutil.copy(item, das_bk_dir_chara)

    #remove file so subprocess will generate new for next character
    os.remove('xml_file01.xml')

#remove extra file
os.remove('xml_file02.xml')