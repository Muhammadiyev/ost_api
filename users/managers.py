from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user_admin(self, username, password=None, is_staff=True):
        if not username:
            raise ValueError('users must have a username number')
        if not password:
            raise ValueError('user must have a username password')

        user_obj = self.model(username=username)
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.save(using=self._db)
        return user_obj

    def _create_user(self, username, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)


    def create_superuser(self, username, password=None):
        user = self.create_user_admin(
            username,
            password=password,
            is_staff=True,
            )