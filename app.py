import sys
from app_updatedb import updatedb
from app_compare import compare
from app_list import list
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QDialogButtonBox, QDialog
from PySide6.QtGui import QFont

mapDict = {1: False, 2: False, 3: False}
horseDict = {"FLP": False, "WSY": False, "DDD": False, "MET": False, "LFS": False, "SFE": False, "GUN": False, "LWN": False, "SUN": False, "PSN": False, "SJU": False, "VOID": False}

mapList = ["Pools", "Vyral_CBT", "Reya_Castle"]
horse1list = ["FLP", "WSY", "DDD", "MET", "LFS", "SFE"]
horse2list = ["GUN", "LWN", "SUN", "PSN", "SJU", "VOID"]

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

        self.Maps = [QPushButton(f"{i}") for i in mapList]
        for btn in self.Maps:
            btn.setCheckable(True)
            layout2.addWidget(btn)

        layout1.addLayout( layout2 )

        self.buttonGeneration1 = QPushButton("Gen 1")
        self.buttonGeneration1.setCheckable(True)
        self.buttonGeneration1.clicked.connect(self.sync_children_to_gen1)
        layout3.addWidget(self.buttonGeneration1)

        self.buttonGeneration1children = [QPushButton(f"{i}") for i in horse1list]
        for btn in self.buttonGeneration1children:
            btn.setCheckable(True)
            layout3.addWidget(btn)
            # Link each child to the checker function
            btn.clicked.connect(self.sync_gen1_to_children)
        
        layout1.addLayout( layout3 )

        self.buttonGeneration2 = QPushButton("Gen 2")
        self.buttonGeneration2.setCheckable(True)
        self.buttonGeneration2.clicked.connect(self.sync_children_to_gen2)
        layout4.addWidget(self.buttonGeneration2)

        self.buttonGeneration2children = [QPushButton(f"{i}") for i in horse2list]
        for btn in self.buttonGeneration2children:
            btn.setCheckable(True)
            layout4.addWidget(btn)
            # Link each child to the checker function
            btn.clicked.connect(self.sync_gen2_to_children)

        layout1.addLayout( layout4 )

        self.buttonList = QPushButton("List")
        self.buttonList.clicked.connect(self.buttonListClicked)
        
        self.buttonCompare = QPushButton("Compare")
        self.buttonCompare.clicked.connect(self.buttonCompareClicked)

        layout5.addWidget(self.buttonList)
        layout5.addWidget(self.buttonCompare)

        layout1.addLayout( layout5 )

        widget = QWidget()
        widget.setLayout(layout1)
        app_font = QFont('Arial', 24)
        widget.setFont(app_font)
        widget.setStyleSheet("background-color: #6398d1;")
        self.setCentralWidget(widget)

        # Connecting Generation 1 parent to children
    def sync_children_to_gen1(self):
        state = self.buttonGeneration1.isChecked()
        for btn in self.buttonGeneration1children:
            btn.setChecked(state)


    def sync_gen1_to_children(self):
        """When a child is clicked, update the parent status."""
        all_checked = all(btn.isChecked() for btn in self.buttonGeneration1children)
        # If any child is unchecked, parent must be unchecked
        self.buttonGeneration1.setChecked(all_checked)

        # Connecting Generation 2 parent to children
    def sync_children_to_gen2(self):
        state = self.buttonGeneration2.isChecked()
        for btn in self.buttonGeneration2children:
            btn.setChecked(state)

    def sync_gen2_to_children(self):
        """When a child is clicked, update the parent status."""
        all_checked = all(btn.isChecked() for btn in self.buttonGeneration2children)
        # If any child is unchecked, parent must be unchecked
        self.buttonGeneration2.setChecked(all_checked)

    def buttonListClicked(self):
        print("List button clicked!")
        maps, horses = self.getCheckedItems()
        dlg = CustomDialog(calculatedStats=list(maps, horses))
        dlg.exec()

    def buttonCompareClicked(self):
        print("Compare button clicked!")
        maps, horses = self.getCheckedItems()
        dlg = CustomDialog(calculatedStats=compare(maps, horses))
        dlg.exec()

    
    def getCheckedItems(self):
        checked_maps = [btn.text() for btn in self.Maps if btn.isChecked()]
        checked_gen1 = [btn.text() for btn in self.buttonGeneration1children if btn.isChecked()]
        checked_gen2 = [btn.text() for btn in self.buttonGeneration2children if btn.isChecked()]
        checked_horses = checked_gen1 + checked_gen2
        return checked_maps, checked_horses

class CustomDialog(QDialog):
    def __init__(self, calculatedStats):
        super().__init__()

        self.calculatedStats = calculatedStats

        chars_to_remove = "[]'"
        translation_table = str.maketrans('', '', chars_to_remove)
        new_string = calculatedStats.translate(translation_table)

        self.setWindowTitle("Calculated Stats")

        lines = calculatedStats.count('\n')+1
        window_height = (lines*14)+55
        self.setFixedSize(QSize(495, window_height))
        self.setStyleSheet("background-color: #6398d1;")

        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()

        self.Stats = QLabel(new_string)
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

updatedb()
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()