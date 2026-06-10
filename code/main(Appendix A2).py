from compare import *
import geopandas as gpd
import pandas as pd
import numpy as np
import csv
from shapely.geometry import Point

class PointFeature:
    """Point feature class"""
    def __init__(self, attributes):
        """
        Initialize point feature
        :param attributes: A tuple containing all attributes, ordered as follows:
            0: ID
            1: Name
            2: X coordinate
            3: Y coordinate
            4: Parent material
            5: Soil subgroup
            6: Landform
            7: Elevation
            8: Temperature
            9: Precipitation
        """
        self.id = attributes[0]    # ID
        self.name = attributes[1]  # Name
        self.x = attributes[2]     # X coordinate
        self.y = attributes[3]     # Y coordinate
        self.parent_material = attributes[4]  # Parent material
        self.subgroup = attributes[5]         # Soil subgroup
        self.landform = attributes[6]         # Landform
        self.elevation = attributes[7]        # Elevation
        self.temperature = attributes[8]      # Temperature
        self.precipitation = attributes[9]    # Precipitation
        self.geometry = Point(self.x, self.y) # Geometry information

    def get_properties(self):
        """Get the 6 properties used for similarity calculation (order corresponds to the weight coefficients)"""
        return [
            self.parent_material,  # Parent material
            self.subgroup,         # Soil subgroup
            self.landform,         # Landform
            self.elevation,        # Elevation
            self.temperature,      # Temperature
            self.precipitation     # Precipitation
        ]

class PolygonFeature:
    """Polygon feature class (updated attribute order)"""
    def __init__(self, attributes):
        """
        Initialize polygon feature (attribute order adjusted)
        :param attributes: A tuple containing all attributes, ordered as follows:
            0: ID
            1: Name
            2: Parent material
            3: Soil subgroup
            4: Landform
            5: Elevation
            6: Temperature
            7: Precipitation
            8: Geometry information
        """
        self.id = attributes[0]    # ID
        self.name = attributes[1]  # Name
        self.parent_material = attributes[2]  # Parent material
        self.subgroup = attributes[3]         # Soil subgroup
        self.landform = attributes[4]         # Landform
        self.elevation = attributes[5]        # Elevation
        self.temperature = attributes[6]      # Temperature
        self.precipitation = attributes[7]    # Precipitation
        self.geometry = attributes[8]         # Geometry information
        
    def get_properties(self):
        """Get the 6 properties used for similarity calculation (order corresponds to the weight coefficients)"""
        return [
            self.parent_material,  # Parent material
            self.subgroup,         # Soil subgroup
            self.landform,         # Landform
            self.elevation,        # Elevation
            self.temperature,      # Temperature
            self.precipitation     # Precipitation
        ]
    
    def get_centroid(self):
        """Get the centroid coordinates of the polygon feature"""
        centroid = self.geometry.centroid
        return [centroid.x, centroid.y]

class SimilarityCalculator:
    """Similarity calculation class"""
    def __init__(self, threshold=0.7):
        self.threshold = threshold
        # Attribute weight coefficients (Order: Parent material, Soil subgroup, Landform, Elevation, Temperature, Precipitation)
        self.coefficients = [0.297511, 0.566607, 0.058110, 0.032395, 0.031473, 0.013905]
        self.resultxy = []
        self.similarities = []
    
    def calculate_similarity(self, parameters):
        """Calculate weighted similarity"""
        return sum(coef * param for coef, param in zip(self.coefficients, parameters))
    
    def is_adjacent(self, unit, current_feature):
        """Determine if two polygon features are adjacent"""
        return unit.geometry.intersects(current_feature.geometry)
    
    def process_features(self, point_features, polygon_features):
        """Process all point and polygon features"""
        print(f"Started processing {len(point_features)} point features...")
        for i, point_feature in enumerate(point_features):
            self._process_single_point(point_feature, polygon_features)
            print(f"Progress: {i+1}/{len(point_features)} - Coordinates: {self.resultxy[i]} - Similarity: {self.similarities[i]:.4f}")
    
    def _process_single_point(self, point_feature, polygon_features):
        """Process a single point feature"""
        polygon_feature = self._find_polygon_by_id(polygon_features, point_feature.id)
        
        if polygon_feature is None:
            print(f"Warning: Polygon feature with ID {point_feature.id} not found")
            self.resultxy.append([0, 0])
            self.similarities.append(0)
            return
        
        similarity = self._calculate_feature_similarity(point_feature, polygon_feature)
        
        if similarity >= self.threshold:
            self._handle_high_similarity(polygon_feature, similarity)
        else:
            self._handle_low_similarity(point_feature, polygon_feature, polygon_features, similarity)
    
    def _calculate_feature_similarity(self, point_feature, polygon_feature):
        """Calculate the similarity between two features"""
        result = compare(point_feature.get_properties(), polygon_feature.get_properties())
        return self.calculate_similarity(result)
    
    def _find_polygon_by_id(self, polygon_features, feature_id):
        """Find polygon feature by ID"""
        return next((f for f in polygon_features if f.id == feature_id), None)
    
    def _handle_high_similarity(self, polygon_feature, similarity):
        """Handle high similarity cases"""
        self.resultxy.append(polygon_feature.get_centroid())
        self.similarities.append(similarity)
    
    def _handle_low_similarity(self, point_feature, current_feature, polygon_features, similarity):
        """Handle low similarity cases"""
        max_similarity = similarity
        max_feature = current_feature
        
        # Find polygon features with the same name
        same_name_features = [f for f in polygon_features if f.name == point_feature.name]
        
        # Check adjacent units
        for feature in same_name_features:
            if self.is_adjacent(feature, current_feature):
                current_sim = self._calculate_feature_similarity(point_feature, feature)
                if current_sim > max_similarity:
                    max_similarity = current_sim
                    max_feature = feature
        
        if max_similarity >= self.threshold:
            self._handle_high_similarity(max_feature, max_similarity)
        else:
            # Globally search for the most similar unit
            for feature in polygon_features:
                current_sim = self._calculate_feature_similarity(point_feature, feature)
                if current_sim > max_similarity:
                    max_similarity = current_sim
                    max_feature = feature
            
            self._handle_high_similarity(max_feature, max_similarity)
    
    def save_results(self):
        """Save results to CSV files"""
        # Save coordinate information
        pd.DataFrame(self.resultxy, columns=['lon', 'lat']).to_csv('location.csv', index=False)
        # Save similarity information
        pd.DataFrame(self.similarities, columns=['similarity']).to_csv('similarity.csv', index=False)
        print(f"Results saved: location.csv ({len(self.resultxy)} records), similarity.csv ({len(self.similarities)} records)")

def load_features(point_shp, polygon_shp):
    """Load data (adjusted according to the new attribute order)"""
    # Read point features (adjust according to the actual table structure, determine which column to start reading from)
    test_points = gpd.read_file(point_shp)
    point_features = [PointFeature(tuple(row)[1:]) for _, row in test_points.iterrows()]
    
    # Read polygon features
    polygons = gpd.read_file(polygon_shp)
    # Adjust according to the actual table structure, determine which column to start reading from
    polygon_features = [PolygonFeature(tuple(row)[2:]) for _, row in polygons.iterrows()]
    
    print(f"Data loaded successfully: {len(point_features)} point features, {len(polygon_features)} polygon features")
    return point_features, polygon_features

def main():
    try:
        point_features, polygon_features = load_features("point.shp", "polygon.shp")
        calculator = SimilarityCalculator(threshold=0.7)
        calculator.process_features(point_features, polygon_features)
        calculator.save_results()
    except Exception as e:
        print(f"Program runtime error: {str(e)}")

if __name__ == "__main__":
    main()