# ![Icon](https://raw.githubusercontent.com/kangabru/skin-tone-checker/assets/readme/logo.png) Skin Tone Checker

A simple desktop colour picker tool which helps you to edit your photos to achieve perfect skin tones.

Key Features:
- Pick skin tone colours on screen and see hints to improve them.
- Watch a specific point on screen whilst you make photo adjustments.
- It's fast, and (should) support every OS and editing app like Photoshop or Lightroom.

![Banner Image](https://raw.githubusercontent.com/kangabru/skin-tone-checker/assets/readme/banner.jpg)

---

## Download

| OS | Version | Download |
|:---:|:---:|:---:|
| Windows | [v1.0](https://github.com/kangabru/skin-tone-checker/releases/tag/v1.0) | [Download](https://github.com/kangabru/skin-tone-checker/releases/download/v1.0/Skin.Tone.Checker.exe) |
| Linux | - | [Install from source](#Install) |
| MacOS | - | [Install from source](#Install) |

---

## Usage

### Colour Check
- Click inside the app and drag to analyse colours anywhere on screen.
- Basic stats and hints are displayed to help indicate skin tone problems.
- Note that a colour average is used rather than a single pixel colour.

### Colour Watch
- Click and drag the eye dropper tool to place the 'watcher' tool anywhere on screen.
- The colour under the watcher will be watched to allow the user to make colour adjustments in external programs.
- Click anywhere inside the app to disable the watcher.
- Drag the watcher to update its position.

### Fix Above Windows
- Right click anywhere inside the app to toggle whether the app is fixed above others.
- Usage of the watcher tool temporarily fixes the window until the watcher is deactivated.
- A dark border is displayed whilst the app is fixed above others.

---

## Colour Correction

This app simply displays information about skin tone colours and thus can be used with any external editing application. It does not provide any colour correction abilities itself.

Use cases:
- Determine whether skin tones have the correct hue, saturation, and brightness.
- Correct a photo's white balance via skin tones instead of using a neutral grey colour.
- Useful for colour blind users who cannot see subtle skin tone differences.

Use your editing program of choice to fix incorrect tones as follows:
- Adjust the tint of a photo to fix the skin tone hue.
- Adjust the warmth, saturation, or vibrance to fix the skin tone saturation.
- Adjust the exposure or tone controls to fix the skin tone brightness.
- Use global or local adjustments as needed to correct skin tones of each person individually.

**Disclaimer**

- This tool should be used as a guide and does not necessarily dictate the best skin tone in every use case.
- Photos taken under harsh or coloured light will not always look good when adjusted using this tool.
- Stylistic choices resulting in 'wrong' hue, saturation, or brightness levels are valid and can still result in good photos.
- This tool simply helps to inform your editing decisions, but ultimately you should edit your photo as you wish.

---

## Install

### (Optional) Setup Virtual Environment

`$ pip install virtualenv`

`$ virtualenv env`

Activate the environment via your IDE or manually with the scripts under `env/Scripts`.

### Install Packages

`$ pip install -r requirements.txt`

### Run Locally

`$ python main.py`

### Package Executable

`$ python package.py`

Note that [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/) is used to package the app. Adjustments may be required to package the app for non-windows operating systems.

---

## Technical Details

- The app is built with [Python](https://www.python.org/downloads/) and [Qt](https://pyqt5.com).
- The perfect skin tone range was manually chosen based on [this PixPerfect video](https://www.youtube.com/watch?v=Wvr8LCSuFjE) and further analysis of [peoples' faces](http://vis-www.cs.umass.edu/lfw/alpha_all_30.html).

---

## Acknowledgments

- [This PixPerfect video](https://www.youtube.com/watch?v=Wvr8LCSuFjE) for the inspiration.
- [This Qt widget repo](https://github.com/PyQt5/CustomWidgets) for the colour related widgets.
- Photos by [Brooke Cagle](https://unsplash.com/photos/HRZUzoX1e6w) and [Ayo Ogunseinde](https://unsplash.com/photos/sibVwORYqs0) on [Unsplash](https://unsplash.com/).