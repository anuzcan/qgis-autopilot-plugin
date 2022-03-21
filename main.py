import os
import serial
import serial.tools.list_ports
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox

from qgis.utils import iface
from qgis.gui import QgsRubberBand, QgsMapToolEmitPoint
from qgis.core import Qgis, QgsApplication, QgsProject, QgsSettings, QgsMessageLog, QgsVectorLayer, QgsPoint, QgsGeometry, QgsWkbTypes, QgsDistanceArea

from .autopilot import getRute

def classFactory(iface):
	return Main_Plugin(iface)

class Main_Plugin:
	def __init__(self, iface):
		self.iface = iface
        
		self.canvas = iface.mapCanvas()
	
	def initGui(self):

		#Definir icono agregar al interfaz de Qgis
		path = os.path.dirname( os.path.abspath( __file__ ) )
		icon_path = os.path.join(path,"icon.png")
		self.action = QAction(QIcon(icon_path),"&Herramienta",self.iface.mainWindow())
		self.iface.addToolBarIcon(self.action)
		self.action.triggered.connect(self.run)
		
		#Cargamos la interfaz grafica
		self.dock = uic.loadUi( os.path.join( path, "dock.ui" ) )
		
		self.dock.buttonConnect.clicked.connect(self.connect_port)
		self.dock.led_on.clicked.connect(self.led_on)
		self.dock.led_off.clicked.connect(self.led_off)
		self.dock.testButton.clicked.connect(self.test)
		self.dock.selectLayerRuteButton.clicked.connect(self.selectLayerRute)
		self.dock.buttonClose_plugin.clicked.connect(self.closePlugin)
		
		#Banderas
		self.flatPort = False

		#self.pointTool = QgsMapToolEmitPoint(self.canvas)
		#self.pointTool.canvasClicked.connect(self.display_point)	

	def unload(self): 

		self.iface.removeToolBarIcon(self.action)
		del self.action

	def run(self):					# Iniciamos plugin en interfaz

		self.iface.addDockWidget( Qt.RightDockWidgetArea, self.dock )   # Agregamos panel a interface
		#self.iface.mapCanvas().renderComplete.connect(self.renderTest)
		self.initPlugin()

	def initPlugin(self):
		ports = []
		for i in serial.tools.list_ports.comports():
			#print(str(i).split(" ")[0])
			ports.append(str(i).split(" ")[0])
		
		self.dock.comboBox_ports.addItems(ports)
	
	def display_point(self, pointTool):
		print('{:.4f},{:.4f}'.format(pointTool[0], pointTool[1]))	
		print("algo")	

	def test(self):
		#self.r = QgsRubberBand(self.canvas, False)  # False = not a polygon
		#points = [QgsPoint(-100, 45), QgsPoint(10, 60), QgsPoint(120, 45)]
		#self.r.setToGeometry(QgsGeometry.fromPolyline(points), None)
		print("test")

	def renderTest(self, painter):
    		# use painter for drawing to map canvas
    		print ("TestPlugin: renderTest called!")

	def selectLayerRute(self):
		ruta = QgsProject().instance().mapLayersByName(self.dock.mMapLayerComboBox.currentText())[0]
		
		rute = getRute(ruta)
		rute.printVert()
		rute.distance_points()

	def connect_port(self):
		if self.flatPort == False:
			self.port = serial.Serial(self.dock.comboBox_ports.currentText())
			
			if self.port.is_open == True:
				self.dock.buttonConnect.setText("Disconnect")
				self.flatPort = True
		else:
			self.port.close()
			self.flatPort = False
			self.dock.buttonConnect.setText("Connect")
	
	def led_on(self):
		self.port.write(b'1')

	def led_off(self):
		self.port.write(b'0')

	def closePlugin(self):
		
		if self.flatPort == True:
			self.port.close()
		
		#self.iface.mapCanvas().renderComplete.disconnect(self.renderTest)
		self.dock.close()                                   # Cierra plugin
