import sys, os
import json
from app_updatedb import updatedb
from app_compare import compare
from app_listtest import list
from PySide6 import QtGui 
from PySide6.QtCore import QSize, Qt, QSettings
from PySide6.QtWidgets import QToolButton, QApplication, QMainWindow, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QDialogButtonBox, QDialog, QTextEdit, QMenu
from PySide6.QtGui import QIcon, QFont, QPixmap, QAction
import resources

####################################################################
################## REMEMBER TO UNCOMMENT updatedb ##################
####################################################################


mapList = ["Pools", "Vyral_CBT", "Reya_Castle"]
mapOn = [":/graphics/level1off", ":/graphics/level2off", ":/graphics/level3off"]
mapOff = [":/graphics/level1on", ":/graphics/level2on", ":/graphics/level3on"]
horse1list = ["FLP", "WSY", "DDD", "MET", "LFS", "SFE"]
horse1on = [":/graphics/FLPoff", ":/graphics/WSYoff", ":/graphics/DDDoff", ":/graphics/METoff", ":/graphics/LFSoff", ":/graphics/SFEoff"]
horse1off = [":/graphics/FLPon", ":/graphics/WSYon", ":/graphics/DDDon", ":/graphics/METon", ":/graphics/LFSon", ":/graphics/SFEon"]
horse2list = ["GUN", "LWN", "SUN", "PSN", "SJU", "VOID"]
horse2on = [":/graphics/GUNoff", ":/graphics/LWNoff", ":/graphics/SUNoff", ":/graphics/PSNoff", ":/graphics/SJUoff", ":/graphics/VOIDoff"]
horse2off = [":/graphics/GUNon", ":/graphics/LWNon", ":/graphics/SUNon", ":/graphics/PSNon", ":/graphics/SJUon", ":/graphics/VOIDon"]
settings = QSettings('AntleredKey', 'HorseHistorian')
maxHorses = 12

try:
    from ctypes import windll
    myappid = 'com.AntleredKey.HorseHistorianApp.0.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Horse Historian Stats")
        self.setFixedSize(QSize(495, 502))

        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        layout5 = QHBoxLayout()

        self.Maps = [QToolButton(self) for i in mapList]

        for btn, text, iconOn, iconOff in zip(self.Maps, mapList, mapOn, mapOff):
            btn.setText(text)
            icon = QIcon()
            icon.addFile(iconOn, QSize(), QIcon.Normal, QIcon.Off)
            icon.addFile(iconOff, QSize(), QIcon.Normal, QIcon.On)
            btn.setIcon(icon)
            btn.setIconSize(QSize(70, 83))
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setCheckable(True)
            layout2.addWidget(btn)
            btn.clicked.connect(self.sync_gen1_to_children)

        layout1.addLayout( layout2 )

        self.buttonGeneration1 = QToolButton()
        buttonGeneration1icon = QIcon()
        buttonGeneration1icon.addFile(":/graphics/gen1off", QSize(), QIcon.Normal, QIcon.Off)
        buttonGeneration1icon.addFile(":graphics/gen1on", QSize(), QIcon.Normal, QIcon.On)
        self.buttonGeneration1.setIcon(buttonGeneration1icon)
        self.buttonGeneration1.setIconSize(QSize(43, 100))
        self.buttonGeneration1.setCheckable(True)
        layout3.addWidget(self.buttonGeneration1)
        self.buttonGeneration1.clicked.connect(self.sync_children_to_gen1)

        """
        self.buttonGeneration1 = QPushButton("Gen 1")
        self.buttonGeneration1.setCheckable(True)
        self.buttonGeneration1.clicked.connect(self.sync_children_to_gen1)
        layout3.addWidget(self.buttonGeneration1)
        """

        self.buttonGeneration1children = [QToolButton(self) for i in horse1list]

        for btn, text, iconOn, iconOff in zip(self.buttonGeneration1children, horse1list, horse1on, horse1off):
            btn.setText(text)
            icon = QIcon()
            icon.addFile(iconOn, QSize(), QIcon.Normal, QIcon.Off)
            icon.addFile(iconOff, QSize(), QIcon.Normal, QIcon.On)
            btn.setIcon(icon)
            btn.setIconSize(QSize(70, 83))
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setCheckable(True)
            layout3.addWidget(btn)
            btn.clicked.connect(self.sync_gen1_to_children)

        layout1.addLayout( layout3 )

        self.buttonGeneration2 = QToolButton()
        buttonGeneration2icon = QIcon()
        buttonGeneration2icon.addFile(":/graphics/gen2off", QSize(), QIcon.Normal, QIcon.Off)
        buttonGeneration2icon.addFile(":graphics/gen2on", QSize(), QIcon.Normal, QIcon.On)
        self.buttonGeneration2.setIcon(buttonGeneration2icon)
        self.buttonGeneration2.setIconSize(QSize(43, 100))
        self.buttonGeneration2.setCheckable(True)
        layout4.addWidget(self.buttonGeneration2)
        self.buttonGeneration2.clicked.connect(self.sync_children_to_gen2)
        

        self.buttonGeneration2children = [QToolButton(self) for i in horse2list]

        for btn, text, iconOn, iconOff in zip(self.buttonGeneration2children, horse2list, horse2on, horse2off):
            btn.setText(text)
            icon = QIcon()
            icon.addFile(iconOn, QSize(), QIcon.Normal, QIcon.Off)
            icon.addFile(iconOff, QSize(), QIcon.Normal, QIcon.On)
            btn.setIcon(icon)
            btn.setIconSize(QSize(70, 83))
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setCheckable(True)
            layout4.addWidget(btn)
            btn.clicked.connect(self.sync_gen2_to_children)

        layout1.addLayout( layout4 )

        self.buttonList = QToolButton()
        buttonListicon = QIcon()
        buttonListicon.addFile(":graphics/liston", QSize(), QIcon.Normal, QIcon.On)
        buttonListicon.addFile(":graphics/listoff", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonList.setIcon(buttonListicon)
        self.buttonList.setIconSize(QSize(70,39))
        self.buttonList.setCheckable(True)
        self.buttonList.clicked.connect(self.buttonListClicked)

        self.buttonCompare = QToolButton()
        buttonCompareicon = QIcon()
        buttonCompareicon.addFile(":graphics/compareon", QSize(), QIcon.Normal, QIcon.On)
        buttonCompareicon.addFile(":graphics/compareoff", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonCompare.setIcon(buttonCompareicon)
        self.buttonCompare.setIconSize(QSize(134,39))
        self.buttonCompare.setCheckable(True)
        self.buttonCompare.clicked.connect(self.buttonCompareClicked)

        layout5.addWidget(self.buttonList)
        layout5.addWidget(self.buttonCompare)

        layout1.addLayout( layout5 )

        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Options")
        action1.triggered.connect(self.openOptions)
        #self.checkSettings()

        widget = QWidget()
        widget.setLayout(layout1)
        app_font = QFont('Arial', 24)
        widget.setFont(app_font)
        widget.setStyleSheet("background-color: #6398d1;")
        self.setCentralWidget(widget)

    # Right Click menu
    def contextMenuEvent(self, event):
        self.context_menu.exec(event.globalPos())

    def openOptions(self):
        dlg = OptionsWindow()
        dlg.exec()

    # Connecting Generation 1 parent to children
    def sync_children_to_gen1(self):
        state = self.buttonGeneration1.isChecked()
        for btn in self.buttonGeneration1children:
            btn.setChecked(state)
    def sync_gen1_to_children(self):
        all_checked = all(btn.isChecked() for btn in self.buttonGeneration1children)
        self.buttonGeneration1.setChecked(all_checked)

    # Connecting Generation 2 parent to children
    def sync_children_to_gen2(self):
        state = self.buttonGeneration2.isChecked()
        for btn in self.buttonGeneration2children:
            btn.setChecked(state)
    def sync_gen2_to_children(self):
        all_checked = all(btn.isChecked() for btn in self.buttonGeneration2children)
        self.buttonGeneration2.setChecked(all_checked)


    def buttonListClicked(self):
        maps, horses = self.getCheckedItems()
        settingsdict = self.getSettings()
        dlg = CustomDialog(calculatedStats=list(maps, horses, settingsdict))
        dlg.exec()
        self.buttonList.setChecked(False)
    def buttonCompareClicked(self):
        maps, horses = self.getCheckedItems()
        settingsdict = self.getSettings()
        dlg = CustomDialog(calculatedStats=compare(maps, horses, settingsdict))
        dlg.exec()
        self.buttonCompare.setChecked(False)
    def getCheckedItems(self):
        checked_maps = [btn.text() for btn in self.Maps if btn.isChecked()]
        checked_gen1 = [btn.text() for btn in self.buttonGeneration1children if btn.isChecked()]
        checked_gen2 = [btn.text() for btn in self.buttonGeneration2children if btn.isChecked()]
        checked_horses = checked_gen1 + checked_gen2
        return checked_maps, checked_horses
    
    def getSettings(self):
        yuristate = settings.value('CountYuri', True, type=bool)
        minhorsestate = settings.value('MinHorses', 1, type=str)
        maxhorsestate = settings.value('MaxHorses', maxHorses, type=str)
        settingsDict = {
            'CountYuri': yuristate,
            'MinHorses': minhorsestate,
            'MaxHorses': maxhorsestate
        }
        return settingsDict

class OptionsWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Options")
        self.setStyleSheet("background-color: #6398d1;")
        self.setFixedSize(QSize(332, 203))
        self.PreviousMin = 1
        self.PreviousMax = maxHorses

        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()

        self.YuriLabel = QLabel("Count Released Yuri:")
        layout2.addWidget(self.YuriLabel)

        self.YuriButton = QToolButton()
        YuriIcon = QIcon()
        YuriIcon.addFile(":/graphics/yuriOn", QSize(), QIcon.Normal, QIcon.Off)
        YuriIcon.addFile(":/graphics/yuriOff", QSize(), QIcon.Normal, QIcon.On)
        self.YuriButton.setIcon(YuriIcon)
        self.YuriButton.setIconSize(QSize(70, 83))
        self.YuriButton.setCheckable(True)
        layout2.addWidget(self.YuriButton)
        self.YuriButton.clicked.connect(self.YuriClicked)

        layout1.addLayout( layout2 )

        self.MinLabel = QLabel("Minimum Horses:")
        layout3.addWidget(self.MinLabel)

        self.MinEdit = QLineEdit()
        self.MinEdit.setMaxLength(2)
        self.MinEdit.editingFinished.connect(self.MinEdited)
        layout3.addWidget(self.MinEdit)

        self.MaxLabel = QLabel("Maximum Horses:")
        layout3.addWidget(self.MaxLabel)

        self.MaxEdit = QLineEdit()
        self.MaxEdit.setMaxLength(2)
        self.MaxEdit.editingFinished.connect(self.MaxEdited)
        layout3.addWidget(self.MaxEdit)

        layout1.addLayout( layout3 )

        QBtn = (
            QDialogButtonBox.Close
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout4.addWidget(self.buttonBox)
        layout1.addLayout( layout4 )

        self.setLayout(layout1)
        self.load_settings()

    def YuriClicked(self):
        state = self.YuriButton.isChecked()
        settings.setValue('CountYuri', state)
        print(state)

    def MinEdited(self):
        if self.MinEdit.text() == "":
            return
        try:
            numberMin = int(self.MinEdit.text())
            if numberMin <= int(self.PreviousMax) and numberMin > 0:
                settings.setValue('MinHorses', numberMin)
                self.PreviousMin = numberMin
                print(numberMin)
                return
            else:
                self.MinEdit.setText(f"{self.PreviousMin}")
                return
        except ValueError:
            self.MinEdit.setText(f"{self.PreviousMin}")
            return
    
    def MaxEdited(self):
        if self.MaxEdit.text() == "":
            return
        try:
            numberMax = int(self.MaxEdit.text())
            if numberMax >= int(self.PreviousMin) and numberMax <= maxHorses:
                settings.setValue('MaxHorses', numberMax)
                self.PreviousMax = numberMax
                print(numberMax)
                return
            else:
                self.MaxEdit.setText(f"{self.PreviousMax}")
                return
        except ValueError:
            self.MaxEdit.setText(f"{self.PreviousMax}")
            return
    
    def load_settings(self):
        yuristate = settings.value('CountYuri', True, type=bool)
        minhorsestate = settings.value('MinHorses', 1, type=str)
        maxhorsestate = settings.value('MaxHorses', maxHorses, type=str)
        self.PreviousMin = minhorsestate
        self.PreviousMax = maxhorsestate
        self.YuriButton.setChecked(yuristate)
        self.MinEdit.setText(minhorsestate)
        self.MaxEdit.setText(maxhorsestate)


class CustomDialog(QDialog):
    def __init__(self, calculatedStats):
        super().__init__()

        self.calculatedStats = calculatedStats

        chars_to_remove = "[]'"
        translation_table = str.maketrans('', '', chars_to_remove)
        removed_string = calculatedStats.translate(translation_table)
        new_string = removed_string.replace("VOD", "VOID")

        self.setWindowTitle("Calculated Stats")

        lines = calculatedStats.count('\n')+2
        window_height = (lines*16)+55
        if window_height > 502:
            self.setFixedSize(QSize(495, 502))
        else:
            self.setFixedSize(QSize(495, window_height))

        self.setStyleSheet("background-color: #6398d1;")

        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()

        if lines == 3:
            self.Stats = QLabel(new_string)
        else:
            self.Stats = QTextEdit()
            self.Stats.setReadOnly(True)
            self.Stats.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.Stats.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.Stats.setPlainText(new_string)

        layout2.addWidget(self.Stats)

        layout1.addLayout( layout2 )

        QBtn = (
            QDialogButtonBox.Close
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout3.addWidget(self.buttonBox)
        layout1.addLayout( layout3 )

        self.setLayout(layout1)


#updatedb()
app = QApplication(sys.argv)
app.setStyleSheet("QToolButton { border: none; background: transparent; }")
app.setWindowIcon(QtGui.QIcon(":/graphics/favicon"))
window = MainWindow()
window.show()
app.exec()