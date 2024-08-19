import json
import random

hard = ["problems/cat.json"]
medium = ["problems/star.json"]
easy = ["problems/square.json"]

dummy_name = {"hard": "고양이", "medium": "별", "easy": "사각형"}


def generate_mission(curr_y, curr_x, level):
    json_file = None
    if level == "hard":
        json_file = random.choice(hard)
    elif level == "medium":
        json_file = random.choice(medium)
    else:
        json_file = random.choice(easy)

    json_file = json.load(open(json_file, "r"))
    coords = json_file["coords"]

    coords = [{"y": curr_y + data["y"], "x": curr_x + data["x"]} for data in coords]
    return coords, dummy_name[level]
