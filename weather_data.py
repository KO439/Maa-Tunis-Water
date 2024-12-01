import requests
import json

# Clé API OpenWeatherMap (inscrivez-vous sur https://openweathermap.org/ pour obtenir votre clé)
api_key = '14511214'  # Remplacez par votre clé API personnelle

# Définir l'emplacement (latitude et longitude de la Tunisie, par exemple)
location = '33.8869,9.5375'  # Coordonnées de la Tunisie

# Définir l'URL pour les données météorologiques
url = f"http://api.openweathermap.org/data/2.5/weather?lat={location.split(',')[0]}&lon={location.split(',')[1]}&appid={api_key}&units=metric"

# Récupérer les données depuis l'API météo
response = requests.get(url)
data = response.json()

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Extraire les informations météorologiques pertinentes
    temperature = data['main']['temp']  # Température actuelle en Celsius
    humidity = data['main']['humidity']  # Humidité actuelle en pourcentage
    precipitation = data.get('rain', {}).get('1h', 0)  # Précipitation dans la dernière heure (mm)
    
    # Afficher les résultats
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Precipitation (last hour): {precipitation} mm")
    
    # Vous pouvez maintenant intégrer ces données dans votre logique d'irrigation ou de gestion de l'eau.
else:
    print(f"Error fetching weather data: {data['message']}")
