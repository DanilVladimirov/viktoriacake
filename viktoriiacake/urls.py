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
                         addcart)
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
    path('addcart/', addcart, name='addcart')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
