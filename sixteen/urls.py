from django.contrib import admin
from django.urls import path, include
from codestar.views import logout_view  # Import the new logout view
from codestar import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('codestar.urls')),
    path('accounts/', include('accounts.urls')),
    path('logout/', logout_view, name='logout'),  # Use the new logout view
]