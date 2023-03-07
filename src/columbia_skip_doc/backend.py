import logging
import os

import datapipeline as data_pipeline
import utils

from utils import setup_logging
from constants import PRJ_ROOT_STR

from openprompt.plms import load_plm

FILE_NAME = __name__

_logger = setup_logging(logging.DEBUG, FILE_NAME)


class OpenPromptPipeline:
    def __init__(self, model_type, model_name):
        self.model_type = model_type
        self.model_name = model_name

    def load_model(self):
        return load_plm(self.model_type, self.model_name)



if __name__ == "__main__":
    data_fp = os.path.join(PRJ_ROOT_STR, "data", "All-2479-Answers-retrieved-from-MedQuAD.csv")
    batch_size = 32
    data_classes_fp = os.path.join(PRJ_ROOT_STR, "data", "All-qrels_LiveQAMed2017-TestQuestions_2479_Judged-Answers.txt")
    shuffle = False
    class_filter = None

    dp = data_pipeline.DataPipeline(data_fp, batch_size, data_classes_fp, shuffle, class_filter)
    dp.read_and_clean_data()

    op = OpenPromptPipeline('bert', 'emilyalsentzer/Bio_ClinicalBERT')
    plm, tokenizer, model_config, WrapperClass = op.load_model()
    _logger.info(f"Loaded model: {plm}")