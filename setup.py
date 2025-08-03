"""
    The setup.py file is a python build script used for packaging and distributing 
    Python projects; it is used by setuptools (or distutils in older python versions) to define
    the configuration of your project, such as its metadata, dependencies, and more
"""

from setuptools import find_packages, setup
from typing import List
from src.datascience import logger

project_name = "datascienceendtoend"


def get_requirements() -> List[str]:
    """
    Reads and parse requirements from requirements.txt

    Returns:
        List[str]: List of package requirements

    Raises:
        FileNotFoundError: If requirements.txt doesn't exist
    """

    requirements: List[str] = []
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()  # Read line by line

            for line in lines:
                requirement=line.strip()

                # Skip empty lines, comments, and editable installs
                if requirement and requirement != '-e .' and not requirement.startswith('#'):
                    requirements.append(requirement)
    except FileNotFoundError as f:
        logger.warning("requirements.txt not found")
    
    return requirements

setup(
    name=project_name,
    version="0.0.1",
    author="Armando Albornoz",
    author_email="albornoz.armando31416@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements()
)