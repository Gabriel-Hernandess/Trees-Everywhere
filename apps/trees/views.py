from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
import json
from decimal import Decimal
from django.contrib.auth.models import User

from ..trees.models import Tree, PlantedTree
from ..users.models import Account
from ..core.decorators import login_required_custom

@method_decorator(login_required_custom, name='dispatch')
class MyTreesView(View):
    def get(self, request):
        try:
            user = request.user

            trees = Tree.objects.all()
            planted_trees = PlantedTree.objects.filter(user=user)
            accounts = user.accounts.all()

            context = {'trees': trees, 'planted_trees': planted_trees, 'accounts': accounts}
            return render(request, 'planted_trees.html', context)
        except Exception as error:
            print('Erro ao obter arvores: ', error)
            return render(request, 'planted_trees.html')
        
    def post(self, request):
        data = json.loads(request.body)
        trees_data = data.get('trees')
        user = request.user
        plants = []

        for item in trees_data:
            try:
                tree = Tree.objects.get(id=item['tree_id'])
                location = (Decimal(item['lat']), Decimal(item['lng']))

                account = None
                account_id = item.get('account')
                if account_id:
                    try:
                        account = Account.objects.get(id=account_id)
                    except Account.DoesNotExist:
                        account = None

                plants.append((tree, location, account))
            except (Tree.DoesNotExist, KeyError, ValueError):
                continue
        
        print(plants)
        user.plant_trees(plants)

        return JsonResponse({'success': True})
    
@method_decorator(login_required_custom, name='dispatch')
class MyProfile(View):
    def get(self, request):
        return render(request, 'my_profile.html')

@method_decorator(login_required_custom, name='dispatch')
class GroupsTrees(View):
    def get(self, request):
        return render(request, 'groups_trees.html')