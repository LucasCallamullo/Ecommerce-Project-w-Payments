

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import get_object_or_404

from users.serializers import *
from users.permissions import IsAdminOrSuperUser
from users.models import CustomUser



class UserRoleEditView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]
    
    def post(self, request):
        # Mejor forma de manejar el error si no existiera el objeto como tal
        try:
            user = get_object_or_404(CustomUser, id=request.data.get("id"))
        except Http404:
            return Response({"success": False, "error": "El Usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRoleSerializer(user, data=request.data, partial=True)
        
        # Devuelve error 400 automático si falla
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data_response = {"success": True, "message": "Rol actualizado correctamente", "data": serializer.data}
        return Response(data_response, status=status.HTTP_200_OK)
            

class RegisterUserView(APIView):
    
    def post(self, request):    
        # When you pass `data=params`, the serializer calls the `validate` methods
        serializer = RegisterLoginSerializer(data=request.data)  
        if serializer.is_valid():  
            # Calling `.save()` triggers the `create()` or `update()` method in the serializer
            user = serializer.save()  # Executes `create()` and returns a `CustomUser` instance
            login(request, user)      # Logs the user into the Django session
            
            # To return the `CustomUser` object as JSON, pass it to the serializer without `data=`.
            # This tells the serializer to serialize the object instead of validating it.
            
            # Prepare the response with data    
            response_data = {
                "user": RegisterLoginSerializer(user).data,
                "message": "Registration successful"
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    View that handles the login of a registered user.

    Receives the form data from "widget_login.html" and validates it using the WidgetLoginSerializer.
    If the data is valid, the user is authenticated and logged in to the Django session.

    On success, it returns a response with the redirect URL and a success message.
    On error, it returns the serializer errors to be displayed to the user.

    **POST Method**
    - Request: `data` (containing the email and password of the user).
    
    - Success Response: A JSON object with:
      - `message`: A message indicating the login was successful.

    - Error Response: 
      - A JSON object with errors as "detail" to handle unsuccessful responses.
    """
    def post(self, request):
        serializer = WidgetLoginSerializer(data=request.data)

        if serializer.is_valid():
            # Get data from the serializer's response
            user = serializer.validated_data["user"]
            message = serializer.validated_data["message"]
            
            login(request, user)  # Log the user into the Django session
            return Response({"message": message}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseView(APIView):
    """
    View that allows a logged-in user to log out.

    **POST Method**
    - Success Response: A JSON object with:
      - `redirect_url`: The URL to which the user will be redirected after logging out.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can log out

    def post(self, request):
        logout(request)  # Log the user out
        # Always return a JSON with a redirect URL to prevent errors
        return Response({"message": "You close the session."}, status=status.HTTP_200_OK)

