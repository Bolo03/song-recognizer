import flask
from flask import request, jsonify, render_template
import requests


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
    with open("response.json", "w") as f:
        f.write(response.text)

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


if __name__ == "__main__":
    app.run(debug=True)
