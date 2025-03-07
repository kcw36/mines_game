## Installing the Game
Inside the destination directory for the project run
```bash
git clone https://github.com/kcw36/mines_game.git
```
This project requires python3 with Tkinter for the graphical interface

### Mac
This project can be installed using homebrew:
- In your terminal run `brew list`
- If homebrew is not installed, in terminal run 
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- Repeat the command from step 1 you should now see a version number for homebrew

- check your system for the other dependencies run the following in your terminal
```bash
python --version
brew list
```
- if python is not installed run `brew install python@3.12`
- then add python to your .zsh path by opening your profile with ` open -e ~/.zprofile` and add this line to the end of the file `export PATH=/opt/homebrew/opt/python@3.12/libexec/bin/:$PATH`
- check python is configured correctly by running `python --version` the response should be a version of 3.12.XX
- if not double check homebrew installation path for python with `brew info python@3.12` add the installation path from their into your .zsh profile
- install tkinter with homebrew: `brew install python-tk@3.12`

### Windows
- Tkinter is installed as default on windows systems so all that is required is Python itself
- to install python go to <a href>https://www.python.org/downloads/windows/</a>
- during installation you can add python to PATH to check that works in your terminal run `python --version`
- if python is not found add it to your path using this tutorial <a href>https://www.liquidweb.com/help-docs/adding-python-path-to-windows-10-or-11-path-environment-variable/</a>

##  Running the Mine Game
Inside the project folder in your terminal run the following command:
```bash
python main.py
```