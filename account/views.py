from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.models import User

from store.models import Product

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('account:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('account:login')
    else:
        return render(request, 'account/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == 'POST':
        # Get form values
        username = request.POST['username']
        email = request.POST['useremail']
        password = request.POST['password']

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'That username is taken')
            return redirect('account:register')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is being used')
                return redirect('account:register')
            else:
                # Looks good
                user = User.objects.create_user(username=username, password=password,email=email)
                # Login after register
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('account:dashboard')
    else:
        return render(request, 'account/register.html')

class DashboardView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'account/dashboard.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(user_id=self.request.user.id)

def logout_view(request):
    messages.success(request, 'You are now logged out!')
    logout(request)
    return redirect('account:login')
