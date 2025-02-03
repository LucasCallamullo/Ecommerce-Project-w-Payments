

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

CustomUser = get_user_model()

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class RegisterLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    cellphone = serializers.CharField()
    province = serializers.CharField()
    address = serializers.CharField()

    def validate_email(self, value):
        """Ensures the email has a valid format and is not already in use."""
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("El correo electrónico no es válido.")
        
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        
        return value

    def validate_password(self, value):
        """Applies Django's password validation rules for security."""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, data):
        """Ensures that required fields are not empty."""
        required_fields = ["first_name", "last_name", "cellphone", "province", "address"]
        for field in required_fields:
            if not data.get(field, "").strip():
                raise serializers.ValidationError({field: "Este campo no puede estar vacío."})
        return data

    def create(self, validated_data):
        """Creates a new user using the validated data."""
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            cellphone=validated_data["cellphone"],
            province=validated_data["province"],
            address=validated_data["address"]
        )
        return user


class WidgetLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates the user-provided data to authenticate the user and provide feedback.

        Args:
            data (dict): Contains the data received as JSON from the form.

        Raises:
            AuthenticationFailed: Raised if the email does not exist in the system.
            AuthenticationFailed: Raised if the email exists, but the password is incorrect.

        Returns:
            dict: 
                - 'message' (str): A success message to show if login is successful.
                - 'redirect_url' (str): The URL to redirect to after logging in.
                - 'user' (CustomUser): The authenticated user object to log the user into the Django session.
        """
        
        email = data.get("email")
        password = data.get("password")

        # Try to authenticate the user
        user = authenticate(email=email, password=password)

        if not user:
            # These errors can be accessed later through "data.detail"
            if not CustomUser.objects.filter(email=email).exists():
                raise AuthenticationFailed("The email address is not registered.")

            raise AuthenticationFailed("Invalid password, please check your credentials.")

        return {
            "message": "Login successful!",
            "user": user
        }

