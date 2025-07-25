from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
import json

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
        
    def put(self, request):
        print('PUT recebido')
        try:
            data = json.loads(request.body)
            account_id = data.get('id')

            print(account_id)

            if not account_id:
                return JsonResponse({'success': False})

            account = Account.objects.get(id=account_id)
            account.active = not account.active
            account.save()

            return JsonResponse({'success': True})
        except Exception as error:
            print('Erro ao editar conta', error)
            return JsonResponse({'success': False})
    
@method_decorator(login_required_custom, name='dispatch')
class AdminUsersView(View):
    def get(self, request):
        try:
            accounts = Account.objects.all()

            users = User.objects.all().prefetch_related('accounts')
            users_with_accounts = []

            for user in users:
                users_with_accounts.append({
                    'user': user,
                    'accounts': user.accounts.all()
                })

            context = {'users': users_with_accounts, 'accounts': accounts}
            return render(request, 'users.html', context)
        except Exception as error:
            print('Erro ao obter contas ou usuarios: ', error)
            return render(request, 'users.html')
        
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('name')
            email = data.get('email')
            senha = data.get('password')
            accounts = data.get('accounts', [])

            if not all([username, email, senha]):
                return JsonResponse({'sucess': False, 'msg': 'Preecha as informacoes corretamente.'})

            user = User.objects.create(username=username, email=email)
            user.set_password(senha)
            user.save()

            # Pega os ids das contas para vincular
            account_ids = [acc['id'] for acc in accounts]

            # Busca as contas e vincula ao usuário
            user_accounts = Account.objects.filter(id__in=account_ids)
            for account in user_accounts:
                account.users.add(user)  # adiciona usuário à conta

            return JsonResponse({'sucess': True})
        except Exception as error:
            print('Erro ao adicionar usuario:', error)
            return JsonResponse({'sucess': False, 'error': str(error)})

    
@method_decorator(login_required_custom, name='dispatch')
class AdminTreesView(View):
    def get(self, request):
        try:
            trees_query = Tree.objects.all().prefetch_related('plantings')
            trees = []

            for tree in trees_query:
                trees.append({
                    'name': tree.name,
                    'scientific_name': tree.scientific_name,
                    'planted_trees': tree.plantings.all(),
                })

            context = {'trees': trees}
            return render(request, 'trees.html', context)
        except Exception as error:
            print('Erro ao obter arvores: ', error)
            return render(request, 'trees.html')
        
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            scientific_name = data.get('scientificName')

            Tree.objects.create(name=name, scientific_name=scientific_name)

            return JsonResponse({'success': False})
        except Exception as error:
            print('Erro ao adicionar arvore:', error)
            return JsonResponse({'success': False, 'error': str(error)})

@method_decorator(login_required_custom, name='dispatch')
class RegisterView(View):
    def get(self, request):
        return HttpResponse('TELA DE CADASTRO')