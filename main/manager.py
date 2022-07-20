from django.contrib.auth.models import BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, username, email, account_type="user", firstName=None, secondName=None, password=None,
                    is_admin=False, is_active=False):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not username:
            raise ValueError("User must have a username")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.firstName = firstName
        user.secondName = secondName
        user.username = username
        user.account_type = account_type
        user.set_password(password)  # change password to hash
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.admin = True
        user.active = True
        user.username = username
        user.account_type = "admin"
        user.save(using=self._db)
        user.is_superuser = True
        return user
