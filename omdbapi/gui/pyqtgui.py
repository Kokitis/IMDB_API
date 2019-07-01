import sys
from pprint import pprint

import pandas
from PySide2.QtCore import (
	QAbstractTableModel, QModelIndex,
	Qt
)
from PySide2.QtWidgets import QApplication, QDialog, QHBoxLayout, QHeaderView, QLineEdit, QPushButton, QSizePolicy, QTableView, QVBoxLayout, QWidget


class DataFrameTableModel(QAbstractTableModel):
	def __init__(self, data: pandas.DataFrame = None):
		QAbstractTableModel.__init__(self)
		self.df = data
		self.df['releaseDate'] = self.df['releaseDate'].apply(float)

	def rowCount(self, parent = QModelIndex()):
		return len(self.df)

	def columnCount(self, parent = QModelIndex()):
		return len(self.df.columns)

	def headerData(self, section, orientation, role):
		if role != Qt.DisplayRole:
			return None
		if orientation == Qt.Horizontal:
			return self.df.columns[section]
		else:
			return "{}".format(section)

	def data(self, index, role = Qt.DisplayRole):
		column = index.column()
		row = index.row()
		value = str(self.df.iloc[row, column])
		if role == Qt.DisplayRole:
			return value
		elif role == Qt.BackgroundRole:
			return value
		# return QColor(Qt.white)
		elif role == Qt.TextAlignmentRole:
			return Qt.AlignRight

		return None


class Widget(QWidget):
	def __init__(self, data):
		QWidget.__init__(self)

		# Getting the Model
		self.model = DataFrameTableModel(data)

		# Creating a QTableView
		self.table_view = QTableView()
		self.table_view.setModel(self.model)

		# QTableView Headers
		self.horizontal_header = self.table_view.horizontalHeader()
		self.vertical_header = self.table_view.verticalHeader()
		self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
		self.vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)
		self.horizontal_header.setStretchLastSection(True)

		# QWidget Layout
		self.main_layout = QHBoxLayout()
		size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

		## Left layout
		size.setHorizontalStretch(1)
		self.table_view.setSizePolicy(size)
		self.main_layout.addWidget(self.table_view)

		# Set the layout to the QWidget
		self.setLayout(self.main_layout)


class OMDBAPIGUI(QDialog):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.api_response = None
		self.imdb_request_id = QLineEdit()
		self.button_send_find_request = QPushButton("Find")
		self.button_send_search_request = QPushButton("Search")
		self.button_send_get_request = QPushButton("Get")

		self.table_widget = QTableView()
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.imdb_request_id)
		self.layout.addWidget(self.button_send_find_request)
		self.layout.addWidget(self.button_send_search_request)
		self.layout.addWidget(self.table_widget)
		self.setLayout(self.layout)

		self.button_send_find_request.clicked.connect(self.display_response)
		self.button_send_search_request.clicked.connect(self.display_search_response)

	def update_data(self, data):
		self.response = data
		self.update_table()

	def update_table(self):
		if self.response:
			current_table = self.response.toTable()
			model = DataFrameTableModel(current_table)
			self.table_widget.setModel(model)

	def display_response(self):
		result = apiio.find(self.imdb_request_id.text())
		self.update_data(result)

	def display_search_response(self):
		result = apiio.search(self.imdb_request_id.text())
		self.update_data(result)
		pprint(self.response)


if __name__ == "__main__":
	# app = QApplication([])
	# form = OMDBAPIGUI()
	# form.show()
	# sys.exit(app.exec_())
	from omdbapi.api import apiio

	# Qt Application
	app = QApplication([])
	window = OMDBAPIGUI()
	# QWidget
	# widget = Widget(data)
	# QMainWindow using QWidget as central widget

	window.show()
	sys.exit(app.exec_())
