import json, time
import numpy as np
from google.protobuf import json_format
from generated import types_pb2, level_pb2

def createLevel(data, outputFile):
    level = level_pb2.Level()
    json_format.Parse(data, level)
    with open(outputFile, "wb") as f:
        f.write(level.SerializeToString())

def eulerToQuat(x, y, z):
    roll = np.radians(x)
    pitch = np.radians(y)
    yaw = np.radians(z)

    cy = np.cos(yaw * 0.5)
    sy = np.sin(yaw * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)
    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    return {
        "w": w,
        "x": x,
        "y": y,
        "z": z
    }

grabMap = {
    "formatVersion": 7,
    "title": "Keyframes",
    "creators": ".index BlenderFrames2Grab",
    "description": ".index - Level modding",
    "levelNodes": [],
    "maxCheckpointCount": 10,
    "ambienceSettings": {
        "skyZenithColor": {
            "r": 0.28,
            "g": 0.476,
            "b": 0.73,
            "a": 1
        },
        "skyHorizonColor": {
            "r": 0.916,
            "g": 0.9574,
            "b": 0.9574,
            "a": 1
        },
        "sunAltitude": 45,
        "sunAzimuth": 315,
        "sunSize": 1,
        "fogDDensity": 0
    }
}
delay = 10
with open("data.babylon") as json_file:
    data = json.load(json_file)

meshes = data["meshes"]

length = 0
for mesh in meshes:
    if "animations" in mesh:
        if mesh["ranges"][0]["to"] > length:
            length = mesh["ranges"][0]["to"]

for mesh in meshes:
    position = {
        "x": mesh["position"][0],
        "y": mesh["position"][1],
        "z": mesh["position"][2]
    }
    scale = {
        "x": mesh["scaling"][0] * 2,
        "y": mesh["scaling"][1] * 2,
        "z": mesh["scaling"][2] * 2
    }
    rotation = eulerToQuat(mesh["rotation"][0], mesh["rotation"][1], mesh["rotation"][2])

    levelNode = {
        "levelNodeStatic": {
            "material": 8,
            "shape": 1000,
            "position": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "scale": scale,
            "rotation": {
                "w": 1.0,
                "x": 0,
                "y": 0,
                "z": 0
            },
            "color": {
                "a": 1,
                "r": 0.3,
                "g": 0.3,
                "b": 0.3
            }
        },
        "animations": [
            {
                "frames": [
                    {
                        "position": {},
                        "rotation": {
                            "w": 1.0
                        }
                    },
                    {
                        "position": {},
                        "rotation": {
                            "w": 1.0
                        },
                        "time": delay
                    }
                ],
                "name": "idle",
                "speed": 1
            }
        ]
    }
    if "animations" in mesh:
        rotationAnimation = mesh["animations"][0]
        positionAnimation = mesh["animations"][1]
        lastPos = {}
        lastRot = {}
        lastTime = {}
        for i in range(mesh["ranges"][0]["to"]):
            if i < len(rotationAnimation["keys"]) and i < len(positionAnimation["keys"]):
                rotationFrame = rotationAnimation["keys"][i]["values"]
                positionFrame = positionAnimation["keys"][i]["values"]

                rotation = eulerToQuat(rotationFrame[0], rotationFrame[1], rotationFrame[2])
                position = {
                    "x": positionFrame[0],
                    "y": positionFrame[1],
                    "z": positionFrame[2]
                }

                levelNode["animations"][0]["frames"].append({
                    "position": position,
                    "rotation": rotation,
                    "time": i/48+delay
                })
                lastPos = position
                lastRot = rotation
                lastTime = i/48+delay
                
        levelNode["animations"][0]["frames"].append({
            "position": lastPos,
            "rotation": lastRot,
            "time": length/48+delay*2
        })
        grabMap["levelNodes"].append(levelNode) 

with open("keyframes.json", "w") as outfile:
    json.dump(grabMap, outfile, indent=4)

createLevel(json.dumps(grabMap), f"{int(time.time())}.level")