"""
EXPLORACIÓN BÁSICA  hd_page
"""
import matplotlib.pyplot as plt
import io
import os
import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix
from matplotlib import pyplot as plt


#Cargamos archivo con restricciones en la visualización

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
print("loading set_options")

folder = './DATA/IntropiaCSV'
filename = 'hd_page1.csv'
path = os.path.join(folder, filename)
print(path, os.path.exists(path))
print('loading...')
hd_page_df = pd.read_csv(path, sep=';')

print("Primeras 10 líneas del dataframe")
print(hd_page_df.head(10))

print("Info básica de navegación para aanlizar usuario")
hd_page_df.info()


# seleccionamos columnas que mas nos interesan.
hd_page_df_reduce = hd_page_df[['idPage','idBuyer', 'idSession', 'idItem']]

print("Primeras 10 líneas con las columnas que queremos")
print(hd_page_df_reduce.head(10))

print("Cantidad de sesiones que son recurrentes")
session_count = hd_page_df_reduce.groupby('idSession').size().sort_values(ascending=False)
print(session_count[:10])



"""
Tras efectuar un primer Kmeans me doy cuenta de la grandísima dispersión que tengo.
Por ello efectúo un PCA que se puede ver el archivo K_mens_test.py
Aún así aplicamos un umbral en los datos.

"""

print("Número de elementos únicos")

n_items =hd_page_df_reduce.idItem.shape[0]
n_buyer = hd_page_df_reduce.idBuyer.unique().shape[0]
n_sesion = hd_page_df_reduce.idSession.unique().shape[0]

n_page =hd_page_df_reduce.idPage.unique().shape[0]
# Calculate number of items

print("Hay %s compradores" % (n_buyer))
print("Hay %s sesiones" % (n_sesion))
print("Hay %s páginas vistas" % (n_page))
print("Hay %s productos" % (n_items))




# mínimo y máximo total compra >> que rango necesito.

# print(hd_page_df_reduce['amount'].min(), hd_page_df_reduce['amount'].max())



# cuantos productos ha añadido una sola vez este usuario en concreto.

suma = sum(hd_page_df_reduce[hd_page_df_reduce['idBuyer']== 2000000017305]['idItem'].value_counts() == 1)
print("Numero de productos que ha visto un usuario: %s " % (suma))