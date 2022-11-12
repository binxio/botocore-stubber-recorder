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

deploy: Pipfile.lock
	pipenv run twine upload dist/*

Pipfile.lock: Pipfile setup.py
	pipenv update -d

clean:
	rm -rf venv target
	find . -name \*.pyc | xargs rm 

test: Pipfile.lock
	rm -rf generated tests/generated && pipenv run python setup.py test
	@echo test generated unit tests
	unset AWS_PROFILE ; PYTHONPATH=$PWD pipenv run pytest generated

fmt:
	black $(shell find src -name \*.py) tests/*.py
