PYTHON= ./.env/bin/python

install:
	python3 -m venv .env

pip: install
	$(PYTHON) -m pip install --upgrade pip

numpy: pip
	$(PYTHON) -m pip install numpy
