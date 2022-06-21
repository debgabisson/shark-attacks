import pandas as pd
import folium
from folium.plugins import MarkerCluster

def freq_shark_country(attacks):
    # Top Shark Species by attack by country 
    country_species = pd.crosstab(index=attacks['Species'], columns=attacks['Country_Code'])
    country_species


    country_top_shark = {}
    for i in country_species.columns:
        country_top_shark[i] = country_species[i].sort_values(ascending=False)[:1].index.tolist()

    top_shark = pd.DataFrame.from_dict(country_top_shark, orient='index', dtype=None, columns=None).reset_index()
    top_shark.columns = ['Country_Code', 'Top_Shark']

    # Total number of attacks by country
    freq_country = pd.DataFrame(attacks['Country_Code'].value_counts()).reset_index()
    freq_country.columns = ['Country_Code', 'Frequency']
    freq_country.drop(4, inplace=True)

    # Merging the above Data Frames and includinf coordinates for each country
    coord = pd.read_csv('data/countries_codes_and_coordinates.csv', delimiter='"')
    coord = coord[['Alpha-2 code', 'Latitude (average)', 'Longitude (average)']]
    coord.columns = ['Country_Code', 'Latitude', 'Longitude']
    freq_country = pd.merge(freq_country, coord, on=['Country_Code'], how = 'inner')
    freq_country = pd.merge(freq_country, top_shark, on=['Country_Code'], how = 'inner')
    return freq_country

def world_map_popup(attacks):
    freq_country = freq_shark_country(attacks)
    # World map with pop-up information
    world_map= folium.Map(tiles="cartodbpositron")

    for i in range(len(freq_country)):
            lat_2 = freq_country.iloc[i]['Latitude']
            long_2 = freq_country.iloc[i]['Longitude']
            radius= float(freq_country.iloc[i]['Frequency'])/30
            popup_text = """Country : {}<br>
                        Attacks : {}<br>
                        Top Species: {}<br>"""
            popup_text = popup_text.format(freq_country.iloc[i]['Country_Code'],
                                           freq_country.iloc[i]['Frequency'],
                                           freq_country.iloc[i]['Top_Shark']
                                          )
            tooltip=int(freq_country.iloc[i]['Frequency'])
            folium.CircleMarker(location = [lat_2, long_2], tooltip=tooltip, radius=radius, popup= popup_text, color='#99CC66', fill =True).add_to(world_map)

    return world_map

def world_map_clusters(attacks):
    # World map with clusters by total number of attacks
    world_map= folium.Map(tiles="cartodbpositron")
    marker_cluster = MarkerCluster(show=False).add_to(world_map)

    for i in range(len(attacks)):
            lat_2 = attacks.iloc[i]['Latitude']
            long_2 = attacks.iloc[i]['Longitude']
            radius= 2
            popup_text = """Country : {}<br>"""
            popup_text = popup_text.format(attacks.iloc[i]['Country_Code'],
                                           #freq_country.iloc[i]['Frequency'],
                                           #attacks.iloc[i]['Top_Shark']
                                          )
            #tooltip=int(freq_country.iloc[i]['Frequency'])
            folium.CircleMarker(location = [lat_2, long_2], radius=radius, popup= popup_text, color='#99CC66', fill =True).add_to(marker_cluster)

    return world_map