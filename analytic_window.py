from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QWidget, QComboBox, QPushButton, QSpacerItem, \
    QSizePolicy, QWidgetItem, QFrame

import config as cfg
import re
from graph_analytic import GraphAnalytic
from report_from_db import Reports


class AnalyticWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Graphical analytic menu')
        self.resize(400, 400)
        print('Report win called')

        frame_one_owner = QFrame()
        frame_one_owner.setFrameShape(QFrame.StyledPanel)
        frame_one_owner.setFrameShadow(QFrame.Plain)
        frame_one_owner.setLineWidth(3)

        vbox = QVBoxLayout()
        vbox_cb_one_owner = QVBoxLayout()
        vbox_cb_result = QVBoxLayout()
        vbox.addWidget(self)

        layout_form = QFormLayout()

        # one owner (owner, year)
        self.cb_owner_one_owner = QComboBox()
        self.cb_owner_one_owner.setCurrentText('Select owner')
        self.cb_owner_one_owner.setFixedWidth(299)
        self.cb_owner_one_owner.addItems(Reports.get_owner_list())

        self.cb_year_one_owner = QComboBox()
        self.cb_year_one_owner.setCurrentText('Select year')
        self.cb_year_one_owner.setFixedWidth(299)
        self.cb_year_one_owner.addItems(Reports.get_year_list())

        self.button_one_owner = QPushButton('Analytic by owner')
        self.button_one_owner.setFixedHeight(40)
        print(f'{self.cb_owner_one_owner.currentText()} , {self.cb_year_one_owner.currentText()}')
        self.button_one_owner.clicked.connect(
            lambda: GraphAnalytic.graph_one_owner(self.cb_owner_one_owner.currentText(), self.cb_year_one_owner.currentText())
        )

        self.cb_year_result = QComboBox()
        self.cb_year_result.setCurrentText('Select year')
        self.cb_year_result.setFixedWidth(299)
        self.cb_year_result.addItems(Reports.get_year_list())

        self.cb_result = QComboBox()
        self.cb_result.setCurrentText('Select year')
        self.cb_result.setFixedWidth(299)
        self.cb_result.addItems(Reports.get_result_list())

        self.button_result = QPushButton('Analytic by result')
        self.button_result.setFixedHeight(40)
        print(f'{self.cb_year_result.currentText()} , {self.cb_result.currentText()}')
        self.button_result.clicked.connect(
            lambda: GraphAnalytic.graph_result(self.cb_year_result.currentText(), self.cb_result.currentText())
        )

        self.button_all_owners = QPushButton('Full analytic')
        self.button_all_owners.setFixedHeight(40)
        self.button_all_owners.clicked.connect(
            lambda: GraphAnalytic.graph_all_owners()
        )

        vbox_cb_one_owner.addWidget(self.cb_year_one_owner)
        vbox_cb_one_owner.addWidget(self.cb_owner_one_owner)
        vbox_cb_result.addWidget(self.cb_year_result)
        vbox_cb_result.addWidget(self.cb_result)
        vbox.addWidget(self.button_one_owner)
        vbox.addWidget(self.button_result)
        vbox.addWidget(self.button_all_owners)

        layout_form.addRow(self.button_one_owner, vbox_cb_one_owner)
        layout_form.addRow(self.button_result, vbox_cb_result)
        layout_form.addRow(self.button_all_owners)

        self.setLayout(layout_form)

    def run_widget(self):
        self.show()
