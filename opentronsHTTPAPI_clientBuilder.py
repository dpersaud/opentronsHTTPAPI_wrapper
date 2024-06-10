import requests
import json

class opentronsInstructionClient:
    '''
    each object will represent a single experiment
    '''

    def __init__(self,
                 strRobotIP: str,
                 dicHeaders: dict = {'apiLevel': '2.10'},):
        self.robotIP = strRobotIP
        self.headers = dicHeaders
        self.runID = None
        self.commandURL = None
        self.initalizeRun()

        def initalizeRun(self):
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
            if jsonResponse.status_code == 200:
                dicResponse = json.loads(jsonResponse.text)
                # save the run ID
                self.runID = dicResponse['data']['id']
                # setup command endpoints
                self.commandURL = strRunURL + f"/{self.runID}/commands"
            else:
                raise Exception(f"Failed to create a new run.\nError code: {jsonResponse.status_code}\n Error message: {jsonResponse.text}")



    # *** INITIALIZATION ***
    # needs to be inialized with opentrons IP

        # make a run
        # setup command enpoints
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
