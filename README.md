# INSTRUCCIONES_TFM_Sistema recomendación

Este es mi sistema de recomendación >> basado en filtrado colaborativo. Es un prototipo a modo de ejercicio.
Los datos para poder ejecutarlo están disponibles en el siguiente enlace:

DESCARGA DE LOS DATOS:
https://www.dropbox.com/s/6z4l35g31zjx9hd/DATA.tar.gz?dl=0

Estos datos han de almacenarse al mismo nivel que el resto de las carpetas existente, una vez descomprimidos.Es decir al mismo nivel de jerarquia.


La memoria y mas explicaciones pueden verse en la siguiente dirección.
http://rebecatfm.pythonanywhere.com/masterdata/index.html


Dependencias y paquetes a instalar:

sklearn.cluster, KMeans, SpectralClustering, Birch
sklearn.decomposition, RandomizedPCA, TruncatedSVD
sklearn.neighbors, KNeighborsClassifier, KNeighborsRegressor
sklearn.model_selection import train_test_split
scipy.sparse, lil_matrix
sklearn, manifold

os
pickle
numpy as np
pandas as pd
matplotlib, pyplot
import os
import sys

import RSmodule
import DataJoin
import RSmodule



