import pandas as pd

def generate_report(irrigation_data):
    """
    Générer un rapport au format CSV à partir des données d'irrigation.
    
    :param irrigation_data: Dictionnaire avec les données d'irrigation
    """
    # Calculer les valeurs minimales et maximales pour certaines colonnes
    irrigation_data['Irrigation Need (min)'] = [min(irrigation_data['Irrigation Need (mm)'])] * len(irrigation_data['Irrigation Need (mm)'])
    irrigation_data['Irrigation Need (max)'] = [max(irrigation_data['Irrigation Need (mm)'])] * len(irrigation_data['Irrigation Need (mm)'])
    
    irrigation_data['Rainfall (min)'] = [min(irrigation_data['Rainfall (mm)'])] * len(irrigation_data['Rainfall (mm)'])
    irrigation_data['Rainfall (max)'] = [max(irrigation_data['Rainfall (mm)'])] * len(irrigation_data['Rainfall (mm)'])
    
    irrigation_data['Evapotranspiration Rate (min)'] = [min(irrigation_data['Evapotranspiration Rate (mm)'])] * len(irrigation_data['Evapotranspiration Rate (mm)'])
    irrigation_data['Evapotranspiration Rate (max)'] = [max(irrigation_data['Evapotranspiration Rate (mm)'])] * len(irrigation_data['Evapotranspiration Rate (mm)'])

    # Créer un DataFrame à partir des données d'irrigation modifiées
    df = pd.DataFrame(irrigation_data)
    
    # Sauvegarder le rapport en format CSV
    df.to_csv('irrigation_report.csv', index=False)
    
    print("Rapport généré avec succès!")



# Générer le rapport
generate_report(irrigation_data)
