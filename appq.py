#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for, request
import subprocess, queue, time, threading

app = Flask(__name__)

KEYMAP = {"left": "\x1B[D", "right": "\x1B[C", "up": "\x1B[A", "down": "\x1B[B"}

films = queue.Queue()

class Player(threading.Thread):
    def send_key(self, key):
        try:
            self.backend.stdin.write(KEYMAP.get(key, key))
            self.backend.stdin.flush()
        except:
            print(repr(key), "didn't stdin well")
    def run(self):
        while True:
            if films.empty(): time.sleep(1)
            else:
                self.backend = subprocess.Popen(["omxplayer",films.get()], stdin=subprocess.PIPE, universal_newlines=True)
                self.backend.wait()

player = Player(daemon=True)
player.start()

@app.route("/open")
def vid_open():
    films.put(request.args.get("video_path"))
    return redirect(url_for("home"))

@app.route("/control")
def vid_control():
    player.send_key(request.args.get("key"))
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
