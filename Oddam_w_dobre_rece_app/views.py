from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from Oddam_w_dobre_rece_app.models import Donation, Institution, Person


class LandingPageView(View):
    def get(self, request):
        donations = list(Donation.objects.aggregate(Sum('quantity')).values())[0]
        institutions = len(Institution.objects.all())
        foundations = Institution.objects.filter(type="Fundacja")
        ngo = Institution.objects.filter(type="Organizacja pozarządowa")
        local_collection = Institution.objects.filter(type="Zbiórka lokalna")
        return render(request, "index.html", {"donations": donations, "institutions": institutions, "foundations":foundations, "ngo":ngo, "local_collection":local_collection })


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        username = request.POST.get("email")
        if name and surname and email and password and password2 and password == password2:
            new_user = Person.objects.create(name=name, surname=surname, email=email, password=password,
                                           password2=password2, username=username)
            new_user.save()
            return render(request, "login.html", {"new_user": new_user})

