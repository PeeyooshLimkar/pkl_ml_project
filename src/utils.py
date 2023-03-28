import os
import sys

import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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


def evaluate_models(xtrain, ytrain, xtest, ytest, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model, para, cv = 3)
            gs.fit(xtrain, ytrain)

            model.set_params(**gs.best_params_)
            model.fit(xtrain, ytrain)

            ytrain_pred = model.predict(xtrain)
            ytest_pred = model.predict(xtest)

            train_model_score = r2_score(ytrain, ytrain_pred)
            test_model_score = r2_score(ytest, ytest_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise Custom_Exception(e, sys)