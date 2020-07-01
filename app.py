import os
import json
import flask
from flask import Response,request

import db
import db_query
import bot
import bookeo
import fb_handler

#------ READ VAR FROM env file -----------
from dotenv import load_dotenv
load_dotenv()

BOOKEO_API_SECRET_KEY = os.getenv("BOOKEO_API_SECRET_KEY")
BOOKEO_API_TOKEN_KEY = os.getenv("BOOKEO_API_TOKEN_KEY")
BOOKEO_API_BASE_URL = os.getenv("BOOKEO_API_BASE_URL")

FB_VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

#-------- Init FB bot ---------------------
bot = bot.init_bot(FB_PAGE_ACCESS_TOKEN)

#-------- Init Flask app ------------------
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#-------- App Route -----------------------
@app.route('/webhook', methods=['GET'])
def webhook_get():
    # Check if data is correct
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode=='subscribe' and token == FB_VERIFY_TOKEN :
        resp = Response(challenge, status=200)
        return resp
    else:
        return Response(status=403)

@app.route('/webhook', methods=['POST'])
def webhook_post():
    # Get payload
    payload = request.get_json()
    print(payload)

    if payload['object'] == 'page':
        for entry in payload['entry']:

            # Extract webhook event
            webhook_event = entry['messaging'][0]
            print(webhook_event)

            # Get sender id
            sender_pid = webhook_event['sender']['id']

            if webhook_event.get('message'):
                fb_handler.handle_message(bot, sender_pid, webhook_event['message'])
            elif webhook_event.get('postback'):
                fb_handler.handle_postback(bot, sender_pid, webhook_event['postback'])

            return Response('EVENT RECEIVED', status=200)
    else:
        return Response(status=404)

    return Response(status=403)


if __name__ == "__main__":
    print("Init Database")
    db.init_db()

    print("Fetching games from Bookeo")
    bookeo.fetch_games(BOOKEO_API_SECRET_KEY, BOOKEO_API_TOKEN_KEY, BOOKEO_API_BASE_URL)

    # Start app
    app.run()