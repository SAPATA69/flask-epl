from epl import app, db
from epl import models

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    app.run(debug=True, host='127.0.0.1', port=5000)