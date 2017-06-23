#!/bin/bash


# Creamos certificado y lo ponemos en ~/certs
sudo openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem
mkdir ~/certs
mv mycert.pem ~/certs

# Creamos una configuracion de jupyter
jupyter notebook --generate-config 

# Aniadimos nuestros valores
echo "c = get_config()
c.IPKernelApp.pylab = 'inline' 
c.NotebookApp.certfile = u'/home/ubuntu/certs/mycert.pem' 
c.NotebookApp.ip = '*' 
c.NotebookApp.open_browser = False 

# Your password below will be whatever you copied earlier 
c.NotebookApp.password = u'sha1:8596c479de6d:27bff91ccada863273dd97fdf9a13f0a513ada3b'

c.NotebookApp.port = 8888" >> ~/.jupyter/jupyter_notebook_config.py
