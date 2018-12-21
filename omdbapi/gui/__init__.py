import sys
from pprint import pprint
from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHeaderView, QSizePolicy, QApplication, \
	QLabel, QLineEdit, QTableView, QTableWidget, QHBoxLayout, QTableWidgetItem
from PySide2 import QtWidgets
from omdbapi.api import omdb_api
import pandas
from omdbapi.graphics.pyplot_graph import plot_series
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
class MyMplCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, parent=None, response = None, width=5, height=4, dpi=200):
		self.fig, self.axes = plot_series(response)
		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
								   QtWidgets.QSizePolicy.Expanding,
								   QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

class OMDBAPIGUI(QDialog):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.api_response = None
		self.imdb_request_id = QLineEdit()
		self.button_send_find_request = QPushButton("Find")
		self.button_send_search_request = QPushButton("Search")
		self.button_send_get_request = QPushButton("Get")
		self.button_view_as_table = QPushButton("View as Table")
		self.graph_widget = QtWidgets.QWidget(self)
		self.table = QTableWidget()
		layout = QVBoxLayout()
		layout.addWidget(self.imdb_request_id)
		layout.addWidget(self.button_send_find_request)
		layout.addWidget(self.button_send_search_request)
		layout.addWidget(self.graph_widget)
		self.setLayout(layout)

		self.button_send_find_request.clicked.connect(self.display_response)
		self.button_send_search_request.clicked.connect(self.display_search_response)

	def update_data(self, data):
		self.response = data
		if self.response:
			self.graph_widget= MyMplCanvas(None, self.response, width = 5, height = 4, dpi = 100)
			#self.graph_widget = sc

	def update_table(self, data: pandas.DataFrame):
		self.table.setColumnCount(len(data.columns))
		self.table.setRowCount(len(data))
		self.table.setHorizontalHeaderLabels(data.columns)
		for row_index, row in data.iterrows():
			for column_index, value in enumerate(row.tolist()):
				self.table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

	def display_response(self):
		result = omdb_api.find(self.imdb_request_id.text(), episode_format = 'long')
		self.update_data(result)
		print(self.response.summary())

	def display_search_response(self):
		result = omdb_api.search(self.imdb_request_id.text())
		self.update_data(result)
		pprint(self.response)


if __name__ == "__main__":
	app = QApplication([])
	form = OMDBAPIGUI()
	form.show()
	sys.exit(app.exec_())
