from flask import Flask

application = Flask(__name__)

@application.route('/')
def index():
    return "✅ ¡Mi app Flask está funcionando!"
