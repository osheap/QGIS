
#additional requirements for these classes:
    #1) each one needs an instance caalled name for storing name of water body
    #2) need geometry variable                                                                                                                                                                                                         `

import qgis
import qgis.core

# abstract class Waterbody is the root class of our hierarchy 
class Waterbody():
    
    # constructor (can be derived by subclasses)
    def __init__(self, name, geometry):
        self.name = name
        self.geometry = geometry                # instance variable for storing the name of the watebrbody
    # abstract static class method for creating a waterbody object if the given way satisfies
    # the required conditions; needs to be overridden by instantiable subclasses 
    def fromOSMWay(way, allNodes):     
        pass
    
    # abstract method for creating QgsFeature object for this waterbody;
    # needs to be overridden by instantiable subclasses 
    def toQgsFeature(self):
        pass
    

# abstract class LinearWaterBody is derived from class Waterbody
class LinearWaterbody(Waterbody):
    
    # constructor (can be invoked by derived classes and takes care of the length computation)
    def __init__(self, name, geometry):
        super(LinearWaterbody, self).__init__(name, geometry)
        
        # calculate length of this linear waterbody
        qda = qgis.core.QgsDistanceArea() 
        qda.setEllipsoid('WGS84')
        length = qda.measureLength(geometry)

        # instance variable for storing the length of this linear waterbody
        self.length = qda.convertLengthMeasurement(length, qgis.core.QgsUnitTypes.DistanceMeters) 




# abstract class ArealWaterbody is derived from class Waterbody
class ArealWaterbody(Waterbody):

    # constructor (can be invoked by derived classes and takes care of the area computation)
    def __init__(self, name, geometry):
        super(ArealWaterbody, self).__init__(name, geometry)

        # calculate area of this areal waterbody
        qda = qgis.core.QgsDistanceArea() 
        qda.setEllipsoid('WGS84')
        area = qda.measureArea(geometry)

        # instance variable for storing the length of this areal waterbody
        self.area = qda.convertAreaMeasurement(area, qgis.core.QgsUnitTypes.AreaSquareMeters)

#establish Lake class
class Lake(ArealWaterbody):
    # constructor (calls (ArealWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry, type):
        super(Lake, self).__init__(name, geometry)
        self.type = "lake"

    #establish fromOSMWay() static class method
    def fromOSMWay(way, allNodes):
        #condition for selecting lakes
        if way['type'] == 'way' and 'natural' in way['tags'] and 'water' in way['tags'] and way['tags']['natural'] == 'water' and way['tags']['water']=='lake':
            # condition for defining name
            if 'name' in way['tags']:
                name = way['tags']['name']
            else:
                name = 'unknown'
            #create an empty list to fill with points
            pointsList = []
            type='lake'
            #loop through nodes
            for node in way['nodes']:
                #grab lat and lon, use them to establish a QgsPoints feature, and append the feature to the empty list
                lat = allNodes[node]['lat']
                lon = allNodes[node]['lon']
                feature = qgis.core.QgsPointXY(lon, lat)
                pointsList.append(feature)
            #create geometry from points list, overwrite the instance variables for name and geometry, and return new geometry
            polylineGeometry = qgis.core.QgsGeometry.fromPolygonXY([pointsList])

            newLake = Lake(name, polylineGeometry,type)

            return newLake
        #else condition, return none
        else:
            return None

    # establish toQgsFeature() static class method
    def toQgsFeature(self):
        #grab instances, define type, and establish feature geometry and attributes to be returned
        area = self.area
        name = self.name
        geometry = self.geometry
        type = self.type
        attributesList = [name,type,area]
        feat = qgis.core.QgsFeature()
        feat.setGeometry(geometry)
        feat.setAttributes(attributesList)

        return feat

    # Establish self string method
    def __str__(self):
        return f"feature name: {self.name}, feature type: {self.type}, feature area: {self.area}"

#establish pond class
class Pond(ArealWaterbody):
    # constructor (calls (ArealWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry, type):
        super(Pond, self).__init__(name, geometry)
        self.type = 'pond'

    # establish fromOSMWay() static class method
    def fromOSMWay(way, allNodes):
        # condition for selecting ponds
        if way['type'] == 'way' and 'natural' in way['tags'] and 'water' in way['tags'] and way['tags']['natural'] == 'water' and way['tags']['water'] == 'pond':
            # condition for defining name
            if 'name' in way['tags']:
                name = way['tags']['name']
            else:
                name = 'unknown'
            # create an empty list to fill with points
            pointsList = []
            type='pond'
            # loop through nodes
            for node in way['nodes']:
                # grab lat and lon, use them to establish a QgsPoints feature, and append the feature to the empty list
                lat = allNodes[node]['lat']
                lon = allNodes[node]['lon']
                feature = qgis.core.QgsPointXY(lon, lat)
                pointsList.append(feature)
            # create geometry from points list, overwrite the instance variables for name and geometry, and return new geometry
            polylineGeometry = qgis.core.QgsGeometry.fromPolygonXY([pointsList])

            newPond = Pond(name, polylineGeometry,type)

            return newPond
        # else condition, return none
        else:
            return None

    # establish toQgsFeature() static class method
    def toQgsFeature(self):
        # grab instances, define type, and establish feature geometry and attributes to be returned
        area = self.area
        name = self.name
        geometry = self.geometry
        type = self.type
        attributesList = [name, type, area]
        feat = qgis.core.QgsFeature()
        feat.setGeometry(geometry)
        feat.setAttributes(attributesList)

        return feat

    # Establish self string method
    def __str__(self):
        return f"feature name: {self.name}, feature type: {self.type}, feature area: {self.area}"

#establish Reservoir class
class Reservoir(ArealWaterbody):

    # constructor (calls ArealWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry, type):
        super(Reservoir, self).__init__(name, geometry)
        self.type = "reservoir"
    # establish fromOSMWay() static class method
    def fromOSMWay(way, allNodes):
        # condition for selecting reservoirs
        if way['type'] == 'way' and 'natural' in way['tags'] and 'water' in way['tags'] and way['tags']['natural'] == 'water' and way['tags']['water'] == 'reservoir':
            # condition for defining name
            if 'name' in way['tags']:
                name = way['tags']['name']
            else:
                name = 'unknown'
            # create an empty list to fill with points
            pointsList = []
            type = 'reservoir'
            # loop through nodes
            for node in way['nodes']:
                # grab lat and lon, use them to establish a QgsPoints feature, and append the feature to the empty list
                lat = allNodes[node]['lat']
                lon = allNodes[node]['lon']
                feature = qgis.core.QgsPointXY(lon, lat)
                pointsList.append(feature)
            # create geometry from points list, overwrite the instance variables for name and geometry, and return new geometry
            polylineGeometry = qgis.core.QgsGeometry.fromPolygonXY([pointsList])

            newReservoir = Reservoir(name, polylineGeometry, type)

            return newReservoir
        # else condition, return none
        else:
            return None

    # establish toQgsFeature() static class method
    def toQgsFeature(self):
        # grab instances, define type, and establish feature geometry and attributes to be returned
        area = self.area
        name = self.name
        geometry = self.geometry
        type = self.type
        attributesList = [name, type, area]
        feat = qgis.core.QgsFeature()
        feat.setGeometry(geometry)
        feat.setAttributes(attributesList)

        return feat

    # Establish self string method
    def __str__(self):
        return f"feature name: {self.name}, feature type: {self.type}, feature area: {self.area}"

# establish Stream class
class Stream(LinearWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry, type):
        super(Stream,self).__init__(name, geometry)
        self.type = 'stream'

    # establish fromOSMWay() static class method
    def fromOSMWay(way, allNodes):
        # condition for selecting streams
        if way['type']=='way' and 'waterway' in way['tags'] and way['tags']['waterway']=='stream':
            # condition for defining name
            if 'name' in way['tags']:
                name = way['tags']['name']
            else:
                name = 'unknown'
            # create an empty list to fill with points
            pointsList = []
            type = 'stream'
            # loop through nodes
            for node in way['nodes']:
                # grab lat and lon, use them to establish a QgsPoints feature, and append the feature to the empty list
                lat = allNodes[node]['lat']
                lon = allNodes[node]['lon']
                feature=qgis.core.QgsPointXY(lon,lat)
                pointsList.append(feature)
            # create geometry from points list, overwrite the instance variables for name and geometry, and return new geometry
            polylineGeometry = qgis.core.QgsGeometry.fromPolylineXY(pointsList)

            newStream = Stream(name,polylineGeometry,type)

            return newStream
        # else condition, return none
        else:
            return None

    # establish toQgsFeature() static class method
    def toQgsFeature(self):
        # grab instances, define type, and establish feature geometry and attributes to be returned
        length = self.length
        name = self.name
        geometry = self.geometry
        type = self.type
        attributesList = [name,type,length]
        feat = qgis.core.QgsFeature()
        feat.setGeometry(geometry)
        feat.setAttributes(attributesList)

        return feat

    # Establish self string method
    def __str__(self):
        return f"feature name: {self.name}, feature type: {self.type}, feature length: {self.length}"


# establish Stream class
class River(LinearWaterbody):

    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry, type):
        super(River, self).__init__(name, geometry)
        self.type="river"

    # establish fromOSMWay() static class method
    def fromOSMWay(way, allNodes):
        # condition for selecting river
        if way['type'] == 'way' and 'waterway' in way['tags'] and way['tags']['waterway'] == 'river':
            # condition for defining name
            if 'name' in way['tags']:
                name = way['tags']['name']
            else:
                name = 'unknown'
            # create an empty list to fill with points
            pointsList = []
            type = 'river'
            # loop through nodes
            for node in way['nodes']:
                # grab lat and lon, use them to establish a QgsPoints feature, and append the feature to the empty list
                lat = allNodes[node]['lat']
                lon = allNodes[node]['lon']
                feature = qgis.core.QgsPointXY(lon, lat)
                pointsList.append(feature)
            # create geometry from points list, overwrite the instance variables for name and geometry, and return new geometry
            polylineGeometry = qgis.core.QgsGeometry.fromPolylineXY(pointsList)

            newRiver = River(name, polylineGeometry, type)

            return newRiver
        # else condition, return none
        else:
            return None

    # establish toQgsFeature() static class method
    def toQgsFeature(self):
        # grab instances, define type, and establish feature geometry and attributes to be returned
        length = self.length
        name = self.name
        geometry = self.geometry
        type = self.type
        attributesList = [name,type,length]
        feat = qgis.core.QgsFeature()
        feat.setGeometry(geometry)
        feat.setAttributes(attributesList)

        return feat

    # Establish self string method
    def __str__(self):
        return f"feature name: {self.name}, feature type: {self.type}, feature length: {self.length}"

# establish Canal class
class Canal(LinearWaterbody):

    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry, type):
        super(Canal, self).__init__(name, geometry)
        self.type = 'canal'

    # establish fromOSMWay() static class method
    def fromOSMWay(way, allNodes):
        # condition for selecting canals
        if way['type'] == 'way' and 'waterway' in way['tags'] and way['tags']['waterway'] == 'canal':
            # condition for defining name
            if 'name' in way['tags']:  # ['tags']['name'] == "":
                name = way['tags']['name']
            else:
                name = 'unknown'
            # create an empty list to fill with points
            pointsList = []
            type = 'canal'
            # loops through nodes
            for node in way['nodes']:
                # grab lat and lon, use them to establish a QgsPoints feature, and append the feature to the empty list
                lat = allNodes[node]['lat']
                lon = allNodes[node]['lon']
                feature = qgis.core.QgsPointXY(lon, lat)
                pointsList.append(feature)
            # create geometry from points list, overwrite the instance variables for name and geometry, and return new geometry
            polylineGeometry = qgis.core.QgsGeometry.fromPolylineXY(pointsList)

            newCanal = Canal(name, polylineGeometry, type)

            return newCanal
        # else condition, return none
        else:
            return None

    # establish toQgsFeature() static class method
    def toQgsFeature(self):
        # grab instances, define type, and establish feature geometry and attributes to be returned
        length = self.length
        name = self.name
        geometry = self.geometry
        type = self.type
        attributesList = [name,type,length]
        feat = qgis.core.QgsFeature()
        feat.setGeometry(geometry)
        feat.setAttributes(attributesList)

        return feat

    # Establish self string method
    def __str__(self):
        return f"feature name: {self.name}, feature type: {self.type}, feature length: {self.length}"