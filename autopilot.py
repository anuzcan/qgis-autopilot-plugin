from qgis.core import QgsWkbTypes, QgsDistanceArea, QgsMapLayerType, QgsPointXY, QgsCoordinateReferenceSystem, QgsProject, QgsCoordinateTransform, QgsGeometry, QgsPoint
from qgis.gui import QgsRubberBand
from PyQt5.QtGui import QColor

class getRute:
	def __init__(self,layer, mapCanvas):
		
		self.layerRute = layer
		layer_type = self.layerRute.type()
		layerEPSG = self.layerRute.crs().authid()

		crsMap = QgsCoordinateReferenceSystem(mapCanvas.mapSettings().destinationCrs().authid())
		crsGps = QgsCoordinateReferenceSystem("EPSG:4326")
		crsCalc = QgsCoordinateReferenceSystem("EPSG:3857")   
		crsLayer = QgsCoordinateReferenceSystem(layerEPSG) 

		transformContext = QgsProject.instance().transformContext()             # Crear instancia de tranformacion

		self.gps_to_calc_transformCoord = QgsCoordinateTransform(crsGps, crsCalc, transformContext)             # Crear formulario transformacion
		self.gps_to_map_transformCoord = QgsCoordinateTransform(crsGps, crsMap, transformContext)
		self.calc_to_map_transformCoord = QgsCoordinateTransform(crsCalc, crsMap, transformContext)		
		self.layer_to_map_transformCoord = QgsCoordinateTransform(crsLayer, crsMap, transformContext)
		self.gps_to_layer_transformCoord = QgsCoordinateTransform(crsGps, crsLayer, transformContext)

		self.r_polyline = QgsRubberBand(mapCanvas, False)                                       # False = a no poligono a dibujar
		self.r_polyline.setWidth(1)                                                             # Se define grosor de la linea
		self.r_polyline.setColor( QColor(0, 255, 0) )                                           # Color de la linea
		
		self.point_type = 0

		if layer_type == QgsMapLayerType.VectorLayer:
			#print("Capa Vectorial")
			#print(layer.wkbType())
			features = self.layerRute.getFeatures()
			self.points = []

			for feature in features:
				geom = feature.geometry()
				geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
				
				if geom.type() == QgsWkbTypes.LineGeometry:
					self.point_type = 1
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
						self.point_type = 2
						x = geom.asPoint()
						#print("Punto: ",x)
						self.points.append(geom.asPoint())
					else:
						self.point_type = 3
						x = geom.asMultiPoint()
						#print("Multipunto: ",x)
						for v in x:
							self.points.append(v)
				else:
					print("Geometria desconocida")			

			self.formatVert()

		elif layer_type == QgsMapLayerType.RasterLayer:
			print("Capa Raster no Valida")
		else:
			print("Capa Identificada")


	def formatVert(self):
		if self.point_type == 1:
			self.points = self.points[0]
			#print("Vertices: ", len(self.points))
				
		elif self.point_type == 2:
			print("type = 2")
			print(self.points)	
			#print("Cantidad de Entidades: ", len(self.points))
		
		elif self.point_type == 3:
			print("type = 3")
			print(self.points)	
			#print("Cantidad de Entidades: ", len(self.points))

		else:
			print("Capa Vacia")

	def init_vert(self, longitude, latitude):
		list_vert = []
		pt1 = self.gps_to_layer_transformCoord.transform(QgsPointXY(longitude, latitude))
		index_end = len(self.points) - 1
		
		px_map, py_map = self.layer_to_map_transformCoord.transform(pt1)
		list_vert.append(QgsPoint(px_map, py_map))

		d = QgsDistanceArea()
		d.setEllipsoid('EPSG:3857')

		if d.measureLine(pt1, self.points[0]) > d.measureLine(pt1, self.points[index_end]):
			px_map, py_map = self.layer_to_map_transformCoord.transform(self.points[index_end])
			list_vert.append(QgsPoint(px_map, py_map))
		else:
			px_map, py_map = self.layer_to_map_transformCoord.transform(self.points[0])
			list_vert.append(QgsPoint(px_map, py_map))

		#print("init Distance in meter: ", d.measureLine(pt1, self.points[0]))
		#print("end Distance in meter: ", d.measureLine(pt1, self.points[index_end]))

		self.r_polyline.setToGeometry(QgsGeometry.fromPolyline(list_vert), None)

	def distance_points(self):
		if self.status == 1:
			point1 = self.points[0][0]
			point2 = self.points[0][1]

			print (point1)
			print (point2)
	
			d = QgsDistanceArea()
			d.setEllipsoid('EPSG:5367')
		
			print("Distance in meter: ", d.measureLine(point1, point2))

			coordX = point1.x()
			coordY = point1.y()

			print("x: ", coordX, "y: ", coordY)
	
	def erase(self):
		self.r_polyline.reset(QgsWkbTypes.LineGeometry)
