# GENSET Demo Site

[![Build Status](https://img.shields.io/travis/cheukyin699/genset-demo-site/api_overlord.svg)](https://travis-ci.org/cheukyin699/genset-demo-site)
[![Codacy Badge](https://img.shields.io/codacy/grade/feac75edbe5241eaa206de597efb38ef/api_overlord.svg)](https://www.codacy.com/app/chucksys88/genset-demo-site?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cheukyin699/genset-demo-site&amp;utm_campaign=Badge_Grade)

This is the code for the GENSET website, for demonstrating the GENSET project.

## Pre-requisites

- python>=3.5
- virtualenv
- jdk>=1.7

## Installation

Since the website scripts require `python-weka-wrapper3`, `python3` must be
installed. Installation should be straightforward, but because for some reason,
`javabridge` doesn't install correctly if you haven't got `numpy` installed
already. This is why, before you do the standard:

```sh
pip install -r requirements.txt
```

You should first do:

```sh
pip install numpy
```

Thus, to install everything necessary, you must run:

```sh
# Set up virtual environment (with python 3.5 or higher)
virtualenv -p python3.5 venv
. venv/bin/activate

# Install packages for the scripts
pip install numpy

# Install the rest of the Flask packages
pip install -r requirements.txt
```

## Running

To run the server, you can either use `heroku`, or `python`:

```sh
# Heroku
heroku local
# Python
python run.py
```

### Heroku

To use heroku locally, you will need an environment to run `heroku` in.

```sh
G_CAPTCHA_SITEKEY='SOME SITEKEY'
G_CAPTCHA_SECRET='SOME SECRET'

API_KEY='SOME KEY'
```

Put the above into `.env` in the root directory. For more variables, consult
the accompanying `sample_env`. Remember that the file will be parsed with
`bash`; comments start with `#`.

### Python

To run the server with python, you will need to configure your `config.py` file.
Note that, since saving api keys onto file is pretty unsafe, you are encouraged
to use environmental variables, and refer to them with `os.environ.get`
function. A config file for testing is provided, in order for you to copy it.
Currently, the project is set up such that, it tries to find the `config.py`
file first, and only when it fails will it try to find `test_config.py`. In
other words, `config.py` takes priority over `test_config.py`.

```sh
# Copy and edit config file
cp test_config.py config.py
${EDITOR} config.py
```

Of course, you are fully able to run the site without custom configuration, but
you are unable to run the database part of the website, namely `firebase`.
