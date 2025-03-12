import pygmt
import pandas as pd
import os

def plot_event_moll_map(df_info, event, event_fig, clon=None, colormap='geo', topo_data="@earth_relief_20m"):
    '''
    Utpal Kumar
    2021, March
    Plot a Mollweide projection map showing event and station locations.

    param df_info: pandas DataFrame containing station and event coordinates.
                  Required columns: stlo, stla, evlo, evla.
    param event: event name (type: str).
    param event_fig: output figure name (type: str).
    param clon: central longitude for the projection (type: float, optional).
    param colormap: colormap for topography (type: str, default: 'geo').
    param topo_data: topography data file (type: str, default: '@earth_relief_20m').
    '''
    # Check if required columns are present
    required_columns = ["stlo", "stla", "evlo", "evla"]
    if not all(col in df_info.columns for col in required_columns):
        raise ValueError(f"Input DataFrame must contain the following columns: {required_columns}")

    # Set resolution and central longitude
    res = "f"
    if not clon:
        clon = df_info["stlo"].mean()
    proj = f"W{clon:.1f}/20c"

    # Create figure
    fig = pygmt.Figure()
    fig.basemap(region="g", projection=proj, frame=True)
    fig.grdimage(grid=topo_data, shading=True, cmap=colormap)
    fig.coast(resolution=res, shorelines=["1/0.2p,black", "2/0.05p,gray"], borders=1)

    # Plot stations
    fig.plot(
        x=df_info["stlo"].values,
        y=df_info["stla"].values,
        style="i2p",
        fill="blue",  # Use 'fill' for symbol color
        pen="black",
        label="Station",
    )

    # Plot event
    fig.plot(
        x=df_info["evlo"].values[0],
        y=df_info["evla"].values[0],
        style="a15p",
        fill="red",  # Use 'fill' for symbol color
        pen="black",
        label="Event",
    )

    # Draw lines from event to stations
    for stlo, stla in zip(df_info["stlo"].values, df_info["stla"].values):
        fig.plot(
            x=[df_info["evlo"].values[0], stlo],
            y=[df_info["evla"].values[0], stla],
            pen="1p,red",  # Use 'pen' for line color and thickness
            straight_line=True,
        )

    # Save figure
    fig.savefig(event_fig, crop=True, dpi=300)
    print(f"Map saved as {event_fig}")

if __name__ == "__main__":
    event = "test_event"
    data_info_file = f"data_info_{event}.txt"
    event_fig = f"event_map_{event}.png"

    # Check if input file exists
    if not os.path.exists(data_info_file):
        raise FileNotFoundError(f"Input file {data_info_file} not found.")

    # Read data and plot map
    df_info = pd.read_csv(data_info_file)
    plot_event_moll_map(df_info, event, event_fig)