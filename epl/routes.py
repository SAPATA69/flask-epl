from epl import app

@app.route('/')
def index():
    return "Welcome to EPL Database"

@app.route('/clubs')
def clubs():
    return "List of clubs"