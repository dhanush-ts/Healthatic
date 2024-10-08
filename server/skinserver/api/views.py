from rest_framework.views import APIView
from rest_framework.response import Response
from skinserver.models import User, Hospital
from skinserver.api.Serializer import UserSerializer, HospitalSerializer
from rest_framework import status

class UserListAV(APIView):
    def get(self,request):
        try:
            user = User.objects.all()
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'status':'not found'},status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class Login(APIView):
    def post(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            for i in serializer.data:
                if i['email'] == request.data['email']:
                    if i['password'] == request.data['password']:            
                        return Response(i)
                    return Response({"success": False, "message":"wrong password"})
                return Response({"success": False, "message":"user not found"})
        except User.DoesNotExist:
            return Response({'status':'not found'},status=status.HTTP_404_NOT_FOUND)
        
class HospitalListAV(APIView):
    def get(self, request):
        try:
            hospital = Hospital.objects.all()
            serializer = HospitalSerializer(hospital, many=True)
            return Response(serializer.data)
        except Hospital.DoesNotExist:
            return Response({'status':'not found'},status=status.HTTP_404_NOT_FOUND)
    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HospitalDetailAV(APIView):
    def get(self, request, pk):
        try:
            hospital = Hospital.objects.get(pk=pk)
            serializer = HospitalSerializer(hospital)
            return Response(serializer.data)
        except Hospital.DoesNotExist:
            return Response({'status':'not found'},status=status.HTTP_404_NOT_FOUND)
    