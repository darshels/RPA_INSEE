from urllib.request import urlopen

import io
import pandas as pd
import requests
import zipfile
import pickle
from http import client
from bs4 import BeautifulSoup
from typing import List
from time import sleep

PATH_INSEE = "https://www.insee.fr"
PATH_INSEE_YEA = PATH_INSEE + "/fr/information/4190491"
PATH_INSEE_DEC = PATH_INSEE + "/fr/information/4769950"
PATH_FILES_SAVED = "../files/set_files_saved"
PATH_CSV = "../files/csv_deaths"

list_pages_web = [PATH_INSEE_YEA, PATH_INSEE_DEC]
dtypes = {'nomprenom': str, 'sexe': pd.Int8Dtype(), 'lieunaiss': str, 'datenaiss': pd.Int32Dtype(), 'commnaiss': str,
          'paysnaiss': str, 'datedeces': pd.Int32Dtype(), 'lieudeces': str, 'actedeces': str}


# Les pd.IntxxDType() permettent de gérer les valeurs manquantes pour les entiers


def get_deaths() -> pd.DataFrame:
    """
    Retourne l'ensemble des décès
    :return: dataframe comprenant les décès
    """
    try:
        df_deaths = pd.read_csv(PATH_CSV, sep=";", dtype=dtypes)
    except FileNotFoundError:
        df_deaths = pd.DataFrame()
        df_deaths = get_new_deaths(df_deaths)

    return df_deaths


def get_new_deaths(df_deaths: pd.DataFrame, list_pages: List[str] = list_pages_web) -> pd.DataFrame:
    """
    Recherche les fichiers dans les pages web de l'INSEE qui ne sont pas sauvargés
    :param list_pages: liste des pages web à parcourir
    :param df_deaths: dataframe des décès
    :return: dataframe à jour
    """

    for page in list_pages:
        page_insee_yea = BeautifulSoup(requests.get(page).text, features="html.parser")

        # Récupère la div comprenant le corpus
        corps_insee_yea = page_insee_yea.find("div", {"class": "corps-publication"})

        # Ouvre le fichier ayant le set des fichiers déjà enregistrés
        try:
            with open(PATH_FILES_SAVED, 'rb') as file:
                set_files_saved = pickle.load(file)
        except (EOFError, FileNotFoundError) as e:
            set_files_saved = set()

        # Récupère les liens faisant partie de la classe fichier
        for link in corps_insee_yea.find_all("a", {"class": "fichier"}):
            link = PATH_INSEE + link['href']

            if link not in set_files_saved:
                print("Téléchargement : " + link)
                df_deaths = _append_files_to_csv(df_deaths, link)
                set_files_saved.add(link)

                with open(PATH_FILES_SAVED, 'wb') as file:
                    pickle.dump(set_files_saved, file)
            else:
                print("Déjà téléchargé : " + link)

    return df_deaths


def _append_files_to_csv(df_deaths: pd.DataFrame, link: str) -> pd.DataFrame:
    """
    Télécharge les fichiers du site de l'INSEE et ajoute les données dans le dataframe en entrée
    :param df_deaths: dataframe avec les données déjà possédées
    :param link: lien vers le fichier de téléchargement
    :return: dataframe à jour
    """

    try:
        zip_files = zipfile.ZipFile(io.BytesIO(urlopen(link).read()))
    except client.RemoteDisconnected:
        # 2ème tentative sinon arrêt, possibilité de changer cela en boucle
        sleep(1)
        zip_files = zipfile.ZipFile(io.BytesIO(urlopen(link).read()))

    # Extraction de chaque fichier csv du fichier zip et ajout dans le dataframe donné
    for files in zip_files.namelist():
        df_deaths = df_deaths.append(pd.read_csv(zip_files.open(files), sep=";", dtype=dtypes, index_col=False))

    df_deaths.to_csv(PATH_CSV, sep=";", index=False)

    return df_deaths
