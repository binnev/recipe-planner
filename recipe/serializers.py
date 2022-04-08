from rest_framework import serializers

from recipe.models import Recipe, Ingredient, Equipment, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]

    def to_internal_value(self, data):
        data = {"name": data}
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment


class RecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    title = serializers.CharField(source="name")

    # ingredients = IngredientSerializer(many=True)
    # equipment = EquipmentSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            "title", "author", "prep_time", "cook_time",
            "serves", "source", "image", "notes",
            # "ingredients",
            # "equipment",
        ]

    def create(self, validated_data):
        if author_data := validated_data.pop("author", None):
            author, _ = Author.objects.get_or_create(**author_data)
            validated_data["author"] = author

        return super().create(validated_data)
