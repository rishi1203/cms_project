
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentViewSet, CategoryViewSet, UserViewSet, index, ObtainCustomTokenPairView, RefreshCustomTokenView
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterUser, LoginUser, ContentViewSet, CategoryViewSet
router = DefaultRouter()
router.register(r'content', ContentViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', index, name='index'),  # Frontend index page
    path('api/', include(router.urls)),  # API paths for content, categories, users
    path('api/token/', ObtainCustomTokenPairView.as_view(), name='token_obtain_pair'),  # Obtain JWT tokens
    path('api/token/refresh/', RefreshCustomTokenView.as_view(), name='token_refresh'), 
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('api/', include(router.urls)), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)