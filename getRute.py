import math
from qgis.core import (	QgsWkbTypes, 
			QgsMapLayerType, 
			QgsPointXY, 
			QgsCoordinateReferenceSystem, 
			QgsProject, 
			QgsCoordinateTransform, 
			QgsAnnotationPointTextItem,
			QgsGeometry,
			QgsPoint)

from qgis.gui import QgsRubberBand
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class getRute:
	def __init__(self, layer, mapCanvas):
		
		self.layerRute = layer
		self.layer_type = layer.type()
		self.layerEPSG = layer.crs().authid()
		self.points = []
		self.lines_total = []
		self.mapCanvas = mapCanvas
		
		crsMap = QgsCoordinateReferenceSystem(self.mapCanvas.mapSettings().destinationCrs().authid())
		crsGps = QgsCoordinateReferenceSystem("EPSG:4326")
		crsCalc = QgsCoordinateReferenceSystem("EPSG:3857")   
		crsLayer = QgsCoordinateReferenceSystem(self.layerEPSG) 

		transformContext = QgsProject.instance().transformContext()             # Crear instancia de tranformacion

		self.gps_to_calc_transformCoord = QgsCoordinateTransform(crsGps, crsCalc, transformContext)             # Crear formulario transformacion
		self.gps_to_map_transformCoord = QgsCoordinateTransform(crsGps, crsMap, transformContext)
		self.layer_to_calc_transformCoord = QgsCoordinateTransform(crsLayer, crsCalc, transformContext)
		self.layer_to_map_transformCoord = QgsCoordinateTransform(crsLayer, crsMap, transformContext)
		self.calc_to_layer_transformCoord = QgsCoordinateTransform(crsCalc, crsLayer, transformContext)
		self.calc_to_gps_transformCoord = QgsCoordinateTransform(crsCalc, crsGps, transformContext)
	
	def valid(self):
						
		if self.layer_type == QgsMapLayerType.RasterLayer:
			print("Capa Raster")
			return False

		elif self.layer_type == QgsMapLayerType.VectorLayer:
			if self.layerRute.wkbType() == QgsWkbTypes.LineString or self.layerRute.wkbType() == QgsWkbTypes.MultiLineString:
				print("Capa Linea")
				
				features = self.layerRute.getFeatures()
				for feature in features:
					geom = feature.geometry()
					geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
					if geom.type() == QgsWkbTypes.LineGeometry:

						if geomSingleType:
							#self.lines.append(geom.asPolyline())
							v = geom.asPolyline()
							line = []
							print("Vertines: ", len(v), " Long: ", geom.length())
							if geom.length() > 10:
								for p in v:
									x, y = self.layer_to_calc_transformCoord.transform(p)
									#x, y = p
									point = [x, y]
									line.append(point)
								self.lines_total.append(line)

						else:					
							x = geom.asMultiPolyline()
							for v in x:
								line = []
								print("Vertines: ", len(v), " Long: ", geom.length())
								if geom.length() > 10:
									for p in v:
										x, y = self.layer_to_calc_transformCoord.transform(p)
										#x, y = p
										point = [x, y]
										line.append(point)
									self.lines_total.append(line)

			#for i in self.lines_total:
			#	print(i)

			return True

"""	
			elif self.layerRute.wkbType() == QgsWkbTypes.MultiLineString:
				print("Capa Multilinea")
				
				features = self.layerRute.getFeatures()
				for feature in features:
					geom = feature.geometry()
					geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
					if geom.type() == QgsWkbTypes.LineGeometry:
						if geomSingleType:
							self.points.append(geom.asPolyline())
							x = geom.asPolyline()
							#print("Linea: ", x, "long: ", geom.length())
						else:					
							x = geom.asMultiPolyline()
							for v in x:
								self.points.append(v)
								print(len(v))
								#print("PoliLinea: ", x, "long: ", geom.length())

				return True

		if self.layer_type == QgsMapLayerType.VectorLayer:
		
			#print(self.layerRute.wkbType())
			features = self.layerRute.getFeatures()
			self.points = []

			for feature in features:
				geom = feature.geometry()
				geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
				
				if geom.type() == QgsWkbTypes.LineGeometry:
					point_type = 1
					if geomSingleType:
						self.points.append(geom.asPolyline())
						x = geom.asPolyline()
						#print("Linea: ", x, "long: ", geom.length())
					else:					
						x = geom.asMultiPolyline()
						for v in x:
							self.points.append(v)
						#print("PoliLinea: ", x, "long: ", geom.length())

				elif geom.type() == QgsWkbTypes.PointGeometry:
					if geomSingleType:
						point_type = 2
						x = geom.asPoint()
						self.points.append(geom.asPoint())
					else:
						point_type = 3
						x = geom.asMultiPoint()
						#print("Multipunto: ",x)
						for v in x:
							self.points.append(v)
				else:
					print("Geometria No soportada")
					return False
			
			if point_type != 0:			
				if len(self.points) > 0:
					if point_type == 1:
						self.points = self.points[0]
						point_valid = True
						#print("Vertices: ", len(self.points))
				
					elif point_type == 2:
						#print("type = 2")
						if len(self.points) > 1:
							point_valid = True
							#print("Cantidad de Entidades: ", len(self.points))
		
					elif point_type == 3:
						#print("type = 3")
						if len(self.points) > 1:
							point_valid = True
							#print("Cantidad de Entidades: ", len(self.points))
					
					if point_valid:
						self.create_globals()
						return True
					else:
						return False

				else:	
					print("Capa Vacia")
					return False

			else:
				print("Capa No Valida")
				return False

		elif self.layer_type == QgsMapLayerType.RasterLayer:
			print("Capa Raster no Valida")
			return False
		else:
			print("Capa No soportada")
			return False
"""
"""
	def create_globals(self):
		crsMap = QgsCoordinateReferenceSystem(self.mapCanvas.mapSettings().destinationCrs().authid())
		crsGps = QgsCoordinateReferenceSystem("EPSG:4326")
		crsCalc = QgsCoordinateReferenceSystem("EPSG:3857")   
		crsLayer = QgsCoordinateReferenceSystem(self.layerEPSG) 

		transformContext = QgsProject.instance().transformContext()             # Crear instancia de tranformacion

		self.gps_to_calc_transformCoord = QgsCoordinateTransform(crsGps, crsCalc, transformContext)             # Crear formulario transformacion
		self.gps_to_map_transformCoord = QgsCoordinateTransform(crsGps, crsMap, transformContext)
		self.layer_to_calc_transformCoord = QgsCoordinateTransform(crsLayer, crsCalc, transformContext)
		self.layer_to_map_transformCoord = QgsCoordinateTransform(crsLayer, crsMap, transformContext)
		self.calc_to_layer_transformCoord = QgsCoordinateTransform(crsCalc, crsLayer, transformContext)
		self.calc_to_gps_transformCoord = QgsCoordinateTransform(crsCalc, crsGps, transformContext)
	

		self.r_polyline = QgsRubberBand(self.mapCanvas, False)                                       # False = a no poligono a dibujar
		self.r_polyline.setLineStyle(Qt.PenStyle(Qt.DashLine))
		self.r_polyline.setWidth(2)                                                             # Se define grosor de la linea
		self.r_polyline.setColor( QColor(255, 0, 0) )                                           # Color de la linea
		
		self.g_polyline = QgsRubberBand(self.mapCanvas, False)                                       # False = a no poligono a dibujar
		self.g_polyline.setLineStyle(Qt.PenStyle(Qt.DashLine))
		self.g_polyline.setWidth(2)                                                             # Se define grosor de la linea
		self.g_polyline.setColor( QColor(0, 255, 0) ) 
		
		self.gps_points = []

	def init_rute(self, longitude, latitude):
		
		index_end = len(self.points) - 1
		
		pt_log = self.gps_to_calc_transformCoord.transform(QgsPointXY(longitude, latitude))
		pt1 = self.layer_to_calc_transformCoord.transform(self.points[0])
		pt2 = self.layer_to_calc_transformCoord.transform(self.points[index_end])

		l1 = self.lenth_angle(pt1, pt_log) 
		l2 = self.lenth_angle(pt2, pt_log)

		if l1 > l2:
			self.points = self.points[::-1]
		
		pt1 =  self.layer_to_calc_transformCoord.transform(self.points[0])
		pt2 =  self.layer_to_calc_transformCoord.transform(self.points[1])

		lenth, angle = self.lenth_angle(pt1, pt2)
		x, y = self.point_pos(pt1, 6, angle)

		x, y = self.calc_to_layer_transformCoord.transform(QgsPointXY(x, y))
		self.points.insert(0, QgsPointXY(x, y))

	def run(self, longitude, latitude):

		index = len(self.gps_points)
		
		if index == 0:
			self.gps_points.insert(0, self.gps_to_calc_transformCoord.transform(QgsPointXY(longitude, latitude)))
		
		else:
			pt = self.gps_to_calc_transformCoord.transform(QgsPointXY(longitude, latitude))	
			lenth, angle = self.lenth_angle(pt, self.gps_points[0])
			
			if lenth >= 0.2:
				self.gps_points.insert(0, pt)
				if index == 3:
					self.gps_points.pop(3)

			if index == 3:
				
				#lenth1, angle1 = self.lenth_angle(self.gps_points[0], self.gps_points[1])
				#lenth2, angle2 = self.lenth_angle(self.gps_points[1], self.gps_points[2])
				
				#delta_angle = angle1 - angle2
				#angle_rumbo = delta_angle + angle1
				
				#x, y = self.point_pos(self.gps_points[0],6,angle_rumbo)
				#longitude, latitude =  self.calc_to_gps_transformCoord.transform(QgsPointXY(x, y))
				self.rumbo(self.gps_points)
				self.paint(longitude, latitude)

	def rumbo(self, points):
		
		print(points)

	def paint(self, longitude, latitude):

		#annotation_layer = QgsProject.instance().mainAnnotationLayer()
	
		list_points_paint = []

		px_map, py_map = self.gps_to_map_transformCoord.transform(QgsPointXY(longitude, latitude))
		list_points_paint.append(QgsPoint(px_map, py_map))

		#label = QgsAnnotationPointTextItem('Test', QgsPointXY(px_map - 2, py_map - 2))
		#label.setAngle(45)
		#annotation_layer.addItem(label)
	

		px_map, py_map = self.layer_to_map_transformCoord.transform(self.points[0])
		list_points_paint.append(QgsPoint(px_map, py_map))
		
		self.g_polyline.setToGeometry(QgsGeometry.fromPolyline(list_points_paint), None)

		list_points_paint = []
	
		px_map, py_map = self.gps_to_map_transformCoord.transform(QgsPointXY(longitude, latitude))
		list_points_paint.append(QgsPoint(px_map, py_map))
		
		px_map, py_map = self.layer_to_map_transformCoord.transform(self.points[1])
		list_points_paint.append(QgsPoint(px_map, py_map))
		self.r_polyline.setToGeometry(QgsGeometry.fromPolyline(list_points_paint), None)

	def lenth_angle(self, point2, point1):
		
		angle = math.degrees(math.atan2(point2[1] - point1[1], point2[0] - point1[0]))
		if angle < 0: angle = 360 - abs(angle)
		if angle >= 360: angle %= 360

		lenth = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
		#print("lenth: " + str(lenth))
		#print(angle)
		return lenth, angle

	def point_pos(self, point, distance, angle):
		theta_rad = math.radians(angle)
		return float(point[0] + distance * math.cos(theta_rad)), float(point[1] + distance * math.sin(theta_rad))
	
	def erase(self):
		self.r_polyline.reset(QgsWkbTypes.LineGeometry)
		self.g_polyline.reset(QgsWkbTypes.LineGeometry)

"""
