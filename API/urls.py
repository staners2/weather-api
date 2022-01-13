from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('api/auth/registration', views.registration, name='registration'),
    path('api/auth/login', views.login, name='login'),
    path('api/countries', views.get_all_countries, name="get_all_countries"),
    path('api/types', views.get_all_types, name="get_all_types"),
    path('api/userprofile/<int:userprofile_id>/country', views.update_country, name="update_country"),
    path('api/userprofile/<int:userprofile_id>/histories', views.show_histories, name="show_histories"),
    path('api/userprofile/<int:userprofile_id>/histories/<int:history_id>', views.delete_histories, name="delete_histories"),
    path('api/userprofile/fact/random/<str:type>', views.get_random_fact, name="get_random_fact"),
    path('api/userprofile/fact/<str:type>/<int:number>', views.get_fact_by_type, name="get_fact_by_type"),
]

# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)