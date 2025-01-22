
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentViewSet, CategoryViewSet, UserViewSet, ObtainCustomTokenPairView, RefreshCustomTokenView, RegisterUser, LoginUser, ContentViewSet, CategoryViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'content', ContentViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    
    path('api/', include(router.urls)),  
    path('api/token/', ObtainCustomTokenPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', RefreshCustomTokenView.as_view(), name='token_refresh'), 
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('api/', include(router.urls)), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)