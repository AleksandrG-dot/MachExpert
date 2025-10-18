from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # Без namespace="users" и namespace="orders" обращение к ендпоинту в пространстве имен проще, не надо прописывать
    # полный путь, достаточно указать сразу имя конечного ендпоинта.
    path('', include('users.urls')),  # Главная страница и аутентификация.
    path('orders/', include('orders.urls')),  # Все что связано с заказами
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
