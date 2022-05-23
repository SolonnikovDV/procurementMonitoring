import sys
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QTableView, QPushButton, QVBoxLayout,
                             QWidget, QHBoxLayout)
import config as cfg
# from auto_doc_window import AutoDocWindow
from import_data_to_db import ImportDataToDb
from report_window import ReportWindow
from analytic_window import AnalyticWindow


class SqlTableWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setWindowTitle('SQL Table')
        self.resize(1200, 500)

        # Set up model
        self.model = QSqlTableModel(self)
        self.model.setTable(cfg.dB_table_name)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        # Headers
        self.model.setHeaderData(0, Qt.Horizontal, '№ пп')
        self.model.setHeaderData(1, Qt.Horizontal, 'Блок, value_stream заказчика')
        self.model.setHeaderData(2, Qt.Horizontal, 'Номер закупки')
        self.model.setHeaderData(3, Qt.Horizontal, 'Лот закупки')
        self.model.setHeaderData(4, Qt.Horizontal, 'Предмет закупки')
        self.model.setHeaderData(5, Qt.Horizontal, 'НМЦД')
        self.model.setHeaderData(6, Qt.Horizontal, 'Предмет жалобы')
        self.model.setHeaderData(7, Qt.Horizontal, 'Год решения')
        self.model.setHeaderData(8, Qt.Horizontal, 'Заявитель')
        self.model.setHeaderData(9, Qt.Horizontal, 'Решение по жалобе')
        self.model.setHeaderData(10, Qt.Horizontal, 'Нарушенная норма права')
        self.model.setHeaderData(12, Qt.Horizontal, 'Комментарий')
        self.model.setHeaderData(13, Qt.Horizontal, 'Ссылка на решение ФАС')
        self.model.select()
        # Set up view
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.columnWidth(30)

    def add_row(self):
        row_count = self.model.rowCount()
        self.model.insertRow(row_count)
        print(f'add row to : {row_count}')

    def remove_row(self):
        if self.model.rowCount() > 0:
            self.model.removeRow(self.model.rowCount() - 1)
            print(f'remove row to : {self.model.rowCount() - 1}')

    # @staticmethod
    # def create_auto_doc_window():
    #     win = AutoDocWindow()
    #     win.show()
    #     sys.exit(app.exec_())

    @staticmethod
    def import_excel():
        data_frame = ImportDataToDb.import_data_from_excel(
            f'raw_files/{cfg.import_excel_table_name}',
            cfg.dB_path,
            cfg.dB_table_name
        )
        print(f'Excel {cfg.import_excel_table_name} import is successful')
        return data_frame


class AppTable(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 600)
        self.setWindowTitle('SQL Table')

        main_layout = QHBoxLayout()
        table = SqlTableWindow()
        main_layout.addWidget(table)
        button_layout = QVBoxLayout()

        button_new = QPushButton('New')
        button_new.clicked.connect(table.add_row)
        button_layout.addWidget(button_new)

        button_remove = QPushButton('Remove')
        button_remove.clicked.connect(table.remove_row)
        button_layout.addWidget(button_remove, alignment=Qt.AlignTop)

        button_import_excel = QPushButton('Import Excel')
        button_import_excel.clicked.connect(lambda: table.import_excel())
        button_layout.addWidget(button_import_excel)

        button_auto_doc = QPushButton('(test) Create dashboard')
        # button_auto_doc.clicked.connect(lambda: AutoDocWindow().run_widget())
        button_layout.addWidget(button_auto_doc)

        button_report = QPushButton('Create report')
        # button_report.clicked.connect(lambda: ReportWindow().run_widget())
        button_layout.addWidget(button_report)

        button_graph = QPushButton('Graph visualisation')
        # button_graph.clicked.connect(lambda: AnalyticWindow().run_widget())
        button_layout.addWidget(button_graph)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)


def create_connection():
    con = QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName(cfg.db_file_name)
    if not con.open():
        QMessageBox.critical(None, 'QTableView Example - Error!', 'Database Error: %s' % con.lastError().databaseText())
        return False
    return True


def run_app():
    app = QApplication(sys.argv)
    app.setStyleSheet('QPushButton{font-size: 15px; width: 150px; height: 25px}')
    if not create_connection():
        sys.exit(1)
    win = AppTable()
    win.show()
    sys.exit(app.exec_())