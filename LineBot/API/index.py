from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('hcEpZOqwBDZdCxINNGL3YU3Ak6ZcljLD2MdtdeipKIyfJhi81dpvjwaMTbEsUO4W6zxWYyto0+afaSl/XkgJ8UZz3bPO1aUrNCDRG1BOhwMbD080u7F0i1nv/NF2ocsvue1DH2QQ7zW08Hm21WbQygdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('741a575967ca36b921fca16c7bcc1f1b')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()