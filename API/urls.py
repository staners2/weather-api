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
    path('api/languages', views.get_all_languages, name="get_all_languages"),
    path('api/cities', views.get_all_cities, name="get_all_cities"),
    path('api/userprofile/<int:userprofile_id>/language', views.update_language, name="update_language"),
    path('api/userprofile/<int:userprofile_id>/histories', views.show_histories, name="show_histories"),
    path('api/userprofile/<int:userprofile_id>/histories/<int:history_id>', views.delete_histories, name="delete_histories"),
    path('api/userprofile/weather/<str:city_name>', views.get_weather, name="get_weather"),
]

'''
    path('api/userprofile/fact/<str:type>/<int:number>', views.get_fact_by_type, name="get_fact_by_type"),
'''

# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)