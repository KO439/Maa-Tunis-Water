import ee
from folium import Map

# Authentification avec Google Earth Engine
ee.Authenticate()  # Cela ouvrira un lien pour l'authentification
ee.Initialize()

# Définir la zone d'intérêt
region = ee.Geometry.Rectangle([9.5, 37.5, 10, 37.7])

# Récupérer les données Sentinel-2 pour 2023
sentinel2 = ee.ImageCollection('COPERNICUS/S2') \
    .filterBounds(region) \
    .filterDate('2023-01-01', '2023-12-31') \
    .select(['B4', 'B3', 'B2', 'B8'])

# Calculer l'indice de végétation NDVI
def calculate_ndvi(image):
    return image.normalizedDifference(['B8', 'B4']).rename('NDVI')

ndvi = sentinel2.map(calculate_ndvi)

# Calculer la moyenne du NDVI pour 2023
ndvi_mean = ndvi.mean().clip(region)

# Créer la carte avec Folium
my_map = Map(location=[37.6, 9.75], zoom_start=10)

# Ajouter la couche NDVI sur la carte
map_id = ndvi_mean.getMapId()
folium.TileLayer(
    tiles=map_id['tile_fetcher'].url_format,
    attr="Google Earth Engine",
    overlay=True,
    name="NDVI"
).add_to(my_map)

# Afficher la carte
my_map

