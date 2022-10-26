import hashlib

from dao.model.user import User
from dao.user import UserDAO
from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        user = User(**data)

        user.password = self.get_hash(user.password)

        return self.dao.create(user)

    def update(self, data):
        uid = data["id"]
        user = self.get_one(uid)

        user.role = data["role"]
        user.username = data["username"]
        user.password = self.get_hash(data["password"])

        return self.dao.update(user)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def compare_passwords(self, hash_password, other_password):
        other_hash = self.get_hash(other_password)
        return hash_password == other_hash
