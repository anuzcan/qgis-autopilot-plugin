from qgis.core import QgsWkbTypes, QgsDistanceArea

class getRute:
	def __init__(self,layer):
		
		self.layerRute = layer
		layer_type = self.layerRute.type()
		self.status = 0

		if layer_type == 0:
			print("Capa Vectorial")
			features = self.layerRute.getFeatures()
			self.points = []

			for feature in features:
				geom = feature.geometry()
				geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
				
				if geom.type() == QgsWkbTypes.LineGeometry:
					self.status = 1
					if geomSingleType:
						self.points.append(geom.asPolyline())
						#x = geom.asPolyline()
						#print("Linea: ", x, "long: ", geom.length())
					else:					
						x = geom.asMultiPolyline()
						for v in x:
							self.points.append(v)
						#print("PoliLinea: ", x, "long: ", geom.length())
#				elif geom.type() == QgsWkbTypes.PointGeometry:
#					if geomSingleType:
#						#x = geom.asPoint()
#						#print("Punto: ",x)
#						self.points.append(geom.asPoint())
#					else:
#						x = geom.asMultiPoint()
#						#print("Multipunto: ",x)
#						for v in x:
#							self.points.append(v)


#				elif geom.type() == QgsWbkTypes.PolygonGeometry:
#					if geomSingleType:
#						self.points.append(geom.asPolygon())
#						#x = geom.asPolygon()
#						#print("Poligono: ", x, "Area: ", geom.area())
#					else:
#						x = geom.asMultiPolygon()
#						#print("Poligono Multiple: ", x, "Area: ", geom.area())
#						for v in x:
#							self.points.append(v)
				else:
					print("Geometria desconocida")			

		elif layer_type == 1:
			print("Capa Raster")
		else:
			print("Capa no soportada")


	def printVert(self):
		if self.points:
			print(self.points)	
			print("Cantidad de Entidades: ", len(self.points))
		else:
			print("Capa Vacia")

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
		
	def test(self):
		print("test")
