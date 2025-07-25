from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Account
from django.utils import timezone


class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    age = models.IntegerField(null=True, blank=True)
    planted_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planted_trees')
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='plantings')
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_long = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.tree.name} plantada por {self.user.username}'