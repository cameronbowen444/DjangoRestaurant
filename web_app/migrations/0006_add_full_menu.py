from decimal import Decimal
from django.db import migrations


def add_full_menu(apps, schema_editor):
    Category = apps.get_model("web_app", "Category")
    Item = apps.get_model("web_app", "Item")

    categories = [
        (1, "Appetizers"),
        (2, "Pizza"),
        (3, "Pasta"),
        (4, "Desserts"),
        (5, "Drinks"),
    ]

    for category_id, name in categories:
        Category.objects.update_or_create(
            id=category_id,
            defaults={"name": name}
        )

    menu_items = [
        # Appetizers
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
            "food_name": "Bruschetta",
            "desc": "Toasted bread topped with fresh tomatoes, basil, garlic, and olive oil.",
            "price": Decimal("7.99"),
            "category_id": 1,
        },
        {
            "food_name": "Fried Calamari",
            "desc": "Lightly fried calamari served with lemon and marinara sauce.",
            "price": Decimal("12.99"),
            "category_id": 1,
        },
        {
            "food_name": "Stuffed Mushrooms",
            "desc": "Mushrooms filled with breadcrumbs, herbs, parmesan, and garlic.",
            "price": Decimal("9.99"),
            "category_id": 1,
        },

        # Pizza
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
            "food_name": "Meat Lovers Pizza",
            "desc": "Loaded with pepperoni, sausage, bacon, mozzarella, and marinara.",
            "price": Decimal("18.99"),
            "category_id": 2,
        },
        {
            "food_name": "Veggie Pizza",
            "desc": "Mozzarella pizza with mushrooms, bell peppers, onions, olives, and tomatoes.",
            "price": Decimal("17.99"),
            "category_id": 2,
        },
        {
            "food_name": "BBQ Chicken Pizza",
            "desc": "Grilled chicken, barbecue sauce, red onions, mozzarella, and cilantro.",
            "price": Decimal("18.49"),
            "category_id": 2,
        },
        {
            "food_name": "Hawaiian Pizza",
            "desc": "Mozzarella pizza topped with ham, pineapple, and tomato sauce.",
            "price": Decimal("17.49"),
            "category_id": 2,
        },
        {
            "food_name": "Buffalo Chicken Pizza",
            "desc": "Spicy buffalo chicken, mozzarella, ranch drizzle, and green onions.",
            "price": Decimal("18.99"),
            "category_id": 2,
        },
        {
            "food_name": "Four Cheese Pizza",
            "desc": "A rich blend of mozzarella, parmesan, ricotta, and provolone.",
            "price": Decimal("17.99"),
            "category_id": 2,
        },

        # Pasta
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
            "food_name": "Penne Vodka",
            "desc": "Penne pasta tossed in a creamy tomato vodka sauce with parmesan.",
            "price": Decimal("15.49"),
            "category_id": 3,
        },
        {
            "food_name": "Shrimp Scampi",
            "desc": "Linguine with shrimp, garlic, butter, lemon, and white wine sauce.",
            "price": Decimal("19.99"),
            "category_id": 3,
        },
        {
            "food_name": "Baked Ziti",
            "desc": "Ziti pasta baked with marinara, ricotta, mozzarella, and parmesan.",
            "price": Decimal("14.99"),
            "category_id": 3,
        },

        # Desserts
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
        {
            "food_name": "Chocolate Lava Cake",
            "desc": "Warm chocolate cake with a rich melted center.",
            "price": Decimal("8.49"),
            "category_id": 4,
        },
        {
            "food_name": "Gelato",
            "desc": "Creamy Italian-style ice cream available in seasonal flavors.",
            "price": Decimal("5.99"),
            "category_id": 4,
        },
        {
            "food_name": "New York Cheesecake",
            "desc": "Rich cheesecake with a graham cracker crust and berry topping.",
            "price": Decimal("7.49"),
            "category_id": 4,
        },

        # Drinks
        {
            "food_name": "Italian Soda",
            "desc": "Sparkling soda with your choice of flavored syrup.",
            "price": Decimal("4.99"),
            "category_id": 5,
        },
        {
            "food_name": "Lemonade",
            "desc": "Fresh house lemonade served chilled.",
            "price": Decimal("3.99"),
            "category_id": 5,
        },
        {
            "food_name": "Espresso",
            "desc": "Classic Italian espresso shot.",
            "price": Decimal("3.49"),
            "category_id": 5,
        },
        {
            "food_name": "Iced Tea",
            "desc": "Fresh brewed iced tea served sweetened or unsweetened.",
            "price": Decimal("3.49"),
            "category_id": 5,
        },
        {
            "food_name": "Sparkling Water",
            "desc": "Chilled sparkling mineral water.",
            "price": Decimal("3.99"),
            "category_id": 5,
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


def remove_full_menu(apps, schema_editor):
    Item = apps.get_model("web_app", "Item")

    Item.objects.filter(
        food_name__in=[
            "Garlic Bread",
            "Mozzarella Sticks",
            "Bruschetta",
            "Fried Calamari",
            "Stuffed Mushrooms",
            "Margherita Pizza",
            "Pepperoni Pizza",
            "Meat Lovers Pizza",
            "Veggie Pizza",
            "BBQ Chicken Pizza",
            "Hawaiian Pizza",
            "Buffalo Chicken Pizza",
            "Four Cheese Pizza",
            "Fettuccine Alfredo",
            "Spaghetti Bolognese",
            "Penne Vodka",
            "Shrimp Scampi",
            "Baked Ziti",
            "Tiramisu",
            "Cannoli",
            "Chocolate Lava Cake",
            "Gelato",
            "New York Cheesecake",
            "Italian Soda",
            "Lemonade",
            "Espresso",
            "Iced Tea",
            "Sparkling Water",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("web_app", "0005_seed_menu"),
    ]

    operations = [
        migrations.RunPython(add_full_menu, remove_full_menu),
    ]