from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator

from ..core.decorators import login_required_custom
from ..users.models import Profile, Account
from ..trees.models import Tree
from django.contrib.auth.models import User

@method_decorator(login_required_custom, name='dispatch')
class AdminAccountsView(View):
    def get(self, request):
        try:
            accounts = Account.objects.all()
            context = {'accounts': accounts}
            return render(request, 'accounts.html', context)
        except Exception as error:
            print('Erro ao obter contas: ', error)
            return render(request, 'accounts.html')
        
    def post(self, request):
        try:
            name = request.POST.get('username')
            
            if not name:
                return JsonResponse({'success': False, 'error': 'Nome inválido, tente novamente'})
            
            Account.objects.create(name=name)
            return JsonResponse({'success': True})
        except Exception as error:
            print('Erro ao adicionar nova conta', error)
            return JsonResponse({'success': False, 'error': str(error)})
    
@method_decorator(login_required_custom, name='dispatch')
class AdminUsersView(View):
    def get(self, request):
        try:
            users = User.objects.all()
            context = {'users': users}
            return render(request, 'users.html', context)
        except Exception as error:
            print('Erro ao obter contas: ', error)
            return render(request, 'users.html')
    
@method_decorator(login_required_custom, name='dispatch')
class AdminTreesView(View):
    def get(self, request):
        try:
            trees = Tree.objects.all()
            context = {'trees': trees}
            return render(request, 'trees.html', context)
        except Exception as error:
            print('Erro ao obter arvores: ', error)
            return render(request, 'trees.html')

@method_decorator(login_required_custom, name='dispatch')
class RegisterView(View):
    def get(self, request):
        return HttpResponse('TELA DE CADASTRO')