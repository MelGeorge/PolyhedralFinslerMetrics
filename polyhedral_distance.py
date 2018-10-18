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

# Input: an list of ordered points (x,y)
# Output: true if it is convex, false otherwise
def is_convex(ordered_points):
    # n is the number of points
    n = len(ordered_points)
    
    ordered_points.append(ordered_points[0])
    ordered_points.append(ordered_points[1])
    
    for i in range(0,n):
        p1 = ordered_points[i]
        p2 = ordered_points[i+1]
        p3 = ordered_points[i+2]
        x1 = p2[0] - p1[0]
        y1 = p2[1] - p1[1]
        x2 = p3[0] - p2[0]
        y2 = p3[1] - p2[1]
        dot_product = x1*x2 + y1*y2
        if dot_product > 0 and x1*y2 != x2*y1:
            return False

    return True

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
def find_points(ordered_points, P):
    
    # Get the polar form of both the point P and the ordered_points
    P_polar = cartesian_to_polar(P)
    ordered_points_polar = []
    
    for point in ordered_points:
        ordered_points_polar.append(cartesian_to_polar(point))

    greatest_negative = -np.pi
    greatest_negative_index = 0
    least_positive = np.pi
    least_positive_index = 0

    # Find the vertex/ vertices where phi is between or equal to P_polar's phi coordinate
    for i in range(0, len(ordered_points_polar)):
        # Keep track of where the greatest negative phi and least positive phi are
        if ordered_points_polar[i][1] > greatest_negative and ordered_points_polar[i][1] < 0:
            greatest_negative = ordered_points_polar[i][1]
            greatest_negative_index = i
        if ordered_points_polar[i][1] < least_positive and ordered_points_polar[i][1] > 0:
            least_positive = ordered_points_polar[i][1]
            least_positive_index = i
            
        # Special cases if we're looking at the last point
        if i == len(ordered_points_polar) - 1:
            # Q-P may intersect between the first and last point
            if P_polar[1] > ordered_points_polar[i][1] or P_polar[1] < ordered_points_polar[i][1]:
                return (ordered_points_polar[0], ordered_points_polar[i])
            # Q-P may intersect the last point exactly
            elif P_polar[1] == ordered_points_polar[i][1]:
                return (ordered_points_polar[i], ordered_points_polar[i])
            # Q-P may intersect between the two points nearest to the positive x-axis
            elif P_polar[1] < least_positive and P_polar[1] > greatest_negative:
                return (ordered_points_polar[greatest_negative_index], ordered_points_polar[least_positive_index])
        # Case when Q-P intersects between two points
        elif P_polar[1] > ordered_points_polar[i][1] and P_polar[1] < ordered_points_polar[i+1][1]:
            return (ordered_points_polar[i],ordered_points_polar[i+1])
        # Case when Q-P intersects a point on the polygon exactly
        elif P_polar[1] == ordered_points_polar[i][1]:
            return (ordered_points_polar[i],ordered_points_polar[i])

# Function which takes in ordered set of points for 
# the unit ball and calculates d(P, Q) using the 
# Polyhedral Finsler Metric defined by the points
def calculate_distance(ordered_points, P, Q):
    # Calculate the point Q - P
    R = q_minus_p(Q, P)

    # Special case -- distance is zero
    if R == (0, 0):
        return 0
    
    # Find the corners the polygon between which the line
    # drawn from the origin to R will intersect.
    # Call these points p1 and p2
    V = find_points(ordered_points, R)
    p1 = polar_to_cartesian(V[0])
    p2 = polar_to_cartesian(V[1])

    x = 0
    y = 0

    # Handle cases where different slopes are infinite
    if p1[0] == p2[0] and R[0] != 0:
        # Fit a line to the points R = (x,y) and (0,0)
        m_r, b_r = np.polyfit([R[0], 0], [R[1], 0], 1)

        # Calculate x, y
        x = p1[0]
        y = m_r * x + b_r
    elif p1[0] != p2[0] and R[0] == 0:
        # Fit a line to the points p1 and p2
        m_v, b_v = np.polyfit([p1[0], p2[0]], [p1[1], p2[1]], 1)

        # Calculate x, y
        x = R[0]
        y = m_v * x + b_v
    else:
        # Fit a line to each pair of points
        m_v, b_v = np.polyfit([p1[0], p2[0]], [p1[1], p2[1]], 1)
        m_r, b_r = np.polyfit([R[0], 0], [R[1], 0], 1)
 
        # Calculate x, y
        x = (b_v - b_r) / (m_r - m_v)
        y = m_v * x + b_v

    intersection = (x, y)
    
    # Calculate polar radius to R=Q-P
    R_radius = cartesian_to_polar(R)[0]
    
    # Calculate polar radius to point where R intersects with the polygon
    V_radius = cartesian_to_polar(intersection)[0]
    
    # Distance from P to Q is R_radius / V_radius
    return R_radius / V_radius

# Main function
def main():
    # Take in points for the polygon that defines the metric
    points = []
    point = input("Please enter a point in the form 'x y' or 'done' to signal you're done entering points:\n")
    while point != 'done':
        points.append((float((point.split())[0]), float((point.split())[1])))
        point = input("Enter another point or enter 'done':\n")

    # When user is done, print points so user can confirm
    print("The points you entered are:\n", points)
    
    # Order points
    ordered_points = order_points(points)
    
    # Check if the polygon is convex
    # TODO : Debug is_convex function and uncomment this check
    # It is commented out for now so the program will run in the meantime
    #convex = is_convex(ordered_points)
    convex = True
    
    if not convex:
        # Warn user that points do not form a convex polygon
        # Draw shape so user can see that it is not a convex
        # polygon and then exit the program with an error
        print("The entered points do not form a convex polygon. Here is the current shape:")
        plot_shape(ordered_points)
        raise ValueError("The entered points do not form a convex polygon. Exiting")
        
    # Plot the shape with the specified points
    print("Plotting the unit ball for this metric:\n")
    plot_shape(ordered_points)
    
    # Print instructions on entering points
    print("You can now start finding distances between points in this metric. \
    Enter points in the form 'x y' when prompted, and type 'quit' at any time.")
    
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
    
