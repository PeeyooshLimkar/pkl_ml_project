import os
import sys

import pandas as pd
import numpy as np

from src.exception import Custom_Exception
from src.logger import logging

import dill



def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok = True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)

        logging.info(f'{obj} Object is Dumped at {dir_path}')    

    except Exception as e:
        raise Custom_Exception(e, sys)
