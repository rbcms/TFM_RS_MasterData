"""

RSmodule: contiene la relación funciones fundamentales.

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
    
"""

