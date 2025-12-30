from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Folder, File
import os


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password],style={'input_type': 'password'})
    password2 = serializers.CharField( write_only=True,required=True,style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class FolderSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    file_count = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('id', 'name', 'owner', 'file_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    def get_file_count(self, obj):
        return obj.files.count()

    def validate_name(self, value):
        user = self.context['request'].user
        if self.instance:
            
            if Folder.objects.filter(name=value, owner=user).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("You already have a folder with this name.")
        else:
            
            if Folder.objects.filter(name=value, owner=user).exists():
                raise serializers.ValidationError("You already have a folder with this name.")
        return value


class FileSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    folder_name = serializers.CharField(source='folder.name', read_only=True)
    file_extension = serializers.SerializerMethodField()
    file_size_mb = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = (
            'id', 'name', 'file', 'folder', 'folder_name',
            'owner', 'file_size', 'file_size_mb',
            'file_extension', 'uploaded_at'
        )
        read_only_fields = ('id', 'owner', 'file_size', 'uploaded_at')

    def get_file_extension(self, obj):
        return obj.get_file_extension()

    def get_file_size_mb(self, obj):
        return round(obj.file_size / (1024 * 1024), 2)

    def validate_file(self, value):
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 10MB.")

        # Validate file extension
        ext = os.path.splitext(value.name)[1].lower().replace('.', '')
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )

        return value
    
    # Ensure user owns the folder
    def validate_folder(self, value):
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("You can only upload files to your own folders.")
        return value