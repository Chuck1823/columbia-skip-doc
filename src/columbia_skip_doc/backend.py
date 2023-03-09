import logging
import os

import datapipeline as data_pipeline
import utils

from utils import setup_logging
from constants import PRJ_ROOT_STR

from openprompt.plms import load_plm
from openprompt.prompts import ManualTemplate

FILE_NAME = __name__

_logger = setup_logging(logging.DEBUG, FILE_NAME)


class OpenPromptPipeline:
    def __init__(self, model_type, model_name):
        """ Constructor for OpenPromptPipeline class

        Args:
            model_type (str): the model type - see OpenPrompt documentation for supported models in openpromt.plms.__init__.py
            model_name (str): the model name as seen on huggingface.co's model page
        """
        self.model_type = model_type
        self.model_name = model_name

    def load_model(self):
        """ Uses OpenPrompt function to load a pretrained model, the model's tokenizer, the model's config from huggingface,
        and OpenPrompt's wrapper class object for the model's objective.

        Returns:
            plm: huggingface pretrained model
            tokenizer: huggingface tokenizer for the model
            model_config: huggingface model config
            wrapper_class: OpenPrompt wrapper class for the model's objective
        """
        return load_plm(self.model_type, self.model_name)



if __name__ == "__main__":
    data_fp = os.path.join(PRJ_ROOT_STR, "data", "All-2479-Answers-retrieved-from-MedQuAD.csv")
    data_classes_fp = os.path.join(PRJ_ROOT_STR, "data", "All-qrels_LiveQAMed2017-TestQuestions_2479_Judged-Answers.txt")

    dp = data_pipeline.DataPipeline(data_fp, data_classes_fp)
    data_df = dp.read_and_clean_data(id_col_data='AnswerID', id_col_data_classes='id')
    data_dict = dp.split_data_into_dictionary(data_df)

    op = OpenPromptPipeline('bert', 'emilyalsentzer/Bio_ClinicalBERT')
    plm, tokenizer, model_config, WrapperClass = op.load_model()
    _logger.info(f"Loaded model: {plm}")

    template_text = 'Question: {"placeholder":"text_a"} Answer: {"mask"}.'
    template = ManualTemplate(tokenizer=tokenizer, text=template_text)
    _logger.info(f"Example wrapped in template: {template.wrap_one_example(data_dict['train'][0])}")

    wrapped_mlm_tokenizer = WrapperClass(max_seq_length=128, decoder_max_length=3, tokenizer=tokenizer,truncate_method="head")
    _logger.info(f"Initialized tokenizer: {wrapped_mlm_tokenizer}")