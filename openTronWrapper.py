import requests
import json
import logging
from opentrons import protocol_api

LOGGER = logging.getLogger(__name__)


class OpenTronWrapper:
    def __init__(self, robot_ip="127.0.0.1"):
        """A wrapper for the openTron OT2 HTTP API.

        Args:
            robot_ip (str, optional): IP address of the robot. Defaults to "127.0.0.1".
        """

        self.robot_ip = robot_ip
        self.headers = {"opentrons-version": "3"}
        self.runs_url = f"http://{self.robot_ip}:31950/runs"
        self.run_id = ""
        self.pipette_occupied = False
        self.create_run()

    def check_pipette_occupied(self):
        if self.pipette_occupied:
            LOGGER.error("Pipette is already occupied")
            raise Exception(
                """Pipette is already occupied. Please drop the tool
                before picking up a new one."""
            )

    def create_run(self):
        r = requests.post(url=self.runs_url, headers=self.headers)

        r_dict = json.loads(r.text)
        self.run_id = r_dict["data"]["id"]
        LOGGER.info(f"openTron Run ID:\n{self.run_id}")

        self.create_command_url()

    def create_command_url(self):
        self.commands_url = f"{self.runs_url}/{self.run_id}/commands"

    def create_labware(
        self,
        location: int,
        load_name: str,
        namespace: str = "opentrons",
        version: int = 1,
    ):
        """Load labware into a slot on the robot.

        Args:
            location (int): Slot number on the robot.
            load_name (str): Name of the labware.
            namespace (str, optional): Namespace of the labware. Defaults to "opentrons".
            version (int, optional): Version of the labware. Defaults to 1.

        Returns:
            str: Labware ID.
        """
        command_dict = {
            "data": {
                "commandType": "loadLabware",
                "params": {
                    "location": {"slotName": location},
                    "loadName": load_name,
                    "namespace": namespace,
                    "version": version,
                },
                "intent": "setup",
            }
        }

        command_payload = json.dumps(command_dict)
        LOGGER.info(f"openTron command:\n{command_payload}")

        r = requests.post(
            url=self.commands_url,
            headers=self.headers,
            params={"waitUntilComplete": True},
            data=command_payload,
        )

        r_dict = json.loads(r.text)
        labware_id = r_dict["data"]["result"]["labwareId"]
        LOGGER.info(f"openTron Labware ID:\n{labware_id}\n")

        return labware_id

    def create_pipette(self, pipette_name: str, mount: str):
        """Load a pipette onto the robot.

        Args:
            pipette_name (str): Name of the pipette.
            mount (str): Mount on the robot. Can be either left or right.

        Returns:
            str: Pipette ID.
        """
        command_dict = {
            "data": {
                "commandType": "loadPipette",
                "params": {
                    "pipetteName": pipette_name,
                    "mount": mount,
                },
                "intent": "setup",
            }
        }

        command_payload = json.dumps(command_dict)
        LOGGER.info(f"openTron command:\n{command_payload}")

        r = requests.post(
            url=self.commands_url,
            headers=self.headers,
            params={"waitUntilComplete": True},
            data=command_payload,
        )

        r_dict = json.loads(r.text)
        pipette_id = r_dict["data"]["result"]["pipetteId"]
        LOGGER.info(f"openTron Pipette ID:\n{pipette_id}\n")

        return pipette_id

    def home_robot(self):
        """Home the openTron robot."""
        home_url = f"http://{self.robot_ip}:31950/robot/home"
        command_dict = {"target": "robot"}
        command_payload = json.dumps(command_dict)
        LOGGER.info(f"openTron homing with the command:\n{command_payload}")

        r = requests.post(url=home_url, headers=self.headers, data=command_payload)

        LOGGER.debug(f"openTron response:\n{r}\n{r.text}\n")

    def aspirate(
        self,
        labware_id: str,
        well_name: str,
        volume: float,
        pipette_id: str,
        flow_rate: float = 0.75,
        x_offset: float = 0,
        y_offset: float = 0,
        z_offset: float = 0,
    ):
        """Aspirate a volume of liquid from a well.

        Args:
            labware_id (str): Labware ID.
            well_name (str): Name of the well.
            volume (float): Volume of liquid to aspirate.
            pipette_id (str): Pipette ID.
            flow_rate (float, optional): Flow rate of the liquid.
                Defaults to 0.75.
            x_offset (float, optional): X offset of the well. Defaults to 0.
            y_offset (float, optional): Y offset of the well. Defaults to 0.
            z_offset (float, optional): Z offset of the well. Defaults to 0.
        """
        command_dict = {
            "data": {
                "commandType": "aspirate",
                "params": {
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {
                        "origin": "top",
                        "offset": {"x": x_offset, "y": y_offset, "z": z_offset},
                    },
                    "flowRate": flow_rate,
                    "volume": volume,
                    "pipetteId": pipette_id,
                },
                "intent": "setup",
            }
        }

        command_payload = json.dumps(command_dict)
        LOGGER.info(f"openTron aspirate command:\n{command_payload}")

        r = requests.post(
            url=self.commands_url,
            headers=self.headers,
            data=command_payload,
        )

        LOGGER.debug(f"openTron response:\n{r}\n{r.text}\n")

    def dispense(
        self,
        labware_id: str,
        well_name: str,
        volume: float,
        pipette_id: str,
        flow_rate: float = 0.75,
        x_offset: float = 0,
        y_offset: float = 0,
        z_offset: float = 0,
    ):
        """Dispense a volume of liquid into a well.

        Args:
            labware_id (str): Labware ID.
            well_name (str): Name of the well.
            volume (float): Volume of liquid to dispense.
            pipette_id (str): Pipette ID.
            flow_rate (float, optional): Flow rate of the liquid.
                Defaults to 0.75.
            x_offset (float, optional): X offset of the well. Defaults to 0.
            y_offset (float, optional): Y offset of the well. Defaults to 0.
            z_offset (float, optional): Z offset of the well. Defaults to 0.
        """
        command_dict = {
            "data": {
                "commandType": "dispense",
                "params": {
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {
                        "origin": "top",
                        "offset": {"x": x_offset, "y": y_offset, "z": z_offset},
                    },
                    "flowRate": flow_rate,
                    "volume": volume,
                    "pipetteId": pipette_id,
                },
                "intent": "setup",
            }
        }

        command_payload = json.dumps(command_dict)
        LOGGER.info(f"openTron dispense command:\n{command_payload}")

        r = requests.post(
            url=self.commands_url,
            headers=self.headers,
            data=command_payload,
        )

        LOGGER.debug(f"openTron response:\n{r}\n{r.text}\n")

    def drop_tip(
        self,
        labware_id: str,
        well_name: str,
        pipette_id: str,
        x_offset: float = 0,
        y_offset: float = 0,
        z_offset: float = 0,
    ):
        """Drop a tip into a well.

        Args:
            labware_id (str): Labware ID.
            well_name (str): Name of the well.
            pipette_id (str): Pipette ID.
            x_offset (float, optional): X offset of the well. Defaults to 0.
            y_offset (float, optional): Y offset of the well. Defaults to 0.
            z_offset (float, optional): Z offset of the well. Defaults to 0.
        """
        command_dict = {
            "data": {
                "commandType": "dropTip",
                "params": {
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {
                        "origin": "top",
                        "offset": {"x": x_offset, "y": y_offset, "z": z_offset},
                    },
                    "pipetteId": pipette_id,
                },
                "intent": "setup",
            }
        }

        command_payload = json.dumps(command_dict)
        LOGGER.info(f"openTron drop tip command:\n{command_payload}")

        r = requests.post(
            url=self.commands_url,
            headers=self.headers,
            data=command_payload,
        )

        LOGGER.debug(f"openTron response:\n{r}\n{r.text}\n")

        LOGGER.debug("Setting pipette to unoccupied")
        self.pipette_occupied = False

    def move_to_well(
        self,
        labware_id: str,
        well_name: str,
        pipette_id: str,
        x_offset: float = 0,
        y_offset: float = 0,
        z_offset: float = 0,
    ):
        """Move the pipette to a well.

        Args:
            labware_id (str): Labware ID.
            well_name (str): Name of the well.
            pipette_id (str): Pipette ID.
            x_offset (float, optional): X offset of the well. Defaults to 0.
            y_offset (float, optional): Y offset of the well. Defaults to 0.
            z_offset (float, optional): Z offset of the well. Defaults to 0.
        """
        command_dict = {
            "data": {
                "commandType": "moveToWell",
                "params": {
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {
                        "origin": "top",
                        "offset": {"x": x_offset, "y": y_offset, "z": z_offset},
                    },
                    "pipetteId": pipette_id,
                },
                "intent": "setup",
            }
        }

        command_payload = json.dumps(command_dict)
        LOGGER.info(f"openTron move to well command:\n{command_payload}")

        r = requests.post(
            url=self.commands_url,
            headers=self.headers,
            data=command_payload,
        )

        LOGGER.debug(f"openTron response:\n{r}\n{r.text}\n")

    def delete_run(self):
        """Delete the current run."""
        delete_run_url = f"{self.runs_url}/{self.run_id}"
        r = requests.delete(url=delete_run_url, headers=self.headers)

        LOGGER.info(f"openTron run deleted:\n{r}\n{r.text}\n")

    # TODO Implement pickup tip
    def pickup_tip(self, pipette_id: str, labware_id: str, well_name: str):
        """Pick up a tip from a well.

        Args:
            pipette_id (str): Pipette ID.
            labware_id (str): Labware ID.
            well_name (str): Name of the well, eg. 'A1'.
        """
        # Check if the pipette is already occupied
        self.check_pipette_occupied()

        command_dict = {
            "data": {
                "commandType": "pickUpTip",
                "params": {
                    "pipetteId": pipette_id,
                    "labwareId": labware_id,
                    "wellName": well_name,
                },
                "intent": "setup",
            }
        }

        command_payload = json.dumps(command_dict)
        LOGGER.info(f"openTron pick up tip command:\n{command_payload}")

        r = requests.post(
            url=self.commands_url,
            headers=self.headers,
            data=command_payload,
        )

        LOGGER.debug(f"openTron response:\n{r}\n{r.text}\n")

        LOGGER.debug("Setting pipette to occupied")
        self.pipette_occupied = True

    # TODO Implement trash container

    # TODO Implement pickup_tool and check if the pipette is already occupied
