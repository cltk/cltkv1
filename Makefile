build:
	poetry build

develop:
	python setup.py sdist develop

docs:
	poetry run sphinx-apidoc -f -o docs src/cltkv1 && cd docs && poetry run make html && cd ..

format:
	isort --recursive . && poetry run black src/cltkv1 tests docs scripts

install:
	# Equivalent of ``python setup.py install``
	poetry install

installPyPITest:
	pip install --index-url https://test.pypi.org/simple/ cltk

lint:
	mkdir pylint && poetry run pylint --output-format=json cltkv1 > pylint/pylint.json || true && poetry run pylint-json2html pylint/pylint.json 1> pylint/pylint.html

preCommitRun:
	poetry run pre-commit autoupdate && poetry run pre-commit install && poetry run pre-commit autoupdate

test:
	# poetry run nosetests --no-skip --with-coverage --cover-erase --cover-html-dir=htmlcov --cover-html --cover-package=cltkv1 --with-doctest
	poetry run tox

typing:
	poetry run mypy --html-report .mypy_cache src/cltkv1

updateDependencies:
	# Equivalent of ``pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U``
	poetry update

uml:
	cd docs/ && poetry run pyreverse -o png ../src/cltkv1/ && cd ../

upload:
	poetry publish

uploadTest:
	poetry publish --repository=testpypi

all: black lint typing test check uml docs

.PHONY: build docs
