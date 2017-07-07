"""
scores_test: cálculo de los scores basado en conocimiento implícito.

"""


import RSmodule
import DataJoin
import os
import pandas as pd


user_orders = DataJoin.user_orders_df()
rows_array = DataJoin.get_users_list()
cols_array = DataJoin.get_items_list()

###################################



print(user_orders.head(10))

mat_usr_item_orders, row_labels_orders, col_labels_orders = RSmodule.make_sparse(user_orders, rows_array, cols_array, 'idUser', 'idProduct')
print(mat_usr_item_orders)

navigation = DataJoin.get_navigation_df()
mat_usr_item_navigation, row_labels_navigation, col_labels_navigation = RSmodule.make_sparse(navigation, rows_array, cols_array, 'idUser', 'idItem')
print(mat_usr_item_navigation)


"""

La cantidad de compra y carritos representan confianza e intención de compra.
Items comprados han de de tener más peso en nuestra matriz de calificaciones.
Pondero los eventos dándo distintos pesos >> w1 purchase un valor de 15 y a w2 un valor de 5

"""

w1 = 15
w2 = 5
mat_final = (mat_usr_item_orders * w1 + mat_usr_item_navigation * w2) / (w1 + w2)