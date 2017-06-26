import os
import pandas as pd
import numpy as np

# limitamos la tabla en pantalla.
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Cargo el archivo. Lo hacemos mediante el path.

folder = './DATA/IntropiaCSV'
filename = 'hd_page1.csv'

path = os.path.join(folder, filename)

print(path, os.path.exists(path))

# Añado print de control para comprobar que ok.

print('loading...')
hd_page_df = pd.read_csv(path, sep=';', header=0, index_col=0)

print(hd_page_df.head(10))


# items que ha visto cada usuario, primera forma.
# Es lentísima, la hago de otra manera.
print('Analyzing users...')

# items = dict()
#
# nrows, ncols = hd_page_df.shape
#
# iduser_idx = np.where(hd_page_df.columns.values == 'idUser')[0][0]
# iditem_idx = np.where(hd_page_df.columns.values == 'idItem')[0][0]
#
# for i in range(nrows):
#     iduser, iditem = hd_page_df.values[i, [iduser_idx, iditem_idx]]  # estoy sacando en idUser e idItem de cada fila
#
#     if iduser in items.keys():
#         items[iduser].append(iditem)
#     else:
#         items[iduser] = [iditem]

# Lo hago mediante una función agg.
def agg(x):
    """
    copia la lista de elementos agregados en una nueva lista para que todo funcione
    :param x: list de elementos agregados
    :return: lista de elementos agregados
    """
    lst = list()
    for item in x:
        lst.append(item)
    return lst


'''
Estoy llamado a la funcion "nativa" de agregacion del DataFrame
Esto me permite procesar por grupos rapidamente.
He creado una funcion "agg" que coge la lista de elementos agregados y la
copia para que la podamos tener en los resultados

La clave de agregacion es idUser
y el elemneto agregado es idItem (aunque no he agregado nada, solo,la he listado)
'''
agregated_df = hd_page_df.groupby(('idUser'))['idItem'].aggregate(agg)

print('done\n', agregated_df)


