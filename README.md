# PolyhedralFinslerMetrics
--------------------------
By : Adam Azlan, Haidan Tang, Melissa George, Yinlan Shao

## Goal:
Given a Polyhedral Finsler Metric, write a Python script which can calculate the distance between any two points taken as input, and show a visual representation of this calculation.

## So far:
* Created functions for translating between polar/ cartesian coordinates
* Created function for ordering a given set of points based on polar coordinates
* Created function for plotting the shape of a polygon
* Be able to take in points for the polygon from user
* Be able to take in points from user and calculate distance
* Draw a simulation to demonstrate translation/ scaling 

![Octagon](https://raw.githubusercontent.com/MelGeorge/PolyhedralFinslerMetrics/master/images/octagon.png)

Given the Polyhedral Finsler Metric defined by a 'unit octagon', the distance between (10, 10) and (5, 4) is defined as follows:
![OctagonMetric](https://raw.githubusercontent.com/MelGeorge/PolyhedralFinslerMetrics/master/images/octagonMetric.png)

Given the Polyhedral Finsler Metric defined by a unit square, the distance between (10, 10) and (5, 5) is defined as follows:
![SquareMetric](https://raw.githubusercontent.com/MelGeorge/PolyhedralFinslerMetrics/master/images/squareMetric.png)



## To do:
* Be able to take in points for the polygon from user
* Be able to take in points from user and calculate distance
* Draw a simulation to demonstrate translation/ scaling 

## Setup:
To be able to run the project yourself, you'll need to do a few things:
* Install Python3
* Install numpy module
* Install matplotlib module

## To run:
```python
python3 polyhedral_distance.py
```
