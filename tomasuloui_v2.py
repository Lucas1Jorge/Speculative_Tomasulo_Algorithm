# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tomasulov2.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import Tomasulo
import time
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
	def __init__(self):
		self.Tomasulo = None
		self.pause = True

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(839, 658)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.playBtn = QtWidgets.QPushButton(self.centralwidget)
		self.playBtn.setObjectName("playBtn")
		self.horizontalLayout_2.addWidget(self.playBtn)
		self.speedUpBtn = QtWidgets.QPushButton(self.centralwidget)
		self.speedUpBtn.setObjectName("speedUpBtn")
		self.horizontalLayout_2.addWidget(self.speedUpBtn)
		self.pauseBtn = QtWidgets.QPushButton(self.centralwidget)
		self.pauseBtn.setObjectName("pauseBtn")
		self.horizontalLayout_2.addWidget(self.pauseBtn)
		self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
		self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
		self.tabWidget.setObjectName("tabWidget")
		self.tabv1 = QtWidgets.QWidget()
		self.tabv1.setObjectName("tabv1")
		self.gridLayout = QtWidgets.QGridLayout(self.tabv1)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
		self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.estacoesTable = QtWidgets.QTableWidget(self.tabv1)
		self.estacoesTable.setRowCount(11)
		self.estacoesTable.setColumnCount(9)
		self.estacoesTable.setObjectName("estacoesTable")
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(4, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(5, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(6, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(7, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(8, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(9, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setVerticalHeaderItem(10, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setHorizontalHeaderItem(4, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setHorizontalHeaderItem(5, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setHorizontalHeaderItem(6, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setHorizontalHeaderItem(7, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setHorizontalHeaderItem(8, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(0, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(1, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(2, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(3, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(4, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(5, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(6, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(7, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(8, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(9, 0, item)
		item = QtWidgets.QTableWidgetItem()
		self.estacoesTable.setItem(10, 0, item)
		self.horizontalLayout.addWidget(self.estacoesTable)
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
		self.verticalLayout.setContentsMargins(0, -1, -1, -1)
		self.verticalLayout.setSpacing(6)
		self.verticalLayout.setObjectName("verticalLayout")
		self.memoryTable = QtWidgets.QTableWidget(self.tabv1)
		self.memoryTable.setMaximumSize(QtCore.QSize(234, 152))
		self.memoryTable.setObjectName("memoryTable")
		self.memoryTable.setColumnCount(2)
		self.memoryTable.setRowCount(4)
		item = QtWidgets.QTableWidgetItem()
		self.memoryTable.setVerticalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.memoryTable.setVerticalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.memoryTable.setVerticalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.memoryTable.setVerticalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.memoryTable.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.memoryTable.setHorizontalHeaderItem(1, item)
		self.verticalLayout.addWidget(self.memoryTable)
		self.clockTable = QtWidgets.QTableWidget(self.tabv1)
		self.clockTable.setMaximumSize(QtCore.QSize(225, 154))
		self.clockTable.setObjectName("clockTable")
		self.clockTable.setColumnCount(1)
		self.clockTable.setRowCount(4)
		item = QtWidgets.QTableWidgetItem()
		self.clockTable.setVerticalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.clockTable.setVerticalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.clockTable.setVerticalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.clockTable.setVerticalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.clockTable.setHorizontalHeaderItem(0, item)
		self.verticalLayout.addWidget(self.clockTable)
		self.registersTable = QtWidgets.QTableWidget(self.tabv1)
		self.registersTable.setMaximumSize(QtCore.QSize(256, 16777215))
		self.registersTable.setObjectName("registersTable")
		self.registersTable.setColumnCount(2)
		self.registersTable.setRowCount(32)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(4, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(5, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(6, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(7, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(8, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(9, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(10, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(11, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(12, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(13, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(14, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(15, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(16, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(17, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(18, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(19, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(20, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(21, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(22, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(23, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(24, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(25, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(26, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(27, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(28, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(29, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(30, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setVerticalHeaderItem(31, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.registersTable.setHorizontalHeaderItem(1, item)
		self.verticalLayout.addWidget(self.registersTable)
		self.horizontalLayout.addLayout(self.verticalLayout)
		self.horizontalLayout.setStretch(0, 100)
		self.horizontalLayout.setStretch(1, 80)
		self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
		self.tabWidget.addTab(self.tabv1, "")
		self.tabv2 = QtWidgets.QWidget()
		self.tabv2.setObjectName("tabv2")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.tabv2)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.robBufferTable = QtWidgets.QTableWidget(self.tabv2)
		self.robBufferTable.setMaximumSize(QtCore.QSize(650, 350))
		self.robBufferTable.setRowCount(10)
		self.robBufferTable.setObjectName("robBufferTable")
		self.robBufferTable.setColumnCount(5)
		item = QtWidgets.QTableWidgetItem()
		self.robBufferTable.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.robBufferTable.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.robBufferTable.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.robBufferTable.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.robBufferTable.setHorizontalHeaderItem(4, item)
		item = QtWidgets.QTableWidgetItem()
		self.robBufferTable.setHorizontalHeaderItem(5, item)
		self.gridLayout_2.addWidget(self.robBufferTable, 0, 0, 1, 1)
		self.robRegistersTable = QtWidgets.QTableWidget(self.tabv2)
		self.robRegistersTable.setMaximumSize(QtCore.QSize(16777215, 110))
		self.robRegistersTable.setObjectName("robRegistersTable")
		self.robRegistersTable.setColumnCount(32)
		self.robRegistersTable.setRowCount(2)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setVerticalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setVerticalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setHorizontalHeaderItem(4, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setHorizontalHeaderItem(5, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setHorizontalHeaderItem(6, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setHorizontalHeaderItem(7, item)
		item = QtWidgets.QTableWidgetItem()
		self.robRegistersTable.setHorizontalHeaderItem(8, item)
		self.gridLayout_2.addWidget(self.robRegistersTable, 1, 0, 1, 1)
		self.tabWidget.addTab(self.tabv2, "")
		self.gridLayout_3.addWidget(self.tabWidget, 1, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 839, 25))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.btn_grp_play = QtWidgets.QButtonGroup()
		self.btn_grp_play.setExclusive(True)
		self.btn_grp_play.addButton(self.playBtn)
		self.btn_grp_play.buttonClicked.connect(self.on_click_play)
		
		self.btn_grp_auto = QtWidgets.QButtonGroup()
		self.btn_grp_auto.setExclusive(True)
		self.btn_grp_auto.addButton(self.speedUpBtn)
		self.btn_grp_auto.buttonClicked.connect(self.on_click_auto)

		self.btn_grp_pause = QtWidgets.QButtonGroup()
		self.btn_grp_pause.setExclusive(True)
		self.btn_grp_pause.addButton(self.pauseBtn)
		self.btn_grp_pause.buttonClicked.connect(self.on_click_pause)

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Tomasulo"))
		item = self.estacoesTable.verticalHeaderItem(0)
		item.setText(_translate("MainWindow", "ER1"))
		item = self.estacoesTable.verticalHeaderItem(1)
		item.setText(_translate("MainWindow", "ER2"))
		item = self.estacoesTable.verticalHeaderItem(2)
		item.setText(_translate("MainWindow", "ER3"))
		item = self.estacoesTable.verticalHeaderItem(3)
		item.setText(_translate("MainWindow", "ER4"))
		item = self.estacoesTable.verticalHeaderItem(4)
		item.setText(_translate("MainWindow", "ER5"))
		item = self.estacoesTable.verticalHeaderItem(5)
		item.setText(_translate("MainWindow", "ER6"))
		item = self.estacoesTable.verticalHeaderItem(6)
		item.setText(_translate("MainWindow", "ER7"))
		item = self.estacoesTable.verticalHeaderItem(7)
		item.setText(_translate("MainWindow", "ER8"))
		item = self.estacoesTable.verticalHeaderItem(8)
		item.setText(_translate("MainWindow", "ER9"))
		item = self.estacoesTable.verticalHeaderItem(9)
		item.setText(_translate("MainWindow", "ER10"))
		item = self.estacoesTable.verticalHeaderItem(10)
		item.setText(_translate("MainWindow", "ER11"))
		item = self.estacoesTable.horizontalHeaderItem(0)
		item.setText(_translate("MainWindow", "Tipo"))
		item = self.estacoesTable.horizontalHeaderItem(1)
		item.setText(_translate("MainWindow", "Busy"))
		item = self.estacoesTable.horizontalHeaderItem(2)
		item.setText(_translate("MainWindow", "Instrução"))
		item = self.estacoesTable.horizontalHeaderItem(3)
		item.setText(_translate("MainWindow", "Estado"))
		item = self.estacoesTable.horizontalHeaderItem(4)
		item.setText(_translate("MainWindow", "Vj"))
		item = self.estacoesTable.horizontalHeaderItem(5)
		item.setText(_translate("MainWindow", "Vk"))
		item = self.estacoesTable.horizontalHeaderItem(6)
		item.setText(_translate("MainWindow", "Qj"))
		item = self.estacoesTable.horizontalHeaderItem(7)
		item.setText(_translate("MainWindow", "Qk"))
		item = self.estacoesTable.horizontalHeaderItem(8)
		item.setText(_translate("MainWindow", "A"))
		__sortingEnabled = self.estacoesTable.isSortingEnabled()
		self.estacoesTable.setSortingEnabled(False)
		item = self.estacoesTable.item(0, 0)
		item.setText(_translate("MainWindow", "Load/Store"))
		item = self.estacoesTable.item(1, 0)
		item.setText(_translate("MainWindow", "Load/Store"))
		item = self.estacoesTable.item(2, 0)
		item.setText(_translate("MainWindow", "Load/Store"))
		item = self.estacoesTable.item(3, 0)
		item.setText(_translate("MainWindow", "Load/Store"))
		item = self.estacoesTable.item(4, 0)
		item.setText(_translate("MainWindow", "Load/Store"))
		item = self.estacoesTable.item(5, 0)
		item.setText(_translate("MainWindow", "Add"))
		item = self.estacoesTable.item(6, 0)
		item.setText(_translate("MainWindow", "Add"))
		item = self.estacoesTable.item(7, 0)
		item.setText(_translate("MainWindow", "Add"))
		item = self.estacoesTable.item(8, 0)
		item.setText(_translate("MainWindow", "Mult"))
		item = self.estacoesTable.item(9, 0)
		item.setText(_translate("MainWindow", "Mult"))
		item = self.estacoesTable.item(10, 0)
		item.setText(_translate("MainWindow", "Mult"))
		self.estacoesTable.setSortingEnabled(__sortingEnabled)
		self.playBtn.setText(_translate("MainWindow", "Play"))
		self.speedUpBtn.setText(_translate("MainWindow", "Auto play"))
		self.pauseBtn.setText(_translate("MainWindow", "Pause"))
		item = self.memoryTable.verticalHeaderItem(0)
		item.setText(_translate("MainWindow", "24"))
		item = self.memoryTable.verticalHeaderItem(1)
		item.setText(_translate("MainWindow", "28"))
		item = self.memoryTable.verticalHeaderItem(2)
		item.setText(_translate("MainWindow", "32"))
		item = self.memoryTable.verticalHeaderItem(3)
		item.setText(_translate("MainWindow", "36"))
		item = self.memoryTable.horizontalHeaderItem(0)
		item.setText(_translate("MainWindow", "Endereço"))
		item = self.memoryTable.horizontalHeaderItem(1)
		item.setText(_translate("MainWindow", "Valor"))
		item = self.clockTable.verticalHeaderItem(0)
		item.setText(_translate("MainWindow", "Clock Corrente"))
		item = self.clockTable.verticalHeaderItem(1)
		item.setText(_translate("MainWindow", "PC"))
		item = self.clockTable.verticalHeaderItem(2)
		item.setText(_translate("MainWindow", "N.I.C."))
		item = self.clockTable.verticalHeaderItem(3)
		item.setText(_translate("MainWindow", "CPI"))
		item = self.clockTable.horizontalHeaderItem(0)
		item.setText(_translate("MainWindow", "Valor"))

		for i in range(32):
			item = self.robRegistersTable.verticalHeaderItem(i)
			if not item:
				item = QtWidgets.QTableWidgetItem()
				self.registersTable.setVerticalHeaderItem(i, item)
			item.setText(_translate("MainWindow", "R" + str(i)))

		item = self.registersTable.horizontalHeaderItem(0)
		item.setText(_translate("MainWindow", "Qi"))
		item = self.registersTable.horizontalHeaderItem(1)
		item.setText(_translate("MainWindow", "Vi"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabv1), _translate("MainWindow", "Main"))
		# item = self.robBufferTable.horizontalHeaderItem(0)
		# item.setText(_translate("MainWindow", "Entrada"))
		item = self.robBufferTable.horizontalHeaderItem(0)
		item.setText(_translate("MainWindow", "Ocupado"))
		item = self.robBufferTable.horizontalHeaderItem(1)
		item.setText(_translate("MainWindow", "ID"))
		item = self.robBufferTable.horizontalHeaderItem(2)
		item.setText(_translate("MainWindow", "Estado"))
		item = self.robBufferTable.horizontalHeaderItem(3)
		item.setText(_translate("MainWindow", "Destino"))
		item = self.robBufferTable.horizontalHeaderItem(4)
		item.setText(_translate("MainWindow", "Valor"))
		item = self.robRegistersTable.verticalHeaderItem(0)
		item.setText(_translate("MainWindow", "Reordenação"))
		item = self.robRegistersTable.verticalHeaderItem(1)
		item.setText(_translate("MainWindow", "Ocupado"))

		for i in range(32):
			item = self.robRegistersTable.horizontalHeaderItem(i)
			if not item:
				item = QtWidgets.QTableWidgetItem()
				self.registersTable.setHorizontalHeaderItem(i, item)
			item.setText(_translate("MainWindow", "R" + str(i)))

		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabv2), _translate("MainWindow", "ROB"))

	def update_register_bank(self, register_bank):
		_translate = QtCore.QCoreApplication.translate

		for i in range(32):
			item = self.registersTable.item(i, 1)
			if not item:
				item = QtWidgets.QTableWidgetItem()
				self.registersTable.setItem(i, 1, item)
			item.setText(_translate("MainWindow", str(register_bank.registers[i].Vi)))
			# self.registersTable.setItem(i, 1, item)

			item = self.registersTable.item(i, 2)
			if not item:
				item = QtWidgets.QTableWidgetItem()
				self.registersTable.setItem(i, 2, item)
			item.setText(_translate("MainWindow", register_bank.registers[i].Qi))
			# self.registersTable.setItem(i, 2, item)

	def update_RUM(self, RUM):
		_translate = QtCore.QCoreApplication.translate

		for i in range(len(RUM.list)):
			item = self.memoryTable.item(i, 0)
			if not item:
				item = QtWidgets.QTableWidgetItem()
				self.memoryTable.setItem(i, 0, item)
			item.setText(_translate("MainWindow", str(RUM.list[i][0])))

			item = self.memoryTable.item(i, 1)
			if not item:
				item = QtWidgets.QTableWidgetItem()
				self.memoryTable.setItem(i, 1, item)
			item.setText(_translate("MainWindow", str(RUM.list[i][1])))

	def update_Clock_Table(self, list_CLK_PC_NCI_CPI):
		_translate = QtCore.QCoreApplication.translate

		for i in range(4):
			item = self.clockTable.item(i-1, 1)
			if not item:
				item = QtWidgets.QTableWidgetItem()
				self.clockTable.setItem(i-1, 1, item)
			item.setText(_translate("MainWindow", str(list_CLK_PC_NCI_CPI[i])))

	def update_Stations_Table(self, station, pos):
		_translate = QtCore.QCoreApplication.translate

		for i in range(station.max_size):
			instruction = ""
			if len(station.list[i]) > 0:
				instruction = station.list[i][0]
			list = [str(station.busy[i]),
					instruction,
					station.state[i],
					str(station.Vj[i]),
					str(station.Vk[i]),
					station.Qj[i],
					station.Qk[i],
					""
				]
			for j in range(8):
				item = self.estacoesTable.item(i + pos, j + 1)
				if not item:
					item = QtWidgets.QTableWidgetItem()
					self.estacoesTable.setItem(i + pos, j + 1, item)
				item.setText(_translate("MainWindow", list[j]))

	def update_ROB_Buffer_Table(self, ROB):
		_translate = QtCore.QCoreApplication.translate

		for i in range(ROB.max_size):
			instruction = ""
			if len(ROB.list[i]) > 0:
				label = ROB.list[i][0]
				instruction = label
			list = [str(ROB.busy[i]),
					instruction,
					ROB.state[i],
					ROB.destiny[i],
					ROB.value[i]
				]
			if ROB.busy[i] == False: list[0] = ""
			
			for j in range(5):
				item = self.robBufferTable.item(i, j)
				if not item:
					item = QtWidgets.QTableWidgetItem()
					self.robBufferTable.setItem(i, j, item)
				item.setText(_translate("MainWindow", list[j]))

	def update_ROB_Registers_Table(self, ROB):
		_translate = QtCore.QCoreApplication.translate

		for i in range(32):
			item = self.robRegistersTable.item(0, i)
			if not item:
				item = QtWidgets.QTableWidgetItem()
				self.robRegistersTable.setItem(0, i, item)
			item.setText(_translate("MainWindow", ROB.RS_reorder[i]))

			item = self.robRegistersTable.item(1, i)
			if not item:
				item = QtWidgets.QTableWidgetItem()
				self.robRegistersTable.setItem(1, i, item)
			if ROB.RS_Busy[i] == True:
				item.setText(_translate("MainWindow", str(ROB.RS_Busy[i])))

	def set_Tomasulo(self, Tomasulo):
		self.Tomasulo = Tomasulo


	def on_click_play(self, playBtn):
		self.Tomasulo.play()

	def on_click_auto(self, autoplayBtn):
		self.pause = False

		while not self.pause:
			self.Tomasulo.MainWindow.show()
			if not self.Tomasulo.play(): break

	def on_click_pause(self, pauseBtn):
		self.pause = True


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())