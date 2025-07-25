from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

from ..core.decorators import login_required_custom

@method_decorator(login_required_custom, name='dispatch')
class AdminDashboardView(View):
    def get(self, request):
        if request.user.is_superuser:
            return render(request, 'admin_dashboard.html')
        else:
            return render(request, 'user_dashboard.html')

@method_decorator(login_required_custom, name='dispatch')
class RegisterView(View):
    def get(self, request):
        return HttpResponse('TELA DE CADASTRO')