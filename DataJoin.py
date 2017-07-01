import numpy as np
import RSmodule
import pandas as pd
import os

"""
DataJoin >> vista rápida.
En este archivo se preprocesan algunos de los datos de distintas tablas.


** def user_orders_df >> Utilizaré esta función para luego poder obtener los carritos de cada usuario.
Es decir, aquellos artículos que se añadieron a la cesta. 

** det_users_list >> funcion para cargar la lista de id's de usuario
** def get_users_list >>
** def get_items_list >>

"""

def user_orders_df():
    """

    hd_total_order + rs_user + hd_order

    Búsca en el directorio especificado los archivos a mergear y los añade a la lista.
    Importa la función load_data (cargo los archivos ) que hay en el archivo RSmodule.
    Le cambia nombre a dos columnas de dos archivos, se llaman igual, pero no son lo mismo.
    Obtengo en pantalla control mediante print
    Concatenamos los dataframes con los datos que queremos
    Paso la variable pais a categírica, para poder operar con ella. Lo hago mediante un diccionario.

    :return:
    """

    directory = './DATA/IntropiaCSV'

    fnames = list()
    fnames.append('hd_total_order.csv')
    fnames.append('rs_user.csv')
    fnames.append('hd_order.csv')

    hd_total_order, rs_user, hd_order = RSmodule.load_data(directory, fnames)

    rs_user.rename(columns={'active': 'active_user'}, inplace=True)
    hd_order.rename(columns={'active': 'active_order'}, inplace=True)

    # print(hd_total_order.head(10))
    # print(rs_user.head(10))
    # print(hd_order.head(10))

    # concatenar
    df_1 = pd.merge(hd_total_order, rs_user, how='inner', left_on='idUser', right_on='iduser')
    df_2 = pd.merge(df_1, hd_order, how='inner', left_on=['idOrder', 'idBuyer'], right_on=['idOrder', 'idBuyer'])

    # print(df_1.head(10))


    """
    Cambiamos de variable categórica a numérica: 
    Creo un diccionario vacío y otro inverso por si acaso.
    Obtengo los valores únicos del de la columna misc del dataframe obtenido anteriormente, 
    los meto en la variable país.
    Para cada índice de los paises contenidos en esta nueva variable país:
        metemos en el diccionarios el país y el ńumero asignado y al revés.
    Reemplazo la colummna misc del dataframe por la nueva.
    """

    c_dict = dict()  # diccionario de pais->numero
    c_inv_dict = dict()  # diccionario de numero-> pais
    paises = df_2['misc'].unique()  # valores únicos de paises
    for idx, pais in enumerate(paises):
        c_dict[pais] = idx * 100  # entrada en el diccionario pais->numero
        c_inv_dict[idx * 100] = pais  # entrada en el diccionario numero-> pais

    df_2['misc'] = df_2['misc'].replace(c_dict)  # reemplazo la columna 'misc' con una columna donde he reemplazado los paises por numeros

    return df_2


def get_navigation_df():
    """
    hd_page1

    Carga archivo hd_page1 q es la navegación de los usuarios

    :return:
    """
    folder = './DATA/IntropiaCSV'
    filename = 'hd_page1.csv'

    path = os.path.join(folder, filename)

    print(path, os.path.exists(path))

    print('loading...')
    hd_page_df = pd.read_csv(path, sep=';', header=0, index_col=0)

    return hd_page_df


def get_users_list():
    """
    rs_user + hd_page1

    funcion para cargar la lista de id's de usuario
    :return:
    """
    directory = '.DATA/IntropiaCSV'
    fnames = list()
    fnames.append('rs_user.csv')
    fnames.append('hd_page1.csv')
    rs_user, hd_page = RSmodule.load_data(directory, fnames)

    # hd_page = hd_page[hd_page['idItem'] != 0]  # filtrado de los elementos con idItem diferente de cero

    items1 = rs_user['iduser'].unique()
    items2 = hd_page['idUser'].unique()

    # sacamos los usuarios únicos de toda la lista completa
    items = np.unique(np.r_[items1, items2]) # np.r_ forma de obtener en numpay el vector en un eje.

    return items


def get_items_list():
    """
    funcion para cargar la lista de id's de items

    :return:
    """
    directory = '../DATA/IntropiaCSV'
    fnames = list()
    fnames.append('hd_page1.csv')
    fnames.append('hd_order.csv')
    fnames.append('hd_purchase.csv')

    # cargar los DataFrame
    hd_page, hd_order, hd_purchase = RSmodule.load_data(directory, fnames)

    # hd_page = hd_page[hd_page['idItem'] != 0]  # filtrado de los elementos con idItem diferente de cero

    items1 = hd_page['idItem'].unique()
    items2 = hd_order['idProduct'].unique()
    items3 = hd_purchase['idProduct'].unique()

    # sacamos los items únicos de toda la lista completa
    items = np.unique(np.r_[items1, items2, items3])

    return items




if __name__ == '__main__':

    users_list_ = get_users_list()