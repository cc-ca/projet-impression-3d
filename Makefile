# Install all dependancies in an environment
setup: /usr/bin/python3 requirements.txt
	echo "Installation des dépendances système nécessaires"
	sudo apt install libhdf5-dev

	echo "Création de l'environnement virtuel"
	/usr/bin/python3 -m venv .venv

	echo "Installation des dépendances python nécessaires"
	source .venv/bin/activate \
	/usr/bin/python3 -m pip install --upgrade pip \
	/usr/bin/python3 -m pip install -r requirements.txt

	echo "Setup script launch on start up \n if you get an error, please run crontab -e and exit then run make setup again"
	(crontab -l && echo "@reboot source $PWD/.venv/bin/activate && python $PWD/script.py") | crontab -

# Start capture
run: /usr/bin/python3 script.py
	source .venv/bin/activate \
	python $PWD/script.py
