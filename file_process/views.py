# curl -X PUT -H "Content-Disposition: attachment; filename=a.jpeg;" -F file=@a.jpeg http://127.0.0.1:8000/upload/


from django.shortcuts import render
# Create your views here.
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from PIL import Image
from .serializers import FileSerializer
import sys
from django.conf import settings

sys.path.insert(0, '../image_process')
from image_process import process


class ImageUploadParser(FileUploadParser):
    media_type = 'image/*'


class FileUploadView(APIView):
    parser_class = (ImageUploadParser,)

    def put(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        try:
            img = Image.open(f)
            img.verify()

            file_serializer = FileSerializer(data=request.data)

            if file_serializer.is_valid():
                file_serializer.save()
                file_name = file_serializer.data['file'].split('/')[-1]
                full_file_name = settings.MEDIA_ROOT+'/'+file_name
                # print(full_file_name)
                value = process(full_file_name)
                # print("Values " , value)
                return Response(value, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            raise ParseError("Unsupported image type")
