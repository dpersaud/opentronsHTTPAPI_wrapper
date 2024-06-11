from openTronWrapper import OpenTronWrapper
import logging
from datetime import datetime
import sys

# Define the IP address of the robot
ROBOT_IP = "127.0.0.1"

# Folder where data and log-file will be saved
DATA_PATH = ""

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG,  # Can be changed to logging.INFO to see less
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(DATA_PATH + "example_run.log", mode="a"),
        logging.StreamHandler(sys.stdout),
    ],
)
time_now = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")


# Create an instance of the OpenTronWrapper class
robot = OpenTronWrapper(robot_ip=ROBOT_IP)

# Create labware at each slot on the robot
cartridge_pipette_tips = robot.create_labware(
    location=1,
    load_name="opentrons_96_tiprack_1000ul",
    namespace="opentrons",
    version=1,
)
cartridge_wells = robot.create_labware(
    location=2, load_name="XXX", namespace="opentrons", version=1
)
cartridge_wash_wells = robot.create_labware(
    location=3, load_name="XXX", namespace="opentrons", version=1
)
cartridge_tool_rack = robot.create_labware(
    location=4, load_name="XXX", namespace="opentrons", version=1
)

# Create pipette tool
pipette_tool = robot.create_pipette("p1000_single_gen2", "right")

# Load a pipette tip onto the pipette
robot.pickup_tip(pipette=cartridge_pipette_tips, well="A1")
