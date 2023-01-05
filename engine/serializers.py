from rest_framework import serializers

from engine.models import Recipe


class RecipeAddViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        exclude = (
            "user",
        )