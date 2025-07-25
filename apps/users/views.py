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
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser:
                return render(request, 'accounts.html')
            else:
                return render(request, 'planted_trees.html')
        return render(request, 'login.html', {'msg': 'Usuário ou senha inválidos'})
    
@method_decorator(login_required_custom, 'dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')