import docker
from flask import Flask, jsonify, request

app = Flask(__name__)

client = docker.from_env()
incomes = []


@app.route("/images")
def get_images():
    images = [{"id": image.short_id, "tags": "-".join(image.attrs["RepoTags"])} for image in client.images.list()]
    return jsonify(images)


@app.route("/containers")
def get_containers():
    containers = [
        {"id": container.short_id, "name": container.name, "status": container.status}
        for container in client.containers.list(all=True)
    ]
    return jsonify(containers)


@app.route("/containers/run", methods=["POST"])
def run_container():
    payload = request.get_json()
    container_id = payload.get("id")
    if not container_id:
        return jsonify({"message": "Missing id"}), 400

    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound:
        return jsonify({"message": "Container not found"}), 404

    container.start()
    return jsonify({"message": "Container started"}), 200


@app.route("/containers/stop", methods=["POST"])
def stop_container():
    payload = request.get_json()
    container_id = payload.get("id")
    if not container_id:
        return jsonify({"message": "Missing id"}), 400

    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound:
        return jsonify({"message": "Container not found"}), 404

    container.stop()
    return jsonify({"message": "Container stopped"}), 200
