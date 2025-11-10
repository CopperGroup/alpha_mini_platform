from setuptools import setup, find_packages
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '..')

def read_requirements():
    try:
        with open(os.path.join(PROJECT_ROOT, 'requirements.txt'), 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return ['alphamini']

setup(
    name='alpha_platform_custom', 
    version='2.0.0', 
    description='Scalable command platform for UBTECH Alpha Mini Robot',
    author='Yelizaveta Piletska',
    
    packages=find_packages(where=os.path.join(PROJECT_ROOT, 'src')),
    
    package_dir={'': os.path.join(PROJECT_ROOT, 'src')},
    
    install_requires=read_requirements(),

    entry_points={
        'console_scripts': [
            'run_alpha_platform = alpha_mini_pkg.launcher:run', 
        ],
    },

    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)