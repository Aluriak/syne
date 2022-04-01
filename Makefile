

run:
	python -m syne


t: test
test:
	python -m pytest test/ syne/ --doctest-module


.PHONY: test t

develop:
	python setup.py develop
install_deps:
	python -c "import configparser; c = configparser.ConfigParser(); c.read('setup.cfg'); print(c['options']['install_requires'])" | xargs pip install -U
release:  # pip install zest.releaser[recommended]
	fullrelease
