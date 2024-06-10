import requests
import json

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
        self.labware = {}
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
            # save the run ID
            self.runID = dicResponse['data']['id']
            # setup command endpoints
            self.commandURL = strRunURL + f"/{self.runID}/commands"
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

        jsonCommand = json.dumps(dicCommand)

        jsonResponse = requests.post(
            url = self.commandURL,
            headers = self.headers,
            params = {"waitUntilComplete": True},
            data = jsonCommand
        )

        if jsonResponse.status_code == 201:
            dicResponse = json.loads(jsonResponse.text)
            strLabwareID = dicResponse['data']['result']['labwareId']
            self.labware[strLabwareName] = {"id": strLabwareID, "slot": intSlot}
        else:
            raise Exception(f"Failed to load labware.\nError code: {jsonResponse.status_code}\n Error message: {jsonResponse.text}")
        
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

        jsonResponse = requests.post(
            url = self.commandURL,
            headers = self.headers,
            params = {"waitUntilComplete": True},
            data = jsonCommand
        )

        if jsonResponse.status_code == 201:
            dicResponse = json.loads(jsonResponse.text)
            strPipetteID = dicResponse['data']['result']['pipetteId']
            self.pipettes[strPipetteName] = {"id": strPipetteID, "mount": strMount}
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

        jsonResponse = requests.post(
            url = f"http://{self.robotIP}:31950/robot/home",
            headers = self.headers,
            data = jsonCommand
        )

def pickUpTip(self,
              strLabwareName: str,
              strWellName: str,
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

    pass
        

# # Pick up tip
# command_dict = {
# 	"data": {
# 		"commandType": "pickUpTip",
# 		"params": {
# 			"labwareId": labware_1_id,
# 			"wellName": "A1",
# 			"wellLocation": {
# 				"origin": "top", "offset": {"x": 0, "y": 0, "z": 0}
# 			},
# 			"pipetteId": pipette_id
# 		},
# 		"intent": "setup"
# 	}
# }

# command_payload = json.dumps(command_dict)
# print(f"Command:\n{command_payload}\n")

# r = requests.post(
# 	url=commands_url,
# 	headers=HEADERS,
# 	data=command_payload
# 	)

# print(f"Response:\n{r}\n{r.text}\n")


            
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
