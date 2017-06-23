#!/bin/bash

# Descargamos Anaconda
wget "https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh"

# La instalamos (si a todo)
bash Anaconda3-4.3.1-Linux-x86_64.sh
rm Anaconda3-4.3.1-Linux-x86_64.sh

# Descargamos el archivo de datos
wget https://www.dropbox.com/s/eom7sjtp0ftchwo/IntropiaCSV.tar.gz

# Lo descomprimimos
tar -xvf IntropiaCSV.tar.gz

# Ponemos Anaconda en el PATH
export PATH="/home/ubuntu/anaconda3/bin:$PATH"

# Recreamos el environment
conda env create -f environment.yml

source activate pfm

# Creamos archivo config notebook, iniciamos server
./config_notebook.sh
jupyter notebook &
