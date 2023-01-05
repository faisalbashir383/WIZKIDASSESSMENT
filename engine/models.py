from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Recipe(models.Model):
    """
    Model to store users recipes
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    name = models.CharField(_("Recipe Name"), max_length=200, null=False, blank=False)
    category = models.CharField(max_length=100, null=False, blank=False)
    sub_category = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(_("Recipe Description"), null=False, blank=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Recipes'
        verbose_name = 'Recipe'