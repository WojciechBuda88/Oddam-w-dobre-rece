from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View

from Oddam_w_dobre_rece_app.models import Donation, Institution, Category


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
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, "form.html", {"categories":categories, "institutions":institutions})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post (self, request):
        user_login = request.POST.get("email")
        user_password = request.POST.get("password")
        user = authenticate(username=user_login, password=user_password)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return redirect("register")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, "index.html")


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
            new_user = User.objects.create_user(username=username, first_name=name, last_name=surname, email=email,
                                                password=password)
            new_user.save()
            return render(request, "login.html", {"new_user": new_user})

