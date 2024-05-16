import flask
from flask import request, render_template
from werkzeug.utils import secure_filename
import requests


app = flask.Flask(__name__)


# * This is the main page of the website
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# * This is the page for text search, it will be displayed when the song is found
@app.route("/text_search", methods=["POST"])
def text_search():
    # url for the first api
    url = "https://shazam.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": "ff7711ae85msh7c32a1d09f8b33ap1c2075jsn58e69dd603d5",
        "X-RapidAPI-Host": "shazam.p.rapidapi.com",
    }

    # get data from html form
    data = request.form["data"]

    # if user clicks on sumbit button without entering any data
    if data == "":
        return render_template("error.html")

    querystring = {
        "term": data,
        "locale": "en-US",
        "offset": "0",
        "limit": "5",
    }

    # get the response from the api
    response = requests.get(url, headers=headers, params=querystring)

    # check if the response is empty else take the data from the response
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


# * This is the page for file search, it will be displayed when the song is found
@app.route("/file_search", methods=["POST"])
def file_search():
    # url for the 2nd api
    url = "https://api.audd.io/"

    data = {
        "api_token": "3091d8a2b76a6729160c29d6420f881c",
        "return": "apple_music,spotify",
    }

    f = request.files["file"]

    # if user clicks on sumbit button without uploading the sample
    if f.filename == "":
        return render_template("error.html")

    # save the file to send to api
    f.save("mp3/" + secure_filename(f.filename))
    name = "mp3/" + secure_filename(f.filename)

    files = {
        "file": open(name, "rb"),
    }
    result = requests.post(url, data=data, files=files)

    # check if the response is empty else take the data from the response
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
