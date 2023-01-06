from rest_framework import serializers

from engine.models import Recipe


class RecipeAddViewSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    category = serializers.CharField(required=True)
    sub_category = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Recipe
        exclude = (
            "user",
        )


class RecipeUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        exclude = (
            "user",
        )
