# Canvas Scripts
![Compile python to binary](https://github.com/burturt/canvas-scripts/workflows/Compile%20python%20to%20binary/badge.svg)

Warning: this software comes with no guarentees or warranty. See https://github.com/burturt/canvas-scripts/blob/master/LICENSE for more information.

Binaries for this program are automatically built. You can find them in the Actions tab or in releases. Downloading them from Actions requires a github account.

## canvasGrades
Simple script that gets all grades from a canvas api key. Intended for students to get their own grade in all classes.

## Run from binary (recommended):
1. Download the appropriate file from https://github.com/burturt/canvas-scripts/releases/latest and unzip it. Don't download the Source Code, download the canvasGrades-Linux/MacOS/Windows.zip file.
2. Run the program:
- Windows: Double-click on the .exe file
- MacOS: right-click --> open on the file
- Ubuntu: Open a terminal, navigate to where the binary is located, then run `./canvasGrades`

### Run manually:

To run:
1. Download and install python 3 (not 2!) https://www.python.org/downloads/
2. Download and install pip (https://pip.pypa.io/en/stable/installing/)
3. Download or git clone the script
4. `pip[3] install -r requirements.txt [--user]` Try the command with or without each [] until one works. Use sudo on linux (`sudo pip...`), on windows open a command prompt as admin.
5. `python3 SCRIPT_NAME`

### How to get API token:
1. Log into Canvas
2. Click Account.
3. Click Settings.
4. Click New Access Token.
5. Choose expiration date (*highly* recommended but not required)
6. Give name
7. Create!
