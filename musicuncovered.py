from flask import Flask, jsonify
import os

app = Flask(__name__)
print(__name__)

print("test")


@app.route("/", methods=["GET"])
def get_songs():
    return jsonify(os.environ.get("SPOTIFY_CLIENT_ID"))
