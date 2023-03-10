# from PySide6.QtCore import QSize, QRect, Qt
# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSizePolicy
# from PySide6.QtGui import QIcon
import sys
from datetime import datetime
from random import randint

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import main


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


#TODO
#stare QueryWindow pod nowym BEZ PRZERWY POMIĘDZY (funkcja (dodatnie wartości, malejąca, max-i) (stretch)?))
#ogarnąć (naprawić) przerywanie słuchania (nowa klasa przyciksu DONE)


class CustomPropertiesButton(QPushButton):
    """
    Class dedicated to buttons that require 'states' for them to work as intended.
    Regular QPushButton subclass, except with additional instance variables.
    All of the attributes passed by **kwargs are held in `properties_dict` dictionary (instance attribute).
    Attributes already existing in the parent class are not modifiable and their names cannot be duplicated by custom attributes.

    `properties_dict` = dictionary made of attributes given via **kwargs
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        #self._default_dict = self.__dict__.copy()
        #self.properties_dict = {}
        ##adding **kwargs elements that are new (their keys are not in `self._default_dict`)
        #self.__dict__.update({key: val for key, val in kwargs.items() if not key in list(self._default_dict.keys()) and key != "properties_dict" and key != "_default_dict"})
        #adding __dict__ elements that are new (their keys are not in `self._default_dict`)
        # so basically adding elements that were just added to __dict__ from **kwargs
        #^outdated
        self.properties_dict = {key: val for key, val in kwargs.items() if not key in list(self.__dict__.keys()) and key != "properties_dict" and key != "_default_dict"}

        #print(self.__dict__.items())
    
    def set_property(self, **kwargs):
        """
        set_property(attr_name1 = attr_value1, attr_name2 = attr_value2, ...)

        Sets a value to the attribute.
        Adds new attribute if the attribute doesn't already exist and sets a value for it.
        """
        #self.__dict__.update({key: val for key, val in kwargs.items() if not key in list(self._default_dict.keys()) and key != "properties_dict" and key != "_default_dict"})
        #print(kwargs.keys()[0] in list(self._default_dict.keys()))
        self.properties_dict.update({key: val for key, val in kwargs.items() if not key in list(self.__dict__.keys()) and key != "properties_dict" and key != "_default_dict"})
        #self.__dict__.update(self.__dict__.pop("properties_dict"))

    def get_property(self, name:str=None):
        """
        Returns the value for the given key (`name`).
        If given key does not exist, whole dictionary with all coder-defined instance attributes is returned.
        If no parameters are provided, whole dictionary with all coder-defined instance attributes is returned.
        """
        try:
            if name==None:
                raise KeyError
            return self.properties_dict[name]
        except KeyError as ke:
            print(ke)
            return self.properties_dict


class QueryWindow(QFrame):
    """
       0           1
    0  layout_1    layout_2
    1  layout_3
    2  layout_4

    layout_1 - QLabel(Data), QLabel(self.date)
    layout_2 - QLabel(Tokeny), QLabel(self.tokens)
    layout_3 - QLabel(Pytanie), QLabel(self.message)
    layout_4 - QLabel(Odpowiedź), QLabel(self.response)
    """

    def __init__(self, message:str="", response:str="", tokens:int=""):
        super().__init__()

        self.setMinimumHeight(131)
        self.setContentsMargins(15, 15, 15, 15)

        self.message = message
        self.response = response
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tokens = tokens

        self.setFocusPolicy(Qt.StrongFocus)
        layout = QGridLayout()
        layout.setColumnStretch(0, 1) #przepycha tokeny (layout_2) do prawej
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)

        self.setObjectName(u"frame")
        #self.setGeometry(QRect(10, 40, 461, 131))
        self.setBaseSize(461, 131)
        #self.adjustSize()
        self.setSizeIncrement(1, 1)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        layout_1 = QHBoxLayout()
        layout_1.setStretch(1, 0)
        layout_1.setSpacing(43) #odstęp między opisem (QLabel("Data")) a wartością (QLabel(self.date))
        label = QLabel("Data", self)
        label.setObjectName(u"label")
        #label.setAlignment(Qt.AlignLeft)
        #label.setGeometry(QRect(0, 0, 211, 16))

        self.label_val = QLabel(str(self.date), self)
        self.label_val.setTextInteractionFlags(Qt.TextSelectableByMouse) #sprawia, że można tekst kopiować
        #self.label_val.setAlignment(Qt.AlignRight)
        self.label_val.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.label_val.adjustSize()
        #self.label_val.setGeometry(QRect(0, 0, 211, 16))
        layout_1.addWidget(label, alignment = Qt.AlignTop|Qt.AlignLeft)
        layout_1.addWidget(self.label_val, alignment = Qt.AlignTop|Qt.AlignRight)

        layout.addLayout(layout_1, 0, 0, alignment = Qt.AlignTop|Qt.AlignLeft)

        layout_2 = QHBoxLayout()
        label_2 = QLabel("Tokeny", self)
        label_2.setObjectName(u"label_2")
        #label_2.setGeometry(QRect(330, 10, 111, 20))

        self.label_val_2 = QLabel(str(self.tokens), self)
        self.label_val_2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout_2.addWidget(label_2, alignment = Qt.AlignTop|Qt.AlignLeft)
        layout_2.addWidget(self.label_val_2, alignment = Qt.AlignTop|Qt.AlignRight)

        layout.addLayout(layout_2, 0, 1, alignment = Qt.AlignTop|Qt.AlignRight)

        expanding_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) #rozszerzanie label w dół (QSizePolicy)

        layout_3 = QHBoxLayout()
        layout_3.setSpacing(29)
        #layout_3.setSizeConstraint()
        label_3 = QLabel("Pytanie", self)
        label_3.setObjectName(u"label_3")
        #label_3.setGeometry(QRect(20, 40, 421, 21))
        #label_3.setLayoutDirection(Qt.LeftToRight)
        #label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        
        self.label_val_3 = QLabel(str(self.message), self)
        self.label_val_3.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_val_3.setSizePolicy(expanding_policy) #rozszerzanie label w dół
        self.label_val_3.setWordWrap(True) #zawijanie słów do nowej linijki
        self.label_val_3.setScaledContents(True)
        layout_3.addWidget(label_3, alignment = Qt.AlignTop|Qt.AlignLeft)
        layout_3.addWidget(self.label_val_3) #, alignment = Qt.AlignTop|Qt.AlignLeft)
        #ALIGNMENT POWODUJE IGNOROWANIE SIZEPOLICY PRZEZ CO LABEL NIE ZAJMUJE CAŁEGO MIEJSCA!!!

        layout.addLayout(layout_3, 1, 0, 1, 2, alignment = Qt.AlignTop|Qt.AlignLeft)

        layout_4 = QHBoxLayout()
        layout_4.setSpacing(5)
        label_4 = QLabel("Odpowiedź", self)
        label_4.setObjectName(u"label_4")
        #label_4.setGeometry(QRect(20, 70, 421, 51))

        #sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(label_4.sizePolicy().hasHeightForWidth())

        #label_4.setSizePolicy(sizePolicy)
        #label_4.setAutoFillBackground(False)
        #label_4.setScaledContents(False)
        #label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.label_val_4 = QLabel(str(self.response), self)
        self.label_val_4.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_val_4.setSizePolicy(expanding_policy)
        self.label_val_4.setWordWrap(True)
        layout_4.addWidget(label_4, alignment = Qt.AlignTop|Qt.AlignLeft)
        layout_4.addWidget(self.label_val_4) #, 1,  alignment = Qt.AlignTop|Qt.AlignLeft)
        #ALIGNMENT POWODUJE IGNOROWANIE SIZEPOLICY PRZEZ CO LABEL NIE ZAJMUJE CAŁEGO MIEJSCA!!!

        layout.addLayout(layout_4, 2, 0, 1, 2, alignment = Qt.AlignTop|Qt.AlignLeft)

        #layout = QGridLayout()
        #layout.addWidget(label, 0, 0)
        #layout.addWidget(label_2, 0, 1)
        #layout.addWidget(label_3, 1, 0)
        #layout.addWidget(label_4, 2, 0)

        self.setLayout(layout)

    def update_variables_in_labels(self, message:str, response:str, tokens:int):
        self.message = message
        self.response = response
        self.tokens = tokens
        #self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #self.label_val.setText(str(self.date))
        self.label_val_2.setText(str(self.tokens))
        self.label_val_3.setText(str(self.message))
        self.label_val_4.setText(str(self.response))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #test = CustomPropertiesButton(self, clicked="test o", test2 = 201)
        #print(test.__dict__, '\n', test.get_property(), '\n')
        #test.set_property(test1="test zmiana", test2='nanana nanana', test3=test.get_property('test2'))
        #test.set_property(toggled = "!-/ERRA!"*5, sth = 'sOMnia', properties_dict = None, _default_dict = "aeea!!!!eaaaaSSSSaeaeae")
        #test.set_property(test2 = 4444)
        #print(test.__dict__, '\n', test.get_property('__dict__'))

        self.i = 0 #useful with iteration over queries, but easily replacable by vbox.count()

        #self.setBaseSize(600, 800)
        self.setFixedSize(600, 800)
        layout = QGridLayout()
        #layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowMinimumHeight(1, 128)
        layout.setVerticalSpacing(75)

        button_layout = QVBoxLayout()

        button = CustomPropertiesButton(self)
        button.setGeometry(QRect(0, 0, 128, 128))
        #layout.addWidget(button, 1, 1) #
        icon = QIcon()
        icon.addFile(u"microphone.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u"microphone_active.png", QSize(), QIcon.Active, QIcon.On)
        button.setIcon(icon)
        button.setIconSize(QSize(128, 128))
        button.setCheckable(True)

        label = QLabel("Naciśnij, aby mówić", self)
        label.setObjectName(u"label")
        label.setGeometry(QRect(0, 0, 128, 30))
        #layout.addWidget(label, 0, 1, alignment = Qt.AlignCenter) #
        label.setAlignment(Qt.AlignBottom)

        button_layout.addWidget(label, alignment = Qt.AlignCenter)
        button_layout.addWidget(button, 1)

        layout.addLayout(button_layout, 1, 1, alignment = Qt.AlignCenter)

        button2 = CustomPropertiesButton(self)
        icon.addFile(u"stop.png", QSize(), QIcon.Normal, QIcon.Off)
        button2.setIcon(icon)
        button2.setIconSize(QSize(56, 56))
        button2.setGeometry(QRect(0, 0, 56, 56))
        layout.addWidget(button2, 1, 2, alignment = Qt.AlignCenter)

        #source: https://www.pythonguis.com/tutorials/pyside-qscrollarea/
        scroll = QScrollArea(self)             # Scroll Area which contains the widgets, set as the centralWidget
        widget = QWidget(self)                 # Widget that contains the collection of Vertical Box
        vbox = QVBoxLayout(self)               # The Vertical Box that contains the Horizontal Boxes of QueryWindows

        widget.setStyleSheet(u"QFrame{\n"
        "	border-radius: 5px;\n"
        "	border: 1px solid #dfdfdf;\n"
        "	background: #fff;\n"
        "}\n"
        "QLabel{\n"
        #"	border: none;\n"
        #"	color: #000;\n"
        "}\n"
        "")
        widget.setLayout(vbox)

        #scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #only if mainwindow resizable
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        layout.addWidget(scroll, 2, 0, 1, 3)
        mainWidget = QWidget(self)
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

        button.clicked.connect(lambda: self.new_query(vbox, button, button2))
        button2.clicked.connect(lambda: self.stop_query(vbox, button, button2))

    def new_query(self, vbox:QVBoxLayout, listen_button:QPushButton, stop_button:QPushButton):
        print("click")

        losmes = ["THIS IS A MASSAGE ", "LIE DOWN ", "On your knees~ ", "UwU OwO ", "totallyrandom "]
        losres = ["res ", "rez ", "rizz ", "jizz ", "cock! ", "chalk! ", "chuck! ", "hwat else... "]

        if listen_button.isChecked():
            print("checked")
            new_query_window = QueryWindow(tokens=1000)
            vbox.insertWidget(0, new_query_window, (1000-vbox.count()), alignment=Qt.AlignTop)
        else:
            print("unchecked")
            try:
                vbox.itemAt(0).widget().update_variables_in_labels(
                    message=''.join([losmes[randint(0, len(losmes))-1] for i in range(randint(5,30))]), 
                    response=''.join([losres[randint(0, len(losres))-1] for i in range(randint(5,30))]), 
                    tokens=self.i)
            except AttributeError as ae:
                print("uh oh, deleted before i could fill it up ÓmÓ\n"+str(ae))
            self.i+=1
    
    def stop_query(self, vbox:QVBoxLayout, listen_button:QPushButton, stop_button:QPushButton):
        if listen_button.isChecked():
            print("stop query")
            qw = vbox.takeAt(0)
            qw.widget().deleteLater()
        else:
            print("DELETE MODE")

    def show_new_window(self, checked):
        w = AnotherWindow()
        w.show()


app = QApplication(sys.argv)

w = MainWindow()
w.show()

with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
app.exec()