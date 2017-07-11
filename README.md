# GENSET Demo Site

[![Build Status](https://img.shields.io/travis/cheukyin699/genset-demo-site.svg)](https://travis-ci.org/cheukyin699/genset-demo-site)
[![Codacy Badge](https://img.shields.io/codacy/grade/feac75edbe5241eaa206de597efb38ef.svg)](https://www.codacy.com/app/chucksys88/genset-demo-site?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cheukyin699/genset-demo-site&amp;utm_campaign=Badge_Grade)

This is the code for the GENSET website, for demonstrating the GENSET project.

## Installation and Configuration

More detailed instructions are on the [site wiki][install+config].

```bash
virtualenv -p python3.5 venv
. venv/bin/activate

pip install numpy
pip install -r requirements.txt

# Copying config files
cp test_config.py config.py
cp sample_env .env

# Remember to edit `config.py` and `.env`!
vim config.py .env -p

# For heroku
heroku local

# For python
. .env
python run.py
```

[install+config]: https://github.com/cheukyin699/genset-demo-site/wiki/Installation-and-Configuration