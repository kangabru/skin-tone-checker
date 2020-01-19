from PyQt5.QtGui import QColor

HUE_TARGET = 20

# Represents the cubic curve that defines perfect skin tones
# Values are (Saturation, Brightness) in percentages
PERFECT_TONES_CUBIC_POINTS = [(20, 90),(52, 85),(20, 40),(71, 20)]

_LIMIT_HUE_1, _LIMIT_HUE_2 = 10, 20

def getSkinToneMessage(color: QColor):
    error = lambda m: (False, m + " ✘")
    success = lambda m: (True, m + " ✔")
    h, s, v, _ = color.getHsv()

    hue_diff = _getHueDiff(h)
    if hue_diff > _LIMIT_HUE_2: return error("The hue is off")
    if hue_diff > _LIMIT_HUE_1: return error("The hue is off a little")




    return success("The skin tone is perfect")


def _getHueDiff(hue):
    hue_diff = abs(HUE_TARGET - hue) % 360
    if hue_diff > 180: hue_diff = abs(hue_diff - 360)
    return hue_diff