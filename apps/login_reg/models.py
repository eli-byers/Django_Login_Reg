from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]')
PASSWORD_REGEX = re.compile(r'.*[69p].?[4a@].?[s25$].?[s25$].?[3w^].?[o0*].?[r72].?[69d].*')

# ============================================================
#                           USER
# ============================================================

class Manager(models.Manager):
    def login(self, post):
        email = post['email'].strip().lower()
        password = post['password'].strip()
        valid = True

        if not EMAIL_REGEX.match(email) or not 8 <= len(password) <= 15:
            valid = False

        if valid:
            user = User.objects.filter(email = email)
            if user:
                hashed = user[0].password
                if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed:
                    result = { 'status': True, 'user_id': user[0].id}
                    return result

        errors = [{'message': 'Invalid login information', 'tag': 'login'}]
        result = { 'status': False, 'errors': errors }
        return result

    def registerUser(self, post):
        name = post['name'].strip()
        email = post['email'].strip().lower()
        password = post['password']
        password_confirm = post['passwordConfirm']
        errors = []

        # name
        if not 2 <= len(name) <= 30:
            error = {'message': 'Must be 2-30 characters', 'tag': 'name'}
            errors.append(error)
        # email
        if not email:
            error = {'message': 'Email cannot be blank', 'tag': 'email'}
            errors.append(error)
        elif not EMAIL_REGEX.match(email):
            error = {'message': 'Invalid email address', 'tag': 'email'}
            errors.append(error)
        # password
        if not 8 <= len(password) <= 15:
            print "no pass"
            error = {'message': 'Must be 8-15 characters', 'tag': 'password'}
            errors.append(error)
        elif password != password_confirm:
            print "dont match"
            error = {'message': 'Passwords must match', 'tag': 'password'}
            errors.append(error)
        else:
            badPassword = password.strip().lower()
            print "bad", password, PASSWORD_REGEX.match("password")
            if PASSWORD_REGEX.match(badPassword):
                error = {'message': 'Password is insecure', 'tag': 'password'}
                errors.append(error)

        print errors
        #if login form has no errors then check password and set session id.
        if not errors:
            emailExists = User.objects.filter(email = email)
            if not emailExists:
                passwordHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                new_user = User.objects.create(
                    name = name,
                    email = email,
                    password = passwordHash,
                )
                result = { "status": True, "user_id": new_user.id }
                return result
            else:
                error = {'message': 'Invalid email address', 'tag': 'email'}
                errors.append(error)

        result = { "status": False, "errors": errors }
        return result

class User(models.Model):
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Manager()
