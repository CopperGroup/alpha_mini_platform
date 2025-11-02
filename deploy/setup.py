
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
    version='2.0.0', # Оновлена версія для масштабованої платформи
    description='Scalable command platform for UBTECH Alpha Mini Robot',
    author='Copper Group Corporation in partnership with Yevhenii Tymchyk and Yelizaveta Piletska',
    
    # 1. Знаходимо пакети у каталозі 'src'
    packages=find_packages(where=os.path.join(PROJECT_ROOT, 'src')),
    
    # 2. Вказуємо, де знаходяться пакети
    package_dir={'': os.path.join(PROJECT_ROOT, 'src')},
    
    # Вимоги
    install_requires=read_requirements(),
    
    # Визначаємо вхідну точку (для запуску з терміналу)
    entry_points={
        'console_scripts': [
            # Вказуємо на main.py в корені проєкту
            'run_alpha_platform = main:main', 
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