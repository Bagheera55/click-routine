""" Click Routine 2022-12-04

This program lets the user create different types of automation tasks called "sequences". Sequences can be chained together and trigger each other based on if the run was successful or not.
The purpose here is to create a human like automation behavior, where the program will scan the screen for user specified images, and type/button press like a human would, but only a little faster.

Good to knows:
site-package pyscreeze is modified slightly to support multiple monitors using fix in https://github.com/asweigart/pyautogui/issues/321
site-package pyautogui is modified to alert on failsafe, and terminate the program

Bugs:
Seq table sometimes not refreshing when creating new sequence - 2023 09 10 unable to reproduce
After opening a sequence action and pressing accept, highlighted icon will flash for 1 second.

Windows deploy guide:
Go to terminal, type: pyinstaller main.py --noconsole --name "Click Routine" --icon="ClickRoutine.ico"
Copy: "assets" and all html+js files to output "dist" folder


"""
import sys
import os
import json
import webview
import pyautogui
import screenCapture
import screenClickPosition
import time
import global_hotkeys
import re
import base64
import pyperclip

class Api:

    def __init__(self):
        self.cancel_heavy_stuff_flag = False
        self.currentEditingSeqLoc = None
        self.currentJsonSeqCache = None
        self.currentJsonSetCache = None
        self.seqWindow = None
        self.keyboardHotkeys()
        self.currentSeqName = None
        self.programStartTime = int(time.time())
        self.seqRunList = []
        self.lastOpenSeq = self.programStartTime

        self.store1 = ""
        self.store2 = ""
        self.store3 = ""

        # create AppData folder if it doesn't exist
        self.working_path = os.environ['APPDATA'] + "\\ClickRoutine\\"
        if not os.path.exists(self.working_path):
            os.makedirs(self.working_path)
            os.makedirs(self.working_path + "\\exports")
            os.makedirs(self.working_path + "\\sequences")
            os.makedirs(self.working_path + "\\captures")

    def screenCapture(self):
        self.seqWindow.hide()
        location = screenCapture.main()
        self.seqWindow.show()
        response = {
            'location': location
        }
        return response

    def screenPosition(self):
        self.seqWindow.hide()
        xyPos = screenClickPosition.main()
        self.seqWindow.show()
        response = {
            'clickXyPos': xyPos
        }
        return response

    def getJsonLoaded(self):
        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache
        }
        return response

    def newSequence(self, seqName):
        def on_closed():
            self.seqWindow = None

        fullFileName = self.working_path + "\\sequences\\" + seqName + ".seq"
        if os.path.isfile(fullFileName):
            response = {
                'message': 'A file with that name already exists.\r\nPlease try another name.'
            }
            return response

        # file with chosen name does not exist yet, now create it.
        self.currentSeqName = seqName
        self.currentJsonSeqCache = None
        self.currentJsonSetCache = {'typingSpeed': 60, 'timeout': None}

        jsonDefault = {
            "sequence": [],
            "settings": {
                "typingSpeed": 60,
                "timeout": None
            },
            "interaction": {
                "seqEnabled": False,
                "sequenceName": self.currentSeqName,
                "trigger": None,
                "outcome": None
            }
        }

        with open(fullFileName, 'w') as f:
            json.dump(jsonDefault, f, indent=4)
        f.close()

        self.currentEditingSeqLoc = os.path.normpath(fullFileName)
        self.initRunLoop() # restart run loop to include new sequence

        if self.seqWindow is not None:
            # destroy prev open seq
            self.seqWindow.destroy()

        self.seqWindow = webview.create_window('Sequence View', 'sequence-view.html', js_api=api, min_size=(1310, 800))
        self.seqWindow.events.closed += on_closed



    def addTextToJson(self, textInput, overRideId):

        with open(self.currentEditingSeqLoc, 'r', encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)

            if overRideId is not None:
                newJsonId = overRideId
            else:
                newJsonId = len(data['sequence'])+1

            jsonToBeAdded = {
                "type": "text",
                "location": None,
                "content": textInput,
                "wait": 0.2,
                "moveToPositionSuccess": None,
                "moveToPositionFail": None,
                "adjustX": None,
                "adjustY": None,
                "confidence": None
            }
            data['sequence'].append(jsonToBeAdded)
            entireJson = data
            self.currentJsonSeqCache = data['sequence']

        with open(self.currentEditingSeqLoc, 'w', encoding='utf-8') as jsonFile:
            json.dump(entireJson, jsonFile, indent=4)

        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache
        }
        return response

    def addSpecialToJson(self, specialInput, overRideId):

        with open(self.currentEditingSeqLoc, 'r', encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)

            if overRideId is not None:
                newJsonId = overRideId
            else:
                newJsonId = len(data['sequence'])+1

            jsonToBeAdded = {
                "type": "special",
                "location": None,
                "content": specialInput,
                "wait": 0.2,
                "moveToPositionSuccess": None,
                "moveToPositionFail": None,
                "adjustX": None,
                "adjustY": None,
                "confidence": None
            }
            data['sequence'].append(jsonToBeAdded)
            entireJson = data
            self.currentJsonSeqCache = data['sequence']

        with open(self.currentEditingSeqLoc, 'w', encoding='utf-8') as jsonFile:
            json.dump(entireJson, jsonFile, indent=4)

        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache
        }
        return response

    def addCaptureToJson(self, captureLocation, overRideId):

        with open(self.currentEditingSeqLoc, 'r', encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)

            if overRideId is not None:
                newJsonId = overRideId
            else:
                newJsonId = len(data['sequence'])+1

            jsonToBeAdded = {
                "type": "capture",
                "location": captureLocation,
                "content": "singleclick",
                "wait": 0.2,
                "moveToPositionSuccess": None,
                "moveToPositionFail": None,
                "adjustX": None,
                "adjustY": None,
                "confidence": 0.90
            }
            data['sequence'].append(jsonToBeAdded)
            entireJson = data
            self.currentJsonSeqCache = data['sequence']

        with open(self.currentEditingSeqLoc, 'w', encoding='utf-8') as jsonFile:
            json.dump(entireJson, jsonFile, indent=4)

        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache
        }
        return response

    def addPosClickToJson(self, xyPos, overRideId):
        with open(self.currentEditingSeqLoc, 'r', encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)

            if overRideId is not None:
                newJsonId = overRideId
            else:
                newJsonId = len(data['sequence'])+1

            jsonToBeAdded = {
                "type": "position",
                "location": xyPos,
                "content": "singleclick",
                "wait": 0.2,
                "moveToPositionSuccess": None,
                "moveToPositionFail": None,
                "adjustX": None,
                "adjustY": None,
                "confidence": None
            }
            data['sequence'].append(jsonToBeAdded)
            entireJson = data
            self.currentJsonSeqCache = data['sequence']

        with open(self.currentEditingSeqLoc, 'w', encoding='utf-8') as jsonFile:
            json.dump(entireJson, jsonFile, indent=4)

        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache
        }
        return response

    def keyboardHotkeys(self):

        def ctrl_q():
            listOfSeq = self.getAllSequences('list')
            for seq in listOfSeq:
                if seq[2] == 'Ctrl + Q' and seq[1] is True:
                    newSeqToRun = seq[0]
                    seqEnableStatus = seq[1]
                    self.runnerFunc(listOfSeq, newSeqToRun, seqEnableStatus)
        def ctrl_z():
            listOfSeq = self.getAllSequences('list')
            for seq in listOfSeq:
                if seq[2] == 'Ctrl + Z' and seq[1] is True:
                    newSeqToRun = seq[0]
                    seqEnableStatus = seq[1]
                    self.runnerFunc(listOfSeq, newSeqToRun, seqEnableStatus)
        def ctrl_d():
            listOfSeq = self.getAllSequences('list')
            for seq in listOfSeq:
                if seq[2] == 'Ctrl + D' and seq[1] is True:
                    newSeqToRun = seq[0]
                    seqEnableStatus = seq[1]
                    self.runnerFunc(listOfSeq, newSeqToRun, seqEnableStatus)
        def alt_a():
            listOfSeq = self.getAllSequences('list')
            for seq in listOfSeq:
                if seq[2] == 'Alt + A' and seq[1] is True:
                    newSeqToRun = seq[0]
                    seqEnableStatus = seq[1]
                    self.runnerFunc(listOfSeq, newSeqToRun, seqEnableStatus)
        def alt_z():
            listOfSeq = self.getAllSequences('list')
            for seq in listOfSeq:
                if seq[2] == 'Alt + Z' and seq[1] is True:
                    newSeqToRun = seq[0]
                    seqEnableStatus = seq[1]
                    self.runnerFunc(listOfSeq, newSeqToRun, seqEnableStatus)
        def alt_x():
            listOfSeq = self.getAllSequences('list')
            for seq in listOfSeq:
                if seq[2] == 'Alt + X' and seq[1] is True:
                    newSeqToRun = seq[0]
                    seqEnableStatus = seq[1]
                    self.runnerFunc(listOfSeq, newSeqToRun, seqEnableStatus)

        bindings = [
            [["control", "q"], None, ctrl_q],
            [["control", "z"], None, ctrl_z],
            [["control", "d"], None, ctrl_d],
            [["alt", "a"], None, alt_a],
            [["alt", "z"], None, alt_z],
            [["alt", "x"], None, alt_x],
        ]

        # Register all of our keybindings
        global_hotkeys.register_hotkeys(bindings)

        # Finally, start listening for keypresses
        global_hotkeys.start_checking_hotkeys()

    def clearCurrentSeq(self):

        jsonDefault = {
            "sequence": [],
            "settings": {
                "typingSpeed": 60,
                "timeout": None
            },
            "interaction": {
                "seqEnabled": False,
                "sequenceName": self.currentSeqName,
                "trigger": None,
                "outcome": None
            }
        }

        # get all images:
        with open(self.currentEditingSeqLoc, encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
            for p in data['sequence']:
                if p["type"] == "capture" and p['location'] is not None:
                    os.remove(self.working_path + p['location'])

        with open(self.currentEditingSeqLoc, 'w') as f:
            json.dump(jsonDefault, f, indent=4)
        f.close()

        self.currentJsonSeqCache = jsonDefault['sequence']

        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache
        }
        return response


    def runSeq(self, seqToRun):
        if seqToRun == "current":
            seqLocation = self.currentEditingSeqLoc
        else:
            fileLoc = self.working_path + "\\sequences\\" + seqToRun + ".seq"
            fileLoc = os.path.normpath(fileLoc)
            seqLocation = fileLoc

        if os.path.isfile(seqLocation):
            with open(seqLocation, encoding='utf-8') as jsonFile:
                data = json.load(jsonFile)
                self.currentJsonSeqCache = data['sequence']
                self.currentJsonSetCache = data['settings']

                if seqToRun == "current":
                    self.seqWindow.hide()
                    time.sleep(0.4)

                resultMessage = "Run results:\n"
                timeoutSec = data['settings']['timeout']
                if timeoutSec is not None:
                    terminateTime = time.time() + timeoutSec
                else:
                    terminateTime = None

                index = 0
                while index < len(data['sequence']):
                    timeNow = time.time()

                    if terminateTime is not None and timeNow >= terminateTime:
                        resultMessage = resultMessage + "Sequence timeout\n"
                        break

                    p = data['sequence'][index]

                    if p['type'] == "capture":
                        if p['location'] is not None:
                            imgToFind = self.working_path + p['location']
                            confi = p['confidence']
                            clickMode = p['content']
                            jumpPosS = p['moveToPositionSuccess']
                            jumpPosF = p['moveToPositionFail']
                            adjustX = p['adjustX']
                            adjustY = p['adjustY']
                            if adjustX is None:
                                adjustX = 0
                            if adjustY is None:
                                adjustY = 0

                            location = pyautogui.locateOnScreen(imgToFind, confidence=confi)
                            if location is not None:
                                # match found
                                locCenter = pyautogui.center(location)
                                locClick = (locCenter.x + adjustX, locCenter.y + adjustY)

                                if "singleclick" in clickMode:
                                        pyautogui.click(locClick)
                                if "doubleclick" in clickMode:
                                        pyautogui.doubleClick(locClick)
                                if "tripleclick" in clickMode:
                                        pyautogui.tripleClick(locClick)
                                resultMessage = resultMessage + "Position: " + str(index+1) + " - Success\n"

                                # move cursor near center screen position before every new action,
                                # otherwise there will be problems with multimonitor setups
                                mainSx, mainSy = pyautogui.size()
                                pyautogui.moveTo(mainSx/2, mainSy/2)

                                if jumpPosS is not None:
                                    index = int(jumpPosS)
                                    index = int(index)-1
                                else:
                                    index += 1

                            if location is None:
                                # match not found
                                resultMessage = resultMessage + "Position: " + str(index+1) + " - Failure\n"

                                if jumpPosF is not None:
                                    index = int(jumpPosF)
                                    index = int(index)-1
                                else:
                                    break

                            time.sleep(p['wait'])

                    if p['type'] == "text":
                        if p['content'] is not None:
                            fullText = p['content']
                            cpsToSd = (0.5/self.currentJsonSetCache["typingSpeed"]*2)
                            pyautogui.write(fullText, interval=cpsToSd)
                            time.sleep(p['wait'])
                            resultMessage = resultMessage + "Position: " + str(index+1) + " - Success\n"
                            index += 1

                    if p['type'] == "special":
                        if p['content'] is not None:
                            specialText = p['content']

                            if specialText == "ctrl+C":
                                pyautogui.hotkey('ctrl', 'c')
                            elif specialText == "ctrl+V":
                                pyautogui.hotkey('ctrl', 'v')
                            elif specialText == "ctrl+A":
                                pyautogui.hotkey('ctrl', 'a')
                            elif specialText == "ctrl+S":
                                pyautogui.hotkey('ctrl', 's')
                            elif specialText == "ctrl+end":
                                pyautogui.hotkey('ctrl', 'end')
                            elif specialText == "shift+end":
                                pyautogui.hotkey('shiftright', 'shiftleft', 'end')
                            elif specialText == "ctrl+F":
                                pyautogui.hotkey('ctrl', 'f')
                            elif specialText == "alt+F4":
                                pyautogui.hotkey('alt', 'f4')

                            elif specialText == "store1":
                                pyautogui.hotkey('ctrl', 'c')
                                self.store1 = pyperclip.paste()
                            elif specialText == "store2":
                                pyautogui.hotkey('ctrl', 'c')
                                self.store2 = pyperclip.paste()
                            elif specialText == "store3":
                                pyautogui.hotkey('ctrl', 'c')
                                self.store3 = pyperclip.paste()

                            elif specialText == "paste1":
                                pyperclip.copy(self.store1)
                                pyautogui.hotkey('ctrl', 'v')
                            elif specialText == "paste2":
                                pyperclip.copy(self.store2)
                                pyautogui.hotkey('ctrl', 'v')
                            elif specialText == "paste3":
                                pyperclip.copy(self.store3)
                                pyautogui.hotkey('ctrl', 'v')

                            else:
                                pyautogui.press(specialText)
                            time.sleep(p['wait'])
                            resultMessage = resultMessage + "Position: " + str(index+1) + " - Success\n"
                            index += 1

                    if p['type'] == "position":
                        if p['location'] is not None:
                            xyPos = p['location']
                            clickMode = p['content']
                            xpos = int(xyPos.split(",")[0])
                            ypos = int(xyPos.split(",")[1])

                            locCenter = pyautogui.moveTo(xpos, ypos)
                            if "singleclick" in clickMode:
                                pyautogui.click(locCenter)
                            elif "doubleclick" in clickMode:
                                pyautogui.doubleClick(locCenter)
                            elif "tripleclick" in clickMode:
                                pyautogui.tripleClick(locCenter)

                            resultMessage = resultMessage + "Position: " + str(index+1) + " - Success\n"
                            index += 1
                            time.sleep(p['wait'])

                # run in finished
                if seqToRun == "current":
                    self.seqWindow.show()
                if index == len(data['sequence']):
                    completedSuccessfully = True
                else:
                    completedSuccessfully = False
        else:
            resultMessage = "File not found"
            completedSuccessfully = False

        # cut down result message if it is too long
        resultMessageList = resultMessage.split("\n")
        while len(resultMessageList) > 20:
            resultMessageList.pop(0)
        resultMessage = "\n".join(resultMessageList)

        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache,
            'alertMessage': resultMessage,
            'completedSuccessfully': completedSuccessfully
        }
        return response

    def editJsonAction(self, actionId, actionKey, actionValue):

        # set correct datatype for json
        if actionValue == "null" or actionValue == "":
            actionValue = None
        if actionKey in ("moveToPositionSuccess", "moveToPositionFail", "adjustX", "adjustY") and actionValue is not None:
            actionValue = int(actionValue)

        if actionKey == 'confidence' or actionKey == 'wait':
            if actionValue is not None:
                actionValue = float(actionValue)

        # settings json change
        if actionId == "SETTINGS-change":
            if actionValue is not None:
                actionValue = int(actionValue)
            with open(self.currentEditingSeqLoc, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                if actionKey == 'typingspeed':
                    data['settings']['typingSpeed'] = actionValue
                if actionKey == 'seqtimeout':
                    data['settings']['timeout'] = actionValue
                f.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # remove remaining part

                self.currentJsonSetCache = data['settings']

        # sequence json change
        else:
            with open(self.currentEditingSeqLoc, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['sequence'][int(actionId) - 1][actionKey] = actionValue
                f.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # remove remaining part
                self.currentJsonSeqCache = data['sequence']


        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache
        }
        return response


    def moveJsonAction(self, actionId, direction, steps):
        with open(self.currentEditingSeqLoc, 'r+', encoding='utf-8') as f:
            data = json.load(f)

            if direction == 'left':
                # swap list positions
                data['sequence'][int(actionId) - 1], data['sequence'][(int(actionId) - 1) - steps] = data['sequence'][(int(actionId) - 1) - steps], data['sequence'][int(actionId) - 1]

            if direction == 'right':
                # swap list positions
                data['sequence'][int(actionId) - 1], data['sequence'][(int(actionId) - 1) + steps] = data['sequence'][(int(actionId) - 1) + steps], data['sequence'][int(actionId) - 1]

            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()  # remove remaining part

            self.currentJsonSeqCache = data['sequence']

        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache
        }
        return response

    def deleteJsonAction(self, pos):
        with open(self.currentEditingSeqLoc, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            pos = int(pos) - 1
            fileToDelete = data['sequence'][pos]['location']
            data['sequence'].pop(pos)
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()  # remove remaining part
            self.currentJsonSeqCache = data['sequence']

        if fileToDelete is not None and ".png" in fileToDelete:
            os.remove(self.working_path + fileToDelete)

        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache
        }
        return response

    def testSeqPos(self, pos):
        with open(self.currentEditingSeqLoc, encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
            pos = int(pos)-1
            matchStatus = None

            self.seqWindow.hide()
            time.sleep(0.4)

            if data['sequence'][pos]['type'] == "capture":
                if data['sequence'][pos]['location'] is not None:
                    imgToFind = self.working_path + data['sequence'][pos]['location']
                    confi = data['sequence'][pos]['confidence']
                    clickMode = data['sequence'][pos]['content']
                    adjustX = data['sequence'][pos]['adjustX']
                    if adjustX is None:
                        adjustX = 0
                    adjustY = data['sequence'][pos]['adjustY']
                    if adjustY is None:
                        adjustY = 0

                    location = pyautogui.locateOnScreen(imgToFind, confidence=confi)
                    if location is not None:
                        matchStatus = "Match found and clicked"
                        locCenter = pyautogui.center(location)
                        locClick = (locCenter.x + adjustX, locCenter.y + adjustY)

                        if "singleclick" in clickMode:
                            pyautogui.click(locClick)
                        if "doubleclick" in clickMode:
                            pyautogui.doubleClick(locClick)
                        if "tripleclick" in clickMode:
                            pyautogui.tripleClick(locClick)
                    if location is None:
                        print("No match found!")
                        matchStatus = "Match not found"

            if data['sequence'][pos]['type'] == "text":
                if data['sequence'][pos]['content'] is not None:
                    fullText = data['sequence'][pos]['content']
                    cpsToSd = (0.5 / self.currentJsonSetCache["typingSpeed"] * 2)
                    pyautogui.write(fullText, interval=cpsToSd)
                    matchStatus = "Text typed successfully"

            if data['sequence'][pos]['type'] == "special":
                if data['sequence'][pos]['content'] is not None:
                    specialText = data['sequence'][pos]['content']
                    if specialText == "ctrl+C":
                        pyautogui.hotkey('ctrl', 'c')
                    elif specialText == "ctrl+V":
                        pyautogui.hotkey('ctrl', 'v')
                    elif specialText == "ctrl+A":
                        pyautogui.hotkey('ctrl', 'a')
                    elif specialText == "ctrl+S":
                        pyautogui.hotkey('ctrl', 's')
                    elif specialText == "ctrl+end":
                        pyautogui.hotkey('ctrl', 'end')
                    elif specialText == "shift+end":
                        pyautogui.hotkey('shiftright', 'shiftleft', 'end')
                    elif specialText == "ctrl+F":
                        pyautogui.hotkey('ctrl', 'f')
                    elif specialText == "alt+F4":
                        pyautogui.hotkey('alt', 'f4')

                    elif specialText == "store1":
                        pyautogui.hotkey('ctrl', 'c')
                        self.store1 = pyperclip.paste()
                    elif specialText == "store2":
                        pyautogui.hotkey('ctrl', 'c')
                        self.store2 = pyperclip.paste()
                    elif specialText == "store3":
                        pyautogui.hotkey('ctrl', 'c')
                        self.store3 = pyperclip.paste()

                    elif specialText == "paste1":
                        pyperclip.copy(self.store1)
                        pyautogui.hotkey('ctrl', 'v')
                    elif specialText == "paste2":
                        pyperclip.copy(self.store2)
                        pyautogui.hotkey('ctrl', 'v')
                    elif specialText == "paste3":
                        pyperclip.copy(self.store3)
                        pyautogui.hotkey('ctrl', 'v')

                    else:
                        pyautogui.press(specialText)
                    matchStatus = "Key pressed successfully"

            if data['sequence'][pos]['type'] == "position":
                if data['sequence'][pos]['location'] is not None:
                    xyPos = data['sequence'][pos]['location']
                    clickMode = data['sequence'][pos]['content']
                    xpos = int(xyPos.split(",")[0])
                    ypos = int(xyPos.split(",")[1])
                    locCenter = pyautogui.moveTo(xpos, ypos)
                    if "singleclick" in clickMode:
                            pyautogui.click(locCenter)
                    if "doubleclick" in clickMode:
                            pyautogui.doubleClick(locCenter)
                    if "tripleclick" in clickMode:
                            pyautogui.tripleClick(locCenter)
                    matchStatus = "Position clicked successfully"

            time.sleep(0.4)
            self.seqWindow.show()

        response = {
            'activeFile': self.currentEditingSeqLoc,
            'jsonSequence': self.getSeqInBase64(),
            'jsonSettings': self.currentJsonSetCache,
            'alertMessage': matchStatus
        }
        return response

    def getTextValue(self, pos):
        with open(self.currentEditingSeqLoc, encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
            pos = int(pos)-1

            textToReturn = data['sequence'][pos]['content']

        response = {
            'content': textToReturn
        }
        return response

    def getAllSequences(self, outputType):
        allSeqList = []
        seqDirPath = self.working_path + "\\sequences\\"
        seqDirPath = os.path.normpath(seqDirPath)

        for file in os.listdir(seqDirPath):
            if file.endswith(".seq"):
                fileLoc = self.working_path + "\\sequences\\" + file
                fileLoc = os.path.normpath(fileLoc)
                if os.path.isfile(fileLoc):
                    with open(fileLoc, 'r', encoding='utf-8') as jsonFile:
                        try:
                            data = json.load(jsonFile)
                            fileSequenceName = data['interaction']['sequenceName']
                            fileSeqEnabled = data['interaction']['seqEnabled']
                            fileTrigger = data['interaction']['trigger']
                            fileOutcome = data['interaction']['outcome']
                            allSeqList.append([fileSequenceName, fileSeqEnabled, fileTrigger, fileOutcome])
                        except:
                            continue
        allSeqJson = json.dumps(allSeqList)
        response = {
            'allSeqJson': allSeqJson
        }
        if outputType == 'dict':
            return response
        if outputType == 'list':
            return allSeqList

    def openSequence(self, fileName):

        def on_closed():
            self.seqWindow = None

        if (int(time.time())-self.lastOpenSeq) < 2:
            # prevent spam opening or doubleclicks of the sequence
            return
        self.lastOpenSeq = int(time.time())

        from os import path
        self.currentSeqName = fileName
        fileLoc = self.working_path + "\\sequences\\" + fileName + ".seq"
        fileLoc = os.path.normpath(fileLoc)

        missingFilesList = []
        errorOccurred = False

        with open(fileLoc, encoding='utf-8') as jsonFile:
            try:
                data = json.load(jsonFile)

                # check for missing files in sequence
                for p in data['sequence']:
                    if p['type'] == "capture" and p['location'] is not None:
                        if not path.exists(self.working_path + p['location']):
                            missingFilesList.append(p['location'])
                response = {
                    'errorMissingFiles': None
                }
            except:
                # invalid json
                errorOccurred = True
                response = {
                    'errorMissingFiles': 'Missing valid JSON'
                }

        if len(missingFilesList) > 0:
            errorOccurred = True
            response = {
                'errorMissingFiles': json.dumps(missingFilesList)
            }

        if not errorOccurred:
            self.currentJsonSeqCache = data['sequence']
            self.currentJsonSetCache = data['settings']
            self.currentEditingSeqLoc = fileLoc

            if self.seqWindow is not None:
                # destroy prev open seq
                self.seqWindow.destroy()

            self.seqWindow = webview.create_window('Sequence View', 'sequence-view.html', js_api=api, min_size=(1310, 800))
            self.seqWindow.move(self.seqWindow.x - 100, self.seqWindow.y + 100)
            self.seqWindow.events.closed += on_closed

        # showing potential errors in return, otherwise show nothing new.
        return response


    def changeJsonInteraction(self, fileName, statusToSet, type):
        if statusToSet == "null":
            statusToSet = None

        fileLoc = self.working_path + "\\sequences\\" + fileName + ".seq"
        fileLoc = os.path.normpath(fileLoc)
        if type == 'seqEnabled':
            statusToSet = json.loads(statusToSet)

        with open(fileLoc, 'r+', encoding='utf-8') as f:
            data = json.load(f)

            # special case for outcome in order to allow both positive and negative outcomes in json
            currOutcome = data['interaction'][type]
            if type == "outcome" and currOutcome is not None and statusToSet is not None:
                if currOutcome is not None:
                    if "<br>" in currOutcome:
                        # overwrite
                        data['interaction'][type] = statusToSet
                    elif "Success" in currOutcome:
                        if "Failure" in statusToSet:
                            data['interaction'][type] = currOutcome + "<br>" + statusToSet
                        if "Success" in statusToSet:
                            data['interaction'][type] = statusToSet
                    elif "Failure" in currOutcome:
                        if "Success" in statusToSet:
                            data['interaction'][type] = currOutcome + "<br>" + statusToSet
                        if "Failure" in statusToSet:
                            data['interaction'][type] = statusToSet
            else:
                data['interaction'][type] = statusToSet
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()  # remove remaining part

    def delSequence(self, fileName):
        fileLoc = self.working_path + "\\sequences\\" + fileName + ".seq"
        fileLoc = os.path.normpath(fileLoc)

        # get all images:
        with open(fileLoc, encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
            for p in data['sequence']:
                if p["type"] == "capture" and p['location'] is not None:
                    try:
                        os.remove(self.working_path + p['location'])
                    except OSError:
                        pass

        os.remove(fileLoc)
        time.sleep(0.2)
        response = self.getAllSequences("dict")
        return response

    def initRunLoop(self):
        # get all sequences
        listOfSeq = self.getAllSequences('list')
        self.seqRunList = []

        for seq in listOfSeq:
            if seq[2] is not None and "Every" in seq[2]:
                seqName = seq[0]
                secondsToNextRun = re.findall("\d+", seq[2])[0]
                eSecondsToNextRun = self.programStartTime + int(secondsToNextRun)
                self.seqRunList.append([seqName,eSecondsToNextRun])

    def runnerFunc(self, listOfSeq, newSeqToRun, seqEnableStatus):
        runLoopOn = True

        while runLoopOn:
            seqOutcome = None  # start value
            # get data of the current to-run seq
            for seqi in listOfSeq:
                if seqi[0] == newSeqToRun:
                    seqOutcome = seqi[3]
                    seqEnableStatus = seqi[1]

            if seqEnableStatus is True:
                runResponseDict = self.runSeq(newSeqToRun)
            else:
                break

            if seqOutcome is None:
                break

            if "<br>" in seqOutcome:
                # double outcome
                seqOutcomeList = seqOutcome.split("<br>")
                if runResponseDict['completedSuccessfully'] is True:
                    if "Success" in seqOutcomeList[0]:
                        newSeqToRun = seqOutcomeList[0].split(" -> ")[1]
                    if "Success" in seqOutcomeList[1]:
                        newSeqToRun = seqOutcomeList[1].split(" -> ")[1]
                else:
                    if "Failure" in seqOutcomeList[0]:
                        newSeqToRun = seqOutcomeList[0].split(" -> ")[1]
                    if "Failure" in seqOutcomeList[1]:
                        newSeqToRun = seqOutcomeList[1].split(" -> ")[1]
            else:
                # Single outcome, or no outcome
                if runResponseDict['completedSuccessfully'] is True:
                    if "Success" in seqOutcome:
                        newSeqToRun = seqOutcome.split(" -> ")[1]
                    else:
                        runLoopOn = False
                else:
                    if "Failure" in seqOutcome:
                        newSeqToRun = seqOutcome.split(" -> ")[1]
                    else:
                        runLoopOn = False

    def mainRunLoop(self):
        seconds = time.time()
        eSecondsNow = int(seconds)
        for indx,seq in enumerate(self.seqRunList):
            if seq[1] <= eSecondsNow:
                # time condition met.
                listOfSeq = self.getAllSequences('list')

                for seqR in listOfSeq:
                    if seq[0] == seqR[0] and seqR[2] is not None and "Every" in seqR[2] and seqR[1] is True:
                        # name is same, trigger is not null, the word 'Every' is in trigger, seqEnabled it True
                        # print("will run " + str(seq[0]))

                        # set new time for next run
                        secondsToNextRun = re.findall("\d+", seqR[2])[0]
                        eSecondsToNextRun = eSecondsNow + int(secondsToNextRun)
                        del self.seqRunList[indx]
                        self.seqRunList.insert(indx, [seqR[0], eSecondsToNextRun])
                        # now run seq[0]
                        self.runnerFunc(listOfSeq, seq[0], False)


    def importSequence(self):
        from zipfile import ZipFile
        file_types = ('Exported Sequence Files (*.eseq)', 'All Files (*.*)')
        fileSelectArray = startWindow.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)

        for eseqFile in fileSelectArray:
            fileLoc = os.path.normpath(eseqFile)

            zip = ZipFile(fileLoc)
            for fileName in zip.namelist():
                if ".png" in fileName:
                    pngNewLoc = self.working_path + '/captures/' + fileName
                    pngNewLoc = os.path.normpath(pngNewLoc)

                    f = zip.open(fileName)
                    content = f.read()
                    f = open(pngNewLoc, 'wb')
                    f.write(content)
                    f.close()
                if ".seq" in fileName:
                    pngNewLoc = self.working_path + '/sequences/' + fileName
                    pngNewLoc = os.path.normpath(pngNewLoc)

                    f = zip.open(fileName)
                    content = f.read()
                    f = open(pngNewLoc, 'wb')
                    f.write(content)
                    f.close()

        response = self.getAllSequences("dict")
        return response

    def importExample(self):
        from zipfile import ZipFile
        fileLoc = os.path.dirname(os.path.realpath(__file__)) + "\\assets\\Hello World.eseq"
        zip = ZipFile(fileLoc)
        for fileName in zip.namelist():
            if ".png" in fileName:
                pngNewLoc = self.working_path + '/captures/' + fileName
                pngNewLoc = os.path.normpath(pngNewLoc)

                f = zip.open(fileName)
                content = f.read()
                f = open(pngNewLoc, 'wb')
                f.write(content)
                f.close()
            if ".seq" in fileName:
                pngNewLoc = self.working_path + '/sequences/' + fileName
                pngNewLoc = os.path.normpath(pngNewLoc)

                f = zip.open(fileName)
                content = f.read()
                f = open(pngNewLoc, 'wb')
                f.write(content)
                f.close()

    def exportSequence(self, seqToExport):
        from os import path
        from zipfile import ZipFile

        seqFileLoc = self.working_path + "\\sequences\\" + seqToExport + ".seq"
        seqFileLoc = os.path.normpath(seqFileLoc)

        imgFilesList = []
        errorOccurred = False

        with open(seqFileLoc, encoding='utf-8') as jsonFile:
            try:
                data = json.load(jsonFile)
                # check for capture files in sequence
                for p in data['sequence']:
                    if p['type'] == "capture" and p['location'] is not None:
                        if path.exists(self.working_path + p['location']):
                            fileToAdd = self.working_path + p['location']
                            imgFilesList.append(os.path.normpath(fileToAdd))
            except:
                # invalid json
                errorOccurred = True

        # create a ZipFile object
        zipObj = ZipFile(self.working_path + 'exports\\' + seqToExport + '.eseq', 'w')

        for imgFileLoc in imgFilesList:
            # Add multiple files to the zip
            name_file_only = imgFileLoc.split(os.sep)[-1]
            zipObj.write(imgFileLoc, name_file_only)

        name_file_only = seqFileLoc.split(os.sep)[-1]
        zipObj.write(seqFileLoc, name_file_only)

        # close the Zip File
        zipObj.close()

        # open the directory
        exportDir = self.working_path + '\\exports'
        os.system(f'start {os.path.realpath(exportDir)}')

    def openHelp(self):
        webview.create_window('Help', 'help.html', js_api=api, min_size=(1294, 800))

    def openCredits(self):
        webview.create_window('Credits', 'credits.html', js_api=api, min_size=(1294, 800))

    def getSeqInBase64(self):
        # modify json to include base64 images for sequence view, because javascript cannot read Appdata captures folder
        sequenceModdedLocations = self.currentJsonSeqCache
        if sequenceModdedLocations is not None:
            for p in sequenceModdedLocations:
                if p['type'] == "capture" and p['location'] is not None:
                    try:
                        with open(self.working_path + p['location'], "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                            p['location'] = encoded_string.decode('utf-8')
                    except OSError:
                        pass
        return sequenceModdedLocations

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "-nofailsafe":
            pyautogui.FAILSAFE = False

    api = Api()
    startWindow = webview.create_window('Click Routine', 'start-view.html', js_api=api, min_size=(1024, 700))
    webview.start(http_server=False, debug=False)

