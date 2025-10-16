from flask import Flask
from models import db
from routes import routes
import config
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)
    
    app.register_blueprint(routes)



    migrate = Migrate(app,db)   ## python -m flask db init
    ## flask db migrate -m "Initial migration"

  

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    
