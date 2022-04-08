import glob
from pathlib import Path

import yaml
from django.core.management.base import BaseCommand

from sous_chef.settings import RECIPE_DIR


class Command(BaseCommand):
    help = "Imports YAML recipe files"

    def handle(self, *args, **options):
        import_yaml_recipes()


def import_yaml_recipes():
    recipe_files = glob.glob((RECIPE_DIR / "*.yaml").as_posix())
    for filename in recipe_files:
        with open(filename) as f:
            print(f"Loading {filename}")
            recipe_dict = yaml.safe_load(f)
            parse_recipe_dict(recipe_dict)


def parse_recipe_dict(recipe: dict):
    pass
