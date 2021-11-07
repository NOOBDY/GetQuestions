# Question Fetcher

Because I'm really lazy and don't want to login EVERY SINGLE TIME when I want to solve questions so I wrote this

## Installation

For Windows and Linux system users, there are now compiled binaries available!

Now you won't be needing to download lots of files and trigger Git!

Download the files based on your system from the Release tab on the right, unpack them into your desired folder and start using.

## Usage

### Windows

#### Setup

`setup.exe`

Run this script and enter your credentials to create config files. You need to run this script first or the program won't run.

#### Get Question

`get.exe <question_number>`

This command grabs questions and prints to the console, if you want to make it output to a text file, you could use `python get.py <question_number> > file.txt` for now. I will probably add a `-o` flag later on.

#### Submit File

`submit.exe <question_number> <selected_file>.py`

This command submits the selected file to the system.

> You could probably hook this up with unit testing but currently I'm not planning to implement this feature, if you want to contribute please read [CONTRIBUTING.md](./CONTRIBUTING.md)

### Linux

Change `<command>.exe <args>` to `./<command> <args>` and you are good to go.

e.g. `./get 24`

> Remember to specify the "`./`" unless you add it to PATH

### MacOS

I'm not sure whether Linux binaries will run or not. If not, you will have to either use `pyinstaller` or run Python scripts directly from the source code.
