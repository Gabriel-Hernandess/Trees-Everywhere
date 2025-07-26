from django.contrib.auth.models import User
from .models import PlantedTree
from decimal import Decimal

def plant_tree(self, tree, location, account):
    lat, long = location
    PlantedTree.objects.create(
        user=self,
        account=account,
        tree=tree,
        location_lat=Decimal(lat),
        location_long=Decimal(long)
    )

def plant_trees(self, plants):
    for tree, location, account in plants:
        self.plant_tree(tree, location, account)

User.add_to_class('plant_tree', plant_tree)
User.add_to_class('plant_trees', plant_trees)