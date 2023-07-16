SECRET_KEY = "asdfasdfgjfgjhgjhdr"

# database config info
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'qa_platform_schema'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# mail config
MAIL_SERVER = "smtp.gmail.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "yixiongsheng@gmail.com"
MAIL_PASSWORD = "the_generated_app_password_for_windows_computer"
MAIL_DEFAULT_SENDER = "yixiongsheng@gmail.com"
