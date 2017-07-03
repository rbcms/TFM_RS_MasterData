import numpy as np
import RSmodule
import pandas as pd
import os
"""
NOTAS DATAJOIN:

ESTE ARCHIVO PREPROCESA LOS DATOS PARA LUEGO GENERAR LOS RATINGS.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
OJO CON EL VECTOR PRICEEEE VER QUE HAGO AL FINAL AL RESPECTO....cuidadito que me puede dar fallo.





"""

def user_orders_df():

    """
    hd_total_order + rs_user + hd_order

    Hacemos el merge de estas 3 tablas para luego obtener el evento "order".
    Este evento representa los carritos generados por los usuarios.
    Los artículos cargados en los carritos pueden acabar siendo compra (purchase) o no.

    :return: df_2

    PROCESO:
    1._cargamos datos ( funcion load_data en RSmodule )
    2._renombramos algunas columnas evitar equívocos.
    3._es un merge a 3, primero 2 y el resultado contra el 3.
    4._cambio de variable categoríca de la columna "misc" (paises) a valor numérico.
    nota: a priori no utilizo el país pero lo dejo preparado.
    5._resultado

    :return: df_2

    """

    directory = './DATA/IntropiaCSV'

    fnames = list()
    fnames.append('hd_total_order.csv')
    fnames.append('rs_user.csv')
    fnames.append('hd_order.csv')

    # del directorio especificado, los archivos de la lista fnames.
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

    # reemplazo de los países cambio tipo variable
    c_dict = dict()  # diccionario de pais->numero
    c_inv_dict = dict()  # diccionario de numero-> pais (por tener referencia)
    paises = df_2['misc'].unique()  # valores únicos de paises
    for idx, pais in enumerate(paises):
        c_dict[pais] = idx * 100  # entrada en el diccionario pais->numero
        c_inv_dict[idx * 100] = pais  # entrada en el diccionario numero-> pais

    df_2['misc'] = df_2['misc'].replace(c_dict)  # reemplazo la columna 'misc' con una columna donde he reemplazado los paises por numeros

    return df_2


def user_purchase_df():

    """
    hd_total_order + rs_user + hd_order

    Hacemos el merge de estas 3 tablas para luego obtener el evento "purchase".
    Este evento representa las compras generados por los usuarios.

    :return: df_2

    PROCESO:
    1._cargamos datos ( funcion load_data en RSmodule )
    2._es un merge a 3, primero 2 y el resultado contra el 3.

    """

    directory = './DATA/IntropiaCSV'

    fnames = list()
    fnames.append('hd_total_purchase.csv')
    fnames.append('rs_user.csv')
    fnames.append('hd_purchase.csv')

    hd_total_purchase, rs_user, hd_purchase = RSmodule.load_data(directory, fnames)

    # print(hd_total_order.head(10))
    # print(rs_user.head(10))
    # print(hd_order.head(10))

    # concatenar
    df_1 = pd.merge(hd_total_purchase, rs_user, how='inner', left_on='idUser', right_on='iduser')
    df_2 = pd.merge(df_1, hd_purchase, how='inner', left_on=['idPurchase', 'idBuyer'], right_on=['idPurchase', 'idBuyer'])

    return df_2


def get_navigation_df():

    """
    función para cargar el archivo

    :return: hd_page_df

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

    funcion para cargar la lista de id's de usuario.
    comprobamos que corresponden en ambas tablas.

    :return: usuarios únicos de la lista completa.

    """
    directory = './DATA/IntropiaCSV'
    fnames = list()
    fnames.append('rs_user.csv')
    fnames.append('hd_page1.csv')
    rs_user, hd_page = RSmodule.load_data(directory, fnames)

    # hd_page = hd_page[hd_page['idItem'] != 0]  # filtrado de los elementos con idItem diferente de cero

    items1 = rs_user['iduser'].unique()
    items2 = hd_page['idUser'].unique()

    # sacamos los unicos de toda la lista completa
    items = np.unique(np.r_[items1, items2])

    return items



def get_items_list():

    """
    funcion para cargar la lista de id's de items
    comprobamos que son los items únicos en las 3 tablas.


    :return: items únicos de la lista completa.

    """
    directory = './DATA/IntropiaCSV'
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

    # sacamos los unicos de toda la lista completa
    items = np.unique(np.r_[items1, items2, items3])

    return items



def get_all_the_data():

    """
    Función carga las matrices sparse con los los datos.
    Creo la matriz sparse orders y la matriz purchase.

    :return:
    """

    fname = 'usr_item.pkl'

    if not os.path.exists(fname):
        # cargo los datos
        user_orders = user_orders_df()  # carritos
        user_purchase = user_purchase_df()  # purchase

        rows_array = get_users_list()  # todos los usuarios
        cols_array = get_items_list()  # todos los articulos
        print(user_orders.head(10))

        # creo la matriz sparse de carritos
        mat_usr_item_orders, row_labels_orders, col_labels_orders = RSmodule.make_sparse(user_orders, rows_array,
                                                                                         cols_array, 'idUser',
                                                                                         'idProduct')
        # creo la matriz sparse de purchase
        mat_usr_purchase_orders, row_labels_orders, col_labels_orders = RSmodule.make_sparse(user_purchase, rows_array,
                                                                                             cols_array, 'idUser',
                                                                                             'idProduct')

        # OJO DEJO COMENTARIO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        # reflexión: tiene sentido que recomiende en base a price??????

        user_price_vec = RSmodule.make_sparse_vector(user_purchase, rows_array, 'idUser', 'price')


        # guardo la informacion en unpickle
        print('saving pickle...')
        RSmodule.save_pickle(fname, [mat_usr_item_orders, mat_usr_purchase_orders, user_price_vec, row_labels_orders,
                                     col_labels_orders])

    else:

        # como el archivo pickle existe, lo cargo
        print('opening pickle...')
        [mat_usr_item_orders, mat_usr_purchase_orders, user_price_vec, row_labels_orders,
         col_labels_orders] = RSmodule.open_pickle(fname)

    return mat_usr_item_orders, mat_usr_purchase_orders, user_price_vec, row_labels_orders, col_labels_orders



# Ejecuta aquí en este archivo si existe en este.

if __name__ == '__main__':

    # users_list_ = get_users_list()
    df = user_purchase_df()
    print(df.head(200))
