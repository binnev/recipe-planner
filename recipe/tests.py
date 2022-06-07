import pytest
from mixer.backend.django import mixer

from recipe.models import Ingredient

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "amount, original_unit, expected_amount, desired_unit",
    [
        (1, "kg", 1000, "g"),
        (0.5, "kg", 500, "g"),
        (1000, "g", 1, "kg"),
        (1, "g", 0.001, "kg"),
    ],
)
def test_ingredient_amount_in_units(amount, original_unit, expected_amount, desired_unit):
    ingredient = mixer.blend(Ingredient, amount=amount, unit=original_unit)
    assert ingredient.amount_in_units(desired_unit) == expected_amount
