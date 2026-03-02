class Product:
    """Класс для описания товара"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Метод для инициализации экземпляра класса Product"""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для описания категории товаров"""

    # Атрибуты класса для подсчета категорий и товаров
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None):
        """Метод для инициализации экземпляра класса Category"""
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Увеличиваем счетчик категорий при создании нового объекта
        Category.category_count += 1

        # Увеличиваем счетчик товаров на количество товаров в категории
        Category.product_count += len(self.products)
