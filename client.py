class opentronsInstructionClient:
    '''
    each object will represent a single experiment
    '''

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
