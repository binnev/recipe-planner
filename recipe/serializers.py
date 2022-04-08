from rest_framework import serializers

from recipe.models import Recipe, Ingredient, Equipment, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]

    def to_internal_value(self, data):
        return {"name": data}


class IngredientSerializer(serializers.Serializer):
    pass


class EquipmentSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        return {"name": data}


class RecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    title = serializers.CharField(source="name")

    # ingredients = IngredientSerializer(many=True)
    equipment = EquipmentSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            "title", "author", "prep_time", "cook_time",
            "serves", "source", "image", "notes",
            # "ingredients",
            "equipment",
        ]

    def create(self, validated_data):
        if author_data := validated_data.get("author"):
            author, _ = Author.objects.get_or_create(**author_data)
            validated_data["author"] = author

        equipment_data = validated_data.pop("equipment", [])
        ingredient_data = validated_data.pop("ingredients", [])

        recipe = super().create(validated_data)

        for data in equipment_data:
            Equipment.objects.create(recipe=recipe, **data)

        return recipe
