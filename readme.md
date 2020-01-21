# Skin Tone Checker

A small desktop application which can be used to check the accuracy of skin tones. The app also provides basic hints as to what is wrong with the tone.

---

## Features and Usage

### Colour Check
- Click anywhere on the application and drag to analyse colours on screen.
- The picker uses an average of nearby colours rather than a single point.
- Basic stats and a description are displayed to help indicate skin tone problems.

### Colour Watch
- Drag the eye dropper tool to place the watcher marker on screen.
- The colour at the marked position will be watched while the user can update settings in real time.
- Click anywhere on screen to disable the watcher.

### Show Above Windows
- Right click anywhere on the application to toggle whether the application is fixed above other windows.
- Usage of the picker tool temporarily fixes the window until the watcher is deactivated.

### Test
- You can validate the accuracy using a [popular face dataset](http://vis-www.cs.umass.edu/lfw/alpha_all_30.html).

---

## Technical Details

The application is built with python and [Qt](https://pyqt5.com).

---

## Install

### (Optional) Setup Virtual Environment

`$ pip install virtualenv`

`$ virtualenv env`

Activate the environment via the `env/Scripts` scripts or via your IDE.

### Install Packages

`$ pip install -r requirements.txt`

### Package Executable

`$ python package.py`

Note that [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/) is used to package the application.

### Run Locally

`$ python main.py`

---

## Acknowledgments

- The [PixPerfect](https://www.youtube.com/watch?v=Wvr8LCSuFjE) video for the inspiration.
- This [Qt widget repo](https://github.com/PyQt5/CustomWidgets) for the core colour related widgets.