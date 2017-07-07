"""
RSmodule: este archivo contine una relación de las funciones fundamentales empleadas en el proyecto.

"""

import os
import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix
import pickle
from sklearn import manifold
from matplotlib import pyplot as plt


"""

FUNCIONES:

def save_pickle(fname, data1):
def open_pickle(fname):
def plotManifold(X, color=None, size=2):
def plot2D(Y):
def make_index_dict(arr):
def make_sparse(df, rows_array, cols_array, df_rows_attr, df_cols_attr):
def load_data(folder, files_list):
def recomendacion_kmeans(kmeans, X_train, clusters_pred, item_lbl, colname):

#####################################################################333

def user_purchase2_df >> NO ME FUNCIONA


"""

# añadido estilo para  pantalla.
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def save_pickle(fname, data1):
    output = open(fname, 'wb')  # abro el archivo para escritura (w) binaria (b) (wb)
    pickle.dump(data1, output)


def open_pickle(fname):
    pkl_file = open(fname, 'rb')  # abro el archivo para lectura (r) binaria (b) (wb)
    return pickle.load(pkl_file)


def plotManifold(X, color=None, size=2):

    """
    Representacion 2D del datos N-Dimensionales
    :param X: Matrix de puntos n-D
    :return:
    """
    print('Manifold plot...')
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(111)
    # model = manifold.SpectralEmbedding(n_components=5)
    model = manifold.Isomap(n_components=5)
    Y = model.fit_transform(X)
    ax.scatter(Y[:, 0], Y[:, 1], c=color, cmap=plt.cm.Spectral, s=size*100)
    plt.title("Manifold Plot")


def plot2D(Y):

    """
    Representacion 2D del datos N-Dimensionales
    :param X: Matrix de puntos n-D
    :return:
    """
    print('2D plot...')
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(111)
    ax.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
    plt.title("2D Plot")


def make_index_dict(arr):

    """
    Crea un diccionario que funciona al revés que un array
    :param arr: Array de valores
    :return: diccionario dict[valor] -> indice
    """
    dict1 = dict()  # value -> idx
    for i, val in enumerate(arr):
        dict1[val] = i
    return dict1


def make_sparse(df, rows_array, cols_array, df_rows_attr, df_cols_attr):

    """
    Generar matriz sparse con los dos atributos provistos
    :param df: Dataframe original
    :param rows_array: Array de valores posibles del atributo "rows_attr" (se pasa para tener consistencia de dimensiones)
    :param cols_array: Array de valores posibles del atributo "cols_attr" (se pasa para tener consistencia de dimensiones)
    :param df_rows_attr: string con el nombre del atributo que va a ir en las filas de la matriz
    :param df_cols_attr: string con el nombre del atributo que va a ir en las columnas de la matriz
    :return: matriz sparse(rows_attr, cols_attr)
    """

    m = len(rows_array)
    n = len(cols_array)
    print('Making sparse ...', m, n)

    mat = lil_matrix((m, n), dtype=np.float16)
    rows_dict = make_index_dict(rows_array)
    cols_dict = make_index_dict(cols_array)

    # user_counter = Counter()

    def fill(x):
        return list(x)

    df2 = df.groupby((df_rows_attr))[df_cols_attr].aggregate(fill)

    for i, usr in enumerate(df2.index.values):
        usr_idx = rows_dict[usr]

        items = df2.values[i]

        for item in items:
            item_idx = cols_dict[item]
            mat[usr_idx, item_idx] += 1

    return mat, rows_array, cols_array


def make_sparse_vector(df, rows_array, df_rows_attr, df_cols_attr):

    """
    Generar matriz sparse con los dos atributos provistos
    :param df: Dataframe original
    :param rows_array: Array de valores posibles del atributo "rows_attr" (se pasa para tener consistencia de dimensiones)
    :param df_rows_attr: string con el nombre del atributo que va a ir en las filas de la matriz
    :param df_cols_attr: string con el nombre del atributo que va a ir en las columnas de la matriz
    :return: matriz sparse(rows_attr, cols_attr)
    """

    m = len(rows_array)
    n = 1
    print('Making sparse ...', m, n)

    vec = np.zeros(m, dtype=np.float16)
    rows_dict = make_index_dict(rows_array)

    # user_counter = Counter()

    def fill(x):
        return sum(x)
    # agrego todas las propiedades de los usuarios (sumo toda la pasta)
    df2 = df.groupby((df_rows_attr))[df_cols_attr].aggregate(fill)

    for i, usr in enumerate(df2.index.values):
        usr_idx = rows_dict[usr]  # indice del usuario
        vec[usr_idx] += df2.values[i]  # sumo la propiedad al usuario en el vector

    return vec


def most_viewed(sp_matrix, colum_labels, num_views):
    """
    Más vistos
    :param sp_matrix:
    :param colum_labels:
    :param num_views:
    :return:
    """
    views = sp_matrix.sum(axis=0)

    df = pd.DataFrame(data=views.transpose(), columns=['views'], index=colum_labels)
    df.sort_values(by='views', inplace=True, ascending=False)

    return df.head(num_views)


# def new_user(item_num):
#     """
#     Usuario vacio
#     :param item_num:
#     :return:
#     """
#     m = 1
#     n = item_num
#     return lil_matrix((m, n), dtype=np.float16)


def get_process_matrix(mat_usr_item_orders, mat_usr_purchase_orders, row_labels_orders):
    # Juntar matrices
    w1 = 10
    w2 = 500
    mat = (mat_usr_item_orders * w1 + mat_usr_purchase_orders * w2) / (w1 + w2)

    # eliminar usuarios con cero carritos
    suma_de_carritos_por_usuario = mat.sum(axis=1)
    id_row = np.where(suma_de_carritos_por_usuario > 0)[0]  # indices de los usuarios con al menos un carrito

    # filtro la matriz
    # mat_usr_item_orders = mat_usr_item_orders[:, id_col][id_row, :]  # tipo matlab mat_usr_item_orders[id_row, id_col]
    mat_usr_item_orders = mat[id_row, :]
    row_labels_orders = row_labels_orders[id_row]  # pillamos las filas seleccionadas
    # col_labels_orders = col_labels_orders[id_col]  # pillamos las columnas seleccionadas

    return mat

def load_data(folder, files_list):
    """
    Cargar varios DataFrames
    :param folder: carpeta
    :param files_list: lista de nombres de los archivos
    :return: lista de DataFrames
    """
    dfs = list()
    for filename in files_list:
        path = os.path.join(folder, filename)  # crear la ruta completa: directorio + nombre de archivo

        if os.path.exists(path):  # si existe el archivo, cargarlo y meterlo en la lista de DataFrames
            print('loading...')
            df = pd.read_csv(path, sep=';', header=0)
            dfs.append(df)
        else:  # si no existe, avisarme
            print(path, 'no existe!!!')
    return dfs  # devolver lista de DataFrames cargado


def recomendacion_kmeans(kmeans, X_train, clusters_pred, item_lbl, colname, item_num=10):
    """
    Crea una lista de recomendaciones para cada label predicho
    :param kmeans: objeto Kmenas entrenado
    :param X_train: Tensor de entrenamiento
    :param clusters_pred: etiquetas de los test predichas
    :param item_lbl: etiquetas totales
    :param colname: nombre de la columna
    :param item_num: numero de items de la recomendacion
    :return:
    """
    recomendaciones = list()
    n = len(clusters_pred)
    # recorremos las etiquetas de nuestros datos ya clasificados...
    for i, lbl in enumerate(clusters_pred):

        # saco los puntos usados para entrenar que corresponden con la etiqueta
        # nos basamos en la clusterización hecha por kmeans
        pts = X_train[np.where(kmeans.labels_ == lbl)[0]]

        # sumamos los items (nos da una matriz de 1 x N)
        suma_item = pts.sum(axis=0)

        # hacemos un DataFrame para que todo_ sea bonito
        df = pd.DataFrame(data=suma_item.transpose(), index=item_lbl, columns=[colname])

        # ordenar los valores de mayor a menor
        df.sort_values(by=[colname], inplace=True, ascending=False)

        # guardar el DataFrame en la lista
        recomendaciones.append(df.head(item_num))

        print((i+1) / n * 100, "%")

    # devolver la lista de DataFrames con recomendaciones
    return recomendaciones