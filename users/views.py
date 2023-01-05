from django.shortcuts import render
from rest_framework import generics, parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserCreateSerializer


class Register(generics.CreateAPIView):
    """
    Create a user who can create trips
    {
        "email": "bob_marley@gmail.com",
        "first_name": "Bob",
        "last_name": "Marley",
        "phone_no": "123123123"
    }
    """
    serializer_class = UserCreateSerializer
    authentication_classes = []
    permission_classes = []


class ObtainAuthToken(APIView):
    """
    api to login users using email & password
    and return auth Token
    """
    throttle_classes = ()
    permission_classes = [AllowAny]
    authentication_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        # check if username passed is not none and convert to lowercase
        if data.get("username", None) is not None:
            data["username"] = str(data.get("username")).lower()
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'email': user.email,
                         'phone_no': str(user.phone_no)})