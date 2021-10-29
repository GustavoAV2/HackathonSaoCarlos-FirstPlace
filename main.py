from app import create_app
from settings import HOST, PORT

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=HOST,
        port=PORT
    )
