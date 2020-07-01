import json
import db_query

def handle_message(bot, recipient_id, message):
    # Check if message is a quick reply
    quick_reply = message.get('quick_reply')
    if quick_reply:
        handle_quick_reply(bot, recipient_id, quick_reply)
        return

    # Welcome message
    resp = "WE ESCAPE xin chào, chúng tôi có thể giúp gì cho bạn?"

    quick_replies_payloads = [
        {
            "content_type": "text",
            "title": "Tìm game để chơi",
            "payload": json.dumps({ 'action' : 'find-games' })
        },
        {
            "content_type": "text",
            "title": "Xem các suất trống",
            "payload": json.dumps({ 'action' : 'find-available-slots' })
        },
        {
            "content_type": "text",
            "title": "Chat với nhân viên",
            "payload": json.dumps({ 'action' : 'cancel' })
        }
    ]

    if message.get('text'):
        bot.send_quick_reply_message(recipient_id=recipient_id, text=resp, quick_replies=quick_replies_payloads)

def handle_postback(bot, recipient_id, postback):
    # Get payload
    payload = json.loads(postback.get('payload'))
    print(recipient_id, payload)

def handle_quick_reply(bot, recipient_id, message):
    # Debug message
    print("Inside quick reply")

    # Get payload
    payload = json.loads(message.get('payload'))
    print(recipient_id, payload)

    action = payload.get('action')

    if action == 'find-games':
        print("Find Games")
        resp = "Bạn muốn chơi ở chi nhánh nào?"

        locations = db_query.get_location_by_city('Hanoi')

        quick_replies_payloads = []

        for location in locations:
            print(location)
            
            tmp_reply = {
                "content_type":"text",
                "title":location,
                "payload":json.dumps({
                    'action': 'find-games-by-location',
                    'location': location
                })
            }

            quick_replies_payloads.append(tmp_reply)
        
        print(bot.send_quick_reply_message(recipient_id=recipient_id, text=resp, quick_replies=quick_replies_payloads ))

    elif action == 'find-games-by-location':
        location = payload.get('location')

        print("Find games by location: ", location)
        resp = "Đây là các games có tại " + location + ":"

        games = db_query.get_games_by_location('Hanoi', location)

        for game in games:
            #print(game)
            resp += "\n" + game

        #print(resp)

        print(bot.send_text_message(recipient_id=recipient_id, message=resp))

    elif action == 'find-available-slots':
        print("Find Available Slots")
    elif action == 'cancel':
        print("Cancel")