import numpy as np
import pygmt

def plot_geodetic_curve(point1, point2, output_file="geodetic_curve_map.png", dpi=300):
    """
    Plot a geodetic curve between two points on a map and save the figure.
    
    Parameters:
    point1 (list or tuple): Coordinates of the first point [longitude, latitude].
    point2 (list or tuple): Coordinates of the second point [longitude, latitude].
    output_file (str): Name of the output file to save the figure (default: "geodetic_curve_map.png").
    dpi (int): Resolution of the output figure in dots per inch (default: 300).
    """
    # Extract longitude and latitude for both points
    lon1, lat1 = point1
    lon2, lat2 = point2

    # Dynamically determine the region to cover both points with some padding
    lon_min = min(lon1, lon2) - 5  # Add 5 degrees padding on each side
    lon_max = max(lon1, lon2) + 5
    lat_min = min(lat1, lat2) - 5
    lat_max = max(lat1, lat2) + 5

    # Ensure the region stays within valid geographic bounds
    lon_min = max(-180, lon_min)
    lon_max = min(180, lon_max)
    lat_min = max(-90, lat_min)
    lat_max = min(90, lat_max)

    # Create a plot with coast, Mercator projection (M)
    fig = pygmt.Figure()
    fig.coast(
        region=[lon_min, lon_max, lat_min, lat_max],  # Dynamic region based on points
        projection="M15c",
        frame=True,
        borders=1,
        area_thresh=4000,
        shorelines="0.25p,black",
    )

    # Prepare data for the geodetic curve
    data = np.array([list(point1) + list(point2)])

    # Plot geographic geodetic curve between the two points
    fig.plot(
        data=data,
        style="=0.5c+s+e+a30+gblue+h0.5+p1p,blue",  # Geographic curve with endpoints
        pen="1.0p,blue"
    )

    # Add markers for the two points
    fig.plot(x=lon1, y=lat1, style="c0.3c", fill="blue", pen="1p,black")
    fig.plot(x=lon2, y=lat2, style="c0.3c", fill="blue", pen="1p,black")

    # Add labels for the two points (labels are "Point 1" and "Point 2")
    fig.text(text="Point 1", x=lon1, y=lat1+2, font="10p,Helvetica,blue")
    fig.text(text="Point 2", x=lon2, y=lat2+2, font="10p,Helvetica,blue")

    # Save the figure
    fig.savefig(output_file, dpi=dpi)

# Example usage with Vienna and Delhi
VIENNA = [16.3738, 48.2082]  # Vienna coordinates (lon, lat)
DELHI = [77.1025, 28.7041]   # Delhi coordinates (lon, lat)
plot_geodetic_curve(VIENNA, DELHI, output_file="vienna_delhi_map.png")