# Question Fetcher

Because I'm really lazy and don't want to login EVERY SINGLE TIME when I want to solve questions so I wrote this

## Setup

### Windows

If you want to create a virtual environment run these commands, if not, skip this step

`python -m venv env`

`env/Scripts/activate`

To install required dependencies run this command

`pip install -r requirements.txt`

Finally to setup some config run

`python setup.py`

> If you typed the wrong info just <kbd>Ctrl</kbd> + <kbd>C</kbd> to quit, it won't wipe previous data unless you're finished entering these info

### Unix-like systems

Linux system are recommended to create virtual environments (either through venv or virtualenv) to avoid dependency conflicts (idk about mac tho)

After creating a virtual environment, you can run `python` as normal

---

## Commands

### Get Question

`python get.py <question_number>`

This command grabs questions and prints to the console, if you want to make it output to a text file, you could use `python get.py <question_number> > file.txt` for now. I will probably add a `-o` flag later on.

### Submit File

`python submit.py <question_number> <selected_file>.py`

This command submits the selected file to the system.

> You could probably hook this up with unit testing but currently I'm not planning to implement this feature, if you want to contribute please read [CONTRIBUTING.md](./CONTRIBUTING.md)

---

### Unix-like systems

You can run

`chmod +x get.py`

and use it as

`./get.py <question_number>`
