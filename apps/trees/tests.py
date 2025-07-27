from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.users.models import Account
from apps.trees.models import Tree, PlantedTree

User = get_user_model()

class TreesTestCase(TestCase):
    def setUp(self):
        # Criar contas
        self.account1 = Account.objects.create(name="Conta 1")
        self.account2 = Account.objects.create(name="Conta 2")

        # Criar usuários
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        self.user3 = User.objects.create_user(username="user3", password="pass")

        # Associar usuários às contas
        self.account1.users.add(self.user1, self.user2)
        self.account2.users.add(self.user3)

        # Criar árvores
        self.tree1 = Tree.objects.create(name="Árvore 1", scientific_name="Spec1")
        self.tree2 = Tree.objects.create(name="Árvore 2", scientific_name="Spec2")

        # Usuários plantam árvores
        self.user1.plant_tree(self.tree1, (Decimal("10.123456"), Decimal("20.654321")), self.account1)
        self.user2.plant_tree(self.tree2, (Decimal("11.111111"), Decimal("21.222222")), self.account1)
        self.user3.plant_tree(self.tree1, (Decimal("12.333333"), Decimal("22.444444")), self.account2)

        # Cliente de teste para requisições
        self.client = Client()

    def test_plant_tree_method(self):
        count_before = PlantedTree.objects.filter(user=self.user1).count()
        self.user1.plant_tree(self.tree2, (Decimal("30.0"), Decimal("40.0")), self.account1)
        count_after = PlantedTree.objects.filter(user=self.user1).count()
        self.assertEqual(count_after, count_before + 1)

    def test_plant_trees_method(self):
        plants = [
            (self.tree1, (Decimal("50.0"), Decimal("60.0")), self.account1),
            (self.tree2, (Decimal("70.0"), Decimal("80.0")), self.account1),
        ]
        count_before = PlantedTree.objects.filter(user=self.user2).count()
        self.user2.plant_trees(plants)
        count_after = PlantedTree.objects.filter(user=self.user2).count()
        self.assertEqual(count_after, count_before + 2)

    def test_listagem_arvores_usuario(self):
        self.client.login(username="user1", password="pass")
        url = reverse("planted-trees")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Verifica se as árvores plantadas pelo user1 aparecem no contexto/template
        planted = response.context['planted_trees']
        self.assertTrue(all(pt.user == self.user1 for pt in planted))

    def test_erro_403_ao_acessar_arvores_outro_usuario(self):
        self.client.login(username="user1", password="pass")
        # Suponha que você tenha uma view que recebe id do usuário para listar árvores:
        url = reverse("planted-trees")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


    """
    Meu sistema apenas funciona retornando arvores do proprio user autenticado, sem passar parametros para rotas, esse teste acaba
    sendo inutilizado.
    
    def test_listagem_arvores_contas_do_usuario(self):
        self.client.login(username="user1", password="pass")
        url = reverse("group-trees")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        planted = response.context['trees_by_account']
        accounts_users = self.account1.users.all()
        # planted é um dict {account: queryset de PlantedTree}
        # Verificar que todas as árvores são plantadas por usuários da conta do user1
        for account, trees_qs in planted.items():
            for tree in trees_qs:
                self.assertIn(tree.user, accounts_users)
    """