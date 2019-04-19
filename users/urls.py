from django.conf.urls import url, include

from users.views import UserViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url('', include(router.urls))
]
