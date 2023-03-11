import logging
import os

import datapipeline as pipeline
import utils

from utils import setup_logging
from constants import PRJ_ROOT_STR

from openprompt.plms import load_plm
from openprompt.prompts import ManualTemplate
from openprompt import PromptDataLoader
from openprompt import PromptForGeneration

FILE_NAME = __name__

_logger = setup_logging(logging.DEBUG, FILE_NAME)


class OpenPromptPipeline:
    def __init__(self, model_type, model_name):
        """Constructor for OpenPromptPipeline class

        Args:
            model_type (str): the model type - see OpenPrompt documentation for supported models in openpromt.plms.__init__.py
            model_name (str): the model name as seen on huggingface.co's model page
        """
        self.model_type = model_type
        self.model_name = model_name

    def load_model(self):
        """Uses OpenPrompt function to load a pretrained model, the model's tokenizer, the model's config from huggingface,
        and OpenPrompt's wrapper class object for the model's objective.

        Returns:
            plm: huggingface pretrained model
            tokenizer: huggingface tokenizer for the model
            model_config: huggingface model config
            wrapper_class: OpenPrompt wrapper class for the model's objective
        """
        return load_plm(self.model_type, self.model_name)

    def generate_data_loaders(
        self,
        data_dict,
        template,
        tokenizer,
        tokenizer_wrapper_class,
        max_seq_length=1024,
        decoder_max_length=1024,
        batch_size=32,
        predict_eos_token=True,
        truncate_method="head",
    ):
        """Generates OpenPrompt data loaders for the train, validation, and test datasets

        Args:
            data_dict (dict): dictionary containing the three splits of input data
            template (Template): a derived class of :obj:`Template`
            tokenizer (PretrainedTokenizer): the pretrained tokenizer
            tokenizer_wrapper_class (TokenizerWrapper): the class of tokenizer wrapper
            max_seq_length (int, optional): the max sequence length of the input ids. It's used to truncate sentences. Defaults to 256.
            decoder_max_length (int, optional): the decoder maximum length of an encoder-decoder model. Defaults to 256.
            shuffle (bool, optional): defaults to False.
            batch_size (int, optional): the batch_size of data loader. Defaults to 32.
            teacher_forcing (bool, optional): whether to fill the mask with target text. Set to True in training generation model.. Defaults to False.
            predict_eos_token (bool, optional): whether to predict the <eos> token. Suggest to set to True in generation. Defaults to True.
            truncate_method (str, optional): the truncate method to use. select from `head`, `tail`, `balanced`. Defaults to "head".

        Returns:
            train_dataloader: OpenPrompt data loader for the train dataset
            val_dataloader: OpenPrompt data loader for the validation dataset
            test_dataloader: OpenPrompt data loader for the test dataset
        """
        train_dataloader = PromptDataLoader(
            dataset=data_dict["train"],
            template=template,
            tokenizer=tokenizer,
            tokenizer_wrapper_class=tokenizer_wrapper_class,
            max_seq_length=max_seq_length,
            decoder_max_length=decoder_max_length,
            batch_size=batch_size,
            shuffle=True,
            teacher_forcing=True,
            predict_eos_token=predict_eos_token,  # be sure to pass predict_eos_token=True if your template doesn't contain one, or you model may fail to stop generation.
            truncate_method=truncate_method,
        )

        validation_dataloader = PromptDataLoader(
            dataset=data_dict["validation"],
            template=template,
            tokenizer=tokenizer,
            tokenizer_wrapper_class=tokenizer_wrapper_class,
            max_seq_length=max_seq_length,
            decoder_max_length=decoder_max_length,
            batch_size=batch_size,
            shuffle=False,
            teacher_forcing=False,
            predict_eos_token=predict_eos_token,
            truncate_method=truncate_method,
        )

        test_dataloader = PromptDataLoader(
            dataset=data_dict["test"],
            template=template,
            tokenizer=tokenizer,
            tokenizer_wrapper_class=tokenizer_wrapper_class,
            max_seq_length=max_seq_length,
            decoder_max_length=decoder_max_length,
            batch_size=batch_size,
            shuffle=False,
            teacher_forcing=False,
            predict_eos_token=predict_eos_token,
            truncate_method=truncate_method,
        )

        return train_dataloader, validation_dataloader, test_dataloader


if __name__ == "__main__":
    data_fp = os.path.join(
        PRJ_ROOT_STR, "data", "All-2479-Answers-retrieved-from-MedQuAD.csv"
    )
    data_classes_fp = os.path.join(
        PRJ_ROOT_STR,
        "data",
        "All-qrels_LiveQAMed2017-TestQuestions_2479_Judged-Answers.txt",
    )

    dp = pipeline.DataPipeline(data_fp, data_classes_fp)
    data_df = dp.read_and_clean_data(id_col_data="AnswerID", id_col_data_classes="id")
    data_dict = dp.split_data_into_dictionary(data_df)

    op = OpenPromptPipeline("gpt2", "healx/gpt-2-pubmed-medium")
    plm, tokenizer, model_config, WrapperClass = op.load_model()
    _logger.info(f"Loaded model: {plm.name_or_path}")

    template_text = (
        'Question: {"placeholder":"text_a", "shortenable": "True"} Answer: {"mask"}'
    )

    template = ManualTemplate(tokenizer=tokenizer, text=template_text)
    wrapped_example = template.wrap_one_example(data_dict["train"][0])

    # _logger.info(
    #     f"Example wrapped in template: {wrapped_example}"
    # )

    wrapped_tokenizer = WrapperClass(
        max_seq_length=1024,
        decoder_max_length=1024,
        tokenizer=tokenizer,
        truncate_method="tail",
    )
    _logger.info(f"Initialized tokenizer!")

    tokenized_example = wrapped_tokenizer.tokenize_one_example(
        wrapped_example, teacher_forcing=False
    )

    train_dataloader, validation_dataloader, test_dataloader = op.generate_data_loaders(
        data_dict=data_dict,
        template=template,
        tokenizer=tokenizer,
        tokenizer_wrapper_class=WrapperClass,
        max_seq_length=1024,
        decoder_max_length=1024,
        batch_size=4,
        truncate_method="tail",
    )
    _logger.info(f"Generated PromptDataLoader objects!")

    prompt_model = PromptForGeneration(
        plm=plm, template=template, freeze_plm=True, tokenizer=tokenizer
    )
