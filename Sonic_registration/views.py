from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm, FileForm, File
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from .models import Register
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.conf import settings
from .models import Login
from django.urls import reverse
#from .backends import EmailBackend
# Create your views here.

#Class Based Register View

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request, 'register.html', {'form': form})
        

# Class Based Login View

class LoginView(View):
    print("This is being called right now")
    def get(self, request):
        print("Get that out of the way")
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        print("Post that out of the way")
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email, password)
            try:
                register_model = Register.objects.get(email=email)
                print("It exists",register_model)
            except Register.DoesNotExist:
                print("Does not exist",Register.DoesNotExist)
                return redirect('register')

            # Check if the password is valid for the found register model
            if password == register_model.password:
                # Perform your custom login logic here
                # For example, you can set a session variable to indicate the user is logged in
               
               request.session['email'] = register_model.email
               print(request.session['email'], register_model.pk)
               print("Login successful, redirecting to 'index'")
               return redirect("index")
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid email or password.'})
        else:
            return render(request, 'login.html', {'form': form, 'error_message': 'Invalid'})
        
    redirect_field_name = 'index'
    
  
class IndexView(LoginRequiredMixin, View):
    print("IndexView called")
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'home.html'
    print("IndexView called 2 ")
    
    def get(self, request):
        print("IndexView called 3")
        email_id =   request.session.get('email')
        print("Email ID:", email_id)
        if email_id:
            try:
                print("Trying to get user")
                user = Login.objects.get(email=email_id)
                print(user)
                user_files = File.objects.filter(uploader=user)
                protected_files = File.objects.filter(access_type='protected').exclude(uploader=user)
                public_files = File.objects.filter(access_type='public').exclude(uploader=user)
                print("User:", user)
                print("User Files:", user_files)
                print("Public Files:", public_files)

                context = {
                    'name': user.email,
                    'user_files': user_files,
                    'public_files': public_files,
                    'protected_files': protected_files,
                    'media_url': settings.MEDIA_URL,
                }

                return render(request, self.template_name, context)
            except Login.DoesNotExist:
                # User not found, redirect to login
                print("IndexView called 4")
                return redirect('login')
        else:
            # User ID not found in session, redirect to login
            print("IndexView called 5")
            return redirect('login')

    
    def post(self, request):
        form = FileForm(request.POST, request.FILES)
        print("IndexView called 6")
        if form.is_valid():
            email = request.session.get('email')  # Retrieve the email from the session
            try:
                user = Login.objects.get(email=email)
                file = form.save(commit=False)
                file.uploader = user  # Assign the user as the uploader of the file
                file.save()
                print("Redirecting to 'home'")
                return redirect('index')
            except Login.DoesNotExist:
                # User not found, redirect to login
                print("IndexView called 4")
                return redirect('login')
        else:
            return render(request, 'home.html', {'form': form})
        
# Class Based Logout View
class LogoutView(View):
    def get(self, request):
        # Clear the session
        request.session.pop('email', None)
        request.session.flush()
        return redirect('index')


# Home View
def home(request):
    return render(request, 'home.html')