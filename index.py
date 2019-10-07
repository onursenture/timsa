#!/usr/bin/env python
from flask import Flask, render_template, request, Response, jsonify
from werkzeug.debug import DebuggedApplication
from flup.server.fcgi import WSGIServer
from mailjet_rest import Client
import os

api_key = 'dba159c451643dee5ba84321fef48a2e'
api_secret = 'ffca52ae3b75a71cc29c6e4ee3cbdb9e'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
app = Flask(__name__, static_url_path="/yatirim/static")
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.debug= True

@app.route('/yatirim/')
def index():
    return render_template('index.html')

@app.route('/yatirim/contact/', methods=["POST"])
def contact():
    form = request.form
    data = {
      'Messages': [
        {
          "From": {
            "Email": "can@orkestra.co",
            "Name": "Can"
          },
          "To": [
            {
              "Email": "isilvaizoglu@yahoo.com",
            }
          ],
          "Subject": form["subject"],
          "HTMLPart": "<p>%s</p><p>%s &lt;%s&gt;</p>"%(form["message"],form["name"],form["email"]),
          "TextPart": "%s\n%s <%s>"%(form["message"],form["name"],form["email"])
        }
      ]
    }
    result = mailjet.send.create(data=data)

    response = {"response": "success" if result.status_code == 200 else "error"}

    return jsonify(response)

if __name__ == '__main__':
    WSGIServer(app).run() 
