# deploy/setup.py

from setuptools import setup, find_packages
import os

# Визначаємо базовий каталог, щоб знайти src/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '..')

# Читаємо вимоги
def read_requirements():
    try:
        with open(os.path.join(PROJECT_ROOT, 'requirements.txt'), 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return ['alphamini'] # Базові вимоги

setup(
    name='alpha_platform_custom', 
    version='2.0.0', 
    description='Scalable command platform for UBTECH Alpha Mini Robot',
    author='Copper Group Corporation in partnership with Yevhenii Tymchyk and Yelizaveta Piletska',
    
    # 1. Спрощений пошук: find_packages знайде alpha_mini_pkg та listeners всередині src/
    packages=find_packages(where=os.path.join(PROJECT_ROOT, 'src')),
    
    # 2. Вказуємо, що коренем пакетів є src
    package_dir={'': os.path.join(PROJECT_ROOT, 'src')},
    
    # Видаляємо всі складні конструкції package_dir, find_packages, PACKAGES.
    
    # Вимоги
    install_requires=read_requirements(),
    
    # КЛЮЧОВА ЗМІНА: Вказуємо на launcher.py всередині alpha_mini_pkg (який в src)
    entry_points={
        'console_scripts': [
            'run_alpha_platform = alpha_mini_pkg.launcher:run', 
        ],
    },
    
    # Додаткова конфігурація
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)