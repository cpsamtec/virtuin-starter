import requests
import json
import os
import time


class VirtuinEnv:

    def __init__(self):
        self.inputData = {}
        self.restService = None
        self.virtEnvironment = False
        self.taskUUID = None
        self.getVirtuinRequirements()

    def getVirtuinRequirements(self):
        # First get virtuin input file contents
        inputFile = os.getenv('VIRT_TASK_INPUT_FILE')
        self.inputData = {}
        if inputFile:
            with open(inputFile) as json_file:
                self.inputData = json.load(json_file)

        self.taskUUID = self.inputData.get('taskUUID')
        # REST_SERVER=VIRT_GUI_SERVER_ADDRESS:VIRT_REST_API_PORT
        apiPort = os.getenv('VIRT_REST_API_PORT')
        serverAddress = os.getenv('VIRT_GUI_SERVER_ADDRESS')
        self.restService = None
        if apiPort and serverAddress:
            self.restService = "http://{}:{}/api/v1".format(serverAddress,
                                                            apiPort)
        # Send a message to let operator now everything
        # has started successfully
        self.virtEnvironment = self.taskUUID is not None and self.restService is not None

    def displayMessage(self, message):
        if self.virtEnvironment:
            headers = {'Content-Type': 'text/plain;charset=UTF-8'}
            requests.post('{}/message/{}'.format(self.restService,
                         self.taskUUID), data=message, headers=headers)

    def updateProgress(self, progress):
        if self.virtEnvironment:
            requests.post('{}/progress/{}/{}'.format(self.restService,
            self.taskUUID, progress))

    def displayPrompt(self, message, type='confirmation'):
        if self.virtEnvironment:
            headers = {'Content-Type': 'text/plain;charset=UTF-8'}
            try:
                r = requests.post('{}/prompt/{}/{}'.format(self.restService,
                self.taskUUID, type), data=message, headers=headers)
                parsedJson = json.loads(r.text)
                if parsedJson["success"]:
                    return (True, parsedJson["userResponse"])
                if parsedJson["success"]:
                    return (False, parsedJson["message"])
            except Exception as e:
                print('could not perform prompt. error {}'.format(str(e)))
                return (False, "")




virtuinEnv = VirtuinEnv()
virtuinEnv.displayMessage('beginning')
virtuinEnv.updateProgress(5)
(succ, text) = virtuinEnv.displayPrompt("Make sure you see this message")
print('received succ {} and text {}'.format(succ, text))
time.sleep(5)
virtuinEnv.displayMessage('finishing')
virtuinEnv.updateProgress(90)
time.sleep(1)
virtuinEnv.updateProgress(100)
