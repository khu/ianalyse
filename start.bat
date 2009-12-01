SET CONFIGS_DIR=./analyse/tests/configs
rmdir /S /Q results
mkdir results
python manage.py testserver

