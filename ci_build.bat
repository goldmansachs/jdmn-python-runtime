call ci/make_env.bat .venv

tox -e py310
tox -e linters