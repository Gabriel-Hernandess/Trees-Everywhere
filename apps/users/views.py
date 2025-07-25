from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login, logout

from ..core.decorators import login_required_custom

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('username')

        user = authenticate(username=username, password=password)

        if user:
            login(user)

            if user.is_superuser:
                return render(request, 'admin_dashboard.html')
            else:
                return render(request, 'user_dashboard.html')
        return HttpResponse('Usuário não existe')
    
@method_decorator(login_required_custom, 'dispatch')
class LogoutView(View):
    def post(self, request):
        user = request.user

        logout(user)
        redirect('login')