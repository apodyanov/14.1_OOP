class Product:
    """Класс для описания товара"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Метод для инициализации экземпляра класса Product"""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    # # Задание 3
    # @classmethod
    # def new_product(cls, product_data: dict):
    #     """
    #     Класс-метод для создания нового продукта из словаря.
    #
    #     Args:
    #         product_data: Словарь с данными о продукте, содержащий ключи:
    #                      'name', 'description', 'price', 'quantity'
    #
    #     Returns:
    #         Объект класса Product
    #     """
    #     # Создаем и возвращаем новый экземпляр класса Product
    #     return cls(
    #         name=product_data['name'],
    #         description=product_data['description'],
    #         price=product_data['price'],
    #         quantity=product_data['quantity']
    #     )

    # Доп задание 3
    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None):
        """
        Класс-метод для создания нового продукта из словаря с проверкой на дубликаты.

        Args:
            product_data: Словарь с данными о продукте, содержащий ключи:
                         'name', 'description', 'price', 'quantity'
            existing_products: Список существующих продуктов для проверки дубликатов

        Returns:
            Объект класса Product (новый или обновленный существующий)
        """
        # Проверяем наличие дубликатов, если передан список существующих товаров
        if existing_products:
            for existing_product in existing_products:
                if existing_product.name == product_data['name']:
                    # Найден дубликат - обновляем существующий товар
                    print(f"Найден дубликат товара '{product_data['name']}'. Обновляем данные...")

                    # Складываем количество
                    existing_product.quantity += product_data['quantity']

                    # Выбираем максимальную цену
                    if product_data['price'] > existing_product.price:
                        existing_product.price = product_data['price']
                        print(f"Цена обновлена до {existing_product.price}")
                    else:
                        print(f"Цена оставлена прежней: {existing_product.price}")

                    # Обновляем описание (можно оставить старое или обновить)
                    # existing_product.description = product_data['description']

                    print(f"Новое количество: {existing_product.quantity}")
                    return existing_product

        # Если дубликатов нет или список не передан, создаем новый продукт
        print(f"Создаем новый товар '{product_data['name']}'")
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )


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

    # Доп задание 3
    def add_product_with_check(self, product_data: dict):
        """
        Метод для добавления товара с проверкой на дубликаты внутри категории
        """
        # Используем класс-метод Product.new_product с передачей существующих товаров
        product = Product.new_product(product_data, self.__products)

        # Проверяем, был ли товар добавлен заново или это новый объект
        if product not in self.__products:
            self.add_product(product)

        return product



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

    # Доп задание 3
    @property
    def products_list(self):
        """Геттер для получения списка товаров (для внутреннего использования)"""
        return self.__products