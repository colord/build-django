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


#--------------------------------------#
# 6 - Show additional setup instrutions
#--------------------------------------#
def show_instructions():
    print("⚡ Additional setup is required ⚡\n")

    # core > settings.py configuration
    print("1️⃣  In core > settings.py")
    print(f" • {'Include module at the top': <26}-> from decouple import config")
    print(f"\n • {'Change SECRET_KEY': <26}-> config('SECRET_KEY')")
    django_app_name = APP_NAME.split('_')[0].capitalize() + APP_NAME.split('_')[1].capitalize()
    print(f"\n • {'Add to INSTALLED_APPS': <26}-> '{APP_NAME}.apps.{django_app_name}Config'")
    print(f"\n • {'Add to TEMPLATES DIRS': <26}-> 'templates/'")
    print(f"\n • {'Add under STATIC_URL': <26}-> STATICFILES_DIRS = [BASE_DIR / 'static']")

    # core > urls.py configuration
    print("\n2️⃣  In core > urls.py")
    print(f" • {'Add to urlpatterns': <26}-> path('', include('{APP_NAME}.urls'))")

    # web_app > urls.py configuration
    print("\n3️⃣  In app > urls.py")
    print(f"\n • {'Import module at top': <26}-> from django.urls import path")
    print(f"\n • {'Create urlpatterns': <26}-> urlpatterns = []")
    print(f"\n • Once views are created, add path to view inside urlpatterns")


def main():
    create_project_dir()
    # Enter into project dir and create rest of the build
    chdir(PROJECT_DIR)
    create_django_core()
    create_config_files()
    create_template_static_dirs()
    create_django_app()
    show_instructions()

if __name__ == "__main__":
    main()