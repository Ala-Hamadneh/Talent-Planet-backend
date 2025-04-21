from rest_framework import status
from rest_framework.response import Response
from .models import Users
from .serializers import UserSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password



class UsersView(APIView):
    # list all the users
    def get(self, request):
        queryset = Users.objects.all().order_by('user_id')
        serializer_class = UserSerializer
        res= serializer_class(queryset, many=True)
        return Response(res.data,status=status.HTTP_200_OK)
    # list user details
    def get(self, request, pk=None):
        if pk is None:
            return Response({'error': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Users.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    # # create a new user
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    # User login view
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = Users.objects.get(email=email)
            if check_password(password , user.password_hash):
                serializer = UserSerializer(user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Users.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    


   