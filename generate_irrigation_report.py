import pandas as pd

def generate_report(irrigation_data):
    """
    Générer un rapport au format CSV à partir des données d'irrigation.
    
    :param irrigation_data: Dictionnaire avec les données d'irrigation
    """
    # Créer un DataFrame à partir des données d'irrigation
    df = pd.DataFrame(irrigation_data)
    
    # Sauvegarder le rapport en format CSV
    df.to_csv('irrigation_report.csv', index=False)
    
    print("Rapport généré avec succès!")

# Exemple de données d'irrigation
irrigation_data = {
    'Region': ['Tunisia', 'Sejnane'],
    'Irrigation Need (mm)': [45, 50],
    'Rainfall (mm)': [5, 12],
    'Evapotranspiration Rate (mm)': [3, 2]
}

# Générer le rapport
generate_report(irrigation_data)
