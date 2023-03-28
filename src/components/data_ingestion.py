import os
import sys

import pandas as pd


from sklearn.model_selection import train_test_split


from dataclasses import dataclass


from src.logger import logging
from src.exception import Custom_Exception
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer



# with help of this class we can create and
# initialize class variables without __init__() method.
@dataclass
class DataIngestionConfig:
    # Defining paths where to store data after train test split
    # 'artifacts/tarin.csv'
    train_data_path = os.path.join('artifacts', 'train.csv')
    test_data_path = os.path.join('artifacts', 'test.csv')
    raw_data_path = os.path.join('artifacts', 'data.csv')


class DataIngestion:
    def __init__(self):
        # Store all paths in ingestion_config
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered into data ingestion method.')

        try:
            logging.info('Reading the dataset as dataframe.')
            df = pd.read_csv('notebook\\data\\stud.csv')
            logging.info('Read the dataset as dataframe.')

            # os.path.dirname :- artifacts
            # os.makedirs :- will create directory if exist it will only update
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),
                        exist_ok = True)
            
            # 'artifacts/data.csv'
            # create file_name.csv based on given path
            df.to_csv(self.ingestion_config.raw_data_path,
                      index = False, header = True)
            
            logging.info('Train Test Split Initiated')

            train_set, test_set = train_test_split(df, test_size = 0.2, random_state = 42)

            train_set.to_csv(self.ingestion_config.train_data_path,
                             index = False, header = True)
            
            test_set.to_csv(self.ingestion_config.test_data_path,
                            index = False, header = True)
            
            logging.info("Inmgestion of the data iss completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise Custom_Exception(e, sys)
        

if __name__ == '__main__':
    obj = DataIngestion()
    train_path, test_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_path, test_path)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))