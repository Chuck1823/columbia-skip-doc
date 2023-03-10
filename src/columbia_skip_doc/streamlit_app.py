"""
Streamlit main script
"""

import argparse
import logging
import sys

import streamlit as st
import datapipeline as dp

from utils import setup_logging
from streamlit_chat import message

__author__ = "Charles Antoine Malenfant & Lance Norman"
__copyright__ = "Charles Antoine Malenfant & Lance Norman"
__license__ = "MIT"

CLASS_NAME = __name__


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Streamlit app launch")

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)

# Get user input


def get_input():
    #input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    input_text = st.text_input("Patient (You)", key="input")
    return input_text


def chat_setup():

    # title
    st.title("Skip-DOC")

    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []


def main(args):
    """Wrapper allowing 

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    _logger = setup_logging(logging.DEBUG, CLASS_NAME)

    chat_setup()
    user_input = get_input()
    if user_input:
        output = user_input
        # store the output
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    # TO DO - get better avatars
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i],
                    avatar_style="fun-emoji", key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
