# Oneshell means I can run multiple lines in a recipe in the same shell, so I don't have to
# chain commands together with semicolon
.ONESHELL:

# Env variables
CONDA_ENV_NAME=impression_3d
PYTHON_VERSION=3.11
BIN_ENV=/usr/bin

# Need to specify bash in order for conda activate to work.
SHELL=$(BIN_ENV)/bash

SOURCE_CONDA=source /etc/profile.d/conda.sh 
CONDA_CREATE=$(SOURCE_CONDA) ; conda create --yes 
# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH
CONDA_ACTIVATE=$(SOURCE_CONDA) ; conda activate ; conda activate
CONDA_REMOVE=$(SOURCE_CONDA) ; conda remove --all --yes --name


# Install all dependancies in an environment
install: requirements.txt $(BIN_ENV)/pip  $(BIN_ENV)/conda 
	$(CONDA_CREATE) --name $(CONDA_ENV_NAME) python=$(PYTHON_VERSION)
	$(CONDA_ACTIVATE) $(CONDA_ENV_NAME)
	pip install -r requirements.txt

install_conda: $(BIN_ENV)/sudo $(BIN_ENV)/apt 
	sudo -i
	# Install our public GPG key to trusted store
	curl https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc | gpg --dearmor > conda.gpg
	install -o root -g root -m 644 conda.gpg /usr/share/keyrings/conda-archive-keyring.gpg
	# Check whether fingerprint is correct (will output an error message otherwise)
	gpg --keyring /usr/share/keyrings/conda-archive-keyring.gpg --no-default-keyring --fingerprint 34161F5BF5EB1D4BFBBB8F0A8AEB4F8B29D82806
	# Add our Debian repo
	echo "deb [arch=amd64 signed-by=/usr/share/keyrings/conda-archive-keyring.gpg] https://repo.anaconda.com/pkgs/misc/debrepo/conda stable main" > /etc/apt/sources.list.d/conda.list
	apt update
	apt install conda --yes

# Start 
run: 
	$(CONDA_ACTIVATE) $(CONDA_ENV_NAME)


clean:
	$(CONDA_REMOVE) $(CONDA_ENV_NAME)
