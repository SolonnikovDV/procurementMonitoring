import config as cfg
# from auto_doc_engine import AutoDoc
import re
import logging
from PyQt5.QtWidgets import QMainWindow, QFrame, QWidget, QDialog, QGridLayout, QComboBox, QHBoxLayout, QPushButton, \
    QVBoxLayout, QGroupBox, QFormLayout, QSpacerItem, QSizePolicy
from report_from_db import Reports


class ReportWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Report menu')
        self.resize(400, 400)
        print('Report win called')

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self)

        layout_form = QFormLayout()

        self.cb_year = QComboBox()
        self.cb_year.setCurrentText('Choose report period')
        self.cb_year.setFixedWidth(299)
        self.cb_year.addItems(Reports.get_year_list())

        self.button_year_report = QPushButton('Year report')
        self.button_year_report.setFixedHeight(40)
        print(f'cb_year : {self.cb_year.currentText()}')
        self.button_year_report.clicked.connect(
            lambda : Reports.year_report(self.cb_year.currentText())
        )

        self.cb_owner = QComboBox()
        self.cb_owner.setFixedWidth(300)
        self.cb_owner.setCurrentText('Choose owner')
        self.cb_owner.addItems(Reports.get_owner_list())

        self.button_owner_report = QPushButton('Owner report')
        self.button_owner_report.setFixedHeight(40)
        print(f'cb_owner.currentText() : {self.cb_owner.currentText()}')
        self.button_owner_report.clicked.connect(
            lambda: Reports.owner_report(self.cb_owner.currentText())
        )

        self.cb_result = QComboBox()
        self.cb_result.setFixedWidth(300)
        self.cb_result.setCurrentText('Choose withdraw result')
        self.cb_result.addItems(Reports.get_result_list())

        self.button_result_report = QPushButton('Withdraw result report')
        self.button_result_report.setFixedHeight(40)
        print(f'cb_result.currentText() : {self.cb_result.currentText()}')
        self.button_result_report.clicked.connect(
            lambda: Reports.withdraw_result_report(self.cb_result.currentText())
        )

        self.button_full_report = QPushButton('Full report')
        self.button_full_report.setFixedHeight(40)
        self.button_full_report.clicked.connect(
            lambda: Reports.full_report()
        )

        layout_form.addRow(self.button_owner_report, self.cb_owner)
        layout_form.addRow(self.button_year_report, self.cb_year)
        layout_form.addRow(self.button_result_report, self.cb_result)
        layout_form.addRow(self.button_full_report)

        vbox.addWidget(self.button_year_report)
        vbox.addWidget(self.cb_year)
        vbox.addWidget(self.button_owner_report)
        vbox.addWidget(self.cb_owner)
        vbox.addWidget(self.button_result_report)
        vbox.addWidget(self.cb_result)
        vbox.addWidget(self.button_full_report)

        # layout.addStretch(1)
        # layout_group_box_year.setLayout(layout)

        self.setLayout(layout_form)

    def run_widget(self):
        self.show()
