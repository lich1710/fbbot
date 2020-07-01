import os
from pymessenger.bot import Bot

def send_quick_reply_message(self, recipient_id, text, quick_replies):
    """Send quick replies to the specified recipient.
    https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
    Input:
        recipient_id: recipient id to send to
        text: text of message to send
        quick_replies: quick replies to send
    Output:
        Response from API as <dict>
    """
    payload = {
        'recipient': {
            'id': recipient_id
        },
        "messaging_type": "RESPONSE",
        'message': {
            'text': text,
            'quick_replies': quick_replies
        }
    }
    return self.send_raw(payload)

def init_bot(PAGE_ACCESS_TOKEN):
    setattr(Bot, 'send_quick_reply_message', send_quick_reply_message)
    bot = Bot(PAGE_ACCESS_TOKEN)
    
    return bot