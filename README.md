This is a windows automation program built using: 
- pywebview for GUI
- pyautogui for image based screen recognition (by the help of Pillow for image processing and PyScreeze for screenshot handling)
- global_hotkeys for hotkey detection
- pyperclip for hotkey triggering
- PyInstaller for creating windows EXE application

The program is avaliable on https://routineprograms.com for download as well as some images showcasing the programs capabilites.

Click Routine lets the user create different types of automation tasks called "sequences". Sequences can be chained together and trigger each other based on if the run was successful or not.
The purpose here is to create a human like automation behavior, where the program will scan the screen for user specified images, and type/button press like a human would, but only a little faster.

This program was created to help automate daily repetative tasks of older applications that are lacking APIs, therefore image bases screen recognition is used with good capabilites to configure the image processing. 
Another reason was to give non technical users powerful capabilities to easily create their own automations without having to use any programming.

The code is sadly a bit messy to read, could be improved by using some refractoring and modularization. But the application is fully working and reliable.

An installer is avaliable on https://routineprograms.com but if you want to build the exe yourself, then do as follow:

Go to the venv, type: _pyinstaller main.py --noconsole --name "Click Routine" --icon="ClickRoutine.ico"_

Manually copy: "assets" and all html+js files to output "dist" folder

Ta-da... Run the program via the newly created exe


