from application import db
from models import User, Post

db.drop_all()
db.create_all()

# input sample data here

test_user_1 = User(username='amberleeshand2',
                   email='amberlee2shand@gmail.com', image_file='')

# add and commit sample data to db here
db.session.add(test_user_1)
db.session.commit()