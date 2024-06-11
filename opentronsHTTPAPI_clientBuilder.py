import requests
import json
import logging

LOGGER = logging.getLogger(__name__)

class opentronsClient:
    '''
    each object will represent a single experiment
    '''

    def __init__(self,
                 strRobotIP: str,
                 dicHeaders: dict = {"opentrons-version": "3"},):
        '''
        initializes the object with the robot IP and headers

        arguments
        ----------
        strRobotIP: str
            the IP address of the robot

        dicHeaders: dict
            the headers to be used in the requests

        returns
        ----------
        None
        '''
        self.robotIP = strRobotIP
        self.headers = dicHeaders
        self.runID = None
        self.commandURL = None

        # need to fix this
        self.labware = {"fixed-trash": {'id': 'fixed-trash', 'slot': 12}}
        self.pipettes = {}
        self._initalizeRun()


    def _initalizeRun(self):
        '''
        creates a new blank run on the opentrons with command endpoints
        
        arguments
        ----------
        None

        returns
        ----------
        None
        '''

        strRunURL = f"http://{self.robotIP}:31950/runs"
        # create a new run
        jsonResponse = requests.post(url = strRunURL,
                                     headers = self.headers
                                     )
        if jsonResponse.status_code == 201:
            dicResponse = json.loads(jsonResponse.text)
            # get the run ID
            self.runID = dicResponse['data']['id']
            # setup command endpoints
            self.commandURL = strRunURL + f"/{self.runID}/commands"
            
            # LOG - info
            LOGGER.info(f"New run created with ID: {self.runID}")
            LOGGER.info(f"Command URL: {self.commandURL}")

        else:
            raise Exception(f"Failed to create a new run.\nError code: {jsonResponse.status_code}\n Error message: {jsonResponse.text}")
        
        
    def loadLabware(self,
                    intSlot: int,
                    strLabwareName: str,
                    strNamespace: str = "opentrons",
                    intVersion: int = 1,
                    strIntent: str = "setup"):
        '''
        loads labware onto the robot

        arguments
        ----------
        intSlot: int
            the slot number where the labware is to be loaded

        strLabwareName: str
            the name of the labware to be loaded
            
        strNamespace: str
            the namespace of the labware to be loaded
            default: "opentrons"

        intVersion: int
            the version of the labware to be loaded
            default: 1

        strIntent: str
            the intent of the command
            default: "setup"

        returns
        ----------
        None
        '''
    
        dicCommand = {
            "data": {
                "commandType": "loadLabware",
                "params": {
                    "location": {"slotName": str(intSlot)},
                    "loadName": strLabwareName,
                    "namespace": strNamespace,
                    "version": str(intVersion)
                },
                "intent": strIntent
            }
        }

        strCommand = json.dumps(dicCommand)

        # LOG - info
        LOGGER.info(f"Loading labware: {strLabwareName} in slot: {intSlot}")
        # LOG - debug
        LOGGER.debug(f"Command: {strCommand}")
        

        jsonResponse = requests.post(
            url = self.commandURL,
            headers = self.headers,
            params = {"waitUntilComplete": True},
            data = strCommand
        )

        # LOG - debug
        LOGGER.debug(f"Response: {jsonResponse.text}")

        if jsonResponse.status_code == 201:
            dicResponse = json.loads(jsonResponse.text)
            print(dicResponse)
            strLabwareID = dicResponse['data']['result']['labwareId']
            self.labware[strLabwareName] = {"id": strLabwareID, "slot": intSlot}
            # LOG - info
            LOGGER.info(f"Labware loaded with name: {strLabwareName} and ID: {strLabwareID}")
        else:
            raise Exception(f"Failed to load labware.\nError code: {jsonResponse.status_code}\n Error message: {jsonResponse.text}")
        
        
    def loadCustomLabware(self,
                          dicLabware: dict,
                          intSlot: int,
                          ):
        '''
        loads custom labware onto the robot

        arguments
        ----------
        dicLabware: dict
            the JSON object of the custom labware to be loaded (directly from opentrons labware definitions)

        returns
        ----------
        None
        '''

        dicCommand = {'data' : dicLabware}

        strCommand = json.dumps(dicCommand)

        # LOG - info
        LOGGER.info(f"Loading custom labware: {dicLabware['parameters']['loadName']} in slot: {intSlot}")
        # LOG - debug
        LOGGER.debug(f"Command: {strCommand}")

        jsonResponse = requests.post(
            url = f"http://{self.robotIP}:31950/runs/{self.runID}/labware_definitions",
            headers = self.headers,
            data = strCommand
        )

        # LOG - debug
        LOGGER.debug(f"Response: {jsonResponse.text}")
        
        if jsonResponse.status_code == 201:
            # LOG - info
            LOGGER.info(f"Custom labware pushed to the robot.")
            # load the labware
            self.loadLabware(intSlot = intSlot,
                             strLabwareName = dicLabware['parameters']['loadName'],
                             strNamespace = dicLabware['namespace'],
                             intVersion = dicLabware['version'],
                             strIntent = "setup"
                             )
        else:
            raise Exception(f"Failed to load custom labware.\nError code: {jsonResponse.status_code}\n Error message: {jsonResponse.text}")

        

    def loadPipette(self,
                    strPipetteName: str,
                    strMount: str):
        '''
        loads a pipette onto the robot

        arguments
        ----------
        strPipetteName: str
            the name of the pipette to be loaded

        strMount: str
            the mount where the pipette is to be loaded

        returns
        ----------
        None
        '''

        dicCommand = {
            "data": {
                "commandType": "loadPipette",
                "params": {
                    "pipetteName": strPipetteName,
                    "mount": strMount
                },
                "intent": "setup"
            }
        }

        jsonCommand = json.dumps(dicCommand)

        # LOG - info
        LOGGER.info(f"Loading pipette: {strPipetteName} on mount: {strMount}")
        # LOG - debug
        LOGGER.debug(f"Command: {jsonCommand}")

        jsonResponse = requests.post(
            url = self.commandURL,
            headers = self.headers,
            params = {"waitUntilComplete": True},
            data = jsonCommand
        )

        # LOG - debug
        LOGGER.debug(f"Response: {jsonResponse.text}")

        if jsonResponse.status_code == 201:
            dicResponse = json.loads(jsonResponse.text)
            strPipetteID = dicResponse['data']['result']['pipetteId']
            self.pipettes[strPipetteName] = {"id": strPipetteID, "mount": strMount}
            # LOG - info
            LOGGER.info(f"Pipette loaded with name: {strPipetteName} and ID: {strPipetteID}")
        else:
            raise Exception(f"Failed to load pipette.\nError code: {jsonResponse.status_code}\n Error message: {jsonResponse.text}")
        

        
    def homeRobot(self):
        '''
        homes the robot - this should be done before doing any other movements of the robot per instance but need to implement this***

        arguments
        ----------
        None

        returns
        ----------
        None
        '''

        jsonCommand = json.dumps({"target": "robot"})

        # LOG - info
        LOGGER.info(f"Homing the robot")
        # LOG - debug
        LOGGER.debug(f"Command: {jsonCommand}")

        jsonResponse = requests.post(
            url = f"http://{self.robotIP}:31950/robot/home",
            headers = self.headers,
            data = jsonCommand
        )

        # LOG - debug
        LOGGER.debug(f"Response: {jsonResponse.text}")
        if jsonResponse.status_code == 200:
            # LOG - info
            LOGGER.info(f"Robot homed successfully.")
        else:
            raise Exception(f"Failed to home the robot.\nError code: {jsonResponse.status_code}\n Error message: {jsonResponse.text}")
        

    def pickUpTip(self,
                  strLabwareName: str,
                  strPipetteName: str,
                  strOffsetStart: str = "top",
                  strOffsetX: int = 0,
                  strOffsetY: int = 0,
                  strOffsetZ: int = 0,
                  strWellName: str = "A1",
                  strIntent: str = "setup"
                  ):
        '''
        picks up a tip from a labware

        arguments
        ----------
        strLabwareName: str
            the name of the labware from which the tip is to be picked up

        strWellName: str
            the name of the well from which the tip is to be picked up

        returns
        ----------
        None
        '''

        # *** WIP ***
        # build in some check to see if the tip is already picked up


        dicCommand = {
            "data": {
                "commandType": "pickUpTip",
                "params": {
                    "labwareId": self.labware[strLabwareName]["id"],
                    "wellName": strWellName,
                    "wellLocation": {
                        "origin": strOffsetStart,
                        "offset": {"x": strOffsetX, "y": strOffsetY, "z": strOffsetZ}
                        },
                    "pipetteId": self.pipettes[strPipetteName]["id"],
                },
                "intent": strIntent
            }
        }

        jsonCommand = json.dumps(dicCommand)

        # LOG - info
        LOGGER.info(f"Picking up tip from labware: {strLabwareName}")
        # LOG - debug
        LOGGER.debug(f"Command: {jsonCommand}")

        jsonResponse = requests.post(
            url = self.commandURL,
            headers = self.headers,
            params = {"waitUntilComplete": True},
            data = jsonCommand
        )

        # LOG - debug   
        LOGGER.debug(f"Response: {jsonResponse.text}")

        if jsonResponse.status_code == 201:
            # LOG - info
            LOGGER.info(f"Tip picked up from labware: {strLabwareName}, well: {strWellName}")

        else:
            raise Exception(f"Failed to pick up tip.\nError code: {jsonResponse.status_code}\n Error message: {jsonResponse.text}")


        
    def dropTip(self,
                strPipetteName: str,
                strLabwareName: str = "fixed-trash",
                strWellName: str = "A1",
                strOffsetStart: str = "top",
                strOffsetX: int = 0,
                strOffsetY: int = 0,
                strOffsetZ: int = 0,
                boolHomeAfter: bool = False,
                boolAlternateDropLocation: bool = False,
                strIntent: str = "setup",
                ):
        '''
        drops a tip into a labware

        arguments
        ----------
        strLabwareName: str
            the name of the labware into which the tip is to be dropped

        strWellName: str
            the name of the well into which the tip is to be dropped

        returns
        ----------
        None
        '''

        # *** WIP ***
        # build in some check to see if the tip is already dropped

        dicCommand = {
            "data": {
                "commandType": "dropTip",
                "params": {
                    "pipetteId": self.pipettes[strPipetteName]["id"],
                    "labwareId": self.labware[strLabwareName]["id"],
                    "wellName": strWellName,
                    "wellLocation": {
                        "origin": strOffsetStart,
                        "offset": {"x": strOffsetX, "y": strOffsetY, "z": strOffsetZ}
                    },
                    "homeAfter": boolHomeAfter,
                    "alternateDropLocation": boolAlternateDropLocation
                },
                "intent": strIntent
            }
        }

        jsonCommand = json.dumps(dicCommand)

        # LOG - info
        LOGGER.info(f"Dropping tip into labware: {strLabwareName}")
        # LOG - debug
        LOGGER.debug(f"Command: {dicCommand}")

        print(jsonCommand)

        jsonResponse = requests.post(
            url = self.commandURL,
            headers = self.headers,
            params = {"waitUntilComplete": True},
            data = jsonCommand
        )

        print(jsonResponse.text)

        # LOG - debug
        LOGGER.debug(f"Response: {jsonResponse.text}")

        if jsonResponse.status_code == 201:
            # LOG - info
            LOGGER.info(f"Tip dropped into labware: {strLabwareName}, well: {strWellName}")
    
    def aspirate(self,):
        pass

    def dispense(self,):
        pass

    def moveTo(self,):
        pass


            


    '''
    TODO LIST 

    ADD ADDITIONAL CHECK -  status == FAILED
        it is possible for the robot to return a response (ie. status_code == 201) but the command to fail

    FIGURE OUT FIXED 


    '''
    # *** INITIALIZATION ***

        # some way to manage IDs (run, labware, pipettes, etc)
        # some way to track the state of the robot (shorthand)
        # tracking the state of the experiment will be done by the experiment handler (dependant on the projects)

    #  (https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/atomic_commands_setup.py)


    # *** INTERNAL FUNCTIONS ***
    # function to send request to the robot

    # *** METHODS ***
    # pickup tip
    # drop tip
    # aspiate
    # dispense
    # move to
