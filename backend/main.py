from os import environ
from flask import render_template
from core.app_factory import create_app

PORT = environ.get('BACKEND_PORT', 8000)
DEBUG = environ.get('DEBUG', True)

app = create_app()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

app.run(extra_files=[], debug=DEBUG, host='0.0.0.0', port=PORT)
