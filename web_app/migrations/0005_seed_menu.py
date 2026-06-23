from decimal import Decimal
from django.db import migrations


def seed_menu(apps, schema_editor):
    Category = apps.get_model("web_app", "Category")
    Item = apps.get_model("web_app", "Item")

    categories = [
        (1, "Appetizers"),
        (2, "Pizza"),
        (3, "Pasta"),
        (4, "Desserts"),
    ]

    for category_id, name in categories:
        Category.objects.update_or_create(
            id=category_id,
            defaults={"name": name}
        )

    menu_items = [
        {
            "food_name": "Garlic Bread",
            "desc": "Toasted Italian bread with garlic butter, parsley, and parmesan.",
            "price": Decimal("6.99"),
            "category_id": 1,
        },
        {
            "food_name": "Mozzarella Sticks",
            "desc": "Crispy fried mozzarella served with warm marinara sauce.",
            "price": Decimal("8.99"),
            "category_id": 1,
        },
        {
            "food_name": "Margherita Pizza",
            "desc": "Classic pizza with tomato sauce, fresh mozzarella, basil, and olive oil.",
            "price": Decimal("14.99"),
            "category_id": 2,
        },
        {
            "food_name": "Pepperoni Pizza",
            "desc": "Hand-tossed pizza with mozzarella, tomato sauce, and pepperoni.",
            "price": Decimal("16.99"),
            "category_id": 2,
        },
        {
            "food_name": "Fettuccine Alfredo",
            "desc": "Creamy parmesan alfredo sauce tossed with fresh fettuccine pasta.",
            "price": Decimal("15.99"),
            "category_id": 3,
        },
        {
            "food_name": "Spaghetti Bolognese",
            "desc": "Traditional spaghetti with slow-cooked meat sauce and parmesan.",
            "price": Decimal("16.99"),
            "category_id": 3,
        },
        {
            "food_name": "Tiramisu",
            "desc": "Classic Italian dessert with espresso-soaked ladyfingers and mascarpone cream.",
            "price": Decimal("7.99"),
            "category_id": 4,
        },
        {
            "food_name": "Cannoli",
            "desc": "Crispy pastry shells filled with sweet ricotta cream and chocolate chips.",
            "price": Decimal("6.99"),
            "category_id": 4,
        },
    ]

    for item in menu_items:
        category = Category.objects.get(id=item["category_id"])

        Item.objects.update_or_create(
            food_name=item["food_name"],
            defaults={
                "desc": item["desc"],
                "price": item["price"],
                "category": category,
            }
        )


def remove_seed_menu(apps, schema_editor):
    Item = apps.get_model("web_app", "Item")
    Category = apps.get_model("web_app", "Category")

    Item.objects.filter(
        food_name__in=[
            "Garlic Bread",
            "Mozzarella Sticks",
            "Margherita Pizza",
            "Pepperoni Pizza",
            "Fettuccine Alfredo",
            "Spaghetti Bolognese",
            "Tiramisu",
            "Cannoli",
        ]
    ).delete()

    Category.objects.filter(
        name__in=["Appetizers", "Pizza", "Pasta", "Desserts"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("web_app", "0004_alter_category_id_alter_customer_id_alter_item_id_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_menu, remove_seed_menu),
    ]