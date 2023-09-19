from django.contrib.auth.models import BaseUserManager


class ModUserManager():
    """Mode User Custom Manager"""

    # Contains already two functions
    # 1.- create_user
    # rock -> 123456#
    def create_user(self, email, user_name, first_name, password, **other_fields):
        """Overwriting create_user func for ModeUserManager."""

        # Adding some validations
        if not email:
            raise ValueError("Must provide an email....")

        # Normalizing info
        email = self.normalize_email(email)

        user = self.model(email=email,
                          user_name=user_name,
                          first_name=first_name,
                          #password=password, remove it or password would be store as plain text
                          **other_fields
                          )
        # Proceed to store password encrypted
        user.set_password(password)

        # Save user on DB
        user.save()
        return user



    # 2.- create_superuser
    # admin -> 123456# -> createsuperuser
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        """Overwriting create_superuser func for ModUsermManger."""
        # is_staff -> True
        # is_active -> True
        # i_superuser -> True
        other_fields.setdefault("is_staff", True) # Setting field is_staff -> True
        other_fields.setdefault("is_active", True)  # Setting field is_staff -> True
        other_fields.setdefault("is_superuser", True)  # Setting field is_superuser -> True

        # Creating superuser using the previous written function
        return self.create_user(email, user_name, first_name, password, **other_fields)

