from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Person
from home.serializers import PeopleSerializer , LoginSerializer , RegisterSerializer

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class LoginAPI(APIView):
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data  = data)
        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        print(serializer.data)
        user = authenticate(username = serializer.data['username'],password = serializer.data['password'])
        if not user :
            return Response({
                'status' : False,
                'message' : 'Invalid Credentials'
            }, status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return Response({'status': True , 'message': 'user login', 'token' : str(token)}, status = status.HTTP_201_CREATED )

class RegisterAPI(APIView):

    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({'status': True , 'message': 'user created'}, status = status.HTTP_201_CREATED )
# Create your views here.
@api_view(['GET','POST'])
def index(request):

        if request.method == 'GET':
            json_response = {
                'name':'Akanksha',
                'courses' : ['c++','python'],
                'method' : 'GET'
            }
        else:
            data = request.data 
            print(data)
            json_response = {
                'name':'Akanksha',
                'courses' : ['c++','python'],
                'method' : 'POST'
            }
        return Response(json_response)
            

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message' : 'success'})

    return Response(serializer.errors)


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        print(request.user)
        objs = Person.objects.filter(color_isnull = False)
        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
        
    
    def post(self,request):
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
      
    
    def put(self,request):
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
    
    def patch(self,request):
        data = request.data
        obj = Person.objects.get(id = data['id'] )
        serializer = PeopleSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request):
        data = request.data
        obj = Person.objects.get(id = data['id'] )
        obj.delete()
        return Response({'message' : 'person deleted'})


@api_view(['GET','POST','PUT', 'PATCH','DELETE'])
def person(request):

    if request.method == 'GET' :
        objs = Person.objects.filter(color_isnull = False)
        serializer = PeopleSerializer(objs, many = True)
        serializer_context = {
            'request':(request),
        }
        context = serializer_context
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'] )
        serializer = PeopleSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    else :
        data = request.data
        obj = Person.objects.get(id = data['id'] )
        obj.delete()
        return Response({'message' : 'person deleted'})
    


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self,request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset.filter(name_startswith = search)

        serializer = PeopleSerializer(queryset, many = True)
        return Response({'status' : 200 , 'data' : serializer.data}, status = status.HTTP_204_NO_CONTENT) 