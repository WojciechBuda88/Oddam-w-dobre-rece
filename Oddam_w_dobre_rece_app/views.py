from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.core.mail import send_mail

from Oddam_w_dobre_rece.settings import ADMINS
from Oddam_w_dobre_rece_app.models import Donation, Institution, Category


class LandingPageView(View):
    def get(self, request):
        donations = list(Donation.objects.aggregate(Sum('quantity')).values())[0]
        institutions = len(Institution.objects.all())
        foundations = Institution.objects.filter(type="Fundacja")
        ngo = Institution.objects.filter(type="Organizacja pozarządowa")
        local_collection = Institution.objects.filter(type="Zbiórka lokalna")

        def num_of_page(items):
            paginator = Paginator(items, 5)
            page = request.GET.get('page')

            if page is None:
                return paginator.get_page(1)

            return paginator.get_page(page[:-1])

        return render(request, "index.html", {"donations": donations, "institutions": institutions,
                                              "foundations": num_of_page(foundations), "ngo": num_of_page(ngo),
                                              "local_collection": num_of_page(local_collection)})


class AddDonationView(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, "form.html", {"categories":categories, "institutions":institutions})

    def post(self, request):
        active_user = request.user.id
        quantity = request.POST.get("bags")
        categories = request.POST.getlist("categories")
        organization = request.POST.get("organization")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone")
        city = request.POST.get("city")
        pick_up_date = request.POST.get("data")
        pick_up_time = request.POST.get("time")
        pick_up_comment = request.POST.get("more_info")
        user = active_user
        institution = Institution.objects.get(id=organization)
        is_taken = False
        print(categories)
        if quantity and categories and institution and address and phone_number and pick_up_date and pick_up_time and \
                pick_up_comment and user:
            new_donation = Donation.objects.create(quantity=quantity, address=address, phone_number=phone_number,
                                                   institution=institution, city=city, pick_up_date=pick_up_date,
                                                   pick_up_time=pick_up_time, pick_up_comment=pick_up_comment,
                                                   institution_id=institution.id, is_taken=is_taken, user_id=user)
            new_donation.save()
            for i in range(len(categories)):
                new_categories = Category.objects.get(id=categories[i])
                new_donation.categories.add(new_categories)
            return redirect("/confirmation")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post (self, request):
        if request.method == "POST":
            username = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            try:
                if user == User.objects.get_by_natural_key(username=username):
                    login(request, user)
                    return redirect(reverse("landing_page"))
                else:
                    message = "Niepoprawne hasło!"
                    return render(request, "login.html", context={"message": message})
            except Exception:
                return redirect("/register")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("landing_page")


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
            return redirect("/login")


class ProfileView(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        donations = Donation.objects.filter(user_id=id, is_taken=False)
        archived_donations = Donation.objects.filter(user_id=id, is_taken=True)
        categories = Category.objects.all()
        return render(request, "profile.html", {"user": user, "donations": donations, "categories":categories,
                                                "archived_donations":archived_donations})


def archive(request, id):
    donation = Donation.objects.get(id=id)
    donation.is_taken = True
    donation.save()
    user = donation.user.id
    return redirect(f"/profile/{user}#donation")


class FormConfirmationView(View):
    def get(self, request):
        return render(request, "form-confirmation.html")


class SettingsView(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        return render(request, "settings.html", {"user":user})

    def post(self,request,id):
        user = User.objects.get(id=id)
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if name and surname and email and password and True == user.check_password(raw_password=password):
            user.first_name = name
            user.last_name = surname
            user.email = email
            user.save()
            return redirect(f"/profile/{user.id}")


class ChangePasswordView(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        return render(request, "password.html", {"user":user})

    def post(self, request, id):
        user = User.objects.get(id=id)
        password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_repeat = request.POST.get("new_password_repeat")
        if password and new_password and new_password_repeat and new_password == new_password_repeat \
                and True == user.check_password(raw_password=password):
            user.set_password(new_password)
            user.save()
            return redirect("logout")


class ContactView(View):
    def post(self, request):
        data = request.POST

        mail_subject = f"Contact message - { request.user.username }"
        message = f"{data['message']} - Pozdrawiam {data['name']} {data['surname']}"
        send_mail(mail_subject,message, "reprezentacjaoverwatch@gmail.com", ADMINS)

        return redirect("landing_page")
