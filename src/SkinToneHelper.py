from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QImage, QPainter, QBrush, QPen
from src.util import GetLinePath
from enum import Enum, auto
from typing import Tuple


class ErrorLevel(Enum):
    good = auto()
    ok = auto()
    bad = auto()

class _SaturationResult(Enum):
    good = auto()
    low_limit_1 = auto()
    low_limit_2 = auto()
    high_limit_1 = auto()
    high_limit_2 = auto()

HUE_TARGET = 20

# Represents the cubic curve that defines perfect skin tones. Values are (Saturation, Brightness) in percentages.
PERFECT_TONES_CUBIC_POINTS = [(20, 90),(52, 85),(20, 40),(71, 20)]

# Represents the lines that define perfect skin tones. Values are (Saturation, Brightness) in percentages.
DEBUG_PERFECT_TONES_POINTS = True
PERFECT_TONES_POINTS = [(20, 90),(33, 85),(37, 75),(39, 51),(52, 32),(71, 20)]

_LIMIT_HUE_1, _LIMIT_HUE_2 = 10, 20
_LIMIT_BRIGHT_1, _LIMIT_BRIGHT_2 = 5, 10
_LIMIT_SAT_1, _LIMIT_SAT_2 = 10, 20


def getSkinToneMessage(color: QColor) -> Tuple[ErrorLevel, str]:
    error, ok, success = lambda m: (ErrorLevel.bad, m + " ✘"), lambda m: (
        ErrorLevel.ok, m), lambda m: (ErrorLevel.good, m + " ✔")

    hue, sat, bright, _ = color.getHsv()
    sat, bright = sat / 2.55, bright / 2.55 # Convert to percentage

    hue_diff = _getHueDiff(hue)
    if hue_diff > _LIMIT_HUE_2: return error("The hue is off")
    if hue_diff > _LIMIT_HUE_1: return ok("The hue is off a little")

    bright_diff = _getBrightDiff(bright)
    if bright_diff < -_LIMIT_BRIGHT_2: return error("The brightness is low")
    if bright_diff < -_LIMIT_BRIGHT_1: return ok("The brightness is a little low")
    if bright_diff > _LIMIT_BRIGHT_2: return error("The brightness is high")
    if bright_diff > _LIMIT_BRIGHT_1: return ok("The brightness is a little high")

    sat_result = _getSatResult(sat, bright)
    if sat_result == _SaturationResult.low_limit_2: return error("The saturation is low")
    if sat_result == _SaturationResult.low_limit_1: return ok("The saturation is a little low")
    if sat_result == _SaturationResult.high_limit_2: return error("The saturation is high")
    if sat_result == _SaturationResult.high_limit_1: return ok("The saturation is a little high")

    return success("The skin tone is perfect")


def _getHueDiff(hue):
    hue_diff = abs(HUE_TARGET - hue) % 360
    if hue_diff > 180: hue_diff = abs(hue_diff - 360)
    return hue_diff

def _getBrightDiff(bright):
    first, last = PERFECT_TONES_POINTS[0][1], PERFECT_TONES_POINTS[-1][1]
    bright_min, bright_max = min(first, last), max(first, last)
    if bright < bright_min: return bright - bright_min # Negative number
    if bright > bright_max: return bright - bright_max # Positive number
    return 0

def _getSatResult(sat, bright) -> _SaturationResult:
    color_good = QColor.fromHsv(0, 0, 255)  # White
    color_bad = QColor.fromHsv(0, 0, 0)  # Black

    proximity_map = _getColorMapImage()
    colorAtPosition: QColor = proximity_map.pixelColor(sat, bright)
    brightness = colorAtPosition.getHsvF()[2] # Return 0.0, 0.5, 1.0 to represent bad, ok, good respectively
    isLow = _isInLowZone(sat, bright) # Left or right of the curve

    if brightness < 0.2 and isLow: return _SaturationResult.low_limit_2
    if brightness < 0.8 and isLow: return _SaturationResult.low_limit_1
    if brightness < 0.2 and not isLow: return _SaturationResult.high_limit_2
    if brightness < 0.8 and not isLow: return _SaturationResult.high_limit_1
    return _SaturationResult.good


def _getColorMapImage():
    """Returns a 100x100 px image grayscale image representing the saturation boundaries."""
    color_bad, color_limit, color_good = Qt.black, _getColorB(50), Qt.white

    proximity_map = QImage(100, 100, QImage.Format_Grayscale8)
    painter = QPainter()
    painter.begin(proximity_map)

    # Paint limits
    painter.fillRect(QRect(0, 0, 100, 100), QBrush(color_bad)) # Bad zone

    painter.setPen(QPen(color_limit, _LIMIT_SAT_2))
    painter.drawPath(GetLinePath(PERFECT_TONES_POINTS)) # Limit 2 zone

    painter.setPen(QPen(color_good, _LIMIT_SAT_1))
    painter.drawPath(GetLinePath(PERFECT_TONES_POINTS))  # Limit 1 zone (good zone)
    painter.end()

    return proximity_map

def _getColorB(brightness) -> QColor:
    return QColor.fromHsvF(0, 0, brightness/100)

def _isInLowZone(sat, bright):
    # Top and bottom out of region edge cases
    if sat < PERFECT_TONES_POINTS[0][0]: return True
    if sat > PERFECT_TONES_POINTS[-1][0]: return False

    # The the two points the define the segment the brightness is in
    point0, point1 = None, None
    for point in PERFECT_TONES_POINTS:
        point0 = point1; point1 = point
        if point0 is None or point1 is None: continue # used to init variables

        # Check if this segment is the one we will compare
        bright0, bright1 = point0[1], point1[1]
        bright_min, bright_max = min(bright0, bright1), max(bright0, bright1)
        if bright >= bright_min and bright <= bright_max: break # yes it is

    # Get the saturation point on the line segment given the input brightness
    sat0, bright0 = point0; sat1, bright1 = point1
    bright_mult = (bright - bright0) / (bright1 - bright0)
    sat_point = sat0 + (sat1 - sat0) * bright_mult

    return sat < sat_point # Simply see if it's left or right of the line