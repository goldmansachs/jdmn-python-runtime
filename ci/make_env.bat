@ECHO OFF

set CI_PROJECT_DIR=%cd%

IF "%1"=="" (
    ECHO Usage make_env.bat PYTHON_ENV_DIR
    exit /b
)

REM set PIP_INDEX_URL=https://pypi.python.org/pypi
REM set PIP_TRUSTED_HOST=pypi.python.org

set PYTHON_ENV_DIR=%1
python -m venv %PYTHON_ENV_DIR%
call %PYTHON_ENV_DIR%/Scripts/activate

python --version
pip --version
python -m pip install -U pip
pip install -r %CI_PROJECT_DIR%/ci/ci_requirements.txt

