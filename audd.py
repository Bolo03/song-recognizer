import requests

data = {
    "api_token": "3091d8a2b76a6729160c29d6420f881c",
    "return": "apple_music,spotify",
}
files = {
    "file": open("./mp3/test.mp3", "rb"),
}
result = requests.post("https://api.audd.io/", data=data, files=files)

with open("audd.json", "w") as f:
    f.write(result.text)
