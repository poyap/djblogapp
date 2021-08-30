"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from django.conf.urls.static import static
from django.conf import settings
from articles.views import contact_form_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('articles.urls')),
    path('about/',contact_form_view, name='about-view'),
        path('password-reset/', auth_views.PasswordResetView.as_view(template_name='articles/password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='articles/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='articles/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='articles/password_reset_complete.html'), name='password_reset_complete'),
]


#  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) it is for cdn(for development)