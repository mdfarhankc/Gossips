from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import include, path


def index(request):
    # signed-in users skip the marketing page and go straight to rooms.
    if request.user.is_authenticated:
        return redirect('rooms')
    return render(request, 'index.html')


urlpatterns = [
    path('', index, name='index'),
    path('', include('accounts.urls')),
    path('rooms/', include('room.urls')),
    path('admin/', admin.site.urls),
]
