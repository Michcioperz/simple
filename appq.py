#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for, request
import subprocess, queue, time, threading

app = Flask(__name__)

films = queue.Queue()

class Player(threading.Thread):
    def run(self):
        while True:
            if films.empty(): time.sleep(1)
            else:
                subprocess.call(["omxplayer",films.get()])

Player(daemon=True).start()

@app.route("/open")
def vid_open():
    films.put(request.args.get("video_path"))
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
