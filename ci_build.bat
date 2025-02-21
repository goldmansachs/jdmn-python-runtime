call ci/make_env.bat .venv

tox -e py312
tox -e linters