from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def main():
    return "I'm playing Unital Ring"


def run():
    app.run()


def keep_alive():
    server = Thread(target=run)
    server.start()