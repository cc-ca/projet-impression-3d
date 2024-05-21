#
# Ce Makefile est destiné à une utilisation sur un système à base Debian comme Raspbian,
# il est possible qu'il ne fonctionne pas sur d'autres systèmes et qu'il nécessite des modifications.
#

SHELL := /bin/bash

define SYSTEMD_SERVICE
[Unit]
Description=Run 3D printer Error Detection python script on boot
After=default.target

[Service]
Type=exec
WorkingDirectory=$(PWD)
ExecStart=/usr/bin/bash -c "source .venv/bin/activate && cd 3d-printer-error-detector && python script.py"
Restart=on-failure

[Install]
WantedBy=default.target
endef
export SYSTEMD_SERVICE


# Install all dependancies in a virtual environment
setup_env: /usr/bin/apt /usr/bin/python3 requirements.txt
	@echo "Installation des dépendances système nécessaires"
	sudo apt update && sudo apt upgrade
	sudo apt install python3-dev libhdf5-dev

	@echo "Création de l'environnement virtuel"
	/usr/bin/python3 -m venv .venv

	@echo "Installation des dépendances python nécessaires (peux être long)"
	source .venv/bin/activate &&\
	python -m pip install --upgrade pip &&\
	python -m pip install -r requirements.txt


# Enable auto start of the script on boot
# This will add a cron job to the user's crontab
# Need to setup the environment first
setup_autolaunch: .venv/bin/activate 3d-printer-error-detector/script.py
	@echo "Setup script launch on start up"
	@echo "$$SYSTEMD_SERVICE" | sudo tee /etc/systemd/system/3dprinter_error_detector.service
	@echo "Reload services and start it on boot"
	sudo systemctl daemon-reload
	sudo systemctl enable 3dprinter_error_detector.service


setup_webserver: /usr/bin/apt 3d-printer-error-detector/web/
	@echo "Installation du serveur web"
	sudo apt install apache2

	@echo "Configuration du serveur web"
	sudo cp 3d-printer-error-detector/web/* /var/www/html/
	sudo systemctl enable apache2.service


# Install all dependancies in an environment
setup: setup_env setup_autolaunch setup_webserver


# Start capture manually
# Need to setup the environment first by running 'make setup' or as a minimum 'make setup_env'
run: .venv/bin/activate 3d-printer-error-detector/script.py
	source .venv/bin/activate &&\
	cd 3d-printer-error-detector &&\
	python script.py


setup_and_run: setup run

all: setup_and_run
