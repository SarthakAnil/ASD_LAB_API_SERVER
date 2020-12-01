
# A very simple Flask Hello World app for you to get started with...

from config import app


@app.route('/')
def hello_world():
    return 'Hello from Flask!'

