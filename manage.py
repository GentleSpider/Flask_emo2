from flask_script import Manager, Shell
from app import create_app, db
from flask_migrate import MigrateCommand,Migrate
from app.model import *


app = create_app(config_name='development')
migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command("db",MigrateCommand)

#创建数据库脚本
@manager.command
def create_db():
    db.create_all()

if __name__ == '__main__':
    manager.run()

