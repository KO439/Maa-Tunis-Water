import requests
import numpy as np

# Clé API OpenWeatherMap (ne jamais exposer la clé directement dans le code en production)
api_key = 'VOTRE_CLE_API'  # Remplacez par votre clé API personnelle

# Fonction pour récupérer les données météo
def get_weather_data(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lance une exception en cas de réponse erronée
        data = response.json()

        # Extraire les informations météorologiques pertinentes
        temperature = data['main']['temp']  # Température actuelle en Celsius
        humidity = data['main']['humidity']  # Humidité actuelle en pourcentage
        precipitation = data.get('rain', {}).get('1h', 0)  # Précipitation dans la dernière heure (mm)
        
        return temperature, humidity, precipitation

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Fonction pour détecter les anomalies dans les valeurs météorologiques
def detect_and_clean_anomalies(value, value_type):
    # Supposons que les valeurs valides pour la température sont entre -50 et 50°C
    if value_type == "temperature":
        if value < -50 or value > 50:
            return None  # Valeur anormale, la nettoyer (la valeur peut être laissée vide)
    # Supposons que l'humidité doit être comprise entre 0% et 100%
    elif value_type == "humidity":
        if value < 0 or value > 100:
            return None  # Valeur anormale
    # Précipitation ne peut pas être négatif, mais peut être zéro ou supérieur à une certaine limite
    elif value_type == "precipitation":
        if value < 0:
            return 0  # Valeur négative, la nettoyer en la mettant à zéro
    return value  # Si la valeur est normale, la retourner

# Coordonnées de la Tunisie
lat, lon = 33.8869, 9.5375

# Appel de la fonction pour récupérer les données météo
weather_data = get_weather_data(lat, lon, api_key)

# Afficher les résultats si les données sont valides
if weather_data:
    temperature, humidity, precipitation = weather_data

    # Nettoyage des données
    cleaned_temperature = detect_and_clean_anomalies(temperature, "temperature")
    cleaned_humidity = detect_and_clean_anomalies(humidity, "humidity")
    cleaned_precipitation = detect_and_clean_anomalies(precipitation, "precipitation")

    # Affichage des données nettoyées
    if cleaned_temperature is None:
        print("Temperature value is abnormal, cleaning...")
    else:
        print(f"Temperature: {cleaned_temperature}°C")

    if cleaned_humidity is None:
        print("Humidity value is abnormal, cleaning...")
    else:
        print(f"Humidity: {cleaned_humidity}%")

    print(f"Precipitation (last hour): {cleaned_precipitation} mm")

else:
    print("Unable to retrieve weather data.")
