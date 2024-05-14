SHELL := /bin/bash

# Install all dependancies in a virtual environment
setup_env: /usr/bin/python3 requirements.txt
	echo "Installation des dépendances système nécessaires"
	sudo apt install libhdf5-dev

	echo "Création de l'environnement virtuel"
	/usr/bin/python3 -m venv .venv

	echo "Installation des dépendances python nécessaires"
	source .venv/bin/activate &&\
	python -m pip install --upgrade pip &&\
	python -m pip install -r requirements.txt


# Enable auto start of the script on boot
# This will add a cron job to the user's crontab
# Need to setup the environment first
setup_autolaunch: .venv/bin/activate script.py
	echo "Setup script launch on start up"
	(\
		crontab -l 2>/dev/null; # Force crontab to be created if it doesn't exist \
		echo "@reboot source $(PWD)/.venv/bin/activate && python $(PWD)/script.py"\
	) | crontab - # Add the cron job to the user's crontab


# Install all dependancies in an environment
setup: setup_env setup_autolaunch


# Start capture manually
# Need to setup the environment first by running 'make setup' or as a minimum 'make setup_env'
run: .venv/bin/activate script.py
	source .venv/bin/activate &&\
	python script.py


setup_and_run: setup run

all: setup_and_run
