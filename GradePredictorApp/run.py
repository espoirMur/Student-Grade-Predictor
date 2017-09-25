import os

from app import create_app

CONFIG_NAME = os.getenv('APP_CONFIG')
app = create_app(CONFIG_NAME)
if CONFIG_NAME != 'development':
    if __name__ == '__main__':
        app.run(debug=True)
else :
    if __name__ == '__main__':
        app.run(host='localhost', port=9874)
