import requests
import json


class OpenTron:
    def __init__(self, robot_ip="127.0.0.1"):
        self.robot_ip = robot_ip
        self.headers = {"opentrons-version": "3"}
        self.runs_url = f"http://{ROBOT_IP}:31950/runs"
        self.run_id = ""
        self.commands_url = f"{runs_url}/{run_id}/commands"
        labware_1_id = ""
        labware_2_id = ""
        pipette_id = ""

    def create_run(self):
        r = requests.post(url=runs_url, headers=self.headers)

        r_dict = json.loads(r.text)
        run_id = r_dict["data"]["id"]
        print(f"Run ID:\n{run_id}")


ROBOT_IP = "127.0.0.1"
HEADERS = {"opentrons-version": "3"}

"""
Manually (for demo purposes) set IDs from run setup
"""
run_id = ""
labware_1_id = ""
labware_2_id = ""
pipette_id = ""

"""
Set up HTTP endpoints
"""
runs_url = f"http://{ROBOT_IP}:31950/runs"
commands_url = f"{runs_url}/{run_id}/commands"


"""
Move commands
"""
# Move to well 1
command_dict = {
    "data": {
        "commandType": "moveToWell",
        "params": {
            "labwareId": labware_1_id,
            "wellName": "A1",
            "wellLocation": {"origin": "top", "offset": {"x": 0, "y": 0, "z": 0}},
            "pipetteId": pipette_id,
        },
        "intent": "setup",
    }
}

command_payload = json.dumps(command_dict)
print(f"Command:\n{command_payload}\n")

r = requests.post(url=commands_url, headers=HEADERS, data=command_payload)

print(f"Response:\n{r}\n{r.text}\n")


# Move to well 2
command_dict = {
    "data": {
        "commandType": "moveToWell",
        "params": {
            "labwareId": labware_2_id,
            "wellName": "A1",
            "wellLocation": {"origin": "top", "offset": {"x": 0, "y": 0, "z": 0}},
            "pipetteId": pipette_id,
        },
        "intent": "setup",
    }
}

command_payload = json.dumps(command_dict)
print(f"Command:\n{command_payload}\n")

r = requests.post(url=commands_url, headers=HEADERS, data=command_payload)

print(f"Response:\n{r}\n{r.text}\n")
