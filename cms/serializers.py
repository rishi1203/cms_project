from rest_framework import serializers
from .models import User, Content, Category

# cms/serializers.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'address', 'city', 'state', 'country', 'pincode', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Password is write-only

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ContentSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'summary', 'document', 'categories', 'author', 'created_at', 'updated_at']
    
    # def validate(self, data):
    #     # Ensure document is a PDF
    #     if 'document' in data and not data['document'].name.endswith('.pdf'):
    #         raise serializers.ValidationError('Document must be a PDF file.')
    #     return data
