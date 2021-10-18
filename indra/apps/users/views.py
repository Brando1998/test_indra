from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from apps.users.models import Company, Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.models import Group

class RegisterView(View):
    def get(self, request):
        template_name = 'registration/register.html'

        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, template_name)
    
    def post(self, request):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        # check if user email is already registered
        if User.objects.filter(email=email).count() > 0:
            return redirect('register')
        
        # native user creation
        new_user = User.objects.create_user(username=email,email=email,password=password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.is_staff = False
        new_user.save()
        # company creation
        new_company = Company(
            name=company_name
        )
        new_company.save()
        #Profile creation
        profile = Profile(
            company=new_company,
            user=new_user,
            mobile_number=mobile_number
        )
        profile.save()

        # auth 
        user = authenticate(request, username=email, password=password)

        # login
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('register')

class LoginView(View):
    def get(self, request):
        template_name = 'registration/login.html'
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            else:
                return redirect('dashboard')
        else:
            return redirect('login')

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        template_name = 'dashboard/dashboard.html'
        context = {
            'company': Company.objects.get(id=request.user.profile.company.id),
        }
        return render(request, template_name, context)

# CRUD VIEWS

class UsersListView(LoginRequiredMixin, View):
    def get(self, request):
        template_name = 'dashboard/users_list.html'
        context = {
            'company': Company.objects.get(id=request.user.profile.company.id),
            'profiles': Profile.objects.filter(company=request.user.profile.company),
        }
        return render(request, template_name, context)

class UserCreateView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'company': Company.objects.get(id=request.user.profile.company.id),
        }
        template_name = 'dashboard/users_create_update.html'
        return render(request, template_name, context)
    
    def post(self, request):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        root = True if 'user_root' in request.POST else False
        file_1 = request.FILES['docfile_1'] if 'docfile_1' in request.FILES else None
        file_2 = request.FILES['docfile_2'] if 'docfile_2' in request.FILES else None
        # check if user email is already registered
        if User.objects.filter(email=email).count() > 0:
            return redirect('register')
        
        # native user creation
        new_user = User.objects.create_user(username=email,email=email,password=password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.is_staff = False
        new_user.save()

        # add new user to no root group
        if (root == False):
            no_root = Group.objects.get(name='No root')
            no_root.user_set.add(new_user)

        #Profile creation
        profile = Profile(
            company=request.user.profile.company,
            user=new_user,
            mobile_number=mobile_number,
            file_1=file_1,
            file_2=file_2
        )
        profile.save()
        
        return redirect('users_list')


class UserUpdateView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        profile = Profile.objects.get(id=id)
        context = {
            'profile':profile,
            'company': Company.objects.get(id=request.user.profile.company.id),
        }
        template_name = 'dashboard/users_create_update.html'
        return render(request, template_name, context)
    
    def post(self, request, id, *args, **kwargs):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile_number')
        # password = request.POST.get('password')
        root = True if 'user_root' in request.POST else False
        file_1 = request.FILES['docfile_1'] if 'docfile_1' in request.FILES else None
        file_2 = request.FILES['docfile_2'] if 'docfile_2' in request.FILES else None
        
        # native user update
        user = User.objects.get(id=id)
        user.username=email
        user.email=email

        # add new user to no root group
        if (root == True):
            no_root = Group.objects.get(name='No root')
            no_root.user_set.add(user)
        else:
            no_root = Group.objects.get(name='No root')
            no_root.user_set.remove(user)

        # user.password=password
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = False
        user.save()

        #Profile update
        profile = Profile.objects.get(user=user)
        profile.mobile_number = mobile_number
        profile.file_1 = file_1 if file_1 is not None else profile.file_1
        profile.file_2 = file_2 if file_2 is not None else profile.file_2
        profile.save()
        
        return redirect('users_list')

class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        if (id != request.user.id):
            user = User.objects.get(id=id)
            user.delete()
        return redirect('users_list')