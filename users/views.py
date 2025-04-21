from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from .models import Users
from .serializers import UserSerializer
import jwt, datetime

class RegisterView(APIView):
    """
    Create and register a new user to the system.
    No authentication needed.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    User login view.
    This view handles user authentication and returns a JSON Web Token (JWT) upon successful login.
    """
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        try:
            user = Users.objects.get(email=email)

            if check_password(password, user.password_hash):
                payload = {
                    'id': user.user_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }

                token = jwt.encode(payload, 'secret', algorithm='HS256')

                response = Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data = {
                    "message": "Login Successfully"
                }
                return response
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except Users.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UsersView(APIView):
    """
    List all the users in the system, including their roles and statuses.
    Only admin can do that.
    """
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        try:
            user = Users.objects.get(user_id=payload['id'])
        except Users.DoesNotExist:
            raise AuthenticationFailed("User not found")

        # Check if the user is an admin  
        if user.role.role_id != 1:
            return Response({'error': 'Permission denied. Admins only.'}, status=status.HTTP_403_FORBIDDEN)

        # If admin, return all users
        queryset = Users.objects.all().order_by('user_id')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailsView(APIView):
    """
    Get details of the logged-in user (only their own data).
    Also the admin can view any user's details if they provide the user ID.
    """  
    def get(self, request, pk=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")
        
        try:
            user = Users.objects.get(user_id=payload['id'])
        except Users.DoesNotExist:
            raise AuthenticationFailed("User not found")

        if pk is None:
            return Response({'error': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if int(pk) != payload['id'] and user.role.role_id != 1:
                return Response({'error': 'You are not allowed to access this user\'s data'}, status=status.HTTP_403_FORBIDDEN)

            user = Users.objects.get(user_id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class LogoutView(APIView):
    """
     Handles the user logout process by removing the JWT cookie.
    """
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "Message": "Logout Successfully"
        }
