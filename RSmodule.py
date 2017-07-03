import os
import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix
import pickle
from sklearn import manifold
from matplotlib import pyplot as plt

"""
En este archivo tenemos una relación de las funciones fundamentales

"""

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

####HOLAAAAAAAAAAAAAA hOLAAAAAAAAAAAAAAAAAAAAAAA
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
    Crea un diccionario que funciona al revés que un array. Es decir estamos haciendo un diccionario que guarde
    como valores los índices.
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

    nota: La limitación de consistencia de dimensiones consiste en "recortar" los dataframes y que todos tengan las
    mismas dimensiones para poder operar luego.

    """

    m = len(rows_array)
    n = len(cols_array)
    print('Making sparse ...', m, n)

    mat = lil_matrix((m, n), dtype=np.float16) # utilizamos este tipo de matriz por que es más eficiente.

    """
    Preparo las filas y las columnas de la matriz. Las hago mediante la función make_index_dict y la lista correspondiente
    sobre la que se ha de aplicar.
    
    """
    rows_dict = make_index_dict(rows_array)
    cols_dict = make_index_dict(cols_array)

    # user_counter = Counter()

    def fill(x):
        return list(x)

    df2 = df.groupby((df_rows_attr))[df_cols_attr].aggregate(fill)

# HOLAAAAAAAAAAAAAAAAAAAA

    for i, usr in enumerate(df2.index.values):
        usr_idx = rows_dict[usr]

        items = df2.values[i]

        for item in items:
            item_idx = cols_dict[item]
            mat[usr_idx, item_idx] += 1

    return mat, rows_array, cols_array
    # return df2, 1, 1


def load_data(folder, files_list):
    """
    Cargar varios DataFrames
    :param folder: carpeta
    :param files_list: lista de nombres de los archivos
    :return: lista de DataFrames
    """

    """
    Para cada nombre de archivo en la lista de archivos de un directorio, creame la ruta si existe y lo añades
    a la lista de dataframes. Si no existe  el archivo me avisas.
    
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


def recomendacion_kmeans(kmeans, X_train, clusters_pred, item_lbl, colname):
    """
    Crea una lista de recomendaciones para cada label predicho
    :param kmeans: objeto Kmenas entrenado
    :param X_train: Tensor de entrenamiento
    :param clusters_pred: etiquetas de los test predichas
    :param item_lbl: etiquetas totales
    :param colname: nombre de la columna
    :return:
    """
    recomendaciones = list()

    # recorremos las etiquetas de nuestros datos ya clasificados...
    for lbl in clusters_pred:

        # saco los puntos usados para entrenar que corresponden con la etiqueta
        # nos basamos en la clusterización hecha por kmeans
        pts = X_train[np.where(kmeans.labels_ == lbl)[0]]

        # sumamos los items (nos da una matriz de 1 x N)
        suma_item = pts.sum(axis=0)

        # hacemos un DataFrame para que todo_ sea bonito
        df = pd.DataFrame(data=suma_item.transpose(), index=item_lbl, columns=[colname])

        # ordenar los valores de mayor a menor
        df.sort(columns=[colname], inplace=True, ascending=False)

        # guardar el DataFrame en la lista
        recomendaciones.append(df)

    # devolver la lista de DataFrames con recomendaciones
    return recomendaciones