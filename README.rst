.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/columbia-skip-doc.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/columbia-skip-doc
    .. image:: https://readthedocs.org/projects/columbia-skip-doc/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://columbia-skip-doc.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/columbia-skip-doc/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/columbia-skip-doc
    .. image:: https://img.shields.io/pypi/v/columbia-skip-doc.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/columbia-skip-doc/
    .. image:: https://img.shields.io/conda/vn/conda-forge/columbia-skip-doc.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/columbia-skip-doc
    .. image:: https://pepy.tech/badge/columbia-skip-doc/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/columbia-skip-doc
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/columbia-skip-doc

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=================
columbia-skip-doc
=================

## Setup instructions

The repo contains a file called conda_environment_py39.yaml that can be used to create a conda environment with all the necessary
dependencies to run the code. The environment can be created by running the following command:

$ conda env create -f conda_environment_py39.yaml

This Anaconda environment uses Python 3.9.16. Depending on your conda version, activate the environment by running:

$ conda activate columbia-skip-doc

Note: the yaml file containing the environment assumes a Anaconda installation at a standard location: 

$ /usr/local/anaconda3

If your Anaconda installation is not at this location, please modify the yaml file accordingly in order to generate the environment.
However, please do not commit that change to the repo.

With the activated environment, you should be able to run Streamlit by running the following command:

$ streamlit hello

This will open a tab in your browser to give you an idea of Streamlit. Once you're familiarized, you can run the app by running:

$ streamlit run streamlit_app.py

Note: this needs to happen from the $project_root/src/columbia_skip_doc/ directory.

This effectively runs the Python script which for now only sets up a logger, has wrapper functions and takes a few optional command
line argument. Let's follow the standard trunk-based development for branching with a develop and main branch (golden copy). See
"Trunk-based development" in https://www.flagship.io/git-branching-strategies/ for more details.

<A longer description of your project goes here...>

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
