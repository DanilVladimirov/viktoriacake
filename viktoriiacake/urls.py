from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from cakes.views import (start_page,
                         add_cake,
                         view_cakes,
                         create_cake,
                         cart_page,
                         cake_details,
                         remover_session,
                         buy_page,
                         orders_page,
                         addcart,
                         add_to_wishlist,
                         del_from_wishlist,
                         profile_page,
                         login_page,
                         registration_page,
                         logout_page)
from viktoriiacake import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_page, name='start_page'),
    path('addcake/', add_cake, name='add_cake'),
    path('cakes/', view_cakes, name='cakes'),
    path('createcake/', create_cake, name='create_cake'),
    path('cart/', cart_page, name='cart_page'),
    path('details/<int:cid>/', cake_details, name='cake_details'),
    path('remove/', remover_session),
    path('buy/', buy_page, name='buy_page'),
    path('orders/', orders_page, name='orders_page'),
    path('addcart/', addcart, name='addcart'),
    path('add_wishlist/', add_to_wishlist, name='add_wishlist'),
    path('del_wishlist/', del_from_wishlist, name='del_wishlist'),
    path('profile/', profile_page, name='profile_page'),
    path('login/', login_page, name='login_page'),
    path('register/', registration_page, name='register_page'),
    path('logout/', logout_page, name='logout_page')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
