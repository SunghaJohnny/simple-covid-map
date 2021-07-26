import folium
import pandas as pd


df_worldSet = pd.read_csv("time_series_covid19_confirmed_global.csv")
df_worldSet = df_worldSet.fillna('0')
map = folium.Map(location=[13,121],zoom_start = 2, tiles = "OpenStreetMap")
fg = folium.FeatureGroup(name="My Map")

# puts all data to different lists
place = list(df_worldSet["Province/State"])
country = list(df_worldSet["Country/Region"])
lat = list(df_worldSet["Lat"])
long = list(df_worldSet["Long"])
cases = list(df_worldSet[df_worldSet.columns[-1]])

def color_producer(cases):
    # lightgreen - 0 - 50,000 
    # green - 50,001 - 200,000
    # orange - 200,001 - 500,000
    # lightred - 500,001 - 1,000,000
    # red - 1,000,001 ~
    if   cases <= 50000:
        return 'lightgreen'
    elif cases <= 200000:
        return 'green'
    elif cases <= 500000:
        return 'darkgreen'
    elif cases <= 1000000:
        return 'orange'
    else:
        return 'red'

# frame for pop up
html = """<h4>%s</h5>
Total Cases: %s
"""

# iterates all countries and its coordinates and plotting it to map
for la,lo,pl,ctry,ca in zip(lat,long,place,country,cases):
    if pl != '0':
        pl_ctry = "{}, {}".format(pl,ctry)
    else:
        pl_ctry = ctry
    color_ca = color_producer(ca)
    iframe = folium.IFrame(html = html % (pl_ctry, "{:,}".format(ca)),width = 200, height = 100)
    fg.add_child(
        folium.Marker(
            location = (la,lo), 
            popup = folium.Popup(iframe), 
            tool_tip = "hello",
            icon= folium.Icon(color_ca)))
    fg.add_child(
        folium.Circle(
            location = (la,lo),
            color = color_ca,
            radius = (200000 if ca < 5000000 else ca/25),
            fill = True,
            fill_opacity = 0.7,
            fill_color = color_ca))


map.add_child(fg)
map.add_child(folium.LayerControl())
map.save("Map_AllCountries.html")




