from django.contrib import admin
from django.urls import path, include
import HateSpeech.core.views

urlpatterns = [
    #path('admin/', admin.site.urls),
    # padrão
    path('', HateSpeech.core.views.home, name='home'), path('', include('django.contrib.auth.urls')),
]
