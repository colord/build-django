""" 

Automatically build a new django project

"""
import sys
from subprocess import run
from os import chdir, makedirs, path
from django.core.management.utils import get_random_secret_key

# Set project directory if command line argument is given
PROJECT_DIR = str(sys.argv[1]) if sys.argv[1:] else 'web_app'
APP_NAME = PROJECT_DIR
# TODO - Should this be here or part of a config file (yaml)?
# how to collect dependency versions?
DEPENDENCIES = ['django', 'gunicorn', 'whitenoise', 'python-decouple']

#--------------------------#
# 1 - Create project folder
#--------------------------#
def create_project_dir():
    makedirs(PROJECT_DIR)

#------------------------------#
# 2 - Create Django core folder
#------------------------------#
def create_django_core(project_name='core'):
    ''' 
    Real command:   django-admin startproject core . 
    '''
    run(['django-admin', 'startproject', project_name, '.'])


#------------------------------------------------------------#
# 3 - Create config files: .env, .gitignore, requirements.txt
#------------------------------------------------------------#
def create_config_files():
    with open('.env', 'w') as dotenv:
        # Create new secret key
        dotenv.write(f"SECRET_KEY='{get_random_secret_key()}'")
    
    with open('.gitignore', 'w') as git_ignore:
        git_ignore.write(".env")

    with open('requirements.txt', 'w') as requirements:
        for library in DEPENDENCIES:
            requirements.write(library)
            requirements.write('\n')


#---------------------------------------#
# 4 - Create template and static folders
#---------------------------------------#
def create_template_static_dirs():
    makedirs('templates')
    makedirs('static/css')
    makedirs('static/img')
    makedirs('static/fonts')


#-----------------------#
# 5 - Create application
#-----------------------#
def create_django_app():
    ''' 
    Real command:   python manage.py startapp web_app
    '''
    run(['python', 'manage.py', 'startapp', APP_NAME])

    with open(path.join(APP_NAME, 'urls.py'), 'w') as urls:
        urls.write('')


def main():
    create_project_dir()
    # Enter into project dir and create rest of the build
    chdir(PROJECT_DIR)
    create_django_core()
    create_config_files()
    create_template_static_dirs()
    create_django_app()

if __name__ == "__main__":
    main()