Geographic Scene Matching and Evaluation Algorithm
This repository contains the code for matching geographic scene features, evaluating feature similarities, and calculating positioning distances. It consists of a core matching algorithm, an entropy-based weight calculation module, and spatial distance utilities.

Environment & Dependencies
Python Version: Python 3.11.5

Required Libraries: * pandas

numpy

math

csv

geopandas

shapely.geometry

geopy.distance

Code Functionality & Structure
1. compare.py (Feature Matching Library)
This script acts as the foundational library for the project. It implements the configuration of matching parameters and handles the complex similarity calculations between different elements within the selected geographic scene features. It is heavily utilized by the core algorithm (Appendix B) to build the model and compute matching values between scene units and sample points.

2. Appendix A1: Entropy Weight Calculation
This module calculates the feature importance weights for various geographic scene elements. It takes the similarity values of reference sample points (computed using compare.py) and applies the Entropy Weight Method to objectively assign a weight to each geographic feature based on its information entropy.

3. Appendix A2: Core Matching Algorithm
This is the core execution script of the project. Its workflow includes:

Reading the required target sample points and geographic scene units.

Performing spatial and attribute-based filtering.

Calculating weighted similarities using the parameters from compare.py.

Running iterative loops over the units to identify the absolute best-matching scene unit for each sample point.

Outputting the final optimal matching pairs along with their respective similarity scores.

4. Distance Evaluation Module
To evaluate the actual accuracy and effectiveness of the positioning model, an additional distance calculation module is included. By inputting the latitude and longitude coordinates of two distinct points, it calculates the real-world geographic distance between them.