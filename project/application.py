from my_blog import create_app

app = create_app()

if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
