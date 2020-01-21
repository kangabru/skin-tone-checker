# Skin Tone Checker

A simple desktop colour picker tool which helps you to edit your photos to achieve perfect skin tones.

Key Features:
- Pick skin tone colours on screen and see hints to improve them.
- Watch a specific point on screen whilst you make photo adjustments.
- It's fast, and supports every OS and editing app like Photoshop or Lightroom.

---

## Usage

### Colour Check
- Click and drag anywhere inside the app to analyse colours anywhere on screen.
- Basic stats and hints are displayed to help indicate skin tone problems.
- Note that an average of colours is used rather than a single point.

### Colour Watch
- Click and drag the eye dropper tool to place a watch marker anywhere on screen.
- The colour at the marker will be watched to allow the user to make colour adjustments.
- Click anywhere inside the app to disable the watcher.
- Drag the marker to update its position.

### Fix Above Windows
- Right click anywhere inside the app to toggle whether the app is fixed above others.
- Usage of the picker tool temporarily fixes the window until the watcher is deactivated.
- A dark border is displayed whilst the app is fixed above others.

---

## Colour Correction

This app simply displays information about skin tone colours and thus can be used with any external editing application. It does not provide any colour correction abilities itself.

Use cases:
- Determine whether skin tones have the correct hue, saturation, and brightness.
- Correct a photo's white balance via skin tones instead of using a neutral gray indicator.
- Useful for colour blind users who cannot see subtle skin tone differences.

Use your editing program to fix incorrect tones as follows:
- Adjust the tint of a photo to fix the skin tone hue.
- Adjust the warmth, saturation, or vibrance to fix the skin tone saturation.
- Adjust the exposure or tone controls to fix the skin tone brightness.
- Use global or local adjustments as needed to correct skin tones of each person individually.

**Disclaimer**

This tool should be used as a guide and does not necessarily dictate the best skin tone in every use case. For example photos taken in harsh or coloured light will not always look good when adjusted using this tool. Adjust the photo to look good, and use this tool to inform your editing decisions.

---

## Install

### (Optional) Setup Virtual Environment

`$ pip install virtualenv`

`$ virtualenv env`

Activate the environment via your IDE or manually with the scripts under `env/Scripts`.

### Install Packages

`$ pip install -r requirements.txt`

### Package Executable

`$ python package.py`

Note that [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/) is used to package the app. Adjustments may be required to package the app for non-windows operating systems.

### Run Locally

`$ python main.py`

---

## Technical Details

- The app is built with [Python](https://www.python.org/downloads/) and [Qt](https://pyqt5.com).
- The perfect skin tone range was manually chosen based on [this PixPerfect video](https://www.youtube.com/watch?v=Wvr8LCSuFjE) and further analysis of [peoples' faces](http://vis-www.cs.umass.edu/lfw/alpha_all_30.html).

---

## Acknowledgments

- [This PixPerfect video](https://www.youtube.com/watch?v=Wvr8LCSuFjE) for the inspiration.
- [This Qt widget repo](https://github.com/PyQt5/CustomWidgets) for the core colour related widgets.