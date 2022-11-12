include Makefile.mk

NAME=botocore-stubber-recorder

help:
	@echo 'make                 - builds a zip file to target/.'
	@echo 'make release         - builds a zip file and deploys it to s3.'
	@echo 'make clean           - the workspace.'
	@echo 'make test            - execute the tests, requires a working AWS connection.'

do-push: deploy


do-build: Pipfile.lock
	pipenv run python setup.py check
	pipenv run python setup.py build
	pipenv run python setup.py sdist

upload-dist: Pipfile.lock
	pipenv run twine upload dist/*

Pipfile.lock: Pipfile setup.py
	pipenv update -d

clean:
	rm -rf venv target
	find . -name \*.pyc | xargs rm 

test: Pipfile.lock
	[ -z "$(shell ls -1 tests/test*.py 2>/dev/null)" ] || PYTHONPATH=$(PWD)/src pipenv run pytest ./tests/test*.py

fmt:
	black $(shell find src -name \*.py) tests/*.py
