from api.views import UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register('user', UserViewSet, basename='users')

urlpatterns = router.urls
