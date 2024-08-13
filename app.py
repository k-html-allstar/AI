from flask import Flask, request, jsonify
from flask_cors import CORS
from mission import generate_mission

app = Flask(__name__)
CORS(app)


@app.route("/mission", methods=["POST"])
def mission():
    # return jsonify({"message": "Mission API"})
    # 전달받은 JSON 데이터를 파싱
    data = request.get_json()
    print("data", data)

    # JSON 데이터 형식에 맞는지 확인
    if (
        not data
        or "latitude" not in data
        or "longitude" not in data
        or "missionLevel" not in data
    ):
        return jsonify({"error": "Invalid data format"}), 400

    # 미션 생성
    coords, mission_name = generate_mission(
        data["latitude"], data["longitude"], data["missionLevel"]
    )

    # 입력 받은 데이터를 그대로 반환
    return jsonify({"missionTitle": mission_name, "coordinates": coords})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)
