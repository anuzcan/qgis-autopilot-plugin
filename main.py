import os
import serial
import serial.tools.list_ports
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox

from qgis import utils
from qgis.gui import QgsRubberBand
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
		self.flat_gps_active = False
		self.flat_layer_select = False

	def unload(self): 

		self.iface.removeToolBarIcon(self.action)
		del self.action

	def run(self):					# Iniciamos plugin en interfaz

		self.iface.addDockWidget( Qt.RightDockWidgetArea, self.dock )   # Agregamos panel a interface
		self.initPlugin()
		self.connect_GPS()

	def initPlugin(self):
		ports = []
		for i in serial.tools.list_ports.comports():
			#print(str(i).split(" ")[0])
			ports.append(str(i).split(" ")[0])
		
		self.dock.comboBox_ports.addItems(ports)

	def connect_GPS(self):

		self.connectionList = QgsApplication.gpsConnectionRegistry().connectionList()

		if self.connectionList == []:                           # Si no se encuentra ningun dispositivo gps disponible
			utils.iface.messageBar().pushMessage("Error ","Dispositivo GPS no Conectado",level=Qgis.Critical,duration=3)
			self.flat_gps_active = False

		else:                                                   # Dispositivo gps detectado
			utils.iface.messageBar().pushMessage("OK ","Dispositivo GPS Encontrado",level=Qgis.Info,duration=3)
			self.GPS = self.connectionList[0]             
			self.GPS.stateChanged.connect(self.status_changed)  # Conecta signal con recepcion de dato nuevo
			self.GPS.destroyed.connect(self.connectionLost)     # En caso de desconeccion dispara rutina
			self.flat_gps_active = True

	def status_changed(self,gpsInfo):
		if self.GPS.status() == 3:                              # Si se recibe nueva ubicacion GPS
			now = gpsInfo.utcDateTime.currentDateTime().toString(Qt.TextDate)
			print(now)
			print(gpsInfo.longitude)
			print(gpsInfo.latitude)
			if self.flat_layer_select:
				self.rute.init_vert(gpsInfo.longitude, gpsInfo.latitude)

	def connectionLost(self):
		try:
			self.GPS.stateChanged.disconnect(self.status_changed)
		except:
			pass

		utils.iface.messageBar().pushMessage("Error ","Perdida Conexion",level=Qgis.Critical,duration=5)

	def test(self):
		#print("test")
		self.rute.erase()

	def selectLayerRute(self):
		ruta = QgsProject().instance().mapLayersByName(self.dock.mMapLayerComboBox.currentText())[0]
		
		self.rute = getRute(ruta, self.canvas)
		self.flat_layer_select = True
		
		#longitude = -85.49951
		#latitude = 10.39042
		#self.rute.init_vert(longitude, latitude)

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
		if self.flat_gps_active:
			self.GPS.stateChanged.disconnect(self.status_changed)
			del self.GPS

		self.dock.close()                                   # Cierra plugin
