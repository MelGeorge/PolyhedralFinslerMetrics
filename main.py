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

def cross_point(point1, point2, point3):
    x1=point1[0]
    y1=point1[1]
    x2=point2[0]
    y2=point2[1]
    
    x3=point3[0]
    y3=point3[1]
    x4=0
    y4=0
    
    k1=(y2-y1)*1.0/(x2-x1)
    b1=y1*1.0-x1*k1*1.0
    if (x4-x3)==0:
        k2=None
        b2=0
    else:
        k2=(y4-y3)*1.0/(x4-x3)
        b2=y3*1.0-x3*k2*1.0
    if k2==None:
        x=x3
    else:
        x=(b2-b1)*1.0/(k1-k2)
    y=k1*x*1.0+b1*1.0
    return (x,y)

# Returns an ordered list of points using polar coordinates
def order_points(points):
    
    # Create a list of points along with the value of phi
    # when they are written in polar coordinates
    polar_points = []
    
    for point in points:
        polar_points.append(cartesian_to_polar(point))
    # Sort the points based on their polar coordinates
    polar_points.sort(key=lambda tup: tup[1])
    
    return polar_points


# Plots a shape with specified points
def plot_shape(points):
    plt.ylabel('y-axis')
    plt.xlabel('x-axis')
    polygon = plt.Polygon(points, fill=None, edgecolor='r')
    plt.gca().add_patch(polygon)
    plt.plot([0], [0], marker='o', markersize=6, color="r")
    plt.grid(color='k', linestyle=':', linewidth=1)
    plt.axis('scaled')

# Main function
def main():
    
    points = [(1, 0), (0,1), (-1, 0), (0,-1)]
    plot_shape(points)
    polar_points = order_points(points)
    
    # input
    in_1 = (1, 0)
    in_2 = (2, 1)
    
    # vec = Y-X
    vec = (in_2[0] - in_1[0], in_2[1] - in_1[1])
    vec_polar = cartesian_to_polar(vec)
    plt.plot([vec[0]],  [vec[1]], marker='o', markersize=10, color="g")
    plt.show()
    
    lamda=0
    # extract all the angles of vertices
    res_list = [x[1] for x in polar_points]
    for idx in range(len(res_list)) :
        if vec_polar[1] < res_list[idx]
            A = polar_to_cartesian(ordered_points[idx-1])
            B = polar_to_cartesian(ordered_points[idx])
            # the crossing point
            cross = cross_point(A, B, vec)
            # this is the final lamda
            lamda = vec[0]/cross[0]
            break

    #using for testing: lamda = 2
    final_vtx=[]
    for pt in points :
        final_vtx.append((pt[0]*lamda, pt[1]*lamda))

plot_shape(final_vtx)
plt.show()

if __name__ == '__main__':
    main()
