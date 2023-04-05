from setuptools import setup, find_packages
from typing import List



HYPHEN_E_DOT = '-e .' # to tell that setup.py file exist call it and build it

# recieving and returning
def get_requirements(file_path:str)->List[str]:
    
    requirements = list()

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('/n', '') for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(

    # name for the project
    name = 'pkl_ml_project',

    # version of the package
    version = '0.01',

    # author of the package
    author = 'PiyushKLimkar',

    # auther email
    author_email = 'piyushlimkar22@gmail.com',

    # packeges
    # find_packages() will look for folders that have __init__() file
    packages = find_packages(),

    # while anyone install this package following libraries/packages will be installed by default
    # in otherwords these libraries/packages are dependencies for your package/library
    # install_requred = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly']
    install_required = get_requirements('requirements.txt')
)

