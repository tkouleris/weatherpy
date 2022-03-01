import re
from app.models import User


class RegisterValidator(object):
    def __init__(self, response={}):
        self.response = response

    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Password Restriction
    # ------------------------
    # At least 8 chars
    # Contains at least one digit
    # Contains at least one lower alpha char and one upper alpha char
    # Contains at least one char within a set of special chars (@#%$^ etc.)
    # Does not contain space, tab, etc.
    password_regex = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\S+$).{8,20}'

    def validate(self):

        error_messages = []

        email = self.response.get("email", None)
        if not email or not re.fullmatch(self.email_regex, email):
            error_messages.append("Email is empty or not valid")

        email = self.response.get("email", None)
        user_exists = User.query.filter_by(email=email).first()
        if user_exists is not None:
            error_messages.append("User with this email exists")

        username = self.response.get("username", None)
        if not username or len(username) < 5:
            error_messages.append("Username empty or less than 5 characters")

        password = self.response.get("password", None)
        if not password or not re.findall(self.password_regex, password):
            error_messages.append("Password empty or not valid")

        return error_messages