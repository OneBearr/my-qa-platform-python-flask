import config
from flask import Flask, session, g
from extensions import db, mail
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from models import UserModel
from flask_migrate import Migrate

app = Flask(__name__)
# bind config file
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# flask db init：only needs to be executed once
# flask db migrate：Generate a migration script for the ORM model
# flask db upgrade：Map the migration script into the database

# before_request/ before_first_request/ after_request
# hooks
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)    # g: global
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}     # so this "user" can be used in any template

if __name__ == '__main__':
    app.run()

# what I've learnt
# url parameter passing
# Sending emails
# ajax
# orm and databases
# Jinja2 template
# cookie and session
# Keyword search