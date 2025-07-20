import numpy as np
from numpy import sqrt
from scipy.spatial.distance import pdist, squareform
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Data Import Path
SENSORS_CSV = 'data/geocoordinates.csv'
df = pd.read_csv(SENSORS_CSV)
df = df.loc[:, ("LATITUDE", "LONGITUDE")]
df = df[(df["LATITUDE"] != "NEIN") & (df["LONGITUDE"] != "NEIN")]

# Format the latitudes and longitudes
lon = []
lat = []
for row in df["LATITUDE"]:
    lat.append(float(row))
for row in df["LONGITUDE"]:
    lon.append(float(row))

def generate_knn_grid(df):
    N = len(list(df.LATITUDE))
    k = round(sqrt(N))
    X = np.column_stack((lat, lon))
    distmat = squareform(pdist(X, 'euclidean'))
    neighbors = np.sort(np.argsort(distmat, axis=1)[:, 0:k])
    coordinates = np.zeros((N, k, 2, 2))
    for i in np.arange(len(list(df.LATITUDE))):
        for j in np.arange(k):
            coordinates[i, j, :, 0] = np.array([X[i, :][1], X[neighbors[i, j], :][1]])
            coordinates[i, j, :, 1] = np.array([X[i, :][0], X[neighbors[i, j], :][0]])
    return N, k, coordinates

def plot_map(N, k, coordinates):
    fig = px.scatter_mapbox(
        df,
        lat="LATITUDE",
        lon="LONGITUDE",
        zoom=12.2,
        color_discrete_sequence=["rgb(255, 203, 3)"],
        title="<span style='font-size: 32px;'><b>K-Nearest Neighbor KNN Map</b></span>",
        opacity=.8,
        width=1000,
        height=1000,
        center=go.layout.mapbox.Center(lat=48.14, lon=11.57),
        size_max=15
    )
    fig.update_layout(mapbox_style="light", mapbox_accesstoken="", legend=dict(yanchor="top", y=1, xanchor="left", x=0.9))
    fig.update_traces(marker={'size': 15})

    lines = coordinates.reshape((N * k, 2, 2))
    for i in range(len(lines)):
        fig.add_trace(go.Scattermapbox(lon=[lines[i][0][0], lines[i][1][0]], lat=[lines[i][0][1], lines[i][1][1]], mode='lines', showlegend=False, line=dict(color='#ffcb03')))
    fig.data = fig.data[::-1]

    print("Saving image to output folder...")
    fig.write_image('output/knn_map.jpg', scale=5)
    print("Generating map in browser...")
    fig.show()

N, k, coordinates = generate_knn_grid(df)
plot_map(N, k, coordinates)
