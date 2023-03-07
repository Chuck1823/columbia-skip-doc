import logging
import os
import pandas as pd
import utils

from utils import setup_logging
from constants import PRJ_ROOT_STR

FILE_NAME = __name__

_logger = setup_logging(logging.DEBUG, FILE_NAME)

class DataPipeline:
    def __init__(self, data_fp, batch_size, data_classes_fp=None, shuffle=True, class_filter=None):
        """Constructor for DataPipeline class

        Args:
        data_fp (DataFrame): _description_
            batch_size (int): _description_
            data_classes_fp (str, optional): absolute file path to file containing labels - assumes space-delimited txt file with label, id as columns.
            Defaults to None.
            shuffle (bool, optional): boolean indicating if we want to shuffle the data. Defaults to True.
            class_filter (List[str], optional): list containing which examples' labels to keep. Defaults to None (meaning no filtering).
        """
        self.data_fp = data_fp
        self.data_df = None
        self.data_classes_fp = data_classes_fp
        self.data_classes_df = None
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.n_batches = len(data_fp) // batch_size
        self.class_filter = class_filter

    def read_and_clean_data(self):
        try:
            self.data_df = pd.read_csv(self.data_fp)
            _logger.info(f"Successfully read data file of shape: {self.data_df.shape}")
        except OSError as e:
            _logger.error("Could not read data file: {}".format(e))
            raise

        if os.path.exists(self.data_classes_fp):
            self.data_classes_df = pd.read_csv(self.data_classes_fp, sep= " ", names=['label', 'id'])
            _logger.info(f"Successfully read data classes file of shape: {self.data_classes_df.shape}")

        if self.class_filter is not None:
            for class_label in self.class_filter:
                self.data_df = self.data_df[self.data_df['label'] == class_label]

        self.data_df = self.data_df.dropna()

        return
    