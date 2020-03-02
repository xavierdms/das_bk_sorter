# das-sorter-script
Python script to sort .DAS save files by character
* Gets files from game's local save folder
* Copies them into a backup location, sorted into folders by character name
    * Running script after creating new save will add it to backup
    * Running script after deleting saves in game (or directly from game's save folder) will not delete it from backup

Note: used Python 3.7.x, needs changes to work with 3.8.1


### External Libraries Used

#### [Qt for Python](https://doc.qt.io/qtforpython)
```
pip install PySide2
```

#### [PyInstaller](http://www.pyinstaller.org/)
```
pip install pyinstaller
```

To create exe file from script:
```
pyinstaller --windowed --onefile das_sorter.py
```