Stylesheet = """
QLineEdit, QLabel, QTabWidget {
    font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Fira Sans,Droid Sans,Helvetica Neue,sans-serif;
}
#Custom_Color_View {
    background: white;
    border-radius: 3px;
}
CColorPalettes {
    min-width: 322px;
    max-width: 322px;
    max-height: 120px;
}
ColorDisplay {
    min-height: 160px;
    max-height: 160px;
}
ColorCircle {
    min-width: 50px;
    max-width: 50px;
    min-height: 50px;
    max-height: 50px;
}

#editHex {
    min-width: 75px;
}

#splitLine {
    min-height: 1px;
    max-height: 1px;
    background: #e2e2e2;
}

QLineEdit, QSpinBox {
    border: 1px solid #cbcbcb;
    border-radius: 2px;
    background: white;
    min-width: 31px;
    min-height: 21px;
}
QLineEdit:focus, QSpinBox:focus {
    border-color: rgb(139, 173, 228);
}
QLabel {
    color: #a9a9a9;
}
QPushButton {
    border: 1px solid #cbcbcb;
    border-radius: 2px;
    min-width: 21px;
    max-width: 21px;
    min-height: 21px;
    max-height: 21px;
    font-size: 14px;
    background: white;
}
QPushButton:hover {
    border-color: rgb(139, 173, 228);
}
QPushButton:pressed {
    border-color: #cbcbcb;
}

ColorPicker {
    border: none;
    font-size: 18px;
    border-radius: 0px;
}
QPushButton:hover {
    color: rgb(139, 173, 228);
}
QPushButton:pressed {
    color: #cbcbcb;
}

#confirmButton, #cancelButton {
    min-width: 70px;
    min-height: 30px;
}
#cancelButton:hover {
    border-color: rgb(255, 133, 0);
}

QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    padding: 3px 6px;
    color: rgb(100, 100, 100);
    background: transparent;
}
QTabBar::tab:hover {
    color: black;
}
QTabBar::tab:selected {
    color: rgb(139, 173, 228);
    border-bottom: 2px solid rgb(139, 173, 228);
}

QTabBar::tab:!selected {
    border-bottom: 2px solid transparent;
}

QScrollBar:vertical {
    max-width: 10px;
    border: none;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: rgb(220, 220, 220);
    border: 1px solid rgb(207, 207, 207);
    border-radius: 5px;
}
"""