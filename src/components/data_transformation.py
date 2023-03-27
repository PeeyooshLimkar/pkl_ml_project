import os
import sys
import pandas as pd
import numpy as np


from dataclasses import dataclass


from src.exception import Custom_Exception
from src.logger import logging
from src.utils import save_object


from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline



@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def get_data_transformer_object(self):
        # All Transformations will take place here
        try:
            
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education',
                                    'lunch', 'test_preparation_course']
            
            logging.info(f'Numerical Features :-\n{numerical_columns}')
            logging.info(f'Categorical Features :-\n{categorical_columns}')

            logging.info('Creating Pipeline')
            
            num_pipeline = Pipeline(
                steps = [
                ('imputer', SimpleImputer(strategy = 'median')),
                ('scaler', StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                ('impute', SimpleImputer(strategy = 'most_frequent')),
                ('one_hot_encoder', OneHotEncoder()),
                ('scaler', StandardScaler(with_mean = False))
                ]
            )

            logging.info('Applying Pipeline')

            preprocessor = ColumnTransformer(
                [
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise Custom_Exception(e, sys)
    
    
    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read Train & Test data.')

            logging.info('Obtaining Preprocessing Object')

            preprocessing_obj = self.get_data_transformer_object()

            target_column = 'math_score'

            input_feature_train_df = train_df.drop(columns = target_column)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns = target_column)
            target_feature_test_df = test_df[target_column]

            logging.info('Applyimg Preprocessing Object on training and testing dataset.')

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, 
                np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr,
                np.array(target_feature_test_df)
            ]

            logging.info('Saving Preprocessing Object')

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )


        except Exception as e:
            raise Custom_Exception(e, sys)