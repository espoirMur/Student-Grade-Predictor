import os

from app import create_app

CONFIG_NAME = os.getenv('APP_CONFIG')
app = create_app(CONFIG_NAME)
if CONFIG_NAME != 'development':

    app.run(debug=True, host='0.0.0.0')
else :
    if __name__ == '__main__':
        app.run(host='localhost', port=9874)
