from setuptools import setup, find_packages
import thermov

with open("README.md", "r") as f:
    long_description = f.read()

setup(
        name='thermov',
        version=plov.__version__,
        author='Olivier Vincent',
        author_email='olivier.vincent@univ-lyon1.fr',
        url='https://cameleon.univ-lyon1.fr/ovincent/thermo-ov',
        description='Thermodynamic relations for water and solutions',
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
        ],
        setup_requires=[''],
        python_requires='>=3.6'
)
