import pygmt

# Define the two points (latitude, longitude)
point1 = [37.7749, -122.4194]  # San Francisco, CA
point2 = [34.0522, -118.2437]  # Los Angeles, CA

# Create a PyGMT figure
fig = pygmt.Figure()

# Set the region to include both points
fig.basemap(region=[-125, -115, 32, 40], projection="M15c", frame=True)

# Plot the coastlines
fig.coast(shorelines="1/0.5p,black", land="lightgray", water="lightblue")

# Plot the two points
fig.plot(
    x=[point1[1], point2[1]],  # Longitudes
    y=[point1[0], point2[0]],  # Latitudes
    style="c0.3c",  # Circle with 0.3 cm diameter
    fill="red",  # Fill color
    pen="black",  # Outline color
    label="Cities",
)

# Plot the geodetic curve (great-circle path) between the two points
fig.plot(
    x=[point1[1], point2[1]],  # Longitudes
    y=[point1[0], point2[0]],  # Latitudes
    pen="2p,blue",  # Line thickness and color
    straight_line=True,  # Ensures a great-circle path
    label="Geodetic Curve",
)

# Add a legend
fig.legend(position="jBL+jBL+o0.2c", box=True)

# Save the figure
fig.savefig("geodetic_curve_map.png", dpi=300)

# Display the figure
fig.show()