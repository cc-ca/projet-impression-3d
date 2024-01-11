# Oneshell means I can run multiple lines in a recipe in the same shell, so I don't have to
# chain commands together with semicolon
.ONESHELL:

# Env variables
CONDA_ENV_NAME=impression_3d
PYTHON_VERSION=3.11

# Need to specify bash in order for conda activate to work.
SHELL=/bin/bash

CONDA_ENV=$$(conda info --base)
SOURCE_CONDA=source $(CONDA_ENV)/etc/profile.d/conda.sh
CONDA_CREATE=$(SOURCE_CONDA) ; conda create --yes 
# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH
CONDA_ACTIVATE=$(SOURCE_CONDA) ; conda activate ; conda activate
CONDA_REMOVE=$(SOURCE_CONDA) ; conda remove --all --yes --name


# Install all dependancies in an environment
install: requirements.txt /usr/bin/pip  install_conda 
	$(CONDA_CREATE) --name $(CONDA_ENV_NAME) python=$(PYTHON_VERSION)
	$(CONDA_ACTIVATE) $(CONDA_ENV_NAME)
	pip install -r requirements.txt

install_conda: /bin/sudo /bin/apt 
	sudo apt install wget --yes
	mkdir -p ~/miniconda3
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
	bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
	rm -rf ~/miniconda3/miniconda.sh	
	~/miniconda3/bin/conda init bash

# Start 
run: script.py
	$(CONDA_ACTIVATE) $(CONDA_ENV_NAME)
	python script.py


clean: $(CONDA_ENV)/conda 
	$(CONDA_REMOVE) $(CONDA_ENV_NAME)
