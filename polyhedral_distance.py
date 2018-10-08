"""

Calculates the distance between two points using a specified 
polyhedral finsler metric. Also outputs an image demonstrating
the translation/ scaling representing this distance calculation.

By : Adam Azlan, Haidan Tang, Melissa George, Yinlan Shao

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

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
    plt.title('Unit ball for this metric')
    plt.axis('scaled')
    plt.show()
    
# Plots the original unit ball as well as a translated /
# scaled ball which shows the distance calculation
def plot_distance_calculation(ordered_points, P, Q, distance):
    
    # Calculate points for the translated polygon
    transformed_points = []
    for point in ordered_points:
        scaled = p_times_k(point, distance)
        translated = q_plus_p(P, scaled)
        transformed_points.append(translated)
    
    plt.axes()
    original_polygon = plt.Polygon(ordered_points, fill=None, edgecolor='r')
    transformed_polygon = plt.Polygon(transformed_points, fill=None, edgecolor='b')
    plt.gca().add_patch(original_polygon)
    plt.gca().add_patch(transformed_polygon)
    plt.plot([0], [0], marker='o', markersize=4, color="r")
    plt.plot([P[0]], [P[1]], marker='o', markersize=4, color='m')
    plt.plot([Q[0]], [Q[1]], marker='o', markersize=4, color='g')
    plt.grid(color='k', linestyle=':', linewidth=1)
    plt.title('Calculation for d(P, Q)')
    plt.axis('scaled')
    plt.show()


# Calculate the difference between two points P, Q
# in cartesian coordinates
# (Mark's step 1)
def q_minus_p(Q, P):
    return (Q[0] - P[0], Q[1] - P[1])

# Calculate the sum of the two points P, Q 
# in cartesian coordinates
def q_plus_p(Q, P):
    return(Q[0] + P[0], Q[1] + P[1])
    
# Calculate a point when it is scaled by a factor of K
def p_times_k(P, K):
    return (P[0] * K, P[1] * K)

# Given a polygon and a point, find the vertices
# or vertex where the line from the origin to point
# intersects the polygon
# (Mark's step 2)
def find_intersection(ordered_points, P):
    # Get the polar form of both the point P and the ordered_points
    P_polar = cartesian_to_polar(P)
    ordered_points_polar = []
    
    for point in ordered_points:
        ordered_points_polar.append(cartesian_to_polar(point))

    # Find the vertex / vertices where phi coordinate is between
    # or equal to P_polar's phi coordinate
    for i in range(0, len(ordered_points_polar)):
        if i == len(ordered_points_polar) - 1:
            if P_polar[1] > ordered_points_polar[i][1]:
                return (ordered_points_polar[0], ordered_points_polar[i])
            elif P_polar[1] == ordered_points_polar[i][1]:
                return (ordered_points_polar[i], ordered_points_polar[i])
        elif P_polar[1] > ordered_points_polar[i][1] and P_polar[1] < ordered_points_polar[i+1][1]:
            return (ordered_points_polar[i], ordered_points_polar[i + 1])
        elif P_polar[1] == ordered_points_polar[i][1]:
            return (ordered_points_polar[i], ordered_points_polar[i])

# Function which takes in ordered set of points for 
# the unit ball and calculates d(P, Q) using the 
# Polyhedral Finsler Metric defined by the points
# (Mark's step 3)
def calculate_distance(ordered_points, P, Q):
    # Calculate the point Q - P
    R = q_minus_p(Q, P)
    
    # Find the intersection of the polygon and a line
    # drawn from the origin to R
    V = find_intersection(ordered_points, R)
    
    # Divide the polar radius of R by the polar radius
    # of V to get the distance in this metric
    
    R_radius = cartesian_to_polar(R)[0]
    
    if V[0] == V[1]:
        V_radius = V[0][0]
        return R_radius / V_radius
    else:
        p1 = polar_to_cartesian(V[0])
        p2 = polar_to_cartesian(V[1])
        
        m = 0

        if p2[0] != p1[0]:
            m = (p2[1] - p1[1]) / (p2[0] - p1[0])
            
        b = p2[1] - m * p2[0]
        
        V_radius = 0
        
        if R[0] == 0:
            point = (0, b)
            V_radius = cartesian_to_polar(point)[0]
        else:
            j = R[1] / R[0]
            if m == 0 and j == 0:
                point = (p1[0], 0)
                V_radius = cartesian_to_polar(point)[0]
            else:
                x = b / (j - m)
                y = m * x + b
                point = (x, y)
                V_radius = cartesian_to_polar(point)[0]

        return R_radius / V_radius

# Main function
def main():
    # Square
    # points = [(1, -1), (-1, 1), (1, 1), (-1, -1)]
    
    # Octagon
    # points = [(1, 0), (0.707106, 0.707106), (0,1), (-0.707106, 0.707106), (-1, 0), (-0.707106, -0.707106), (0, -1), (0.707106, -0.707106)]
    
    # Take in points for the polygon that defines the metric
    points = []
    point = input("Please enter a point in the form 'x y' or 'done' to signal you're done entering points:\n")
    while point != 'done':
        points.append((float((point.split())[0]), float((point.split())[1])))
        point = input("Enter another point or enter 'done':\n")
    
    print("The points you entered are:\n", points)
    print("Plotting the unit ball for this metric:\n")
    
    # Order points
    ordered_points = order_points(points)
    
    # Plot the shape with the specified points
    plot_shape(ordered_points)
    
    # Print instructions on entering points
    print("You can now start finding distances between points in this metric. Enter points in the form 'x y' when prompted, and type 'quit' at any time.")
    
    # Allow user to enter several points and calculate distances between them
    P = ''
    Q = ''
    while(P != 'quit' and Q != 'quit'):
        
        print("Enter points P and Q to find the distance between them:")
        
        P = input("P:")
        if P != 'quit':
            P = (float(P.split()[0]), float(P.split()[1]))
        else:
            break
            
        Q = input("Q:")
        if Q != 'quit':
            Q = (float(Q.split()[0]), float(Q.split()[1]))
        else:
            break
    
        distance = calculate_distance(ordered_points, P, Q)
        print("Distance between P : ", P[0], " ", P[1], " and Q : ", Q[0], Q[1], " is : ", distance)
        plot_distance_calculation(ordered_points, P, Q, distance)

if __name__ == '__main__':
    main()
    
