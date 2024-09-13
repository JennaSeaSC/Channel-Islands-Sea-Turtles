"SoCal Outreach Interactions Map"
import folium
import pandas as pd
import os

# Load your data from a CSV file
data = pd.read_csv('C:/Users/jbcon/Documents/CODE/CINMS/CINMS_SoCal_LatLongInteractions_MAP.csv')

# Check the unique types in your dataset
unique_types = data['Type'].unique()
print("Unique types in your data:", unique_types)

# Define colors for each type of establishment
type_colors = {
    'Sportfishing & Whale Watching': 'blue',
    'SCUBA': 'red',
    'Tour/Charter': 'yellow',
    'Sportfishing': 'orange',
    'Education/Naturalists': 'green',
    'Ferry': 'white',
    'Enforcement/Protection': 'navy',
    'Fuel Dock': 'grey',
    'Whale Watching': 'teal'
}

# Check for any types not in the type_colors dictionary
missing_types = set(unique_types) - set(type_colors.keys())
if missing_types:
    print("Missing types in the color mapping:", missing_types)

# Create a base map centered around Southern California
m = folium.Map(location=[33.40005, -117.50000], zoom_start=8)

# Calculate scaling factor based on data range (you can adjust these values)
min_radius = 8  # Minimum circle size
max_radius = 28  # Maximum circle size

# Option 1: Simple linear scaling
# Adjust size scaling as needed to fit your data visually
interaction_range = data['Interactions'].max() - data['Interactions'].min()
scaling_factor = (max_radius - min_radius) / interaction_range

for index, row in data.iterrows():
    # Scaling the radius linearly
    radius = min_radius + (row['Interactions'] - data['Interactions'].min()) * scaling_factor
    
    # Get the color based on the establishment type
    color = type_colors.get(row['Type'], 'gray')  # Default to gray if type not found

    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=f"Interactions: {row['Interactions']}<br>Type: {row['Type']}"
    ).add_to(m)

# Create a legend HTML string
legend_html = '''
<div style="
    position: fixed; 
    bottom: 50px; left: 50px; width: 200px; height: 250px; 
    background-color: white; 
    border:2px solid grey; z-index:9999; font-size:14px;
    ">
    <b>Legend</b><br>
    <i style="background:blue; color:blue;">&emsp;&emsp;</i> Sportfishing & Whale Watching<br>
    <i style="background:red; color:red;">&emsp;&emsp;</i> SCUBA<br>
    <i style="background:yellow; color:yellow;">&emsp;&emsp;</i> Tour/Charter<br>
    <i style="background:orange; color:orange;">&emsp;&emsp;</i> Sportfishing<br>
    <i style="background:green; color:green;">&emsp;&emsp;</i> Education/Naturalists<br>
    <i style="background:white; color:black;">&emsp;&emsp;</i> Ferry<br>
    <i style="background:navy; color:navy;">&emsp;&emsp;</i> Enforcement/Protection<br>
    <i style="background:grey; color:grey;">&emsp;&emsp;</i> Fuel Dock<br>
    <i style="background:teal; color:teal;">&emsp;&emsp;</i> Whale Watching<br>
</div>
'''

# Add the legend to the map
m.get_root().html.add_child(folium.Element(legend_html))

# Save and display the map
m.save("C:/Users/jbcon/Documents/CODE/CINMS/sea_turtle_outreach_map.html")
m
