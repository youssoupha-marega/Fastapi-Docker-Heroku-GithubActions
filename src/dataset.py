import os
import base64
import pymysql
import pandas as pd
from sshtunnel import SSHTunnelForwarder
from datetime import datetime, timedelta
from dotenv import load_dotenv
import tempfile

#from meteostat import Daily,Point,Hourly

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Fonction pour ouvrir le tunnel SSH
def ouvrir_tunnel():
    ssh_host = '35.182.184.19'
    ssh_username = 'ec2-user'
    
    # Récupérer la clé SSH depuis les variables d'environnement
    pem_base64 = os.getenv('GEOPROJECTION_PEM')
    if pem_base64:
        # Décoder la clé Base64
        pem_key = base64.b64decode(pem_base64)
        
        # Créer un fichier temporaire pour la clé PEM
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            ssh_key_path = temp_file.name
            temp_file.write(pem_key)
    else:
        raise ValueError("La variable d'environnement GEOPROJECTION_PEM n'est pas définie")
    
    local_port = 23306
    remote_port = 3306
    
    # Création du tunnel SSH
    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_username,
        ssh_pkey=ssh_key_path,
        remote_bind_address=(os.getenv("REMOTE_BIND_ADDRESS"), remote_port),
        local_bind_address=('0.0.0.0', local_port)
    )
    
    # Démarrer le tunnel
    tunnel.start()
    
    return tunnel


# Fonction d'extraction de données
def fetch_data_raw(tunnel, db_name, tb_name, var_names, debut, fin):
    db_host = '127.0.0.1'
    db_user = os.getenv('DB_USER')  # Récupérer le user de la base de données
    db_password = os.getenv('DB_PASSWORD')  # Récupérer le password depuis l'environnement
    local_port = tunnel.local_bind_port

    # Connexion à la base de données via le tunnel SSH
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_name,
        port=local_port
    )

    try:
        # Exécution de la requête et extraction des données
        with connection.cursor() as cursor:
            var_string = ', '.join(var_names)  # Création d'une chaîne de caractères pour les noms de colonnes
            sql_query = f"""
            SELECT date_creation, {var_string}
            FROM {tb_name}
            WHERE date_creation BETWEEN '{debut.strftime("%Y-%m-%d %H:%M:%S")}' AND '{fin.strftime("%Y-%m-%d %H:%M:%S")}'
            """
            cursor.execute(sql_query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

        # Conversion des données en DataFrame
        df = pd.DataFrame(data, columns=columns)
    finally:
        connection.close()
    
    return data

#-----------------------------------------------------# 
# Exemple d'utilisation de la fonction fetch_data_raw #
#-----------------------------------------------------#
#tunnel = ouvrir_tunnel()

#db_name = 'saint_esprit'
#tb_name = 'stesp_p_usine_fl'
#var_names = ['debit_stesprit']

# Définir des dates d'exemple pour l'extraction
#debut = datetime(2024, 1, 1, 6, 55, 5)
#fin = datetime(2024, 1, 1, 9, 46, 59)

# Appel de la fonction d'extraction
#debit_stesprit = fetch_data_raw(tunnel, db_name, tb_name, var_names, debut, fin)

# Resampling des données sur 60 secondes
#debit_stesprit = debit_stesprit.set_index('date_creation').resample('60S').mean()

#def fetch_data_meteostat(df, latitude, longitude,altitude):
#    df_copy = df.copy()
#    df_copy["date_creation"] = pd.to_datetime(df_copy["date_creation"])
#    df_copy["aaa_mm_jj_hh"] = df_copy["date_creation"].dt.strftime("%Y %m %d %H")
#    localisation_geographique = Point(latitude,longitude,altitude)
#    start = df_copy["date_creation"].min().to_pydatetime()  
#
#    end = df_copy["date_creation"].max().to_pydatetime() 
#    hourly_data_meteostat=Hourly(localisation_geographique, start=start, end=end).fetch()
#
#
#    hourly_data_meteostat["aaa_mm_jj_hh"] = hourly_data_meteostat.index.strftime("%Y %m %d %H")
#
#    df_copy = df_copy.merge(hourly_data_meteostat, on="aaa_mm_jj_hh", how="outer")
#    df_copy = df_copy.drop(columns=["aaa_mm_jj_hh"])
#    return df_copy



#-----------------------------------------------------------# 
# Exemple d'utilisation de la fonction fetch_data_meteostat #
#-----------------------------------------------------------#

#from dataset import fetch_data_meteostat
#path = "C:/Users/ymarega/Desktop/INO/Extraction/debit_dist_stesp_brut_8_2019_2_2025.csv"
#df = pd.read_csv(path,parse_dates=["date_creation"])
#df = df.tail(1000)

#latitude = 45.89833
#longitude = 73.66027
#altitude = 61
#debit_meteo_brut = fetch_data_meteostat(df,latitude,longitude,altitude)
#debit_meteo_brut


#-----------------------------------------------------------------------------------------------------------# 
# Extraction des données de débit et Météostat de saint barthelemey et les stockes dans le dossier data/raw #
#-----------------------------------------------------------------------------------------------------------#

#if __name__ == "__main__":

    ### Ouverture du tunnell
    #tunnel = ouvrir_tunnel()

    # Names Base données, table et variable
    #db_name = "saint_barthelemy"
    #tb_name = "stbar_p_usine_fl"
    #var_names = ["debit_dist"]

    # Définir des dates d'exemple pour l'extraction
    #debut = datetime(2021, 8, 9, 13, 44, 0)
    #fin = datetime(2025, 3, 4, 13, 35, 0)

    # Appel de la fonction d'extraction
    #debit_dist_stbar_brut_8_2021_3_2025 =  fetch_data_raw(tunnel, db_name, tb_name, var_names, debut, fin)

    ## Enregistrer les données de débit de distibution de saint barthélemy au format csv dans data/raw
    #debit_dist_stbar_brut_8_2021_3_2025.to_csv('data/raw/debit_dist_stbar_brut_8_2021_3_2025.csv', index=False)
    
    # Les coordonnées Géométrique approximatives pour Saint-Barthélemy (Québec):
    #latitude = 46.1586
    #longitude = -73.1842
    #altitude = 20 
    
    ## Extraction des données mété à partir de l'API metostat et lesconcatener avec les données de débit de distribution 
    # d'eau potable de Saint-Barthelemy
    #debit_dist_stbar_brut_meteostat_8_2021_3_2025 = fetch_data_meteostat(debit_dist_stbar_brut_8_2021_3_2025,
    #                                                                     latitude, longitude, altitude)
    
    
    ## Enregistrer les données de débit de distibution d'EP et de Meteostat de saint barthéleme au format csv dans data/external
    #debit_dist_stbar_brut_meteostat_8_2021_3_2025.to_csv('data/external/debit_dist_stbar_brut_meteostat_8_2021_3_2025.csv', 
    #                                                     index=False)
    
    







