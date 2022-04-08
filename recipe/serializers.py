from rest_framework import serializers

from recipe.models import Recipe, Ingredient, Equipment, Author, MethodStep
from recipes import parse_ingredient


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]

    def to_internal_value(self, data):
        return {"name": data}


class IngredientSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        amount, unit, description, preparation = parse_ingredient(data)
        return {
            "amount": amount,
            "unit": unit,
            "description": description,
            "preparation": preparation,
        }


class EquipmentSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        return {"name": data}


class MethodStepSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        return {"description": data}


class RecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    title = serializers.CharField(source="name")

    ingredients = IngredientSerializer(many=True)
    equipment = EquipmentSerializer(many=True, required=False)
    method = MethodStepSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            "title", "author", "prep_time", "cook_time",
            "serves", "source", "image", "notes",
            "ingredients",
            "equipment",
            "method",
        ]

    def create(self, validated_data):
        if author_data := validated_data.get("author"):
            author, _ = Author.objects.get_or_create(**author_data)
            validated_data["author"] = author

        equipment_data = validated_data.pop("equipment", [])
        ingredient_data = validated_data.pop("ingredients", [])
        method_data = validated_data.pop("method", [])

        recipe = super().create(validated_data)

        for data in equipment_data:
            Equipment.objects.create(recipe=recipe, **data)

        for data in ingredient_data:
            Ingredient.objects.create(recipe=recipe, **data)

        for data in method_data:
            MethodStep.objects.create(recipe=recipe, **data)

        return recipe
