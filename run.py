from app import create_app
from livereload import Server

app = create_app()

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.watch('static/**/*.html')
    server.watch('static/**/*.*')
    server.serve()
    # app.run(debug=True)
