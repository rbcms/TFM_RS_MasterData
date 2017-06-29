"""
CALCULO DE LOS SCORES EN BASE A LOS EVENTOS.

Este conjunto de recomendadores presentes en este proyecto son del tipo Filtrado Colaborativo,
basado en memoria.

Eventos pora el cálculo de los ratings >>

* páginas vistas (Page), que son de productos.
* elementos añadidos a los carritos (orders), pueden quedar abandonados o no (purchases).
* items (purchases), compras finalizadas.

"""
user_orders = DataJoin.user_orders_df() # Dentro del archivo DataJoin la función user_orders.

rows_array = DataJoin.get_users_list() # Dentro del archivo DataJoin la función get_users_list.
cols_array = DataJoin.get_items_list() #
print(user_orders.head(10))

mat_usr_item_orders, row_labels_orders, col_labels_orders = RSmodule.make_sparse(user_orders, rows_array, cols_array, 'idUser', 'idProduct')
print(mat_usr_item_orders)

navigation = DataJoin.get_navigation_df()
mat_usr_item_navigation, row_labels_navigation, col_labels_navigation = RSmodule.make_sparse(navigation, rows_array, cols_array, 'idUser', 'idItem')
print(mat_usr_item_navigation)


w1 = 15
w2 = 5
mat_final = (mat_usr_item_orders * w1 + mat_usr_item_navigation * w2) / (w1 + w2)

import RSmodule
import DataJoin
import os
import pandas as pd


