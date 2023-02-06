from flask import Flask, render_template, redirect, request
import requests
import json

TOKEN="5626006846:AAFdweDNkQjpsQjQuwlT6_YgHQAyQttKZAs"

# response=requests.get('https://api.telegram.org/bot5626006846:AAFdweDNkQjpsQjQuwlT6_YgHQAyQttKZAs/getme')
app = Flask(__name__)

@app.route('/')
def home():
    response=requests.get('https://api.telegram.org/bot5626006846:AAFdweDNkQjpsQjQuwlT6_YgHQAyQttKZAs/getupdates')
    info = json.loads(response.text)
    chat_id
    new_chat_member = info['result'][0]['message']['new_chat_participant']
    return render_template("index.html", data=new_chat_member)

# @app.route('/updates', methods=['POST'])
# def updates():
#     if request.method == 'POST':
#         information = request.form
#         return render_template("updates.html", data=information)

if __name__=='__main__':
    app.run(debug=True)


