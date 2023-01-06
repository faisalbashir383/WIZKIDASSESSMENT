from engine.models import Recipe
from rest_framework.response import Response
from rest_framework import generics, status, filters
from engine.serializers import RecipeAddViewSerializer, RecipeUpdateSerializer
from engine.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend


class UserRecipeView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    1. api to retrieve users recipes & add new recipes for user
    2. updated users recipe
    3. deletes users recipes
    """
    serializer_class = RecipeAddViewSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'added_on']

    def get_object(self):
        try:
            recipe_id = int(self.request.query_params.get("recipe_id", 0))
            return self.request.user.recipes.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return None

    def get_queryset(self):
        return self.request.user.recipes.all().order_by("-added_on")

    def get(self, request, *args, **kwargs):
        query_set = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = RecipeUpdateSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(dict({"error": "Recipe does not exist or invalid recipe_id passed in params"}),
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response(dict({"msg": "Recipe deleted successfully"}), status=status.HTTP_200_OK)
        return Response(dict({"error": "Recipe does not exist or invalid recipe_id passed in params"}), status=status.HTTP_400_BAD_REQUEST)


class AllRecipes(generics.ListAPIView):
    """
    api to retrieve all users recipes
    """
    serializer_class = RecipeAddViewSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'added_on']

    def get_queryset(self):
        return Recipe.objects.all().order_by("-added_on")

    def get(self, request, *args, **kwargs):
        query_set = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
