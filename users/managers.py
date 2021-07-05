from django.contrib.auth.models import UserManager


class MarketerManager(UserManager):
    # def create_user(self, username, password=None, **extra_fields):
    #     if not username:
    #         raise ValueError("username is required...!")
    #     user = self.model(username=username, **extra_fields)
    #     user.set_password(password)
    #     user.save()
    #     return user

    def create_superuser(self, username, password=None, email=None, **extra_fields):
        extra_fields.setdefault('national_id', -1)
        extra_fields.setdefault('company_code', -1)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email=None, password=password, **extra_fields)
