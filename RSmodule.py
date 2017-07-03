"""
RSmodule: recoge las funciones más relevantes del proyecto.
De manera que luego se pueden llamar y reutilizar cómodoamente

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
def most_viewed(sp_matrix, colum_labels, num_views):
def get_process_matrix(mat_usr_item_orders, mat_usr_purchase_orders, row_labels_orders):
def load_data(folder, files_list):
def recomendacion_kmeans(kmeans, X_train, clusters_pred, item_lbl, colname, item_num=10):

"""

