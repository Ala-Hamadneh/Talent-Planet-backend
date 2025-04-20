from rest_framework import status
from rest_framework.response import Response
from .models import Users
from .serializers import UserSerializer
from rest_framework.views import APIView

class UserView(APIView):
    def get(self, requist):
        queryset = Users.objects.all()
        serializer_class = UserSerializer
        res= serializer_class(queryset, many=True)
        return Response(res.data,status=status.HTTP_200_OK)
    


   