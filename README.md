# Question Fetcher

Because I'm really lazy and don't want to login EVERY SINGLE TIME when I want to solve questions so I wrote this

## Setup

### Windows (or your Unix-like system has pyenv setup)

If you want to create a virtual environment run these commands, if not, skip this step

`python -m venv env`

`env/Scripts/activate`

To install required dependencies run this command

`pip install -r requirements.txt`

### Unix-like systems

Basically the same but change `python` to `python3` and run `source env/bin/activate` instead

## Execution

Run `python get.py <question_number>`

### Unix-like systems

You can run `chmod +x get.py` and use it as `./get.py <question_number>`

> If you get warnings don't worry (or you should?) because to certificate is self-signed and I manually turned off the verification