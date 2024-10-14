from rest_framework.views import APIView
from rest_framework.response import Response
from skinserver.models import User, Hospital, History
from skinserver.api.Serializer import UserSerializer, HospitalSerializer, HospitalDeailsSerializer, DiseaseSerializer
from rest_framework import status, generics
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from django.core.files import File

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
            model = load_model('skinserver/api/skin.h5')
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                print("Uploaded File Name:", image_file.name)
                print("Uploaded File Content Type:", image_file.content_type)
                print("Uploaded File Size:", image_file.size)
                print("Is File Empty:", image_file.size == 0)
            else:
                return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)
            def preprocess_image(img):
                img = cv2.imdecode(np.frombuffer(img.read(), np.uint8), cv2.IMREAD_COLOR)  
                img = cv2.resize(img, (150, 150))  
                img = img.astype('float32') / 255.0  
                img = np.expand_dims(img, axis=0)  
                return img
            def predict_top_4_diseases(img):
                class_names1 = ['Healthy', 'Warts', 'Melanoma', 'Atopic', 'Basal', 'Melanocytic','Benign', 'Psoriasis', 'Seborrheic', 'Tinea', 'Acne', 'Vitiligo', 'Chickenpox']
                processed_img = preprocess_image(img)
                predictions = model.predict(processed_img)
                top_4_indices = np.argsort(predictions[0])[-3:][::-1]
                top_4_diseases = [class_names1[i] for i in top_4_indices]
                return top_4_diseases
            image_file = request.FILES['image']
            top_4_diseases = predict_top_4_diseases(image_file)
            data = {
                "disease": str(top_4_diseases),
                "user": int(request.POST.get('user')),
            }
            serializer = DiseaseSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({"top_3_predictions": top_4_diseases}, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
       
        if pk == 2:
                model = load_model('skinserver/api/eye.h5')
                if 'image' in request.FILES:
                    image_file = request.FILES['image']
                    print("Uploaded File Name:", image_file.name)
                    print("Uploaded File Content Type:", image_file.content_type)
                    print("Uploaded File Size:", image_file.size)
                    print("Is File Empty:", image_file.size == 0)
                else:
                    return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)
                def preprocess_image(img):
                    img = cv2.imdecode(np.frombuffer(img.read(), np.uint8), cv2.IMREAD_COLOR)  
                    img = cv2.resize(img, (224, 224))  
                    img = img.astype('float32') / 255.0  
                    img = np.expand_dims(img, axis=0)  
                    return img
                def predict_top_4_diseases(img):
                    class_names1 = ['Cataract', 'Diabetic Retinopathy', 'Glaucoma', 'Normal']
                    processed_img = preprocess_image(img)
                    predictions = model.predict(processed_img)
                    top_4_indices = np.argsort(predictions[0])[-3:][::-1]
                    top_4_diseases = [class_names1[i] for i in top_4_indices]
                    return top_4_diseases
                image_file = request.FILES['image']
                top_4_diseases = predict_top_4_diseases(image_file)
                data = {
                    "disease": str(top_4_diseases),
                    "user": int(request.POST.get('user')),
                }
                serializer = DiseaseSerializer(data = data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"top_3_predictions": top_4_diseases}, status=status.HTTP_200_OK)
                else:
                    print(serializer.errors)

    
class HospitalsFilter(generics.ListAPIView):
    serializer_class = HospitalSerializer
    
    def get_queryset(self):
        disease = self.request.data.get('disease')
        if disease:
            return Hospital.objects.filter(specialties=disease)
        else:
            return Hospital.objects.none()

import json
class HistoryAV(generics.ListAPIView):
    serializer_class = DiseaseSerializer
    
    def get_queryset(self):
        body_unicode = self.request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        
        user = body_data.get('user')
        return History.objects.filter(user=user)