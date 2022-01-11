from django.shortcuts import render, redirect
from django.views import View
from main.models import Institution, Donation, InstitutionCategories
from django.contrib.auth.models import User


class LandingPageView(View):
    def get(self, request):
        supported_institutions = len(Institution.objects.all())
        donation_extra_quantity = 0
        for donation in Donation.objects.all():
            donation_extra_quantity += donation.quantity
        donation_quantity = len(Donation.objects.all()) + donation_extra_quantity
        foundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        local_collections = Institution.objects.filter(type=3)
        institution_categories = InstitutionCategories.objects.all()
        return render(request, 'index.html', {'supported_institutions': supported_institutions,
                                              'donation_quantity': donation_quantity,
                                              'foundations': foundations,
                                              'organizations': organizations,
                                              'local_collections': local_collections,
                                              'institution_categories': institution_categories})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            User.objects.create_user(username=email, first_name=name, last_name=surname, email=email, password=password)
            return redirect('/login')
        elif password != password2:
            return render(request, 'register.html')
