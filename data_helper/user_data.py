from user import User

users = [
    User(1, 'bob', 'asdf'),
    User(2, 'siri', 'asdf'),
    User(3, 'kate', 'asdf'),
    User(4, 'james', 'asdf'),
    User(5, 'esther', 'asdf')
]

username_mapping = {user.username: user for user in users}
userid_mapping = {user.id: user for user in users}