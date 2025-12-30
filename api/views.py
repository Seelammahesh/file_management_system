from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Folder, File
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    FolderSerializer,
    FileSerializer
)
import os



@api_view(['GET','POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response(
            {'error': 'Refresh token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Invalid or expired refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_folder(request):
    serializer = FolderSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response({
            'message': 'Folder created successfully',
            'folder': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_folders(request):
    folders = Folder.objects.filter(owner=request.user)
    serializer = FolderSerializer(folders, many=True, context={'request': request})
    
    return Response({
        'count': folders.count(),
        'folders': serializer.data
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    # Check if file is in request
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = FileSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response({
            'message': 'File uploaded successfully',
            'file': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    files = File.objects.filter(owner=request.user)
    
    # Filter by folder if provided
    folder_id = request.query_params.get('folder', None)
    if folder_id:
        files = files.filter(folder_id=folder_id)
    
    serializer = FileSerializer(files, many=True, context={'request': request})
    
    return Response({
        'count': files.count(),
        'files': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, pk):
    try:
        file_obj = File.objects.get(pk=pk)
    except File.DoesNotExist:
        return Response(
            {'error': 'File not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if user is the owner
    if file_obj.owner != request.user:
        return Response(
            {'error': 'You do not have permission to access this file'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Check if file exists
    if not os.path.exists(file_obj.file.path):
        return Response(
            {'error': 'File not found on server'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Return file response
    try:
        response = FileResponse(
            open(file_obj.file.path, 'rb'),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{file_obj.name}"'
        return response
    except Exception as e:
        return Response(
            {'error': f'Error downloading file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)