from django.shortcuts import render
from rest_framework import generics
from .models import Device
from .serializer import DeviceSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.http import HttpResponse
import subprocess

import re
import sys
import json
# Create your views here.

class subAPI(APIView):

    def get(request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if pk:

            snmpRequest = Device.objects.in_bulk([pk])
            deviceIP = snmpRequest[pk].ip

    #  with open('ATOMdata.txt', 'w') as f:

    #     subprocess.run(["snmpwalk", "-v2c", "-c", "public", deviceIP , ".1.3.6.1.4.1.42024"], stdout=f)

         

        with open("ATOMdata.txt") as file:
            lines = file.readlines()
          

        with open("ann.txt") as file:
            annotations = file.readlines()
      
       
        dataJSON = {'pare': []}
        i = 0

        while i < len(lines):
            entry = lines[i]
            ans = re.findall(r'(?<=: ).+', entry)
            stringer = ''.join(ans).replace('"', '')
            ans = annotations[i].strip()
            
            dataJSON['pare'].append({'title': f'{ans}', 'value': f'{stringer}'})
            i += 1

        
        return Response({'post': dataJSON})


    def post(self, request):
        
        
        serilizer = DeviceSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()

        if DeviceSerializer:

            toWrite = str(serilizer.data)
            my_file = open("BabyFile.txt", "w+")
            my_file.write(toWrite)
            my_file.close()

        return Response({'post': serilizer.data})


    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
                return Response({"error:Method put not allowed"})

        try:

            instance = Device.objects.get(pk=pk)

        except:

            return Response({"error:Object does not exists"})

        serializer = DeviceSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(instance)
        return Response({'posts': serializer.data})

def index(request):
    data = {"header": "hi", "message": "Welcome to Python"}
    return render(request, "index.html", context=data)