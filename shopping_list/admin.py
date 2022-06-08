from django.contrib import admin

from shopping_list.models import ShoppingList, PlannedRecipe


class PlannedRecipeInline(admin.TabularInline):
    model = PlannedRecipe
    extra = 0
    raw_id_fields = ["recipe"]
    readonly_fields = ["name"]


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    fields = ["aggregated_items"]
    readonly_fields = ["aggregated_items"]
    inlines = [PlannedRecipeInline]
