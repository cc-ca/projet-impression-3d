# Install all dependancies in an environment
install: /usr/bin/python3 /usr/bin/pip requirements.txt 
	pip install -r requirements.txt

# Start 
run: /usr/bin/python3 raspberry/script.py
	python3 raspberry/script.py
