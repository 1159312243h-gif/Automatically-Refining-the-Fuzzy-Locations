import csv
import numpy as np
import math


def compare(point, polygon):
    result = [0, 0, 0, 0, 0, 0]
    if(point[0] == '其他' or polygon[0] == '其他'):
        result[0] = 0.5
    elif(point[0] == polygon[0]):
        result[0] = 1
    elif(point[0] == '第四纪红黏土' and polygon[0] in '第四纪亚红砂土'):
        result[0] = 0.5
    elif(point[0] in '第四纪亚红砂土' and polygon[0] == '第四纪红黏土'):
        result[0] = 0.5
    elif(point[0] in '第四纪红黏土' and polygon[0] in '红砂岩类'):
        result[0] = 0.5
    elif(point[0] in '红砂岩类' and polygon[0] in '第四纪红黏土'):
        result[0] = 0.5
    elif(point[0] in '第四纪亚红砂土' and polygon[0] in '红砂岩类'):
        result[0] = 0.5
    elif(point[0] in '红砂岩类' and polygon[0] in '第四纪亚红砂土'):
        result[0] = 0.5
    elif(point[0] in '水域' and polygon[0] in '河湖相冲沉积物'):
        result[0] = 0.5
    elif(point[0] in '河湖相冲沉积物' and polygon[0] in '水域'):
        result[0] = 0.5
    elif(point[0] in '水域' and polygon[0] in '河湖相冲/沉积物'):
        result[0] = 0.5
    elif(point[0] in '河湖相冲/沉积物' and polygon[0] in '水域'):
        result[0] = 0.5
    elif(point[0] in '河湖相冲沉积物' and polygon[0] in '河湖相冲/沉积物'):
        result[0] = 1
    elif(point[0] in '河湖相冲/沉积物' and polygon[0] in '河湖相冲沉积物'):
        result[0] = 1
        
    if(point[1] == polygon[1]):
        result[1] = 1
    elif(point[1] == '101'):
        if(polygon[1] == '211'):
            result[1] = 0.6
    elif(point[1] == '211'):
        if(polygon[1] == '101'):
            result[1] = 0.6
        elif(polygon[1] == '221'):
            result[1] = 0.6
    elif(point[1] == '221'):
        if(polygon[1] == '211'):
            result[1] = 0.6
        elif(polygon[1] == '231'):
            result[1] = 0.6
    elif(point[1] == '231'):
        if(polygon[1] == '221'):
            result[1] = 0.6
        elif(polygon[1] == '232'):
            result[1] = 0.6
    elif(point[1] == '232'):
        if(polygon[1] == '231'):
            result[1] = 0.6
        elif(polygon[1] == '242'):
            result[1] = 0.6
    elif(point[1] == '242'):
        if(polygon[1] == '232'):
            result[1] = 0.6

    x1 = float(polygon[2])
    x2 = float(point[2])
    deltx = abs(x1 - x2)
    if deltx / x1 <= 1:
        result[2] = math.sqrt(1 - deltx / x1)
    else:
        result[2] = 0  # Or set other default values
        
    if(point[3] == '其他' or polygon[3] == '其他'):
        result[3] == 0.5
    elif(point[3] == polygon[3]):
        result[3] = 1
    elif(point[3] in ('水稻土', '潴育水稻土', '潜育水稻土', '渗育水稻土')):
        if(polygon[3] in ('水稻土', '潴育水稻土', '潜育水稻土', '渗育水稻土')):
            result[3] = 0.6
        elif(polygon[3] in ('红壤')):
            result[3] = 0.4
    elif(point[3] in ('红壤', '红壤性土', '黄红壤')):
        result[3] = 0.6
    elif(point[3] in ('红壤')):
        if(polygon[3] in ('水稻土', '潴育水稻土', '潜育水稻土', '渗育水稻土')):
            result[3] = 0.4
            
    deltx = abs(float(point[4]) - float(polygon[4]))
    result[4] = 1 - deltx / (float(polygon[4]) - 1000)
    if result[4] < 0:
        result[4] = 0
        
    deltx = abs(float(point[5]) - float(polygon[5]))
    result[5] = 1 - deltx / (float(polygon[5]) - 10)
    if result[5] < 0:
        result[5] = 0
        
    return result

def main():
    dept = []
    with open("data.csv", "r", newline='', encoding='gbk') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            row = [item.strip() for item in row]  # Remove whitespace from each element
            dept.append(row[:13])  # Add the first 13 columns of data to the dept list
    result = []

    for i in range(len(dept)):
        polygon = dept[i][2:7]
        point = dept[i][8:13]
        print(polygon, point)
        result.append(compare(point, polygon))
        
    with open("result.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Result"])  # Write the header row
        for res in result:
            writer.writerow([res])

# Explicitly call the main function
if __name__ == "__main__":
    main()


import csv
import math
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

class SoilFeatureComparator:
    """Soil feature comparator"""
    @staticmethod
    def compare(point_props, polygon_props):
        """
        Compare 6 attributes of point and polygon features
        :param point_props: Point feature attributes [parent material, soil subgroup, landform, elevation, temperature, precipitation]
        :param polygon_props: Polygon feature attributes [parent material, soil subgroup, landform, elevation, temperature, precipitation]
        :return: List of similarity results [0-1, 0-1, 0-1, 0-1, 0-1, 0-1]
        """
        result = [0, 0, 0, 0, 0, 0]
        
        # 1. Parent material comparison
        pm_point, pm_poly = point_props[0], polygon_props[0]
        if pm_point == '其他' or pm_poly == '其他':
            result[0] = 0.5
        elif pm_point == pm_poly:
            result[0] = 1
        elif pm_point == '第四纪红黏土' and pm_poly in '第四纪亚红砂土':
            result[0] = 0.5
        elif pm_point in '第四纪亚红砂土' and pm_poly == '第四纪红黏土':
            result[0] = 0.5
        elif pm_point in '第四纪红黏土' and pm_poly in '红砂岩类':
            result[0] = 0.5
        elif pm_point in '红砂岩类' and pm_poly in '第四纪红黏土':
            result[0] = 0.5
        elif pm_point in '第四纪亚红砂土' and pm_poly in '红砂岩类':
            result[0] = 0.5
        elif pm_point in '红砂岩类' and pm_poly in '第四纪亚红砂土':
            result[0] = 0.5
        elif pm_point in '水域' and pm_poly in ('河湖相冲沉积物', '河湖相冲/沉积物'):
            result[0] = 0.5
        elif pm_poly in '水域' and pm_point in ('河湖相冲沉积物', '河湖相冲/沉积物'):
            result[0] = 0.5
        elif (pm_point in '河湖相冲沉积物' and pm_poly in '河湖相冲/沉积物') or \
             (pm_point in '河湖相冲/沉积物' and pm_poly in '河湖相冲沉积物'):
            result[0] = 1

        # 2. Soil subgroup comparison
        elev_point, elev_poly = point_props[1], polygon_props[1]
        if elev_point == '其他' or elev_poly == 'other':
            result[1] = 0.5
        elif elev_point == elev_poly:
            result[1] = 1
        elif elev_point in ('水稻土', '潴育水稻土', '潜育水稻土', '渗育水稻土'):
            if elev_poly in ('水稻土', '潴育水稻土', '潜育水稻土', '渗育水稻土'):
                result[1] = 0.6
            elif elev_poly == '红壤':
                result[1] = 0.4
        elif elev_point in ('红壤', '红壤性土', '黄红壤'):
            result[1] = 0.6
        elif elev_point == '红壤' and elev_poly in ('水稻土', '潴育水稻土', '潜育水稻土', '渗育水稻土'):
            result[1] = 0.4

        # 3. Landform comparison
        sg_point, sg_poly = point_props[2], polygon_props[2]
        if sg_point == sg_poly:
            result[2] = 1
        elif sg_point == '101' and sg_poly == '211':
            result[2] = 0.6
        elif sg_point == '211' and sg_poly in ('101', '221'):
            result[2] = 0.6
        elif sg_point == '221' and sg_poly in ('211', '231'):
            result[2] = 0.6
        elif sg_point == '231' and sg_poly in ('221', '232'):
            result[2] = 0.6
        elif sg_point == '232' and sg_poly in ('231', '242'):
            result[2] = 0.6
        elif sg_point == '242' and sg_poly == '232':
            result[2] = 0.6

        # 4. Elevation comparison
        x1 = float(polygon_props[3])
        x2 = float(point_props[3])
        deltx = abs(x1 - x2)
        result[3] = math.sqrt(1 - deltx / x1) if deltx / x1 <= 1 else 0

        # 5. Temperature comparison
        temp_diff = abs(float(point_props[5]) - float(polygon_props[5]))
        result[4] = max(0, 1 - temp_diff / (float(polygon_props[5]) - 10))

        # 6. Precipitation comparison
        precip_diff = abs(float(point_props[6]) - float(polygon_props[6]))
        result[5] = max(0, 1 - precip_diff / (float(polygon_props[6]) - 1000))

        return result

class PointFeature:
    """Point feature class (attribute order adjusted)"""
    def __init__(self, attributes):
        """
        Initialize point feature
        :param attributes: Attribute tuple (ID, Name, X-coordinate, Y-coordinate, Parent Material, Soil Subgroup, Landform, Elevation, Temperature, Precipitation)
        """
        self.id = attributes[0]    # ID
        self.name = attributes[1]  # Name
        self.x = attributes[2]     # X-coordinate
        self.y = attributes[3]     # Y-coordinate
        self.parent_material = str(attributes[4]).strip()  # Parent material
        self.subgroup = str(attributes[5]).strip()         # Soil subgroup
        self.landform = str(attributes[6]).strip()         # Landform
        self.elevation = str(attributes[7]).strip()        # Elevation
        self.temperature = float(attributes[8])            # Temperature
        self.precipitation = float(attributes[9])          # Precipitation
        self.geometry = Point(self.x, self.y)              # Geometry information
        
    def get_properties(self):
        """Get the 6 attributes used for similarity calculation"""
        return [
            self.parent_material,
            self.subgroup,
            self.landform,
            self.elevation,
            self.temperature,
            self.precipitation
        ]

class PolygonFeature:
    """Polygon feature class (attribute order adjusted)"""
    def __init__(self, attributes):
        """
        Initialize polygon feature
        :param attributes: Attribute tuple (ID, Name, Parent Material, Soil Subgroup, Landform, Elevation, Temperature, Precipitation, Geometry Information)
        """
        self.id = attributes[0]    # ID
        self.name = attributes[1]  # Name
        self.parent_material = str(attributes[2]).strip()  # Parent material
        self.subgroup = str(attributes[3]).strip()         # Soil subgroup
        self.landform = str(attributes[4]).strip()         # Landform
        self.elevation = str(attributes[5]).strip()        # Elevation
        self.temperature = float(attributes[6])            # Temperature
        self.precipitation = float(attributes[7])          # Precipitation
        self.geometry = attributes[8]                      # Geometry information
        
    def get_properties(self):
        """Get the 6 attributes used for similarity calculation"""
        return [
            self.parent_material,
            self.subgroup,
            self.landform,
            self.elevation,
            self.temperature,
            self.precipitation
        ]
    
    def get_centroid(self):
        """Get the centroid coordinates of the polygon feature"""
        centroid = self.geometry.centroid
        return [centroid.x, centroid.y]

def load_point_features(shp_path):
    """Load point feature data"""
    gdf = gpd.read_file(shp_path)
    return [PointFeature(tuple(row)[1:]) for _, row in gdf.iterrows()]

def load_polygon_features(shp_path):
    """Load polygon feature data"""
    gdf = gpd.read_file(shp_path)
    # Assuming geometry information is in the last column, with other attributes preceding it
    return [PolygonFeature((*row[1:-1], row[-1])) for _, row in gdf.iterrows()]

def main():
    try:
        # Load data
        points = load_point_features("point.shp")
        polygons = load_polygon_features("polygon.shp")
        
    except Exception as e:
        print(f"Program error: {str(e)}")

if __name__ == "__main__":
    main()