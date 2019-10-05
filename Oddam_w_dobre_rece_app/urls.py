"""Oddam_w_dobre_rece URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from Oddam_w_dobre_rece_app.views import LandingPageView, AddDonationView, LoginView, RegisterView, LogoutView, \
    ProfileView, archive, FormConfirmationView, SettingsView, ChangePasswordView, ContactView

urlpatterns = [
    path('', LandingPageView.as_view(), name="landing_page"),
    path('add_donation/', AddDonationView.as_view(), name="donation"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/<int:id>', ProfileView.as_view(), name="profile"),
    path('archive/<int:id>', archive, name="archive"),
    path('confirmation/', FormConfirmationView.as_view(), name="confirmation"),
    path('profile/<int:id>/settings', SettingsView.as_view(), name="settings"),
    path('profile/<int:id>/settings/password', ChangePasswordView.as_view(), name="password"),
    path('contact/', ContactView.as_view(), name="contact")
]
