import ee
import folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Authentification avec Google Earth Engine
ee.Authenticate()  # Cela ouvrira un lien pour l'authentification
ee.Initialize()

# Définir la zone d'intérêt (exemple : Tunisie, vous pouvez ajuster les coordonnées)
region = ee.Geometry.Rectangle([9.5, 37.5, 10, 37.7])

# Récupérer les données Sentinel-2 pour 2023
sentinel2 = ee.ImageCollection('COPERNICUS/S2') \
    .filterBounds(region) \
    .filterDate('2023-01-01', '2023-12-31') \
    .select(['B4', 'B3', 'B2', 'B8'])  # Rouge, Vert, Bleu, Infra-Rouge

# Calculer l'indice de végétation NDVI
def calculate_ndvi(image):
    return image.normalizedDifference(['B8', 'B4']).rename('NDVI')

ndvi = sentinel2.map(calculate_ndvi)

# Calculer la moyenne du NDVI pour 2023
ndvi_mean = ndvi.mean().clip(region)

# Créer la carte avec Folium
my_map = folium.Map(location=[37.6, 9.75], zoom_start=10)

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

# Charger les données d'entraînement pour l'exemple (ajustez le chemin selon votre contexte)
X_train_set_fpath = '../input/X_train_sat4.csv'
y_train_set_fpath = '../input/y_train_sat4.csv'

X_train = pd.read_csv(X_train_set_fpath)
Y_train = pd.read_csv(y_train_set_fpath)

# Prétraiter les données d'images
X_train = X_train.values.reshape([X_train.shape[0], 28, 28, 4]).astype(float)  # Si ce sont des images 28x28x4

# Normaliser les images
X_train = X_train / 255.0

# Création du modèle de classification
model = Sequential([
    Dense(64, input_shape=(28 * 28 * 4,), activation='relu'),  # Couche d'entrée
    Dense(4, activation='softmax')  # 4 classes : Barren Land, Trees, Grassland, Other
])

# Compilation du modèle
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Résumé du modèle
model.summary()

# Entraînement du modèle
model.fit(X_train.reshape(-1, 28*28*4), Y_train, batch_size=32, epochs=5, validation_split=0.01, verbose=1)

# Faire des prédictions
preds = model.predict(X_train[-1000:], verbose=1)

# Afficher une prédiction
ix = 5  # Changez l'indice pour voir d'autres images
plt.imshow(np.squeeze(X_train[ix, :, :, 0:3]))  # Affiche seulement les canaux RGB
plt.show()

# Afficher la prédiction
print(f'Prediction:\n{preds[ix]}')

# Afficher la vérité terrain
print('Ground Truth:', end=' ')
if Y_train[ix, 0] == 1:
    print('Barren Land')
elif Y_train[ix, 1] == 1:
    print('Trees')
elif Y_train[ix, 2] == 1:
    print('Grassland')
else:
    print('Other')
