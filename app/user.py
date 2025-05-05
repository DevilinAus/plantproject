import flask_login


class User(flask_login.UserMixin):
    pass


# mock database for now
users = {'andrew@abc.com': {'password': '12345'}}