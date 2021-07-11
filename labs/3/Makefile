PYTHON= ./.env/bin/python

chmod:
	chmod +x mdp

numpy: pip
	$(PYTHON) -m pip install numpy

install:
	python3 -m venv .env

pip: install
	$(PYTHON) -m pip install --upgrade pip

