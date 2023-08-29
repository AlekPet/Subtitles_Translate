# Subtitles_Translate
Translate subtitles from folder to other languages

Make enviroment, activate and install requirements modules
Open cmd from folder where your project will placed, and run
Windows:
```
[1] python -m venv venv (or python -m venv venv path_to_folder_project)
[2] .\venv\Scripts\activate.bat
[3] pip install -r requirements.txt
[4] python subtitles_translate.py
```

# NO CLI (cmd/bat file):
```
@echo off
CALL ".\venv\Scripts\activate.bat"
python subtitles_translate.py --no-cli
pause
```
# Support commands:
```
usage: subtitles_translate.py [-h] [--cli | --no-cli] [--tS TRANS_SRC] [--tT TRANS_TO] [--la | --no-la]
                              [--p PATH_PROCCESS] [--sl TIME_SLEEP] [--al AFTER_LINES]

Translate subtitles

optional arguments:
  -h, --help         show this help message and exit
  --cli, --no-cli    Use interface
  --tS TRANS_SRC     Source language (empty detect language auto)
  --tT TRANS_TO      Translate to language
  --la, --no-la      List support languages
  --p PATH_PROCCESS  Path to srt files
  --sl TIME_SLEEP    Sleep tim in seconds
  --al AFTER_LINES   Sleep program after line
```
