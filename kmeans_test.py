from sklearn.cluster import KMeans, SpectralClustering, Birch
from sklearn.decomposition import RandomizedPCA, TruncatedSVD
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

import RSmodule
import DataJoin


# get data
mat_usr_item_orders, \
mat_usr_purchase_orders, \
user_price_vec, \
row_labels_orders, \
col_labels_orders = DataJoin.get_all_the_data()

# fabricar la matriz de datos sparse
mat = RSmodule.get_process_matrix(mat_usr_item_orders, mat_usr_purchase_orders, row_labels_orders)

print('Training...')
# divido en train y test
X_train, X_test = train_test_split(mat, test_size=0.05, random_state=75)

# reducimos nuestro set de variables >> utilizo este tipo porque admite matriz sparse
pca = TruncatedSVD()
X_train_red = pca.fit_transform(X_train)
X_test_red = pca.transform(X_test)

# calcular clusters con Kmeans en el dataset reducido
method = KMeans(n_clusters=10, n_jobs=-1)
method.fit(X_train_red)

# predecimos los clusters del test
clusters = method.predict(X_test_red)

# Recomendar
print('Recomendation...')
recomendaciones = RSmodule.recomendacion_kmeans(method, X_train, clusters_pred=clusters, item_lbl=col_labels_orders, colname='Visitas')

# scoring del recomendador
score = RSmodule.evaluación_kmeans(method, X_train, X_test, clusters_pred=clusters,
                                   item_lbl=col_labels_orders, colname='Visitas')

# for i, cl in enumerate(clusters):
#     print('item de test ', i, 'label=', cl)
#     print(recomendaciones[i].head(5))  # top 5


df_most_viewed = RSmodule.most_viewed(mat, col_labels_orders, num_views=10)
print('Most viewed:\n', df_most_viewed)

# PLOTS
# plot 2D (solo funciona porque nuestra reducción dimensional tiene 2 dimensiones!)
fig = plt.figure(figsize=(15, 8))
ax = fig.add_subplot(111)

ax.scatter(method.cluster_centers_[:, 0],
           method.cluster_centers_[:, 1],
           c='red', s=400, alpha=0.5, label='Centros de cluster')

ax.scatter(X_test_red[:, 0], X_test_red[:, 1], c='blue', label='Test', s=200)
ax.scatter(X_train_red[:, 0], X_train_red[:, 1], c='green', label='Train')
ax.legend()
RSmodule.plot2D(method.cluster_centers_)

# plot 2D manifold (funciona siempre)
RSmodule.plotManifold(X_test_red, clusters)
RSmodule.plt.show()
