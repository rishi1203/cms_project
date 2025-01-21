from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import User, Content, Category
from .serializers import UserSerializer, ContentSerializer, CategorySerializer
from .permissions import IsAdminOrAuthor, IsOwnerOrAdmin
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


# Frontend View for rendering index.html
def index(request):
    return render(request, 'cms/index.html')


# User API ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Example permission for user management


# Content API ViewSet
class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrAuthor, IsOwnerOrAdmin]

    # Custom queryset based on user role
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Content.objects.all()
        return Content.objects.filter(author=user)

    # Ensure the content is created by the authenticated user (author)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Search functionality (search in title, body, summary, or category name)
    def search(self, request):
        query = request.query_params.get('q', '')
        results = Content.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(summary__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)


# Category API ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# Custom View for obtaining Access and Refresh Tokens
class ObtainCustomTokenPairView(APIView):
    """
    Custom view to issue access and refresh tokens using email and password.
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Create refresh and access tokens for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                "access": access_token,
                "refresh": refresh_token
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# Custom View to Refresh Access Token
class RefreshCustomTokenView(APIView):
    """
    Custom view to refresh the access token using the refresh token.
    """
    def post(self, request):
        refresh_token = request.data.get("refresh")

        try:
            # Use the refresh token to obtain a new access token
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({
                "access": access_token
            })
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        

class RegisterUser(APIView):
    def post(self, request):
        # Create a new User instance from the request data
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # Create the user and set the password correctly
            user = serializer.save()
            user.set_password(request.data["password"])  # Hash the password
            user.save()  # Save the user with the hashed password
            
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUser(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                "access": access_token,
                "refresh": refresh_token
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
