.PHONY: install uninstall build pypi
install:
	python3 setup.py install

uninstall:
	pip3 uninstall pelican-embed-svg

build:
	pip install wheel
	python3 setup.py sdist bdist_wheel

pypi:
	pip3 install twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
