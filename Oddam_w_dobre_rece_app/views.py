from django.db.models import Count, Sum
from django.shortcuts import render
from django.views import View

from Oddam_w_dobre_rece_app.models import Donation, Institution


class LandingPageView(View):
    def get(self, request):
        donations = list(Donation.objects.aggregate(Sum('quantity')).values())[0]
        institutions = len(Institution.objects.all())
        return render(request, "index.html", {"donations": donations, "institutions": institutions})


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")