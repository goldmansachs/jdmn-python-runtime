# jdmn-python-runtime

## How to install

```> pip install jdmn-python-runtime``` 

## SDLC
* Check-out project
* Create a venv (see below) if you do not have one already
* Make changes
* Run tests (see below) and fix errors
* Run linters (see below) and fix errors
* Make sure the test coverage is decent (e.g. around 70-75%)
* Commit changes

### How to create a venv

```> ci/make_env.bat``` 

### How to run tests

```> tox -e py312``` 
or
```> python -m pytest --cov=jdmn tests/``` 

### How to run pylint

```> tox -e pylint``` 

### How to run flake8

```> tox -e flake8``` 

### How to build the wheel

```> tox -e build``` 

### How to publish the wheel

```twine upload --repository testpypi --skip-existing dist/* ```

