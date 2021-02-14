#!/usr/bin/env python3
from __future__ import unicode_literals
import os
import sys
import youtube_dl
from flask import Flask, request, render_template, send_file
app = Flask(__name__)

@app.route('/')
def form():
  return render_template("form.html")

@app.route('/', methods=['POST'])
def submit():
  download_file(request.form["textInput"])
  return send_file("./output.mp3", as_attachment=True)

class MyLogger(object):
  def debug(self, msg):
      pass

  def warning(self, msg):
      pass

  def error(self, msg):
      print(msg)


def download_file(path):
  os.system("rm -rf output.mp3")
  ydl_opts = { 
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }], 
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'outtmpl': 'output.mp3',
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([path])

def my_hook(d):
  if d['status'] == 'finished':
    print('Done downloading, now converting ...')

if __name__ == "__main__":
  app.run(debug=True)
