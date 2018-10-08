"""

Calculates the distance between two points using a specified 
polyhedral finsler metric. Also outputs an image demonstrating
the translation/ scaling representing this distance calculation.

By : Adam Azlan, Haidan Tang, Melissa George, Yinlan Shao

"""

import numpy as np
import matplotlib.pyplot as plt

# From Stack Overflow
def cartesian_to_polar(pair):
    x = pair[0]
    y = pair[1]
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return (rho, phi)

# From Stack Overflow
def polar_to_cartesian(pair):
    rho = pair[0]
    phi = pair[1]
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

# Returns an ordered list of points using polar coordinates
def order_points(points):
    
    # Create a list of points along with the value of phi 
    # when they are written in polar coordinates
    polar_points = []
    
    for point in points:
        rho, phi = cartesian_to_polar(point)
        polar_points.append((point[0], point[1], phi))
        
    # Sort the points based on their polar coordinates
    polar_points.sort(key=lambda tup: tup[2])
    
    # Build and return a list of the (x, y) values for 
    # points in sorted order
    ordered_points = []
    
    for point in polar_points:
        ordered_points.append((point[0], point[1]))
    
    return ordered_points
    

# Plots a shape with specified points
def plot_shape(points):
    plt.axes()
    polygon = plt.Polygon(points, fill=None, edgecolor='r')
    plt.gca().add_patch(polygon)
    plt.plot([0], [0], marker='o', markersize=4, color="r")
    plt.grid(color='k', linestyle=':', linewidth=1)
    plt.axis('scaled')
    plt.show()
    

# Main function
def main():
    # Points for a polygon centered about the origin
    # points = [(1, -1), (-1, 1), (1, 1), (-1, -1), (2, 1), (3, 10), (18, 20)]
    
    # Octagon
    points = [(1, 0), (0.707106, 0.707106), (0,1), (-0.707106, 0.707106), (-1, 0), (-0.707106, -0.707106), (0, -1), (0.707106, -0.707106)]
    
    # Take in points for the polyhedron that defines the metric
    
    # Order points
    ordered_points = order_points(points)
    
    # Plot the shape with the specified points
    plot_shape(ordered_points)

if __name__ == '__main__':
    main()
    
