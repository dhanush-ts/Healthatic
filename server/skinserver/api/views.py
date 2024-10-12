from rest_framework.views import APIView
from rest_framework.response import Response
from skinserver.models import User, Hospital
from skinserver.api.Serializer import UserSerializer, HospitalSerializer, HospitalDeailsSerializer
from rest_framework import status
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os

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
            serializer = HospitalDeailsSerializer(hospital)
            return Response(serializer.data)
        except Hospital.DoesNotExist:
            return Response({'status':'not found'},status=status.HTTP_404_NOT_FOUND)
        
class PredictAV(APIView):
    def post(self, request, pk):
        if pk == 1:
            print(os.listdir())
            model = load_model('skinserver/api/skin.h5')

            if 'image' not in request.FILES:
                return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

            def preprocess_image(img):
                img = cv2.imdecode(np.frombuffer(img.read(), np.uint8), cv2.IMREAD_COLOR)  
                img = cv2.resize(img, (150, 150))  
                img = img.astype('float32') / 255.0  
                img = np.expand_dims(img, axis=0)  
                return img

            def predict_disease(img):
                processed_img = preprocess_image(img)  
                predictions = model.predict(processed_img)  
                predicted_class = np.argmax(predictions, axis=1) 
                return predicted_class

            image_file = request.FILES['image']
            prediction = predict_disease(image_file)  
            class_names = ['Eczema', 'Warts', 'Melanoma', 'Atopic', 'Basal', 'Melanocytic','Benign', 'Psoriasis', 'Seborrheic', 'Tinea', 'Acne', 'Vitiligo','Chickenpox']

            return Response({"predictions": class_names[int(prediction)]}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid pk."}, status=status.HTTP_400_BAD_REQUEST)