import flask
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
import requests
import os


app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/text_search", methods=["POST"])
def text_search():
    # get data from html form
    data = request.form["data"]
    # do something with data

    url = "https://shazam.p.rapidapi.com/search"

    querystring = {
        "term": data,
        "locale": "en-US",
        "offset": "0",
        "limit": "5",
    }

    headers = {
        "X-RapidAPI-Key": "ff7711ae85msh7c32a1d09f8b33ap1c2075jsn58e69dd603d5",
        "X-RapidAPI-Host": "shazam.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    # check if the response is empty
    if response.json() == {}:
        return render_template("error.html")
    else:
        name = response.json()["tracks"]["hits"][0]["track"]["share"]["subject"]
        shazam_url = response.json()["tracks"]["hits"][0]["track"]["share"]["href"]
        image = response.json()["tracks"]["hits"][0]["track"]["share"]["image"]
        apple_music_url = response.json()["tracks"]["hits"][0]["track"]["hub"][
            "options"
        ][0]["actions"][0]["uri"]

        json = {
            "name": name,
            "shazam_url": shazam_url,
            "image": image,
            "apple_music_url": apple_music_url,
        }

        return render_template("text.html", json=json)


@app.route("/file_search", methods=["GET", "POST"])
def file_search():
    if request.method == "POST":
        f = request.files["file"]
        f.save("mp3/" + secure_filename(f.filename))

        name = "mp3/" + secure_filename(f.filename)

    data = {
        "api_token": "3091d8a2b76a6729160c29d6420f881c",
        "return": "apple_music,spotify",
    }
    files = {
        "file": open(name, "rb"),
    }
    result = requests.post("https://api.audd.io/", data=data, files=files)

    with open("audd.json", "w") as f:
        f.write(result.text)

    # check if the response is empty: {"status":"success","result":null}
    if result.json()["result"] is None:
        return render_template("error.html")
    else:
        name = result.json()["result"]["title"]
        artist = result.json()["result"]["artist"]
        name = name + " - " + artist.upper()

        link = result.json()["result"]["song_link"]
        image = result.json()["result"]["spotify"]["album"]["images"][0]["url"]

        json = {
            "name": name,
            "link": link,
            "image": image,
        }

    return render_template("file.html", json=json)


if __name__ == "__main__":
    app.run(debug=True)
