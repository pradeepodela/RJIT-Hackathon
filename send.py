import telepot
bot = telepot.Bot('5387743236:AAFo6ffXGbaIrZjxzZwTOK4uRKnOG5aYFy0')


def senddata(img,data):
    # here replace chat_id and test.jpg with real things
    bot.sendPhoto(5053711674, photo=open(img, 'rb'))
    bot.sendMessage(5053711674, data)