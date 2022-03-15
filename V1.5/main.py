"""
    Created by @Wallee#8314
    Thanks to @Bigjango/FG6 for helping with the getImport method and small bits of code :p
    This program will play any inputed text it is provided.
"""

# Imports
from sys import argv
import os

# Define a method to get a function from am module
def getMed(module, toImport):

        # If toImport equal None
        if toImport == None:
            met = __import__(module)

        # If toImport isn't equal None, or a function is to be imported
        else:
            met = getattr(__import__(module), toImport)

        # Return the module/function
        return(met)

# Define a method to import/install modules that may not be on the user's system
def getImport(moduleName, pip, module, toImport=None):

    # Try to import
    try:

        # Use the getMed function to import a module or method
        met = getMed(module, toImport)
        return(met)

    # Boss music
    except:

        # Define a user input variable
        userInput = ""

        # Loop until the user gives a currect answear
        while not userInput.lower() in ["y", "yes", "n", "no"]:
            userInput = input("The " + moduleName + " module is not installed, may I install it for you? [YES/no] ")

        # If the user answears yes
        if userInput.lower() in ["y", "yes"]:

            # "Try" to import the module
            try:
                os.system("pip3 install " + pip)
                met = getMed(module, None)
                return(met)

            # In case there is no internet of the module cannot be found/imported
            except Exception as error:
                print(error)
                exit()
        else:
            return(None)

# Check if there are any system arguments
if len(argv) < 2:
    # Import modules that may not be on the user's system
    gTTS = getImport("Google Text To Speech", "gtts", "gtts", toImport="gTTS")
    playsound = getImport("Playsound", "playsound", "playsound", toImport="playsound")
    sg = getImport("PySimpleGUI", "pysimplegui", "PySimpleGUI")

# Else the user may be trying to use a system argument
else:
    sg = ""
    try:
        gTTS = getImport("Google Text To Speech", "gtts", "gtts", toImport="gTTS")
        playsound = getImport("Playsound", "playsound", "playsound", toImport="playsound")
    except:
        pass

# Check if the modules are imported
if gTTS == None or playsound == None:

    # Tell the user what modules they need to isntall
    print("\nI am sorry, I cannot speek unless you have installed the following modules")
    print("\ngtts (Google Text To Speech)")
    print("playsound (Audio Player)\n")

    # Check if sg is also None
    if sg == None:

        # Tell the using they are also missing the PySimpleGUI module
        print("Additionally you are missing the PySimpleGUI module\nYou will only be able to use arguments to tell me what to say/read without it\nType \"python3 main.py -help\" for more info")

    # Exit the program
    exit()

# Check if sg is the only module missing
elif sg == None:
    print("You are missing the PySimpleGUI module, I am unable to give you a graphical interface to interact with me\nType \"python3 TTs_GUI.py -help\" for more info")
    exit()
# Open logs file so there can be history
with open("logs.txt", "r") as file:
    lines = file.readlines()

# Convert lines into a list called newLines
newLines = []
for line in lines:
    newLines.append(line.replace("\n", " "))

# Define a method to say stuff
def say(text: str):

    # Check if text is an empty line when stripped of \n and spaces
    if not text.replace("\n", "").replace(" ", "") == "":

        #Something can always go wrong when dealing with user input
        try:

            # Create the audio and store it in a temp file which is deleted once it is played
            voice = gTTS(text=text, lang="en")
            voice.save("temp.mp4")
            playsound("temp.mp4")
            os.system("rm temp.mp4")
        except Exception as error:

            # I hope this isn't ever used
            try:
                sg.Popup("Oops, something went wrong:\n" + error)

            # This may be due to sg not being installed
            except:
                pass

# Define a first time method
def firstTime(lines):

    # Ask the user if they want to listen to an auditorial explination of how to use this program
    userInput = ""
    while not userInput.lower() in ["yes", "y", "no", "n"]:
        userInput = input("Do you want to listen to an auditorial explination on using this program? [YES/no] ")

    # Check if the answear is yes
    if userInput.lower() in ["yes", "y"]:

        # Define a newLines variable
        newLines = "False\n"

        # Loop through the lines and say each one, also convert lines into a string
        for line in lines:
            say(line)
            newLines = newLines + line

        # Mark the file as read
        with open(".assets/first_time.txt", "w") as file:
            file.writelines(newLines)

# Open the first time file
with open(".assets/first_time.txt", "r") as file:
    lines = file.readlines()

# Check if the first line is equal to True
if lines[0].replace("\n", "") == "True":
    firstTime(lines[1:])

# argv stuffs
if len(argv) > 1:

    # -say argument
    if argv[1] == "-say":

        # Check if there is anything to say
        if len(argv) > 2:

            # Define words
            words = ""

            # Loop through each word past the second one in argv and append add it to words
            for word in range(len(argv)-2):
                words = words + argv[word+2]

            # Say words
            say(words)

        # Tell the user that they must give some more arguments
        else:
            say("You didn't give me anything to say, now I am sad")

    # -read argument
    elif argv[1] == "-read":

        # Check if the user has giving a file
        if len(argv) > 2:

            # Define fileName
            fileName = ""

            # Loop through each word after -read to get the file name
            for word in range(len(argv)-2):
                fileName = fileName + argv[word+2]

            # USER INPUTED DATA!
            try:

                # "Attemped" to open the file and read it's lines
                with open(fileName, "r") as file:
                    lines = file.readlines()

                # Loop through each line and say it
                for line in lines:
                    say(line)

            # Tell the user the inputed data caused an error
            except:
                say("I am sorry, I cannot read you that file")

        # Tell the user they need to give a file path
        else:
            say("You need to give a file for me to read from")

    # -how-to
    elif argv[1] == "-how-to":

        # Doesn't need to re-open the file
        firstTime(lines[1:])

    # -help argument
    elif argv[1] == "-help":

        # Define a user input variable
        userInput = ""

        # Wait to get a valid responce from the user, BTW never forget to add () to the str.lower method, pain ;-;
        while not userInput.lower() in ["y", "yes", "n", "no"]:

            # Module may not be installed
            try:
                say("I am calling out to you")
                userInput = input("Did you hear what I just said? [yes/no] ")

            # Audo no if say fails
            except:
                print("\nFailed to call out")
                userInput = "no"

        # If the user said yes
        if userInput.lower() in ["y", "yes"]:

            # Print a lot of stuffs
            print("\n-say (words)")
            print("-read (file)")
            print("-how-to (plays an MP3 file)")
            print("-help (shows this)\n")

            # Make a joke :p
            say("That is good, I am very glad you heard me. Here are some instructions")

        # Oh no, no sound!
        else:

            # Print even more stuffs
            print("\nOh no, I am mute!\n")
            print("Here are some trouble shooting instructions\n")
            print("Sound on?\nTest it by typing VLC or MPV and enter to launch VLC media player or MPV\n")
            print("Modules not found?\nTry using pip or pip3 to install them or let me auto install them when I ask\n")
            print("Something else?\nDM my creator Wallee, on Discord or Reddit\nWarning, Wallee rarely checks reddit\n\nDiscord: Wallee#8314\nReddit: https://www.reddit.com/user/Wallee_pi\n")

            # Define a user input variable, again
            userInput = input("... ")

            # If the user input is either VLC or MPV then play .assets/audio_test.mp3
            if userInput.lower() in ["vlc", "mpv"]:

                # Attemt to play the track
                try:
                    os.system(userInput.lower() + " .assets/" + userInput.lower() + "_audio_test.mp3")
                    print("I hope it was just your volume :)")

                #
                except:
                    print("I am sorry, I could not run " + userInput.upper() + "or find the file to play")

    # Inproper argument
    else:
        say(f'"{argv[1]}" is not a proper argument. Try dash help for a list of usefull tools')

    # Exit the program
    exit()

# The left side of the window
layout_left = [
    [
        sg.In(size=(32, 32), enable_events=True, key="-TEXT-"),
        sg.Button("Speak")
    ],
    [sg.Text("History")],
    [sg.Listbox(values=newLines, key="-HISTORY-", size=(42, 18), enable_events=True)],
    [
        sg.Button("Save as mp3"),
        sg.Button("Remove"),
        sg.Button("Save as script")
    ]
]

# The right side of the window
layout_right = [
    [
        sg.FileBrowse("Browse", enable_events=True),
    ],
    [sg.Listbox(values=[], enable_events=True, key="-FILE-", size=(46, 17))],
    [
        sg.Button("Save this line"),
        sg.Button("Save by line"),
        sg.Button("Save as one")
    ],
    [
        sg.Button("This line"),
        sg.Button("By line"),
        sg.Button("All lines"),
        sg.Button("About")
    ]
]

# The window
layout = [
    [
        sg.Column(layout_left),
        sg.VSeparator(),
        sg.Column(layout_right)
    ]
]

# Create the fortold window
window = sg.Window(title="Wallee's TTs", layout=layout, size=(720, 420))

# Repeat until forever
while True:

    # Get window evenrs and values
    event, values = window.read()

    # Check if the user clicked the close window button
    if event == sg.WIN_CLOSED:
        exit()

    # Speak button
    elif event == "Speak" and not values["-TEXT-"] == "":

        # Open the logs file
        with open("logs.txt", "r") as file:
            lines = file.readlines()

        # Remove any line that is the same as the inputed text
        for lineNo, line in enumerate(lines, 0):
            if line.replace("\n", "") == values["-TEXT-"]:
                lines.pop(lineNo)

        # Creat a new lines variale, why do I have to comment everything? ¯\_(ツ)_/¯
        newLines = []

        # Loop through lines
        for line in lines:

            # Append the current line to newLines making sure to remove any \n
            newLines.append(line.replace("\n", ""))

        # Adds the inputed text to newLines
        newLines.reverse()
        newLines.append(values["-TEXT-"])
        newLines.reverse()

        # Update the history section with the new lines
        window["-HISTORY-"].update(newLines)

        # Create a writeliens variable
        writeLines = ""

        # Loop through newLines and add each line to writeLines
        for line in newLines:
            writeLines = writeLines + line.replace("\n", "") + "\n"

        # Remove the last \n to prevent future reading errors
        writeLines = writeLines[:-1]

        # Write new lines to the logs file
        with open("logs.txt", "w") as file:
            file.writelines(writeLines)

        # Say the inputted text
        say(values["-TEXT-"])

    # Checks if history is empty and if not changes the text to whatever the user has clicked
    elif event == "-HISTORY-" and not values["-HISTORY-"] == []:
        window["-TEXT-"].update(str(values["-HISTORY-"][0]))

    # Browse for a file to read from
    elif event == "Browse":

        # Checks if the user has selected a file or not
        if not values["Browse"] == "":

            # Open the selected file
            with open(values["Browse"], "r") as file:
                lines = file.readlines()

            # Define newLines variable
            newLines = []

            # Loop through lines and replave \n with nothing
            for line in lines:
                if not line == "\n":
                    newLines.append(line.replace("\n", ""))

            # Update the right listbox to contain the selected file's lines
            window["-FILE-"].update(newLines)

    # Saves the selected file as a .mp3
    elif event == "Save as mp3" and not values["-HISTORY-"] == []:

        # Check if history is populated with stuffs and saves the file if it is
        if not values["-HISTORY-"] == "":

            # Get the directory the user wants to save the file to
            directory = sg.PopupGetFolder("Saving as \"" + values["-HISTORY-"][0] + ".mp3\"", "Save as mp3", default_path=os.getcwd() + "/My MP3s")

            # Check if the directory is not None
            if not directory == None:

                # Add a / to the end of directory if it does not have one
                if not directory.endswith("/"):
                    directory = directory + "/"

                # I smell danger
                try:

                    # Convert and save the text
                    voice = gTTS(text=values["-HISTORY-"][0])
                    voice.save(directory + values["-HISTORY-"][0] + ".mp3")

                # This isn't helpful
                except:
                    sg.PopupError(Title="Oops")

    # Removes an item from history, seems to have trouble removing the first item if there is more than one
    elif event == "Remove" and not values["-HISTORY-"] == []:

        # Open the logs file and read it's lines
        with open("logs.txt", "r") as file:
            lines = file.readlines()

        # Define newLines and writeLines
        newLines = []
        writeLines = ""

        # Loop through lines
        for line in lines:

            # Check if not line is the same as the selected line in history
            if not line.replace("\n", "") == values["-HISTORY-"][0]:
                newLines.append(line.replace("\n", ""))
                writeLines = writeLines + line.replace("\n", "") + "\n"

        # Remove unwanted \n from writeLines
        writeLines = writeLines[:-1]

        # Update history
        window["-HISTORY-"].update(newLines)

        # Write the updated writeLines to the logs file
        with open("logs.txt", "w") as file:
            file.writelines(newLines)

    # Save the current logs file but under a different name, I should make the button into a folder selector
    elif event == "Save as script":

        # Get the directory that the user wants to save the script to
        directory = sg.PopupGetFolder("Save to...", "Save as script", default_path=os.getcwd() + "/My Scripts")

        # Check if the user didn't select a directory
        if not directory == None and os.path.exists(directory):

            # Add a / to the end of directory if it does not have one
            if not directory.endswith("/"):
                directory = directory + "/"

            # Am I the only one who doesn't trust both the user and myself when giving data to a program?
            try:

                # Read from the logs file
                with open("logs.txt", "r") as file:
                    lines = file.readlines()

                # Define newLines
                newLines = ""

                # Loop through lines
                for line in lines:
                    newLines = newLines + line

                # Get the number of scripts in the My Scripts directory
                numberOfScripts = 1
                while os.path.exists("My Scripts/script_" + str(numberOfScripts) + ".txt"):
                    numberOfScripts += 1

                # Write the exact data that is in the logs file but to another file, this will be updated -_-
                with open(directory + "script_" + str(numberOfScripts) + ".txt", "w") as file:
                    file.writelines(newLines)

            # Tell the user that there was an error
            except:
                sg.Popup("Error while trying\nto opne the file")

        # Tell the user that the directory does not exist
        else:
            sg.Popup("Couldn't open file or directory, does not exist")
    # Say the currently selected line in the right side of the window
    elif event == "This line" and not values["-FILE-"] == []:

        # Wait, an entire button in just 2 lines? NO, I MUST MAKE IT LONGER WITH COMMENTS!
        say(values["-FILE-"][0])

    # Read from the selected file line by line
    elif event == "By line" and not values["Browse"] == "":

        # Open the selected file
        with open(values["Browse"], "r") as file:
            lines = file.readlines()

        # Loop through the lines
        for line in lines:
            text = line.replace("\n", "")

            # USER PROVIDED DATA, AHHHHHH!
            try:
                say(text)
            except:
                pass

    # Say all the lines by creating one big mp3 file, this'll take a while on slow internet ;-;
    elif event == "All lines" and not values["Browse"] == "":

        # Tell the user this may take a while
        sg.Popup("This may take a while :p")

        # Open the selected file
        with open(values["Browse"], "r") as file:
            line = file.readlines

        # Loop through the lines
        for line in lines:

            # Oh no 0_0
            try:
                say(line)
            except:
                pass

    # Save a single line from the file
    elif event == "Save this line" and not values["-FILE-"] == []:

        # Create the audio
        text = values["-FILE-"][0]
        audio = gTTS(text=text, lang="en")

        # Define newName
        newName = ""

        # Loop through each character in text and check if it is a character that would cause an error
        for char in text:
            if char in "QWERTYUIOPSDFGHJKLZXCVBNM123456890#%^-_=+qwertyuiopasdfghjklzxcvbnm~!@&*()}{[]:;'\",<.>/? ":
                newName = newName + char

        # I am too lazy to check if the audio can be converted so I will just use a try and except statement
        try:
            audio = gTTS(text=newName, lang="en")
            audio.save("My Audio Documents/" + newName + ".mp3")

            # Tell the user the file has been saved
            sg.Popup("Done\nSaved in My Audio Documents")
        except:
            pass

    # Save the audio line by line
    elif event == "Save by line" and not values["Browse"] == "":

        # Open the current file and read it's lines
        with open(values["Browse"], "r") as file:
            lines = file.readlines()

        # Make a path variable
        path = values["Browse"]
        if path.endswith("/"):
            path = path[:-1]

        # Split path with / and assing the last index to path
        path = path.split("/")[-1]

        # Check if the folder already exists
        if not os.path.exists("My Audio Documents/" + path):
            os.mkdir("My Audio Documents/" + path)

            # USER DATA!!!!
            try:
                # Loop through the lines
                for lineNo, line in enumerate(lines, 0):

                    # Define newName
                    newName = ""

                    # Loop through the characters
                    for char in line:

                        # Check if the character is in that really long string
                        if char in "QWERTYUIOPSDFGHJKLZXCVBNM123456890#%^-_=+qwertyuiopasdfghjklzxcvbnm`~!@&*()}{[]:;'\",<>/? ":
                            newName = newName + char

                    # Try and except statements are good, converts the text into audio and saves it
                    try:
                        audio = gTTS(text=newName, lang="en")
                        audio.save("My Audio Documents/" + path + "/" + str(lineNo) + "_" + newName + ".mp3")

                    # Prob a blank line, I hope ~_~
                    except:
                        pass

                # Tell the user the file has been saved
                sg.Popup("Done\nSaved to My Audio Documents/" + path)

            # Tell the user something went wrong
            except:
                sg.Popup("Something went wrong\nCould not open folder")

        # Tell the user that the project already exists
        else:
            sg.Popup("That project already exists")

    # Save the currently selected file as one big mp3
    elif event == "Save as one" and not values["Browse"] == "":

        # Warn the user that this may take sometime and get a file name
        fileName = sg.PopupGetText("Warning, This may take a while if the text file is large\n\nFile name?", "File name")

        # Make sure file name isn't either blank or is None
        if not fileName == "" and not fileName == None:

            # Open the selected file
            with open(values["Browse"], "r") as file:
                lines =  file.readlines()

            # Define newLines
            newLines = ""

            # Loop through lines
            for line in lines:
                newLines = newLines + line

            # These statements are really handy, convert the text to audio and save it
            try:
                audio = gTTS(text=newLines, lang="en")
                audio.save("My Audio Documents/" + fileName + ".mp3")

                # Tell the user that the program didn't crash
                sg.Popup("File is done!")
            except Exception as error:

                # This will most likely be a network error, I hope
                sg.Popup("Oops, an error :(\n" + str(error))

    # About this program
    elif event == "About":
        sg.Popup("""Wallee's TTs:
This program uses the gTTS module
to speak anything you want!
It can either read inputed words
or read from a text file.
For a video on how to use it go to:
https://youtu.be/Yl2_DEX3MGI
""")
