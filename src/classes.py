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
        # Приватный атрибут для списка товаров (начинается с __)
        self.__products = products if products is not None else []

        # Увеличиваем счетчик категорий при создании нового объекта
        Category.category_count += 1

        # Увеличиваем счетчик товаров на количество товаров в категории
        Category.product_count += len(self.__products)

    def add_product(self, product: Product):
        """Метод для добавления товара в категорию"""
        self.__products.append(product)
        # Увеличиваем общий счетчик товаров при добавлении нового продукта
        Category.product_count += 1

    # Задание 1
    # def get_products(self):
    #     """Метод для получения списка товаров (геттер)"""
    #     return self.__products

    # Задание 2
    @property
    def products(self):
        """
        Геттер для получения списка товаров в отформатированном виде.
        Возвращает строку с информацией о каждом товаре в формате:
        "Название продукта, {price} руб. Остаток: {quantity} шт."
        """
        products_str = ""
        for product in self.__products:
            products_str += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return products_str.strip()  # Убираем последний перенос строки
