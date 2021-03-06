"""
Example python app with the Flask framework: http://flask.pocoo.org/
"""

from os import environ
import socket

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           powered_by=environ.get('POWERED_BY', 'google cloud'),
                           hostname=socket.gethostname()
                           )

@app.route('/flask')
def ecs():
    return render_template('index.html',
                           powered_by=environ.get('POWERED_BY', 'ECS'),
                           hostname=socket.gethostname()
                           )


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
