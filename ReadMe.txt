# 🐧 Linux Command Trainer

**Linux Command Trainer** is a desktop quiz application built with **Python** and **CustomTkinter**. Test your knowledge of Linux commands with adaptive questions, scoring, and progress tracking. Questions are stored in an external JSON file, making it easy to add or edit them without touching the code.

---

## Features
- Adaptive question selection based on past performance  
- Score tracking with a progress bar  
- Filter questions by **category** and **difficulty**  
- External JSON file for questions (`questions.json`)  
- No timer – answer at your own pace  

---

## Requirements
- Python 3.10+  
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)  

Install dependencies:
```bash
pip install customtkinter

---

How to Run
Option 1 – Run from Python
Clone the repository or download the files.
Ensure questions.json is in the same folder as linux_trainer.py.
Run the app:
python linux_trainer.py

---

Option 2 – Build a Standalone EXE
You can create a Windows executable (.exe) so the app runs without Python installed:
Ensure questions.json is in the project folder alongside linux_trainer.py.
Install PyInstaller:
pip install pyinstaller


Build the EXE:
python -m PyInstaller --onefile --console --add-data "questions.json;." linux_trainer.py