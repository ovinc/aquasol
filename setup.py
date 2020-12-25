from setuptools import setup, find_packages
import aquasol

with open("README.md", "r", encoding='utf8') as f:
    long_description = f.read()

setup(
    name='aquasol',
    version=aquasol.__version__,
    author='Olivier Vincent',
    author_email='olivier.vincent@univ-lyon1.fr',
    url='https://cameleon.univ-lyon1.fr/ovincent/aquasol',
    description='Thermodynamic relations for water and solutions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pynverse', 'numpy'],
    setup_requires=['pytest'],
    python_requires='>=3.6',
    license='BSD-3-Clause'
)
