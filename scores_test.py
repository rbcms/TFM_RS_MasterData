"""
CALCULO DE LOS SCORES EN BASE A LOS EVENTOS.

Esta conjunto de recomendadores presentes en este proyecto son del tipo Filtrado Colaborativo,
basado en momeria.

Eventos pora el cáĺculo de los ratings >>

* páginas vistas (Page), que son de productos.
* elementos añadidos a los carritos (orders), pueden quedar abandonados o no (purchases).
* items (purchases), compras finalizadas.

"""


import RSmodule
import DataJoin
import os
import pandas as pd


