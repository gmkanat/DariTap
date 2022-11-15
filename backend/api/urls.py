from api.views import *
from rest_framework import routers

router = routers.SimpleRouter()

router.register('user', UserViewSet, basename='users')
router.register('items', ItemViewSet, basename='items')
router.register('categories', CategoryViewSet, basename='categories')
router.register('wishlist', WishlistViewSet, basename='wishlists')


urlpatterns = router.urls
