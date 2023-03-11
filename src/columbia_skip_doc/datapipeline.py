import logging
import os
import pandas as pd
import utils

from utils import setup_logging
from constants import PRJ_ROOT_STR
from openprompt.data_utils import InputExample

from sklearn.model_selection import train_test_split

FILE_NAME = __name__

_logger = setup_logging(logging.DEBUG, FILE_NAME)

class DataPipeline:
    def __init__(self, data_fp, data_classes_fp=None, train_split=0.7, validation_split=0.2, test_split=0.1):
        """Constructor for DataPipeline class

        Args:
        data_fp (DataFrame): absolute file path to csv file containing data
        data_classes_fp (str, optional): absolute file path to cvs file containing labels - assumes space-delimited txt file with label, 
        id as unnamed columns. Defaults to None.
        train_split (float, optional): percentage of data to use for training. Defaults to 0.7.
        validation_split (float, optional): percentage of data to use for validation. Defaults to 0.2.
        test_split (float, optional): percentage of data to use for testing. Defaults to 0.1.
        """
        self.data_fp = data_fp
        self.data_classes_fp = data_classes_fp
        self.train_split = train_split
        self.validation_split = validation_split
        self.test_split = test_split

    def read_and_clean_data(self, id_col_data=None, id_col_data_classes=None):
        # TODO: add data cleaning functionality and make it generic for different datasets
        """
        Function to read in data from a csv file into a pandas DataFrame and it's corresponding labels from a txt file into
        a pandas DataFrame.
        """
        try:
            data_df = pd.read_csv(self.data_fp)
            _logger.info(f"Successfully read data file of shape: {data_df.shape}")
        except OSError as e:
            _logger.error("Could not read data file: {}".format(e))
            raise

        if os.path.exists(self.data_classes_fp):
            data_classes_df = pd.read_csv(self.data_classes_fp, sep= " ", names=['label', 'id'])
            data_classes_df = data_classes_df.reset_index(drop=True)
            _logger.info(f"Successfully read data classes file of shape: {data_classes_df.shape}")
            _logger.info("Merging the two datasets on common id column..")
            try:
                return data_df.merge(data_classes_df, how='inner', left_on=id_col_data, right_on=id_col_data_classes).drop(columns=[id_col_data_classes])
            except KeyError as e:
                _logger.error("Could not merge data and data classes files: {}".format(e))
                raise

        return data_df
    
    def split_data_into_dictionary(self, data_df):
        # TODO: maybe have text_b with any extraneous text?
        """ Method to split data into dictionary of dataframes based on class

        Args:
            data_df (DataFrame): DataFrame containing the data
            data_classes_df (DataFrame, optional): DataFrame containing the data classes
        Returns:
            dict: dictionary of lists of InputExample objects with keys being 'train', 'validation' and 'test'
        """
        raw_data_dict = {}
        data_dict = {}

        train_df = train_test_split(data_df, test_size= (self.test_split + self.validation_split), train_size=self.train_split)[0]
        validation_df = train_test_split(data_df, test_size= self.test_split, train_size=self.validation_split)[0]
        test_df = train_test_split(data_df, test_size= self.test_split, train_size=self.validation_split)[1]

        raw_data_dict['train'] = train_df
        raw_data_dict['validation'] = validation_df
        raw_data_dict['test'] = test_df

        for split in ['train', 'validation', 'test']:
            df = raw_data_dict[split]
            data_dict[split] = []
            for idx, row in df.iterrows():
                try:
                    question = df.loc[idx]['Answer'].split("Question: ")[1].split("URL: ")[0].rstrip()
                    answer = df.loc[idx]['Answer'].split("Question: ")[1].split("URL: ")[1].split("Answer: ")[1].rstrip()
                    meta = {'meta': row['label'].split("-")[1]}
                    guid = row['AnswerID']
                    data_dict[split].append(InputExample(guid=guid, text_a=question, tgt_text=answer, meta=meta))
                except KeyError as e:
                    _logger.error(f"Example mismatch between example classes file and examples file for Answer ID {row['id']}: {e}")
                    raise
                except IndexError as e:
                    _logger.error(f"Could not parse example for Answer ID {row['id']}: {e}")
                    raise
                
        return data_dict
    