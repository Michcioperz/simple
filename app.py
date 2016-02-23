from flask import Flask, render_template, redirect, url_for, request
import subprocess

app = Flask(__name__)

player = None

@app.route("/open")
def vid_open():
    player = subprocess.Popen(["omxplayer",request.args.get("video_path")])
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
