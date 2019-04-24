"""

This example shows how to use managed tasks. This is useful for items that
need to be run in sequence where one task can only run after successful
completion of another.

"""

import requests
import json
import os
import time
import sys


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
                else:
                    return (False, parsedJson.get("message", "unknown error"))
            except Exception as e:
                print('could not perform prompt. error {}'.format(str(e)))
                return (False, "")

    def manageTasks(self, instructions):
        if self.virtEnvironment:
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            try:
                r = requests.post('{}/manageTasks/{}'.format(self.restService,
                         self.taskUUID), json=instructions, headers=headers)
                parsedJson = json.loads(r.text)
                if parsedJson["success"]:
                    return True
                else:
                    return False
            except Exception as e:
                print('could not manage tasks. error {}'.format(str(e)))
                return (False, "")


virtuinEnv = VirtuinEnv()

# passed command line argument from collection.yml
taskNumber = int(sys.argv[1])
virtuinEnv.displayMessage('This is task {}'.format(taskNumber))
virtuinEnv.updateProgress(5)
virtuinEnv.displayMessage('taskIndex can be found in input file data. {}'
                            .format(virtuinEnv.inputData.get('taskIndex')))
time.sleep(1)
virtuinEnv.updateProgress(50)
# now successful lets setup the next task. Check taskNumber, however could
# also compare against taskIndex.
if taskNumber == 1:
    virtuinEnv.displayMessage('First task successfully complete. Enabled second')
    instr = {
        'reset': [1],   # reset status of task 2
        'enable': [1],  # enable task 2
        'disable': [0]  # disable task 1
      }
    virtuinEnv.manageTasks(
        json.loads(json.dumps(instr))
    )
else:
    virtuinEnv.displayMessage('Second task successfully complete. Enabled first')
    instr = {
        'reset': [0],   # reset status task 1
        'enable': [0],  # enable task 1
        'disable': [1]  # disable task 2
      }
    virtuinEnv.manageTasks(
        json.loads(json.dumps(instr))
    )

time.sleep(1)
virtuinEnv.updateProgress(100)
