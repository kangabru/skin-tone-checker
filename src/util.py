from PyQt5.QtGui import QPainter, QPainterPath
from typing import List, Tuple

def GetLinePath(points: List[Tuple[int, int]]):
    """Returns a drawable line path representing. Points should be a list of tuples representing (x, y) pixel values."""
    path = QPainterPath()
    path.moveTo(*points[0])
    [path.lineTo(x, y) for x, y in points]
    return path

def GetCubicPath(points: List[Tuple[int, int]]):
    """Returns a drawable path representing a 4 point cubic curve. Points should be a list of 4 tuples representing four (x, y) pixel values."""
    path = QPainterPath()
    x0, y0 = points[0]
    x1, y1 = points[1]
    x2, y2 = points[2]
    x3, y3 = points[3]
    path.moveTo(x0, y0)
    path.cubicTo(x1, y1, x2, y2, x3, y3)
    return path

def HueColorsToPixels(points: List[Tuple[int, int]], width: int, height: int):
    return [HueColorToPixel(p, width, height) for p in points]

def HueColorToPixel(point: Tuple[int, int], width: int, height: int):
    return (point[0] / 100 * width, height - (point[1] / 100 * height))

def SmoothPainter(painter):
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
