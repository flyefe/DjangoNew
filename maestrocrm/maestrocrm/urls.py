from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from core.views import index, about
from userprofile.views import signup
# from lead.views import add_lead

urlpatterns = [
    path('sign-up/', signup, name='signup'),
    path('log-in/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('lead/', include('lead.urls')),
    path('about/', about, name='about'),
    path('dashboard/lead', include('lead.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', index, name='index'),
    path('admin/', admin.site.urls),
]