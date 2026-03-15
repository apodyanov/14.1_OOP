class Product:
    """Класс для описания товара"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Метод для инициализации экземпляра класса Product"""
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity

    def __str__(self):
        """
        Магический метод для строкового представления продукта.
        Возвращает строку в формате: "Название продукта, 80 руб. Остаток: 15 шт."
        """
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Магический метод для сложения продуктов.
        Возвращает общую стоимость всех товаров на складе:
        (self.price * self.quantity) + (other.price * other.quantity)

        Args:
            other: Другой объект класса Product для сложения

        Returns:
            float: Общая стоимость товаров на складе
        """
        # Проверяем, что other является объектом класса Product
        if not isinstance(other, Product):
            raise TypeError(f"Нельзя сложить Product с {type(other).__name__}")

        # Вычисляем общую стоимость
        total_cost = (self.price * self.quantity) + (other.price * other.quantity)
        return total_cost

    @property
    def price(self):
        """Геттер для получения цены товара"""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """
        Сеттер для установки цены товара с проверкой корректности.

        Args:
            new_price: Новая цена товара

        Returns:
            None. Если цена некорректна, выводится сообщение об ошибке
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None):
        """
        Класс-метод для создания нового продукта из словаря с проверкой на дубликаты.

        Args:
            product_data: Словарь с данными о продукте
            existing_products: Список существующих продуктов для проверки дубликатов

        Returns:
            Объект класса Product (новый или обновленный существующий)
        """
        # Проверяем наличие дубликатов, если передан список существующих товаров
        if existing_products:
            for existing_product in existing_products:
                if existing_product.name == product_data["name"]:
                    # Найден дубликат - обновляем существующий товар
                    print(f"Найден дубликат товара '{product_data['name']}'. Обновляем данные...")

                    # Складываем количество
                    existing_product.quantity += product_data["quantity"]

                    # Выбираем максимальную цену (используем сеттер для проверки)
                    if product_data["price"] > existing_product.price:
                        existing_product.price = product_data["price"]  # Используем сеттер
                        print(f"Цена обновлена до {existing_product.price}")
                    else:
                        print(f"Цена оставлена прежней: {existing_product.price}")

                    print(f"Новое количество: {existing_product.quantity}")
                    return existing_product

        # Если дубликатов нет или список не передан, создаем новый продукт
        print(f"Создаем новый товар '{product_data['name']}'")
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )


class CategoryIterator:
    """
    Вспомогательный класс-итератор для перебора товаров в категории.
    Реализует протокол итератора (методы __iter__ и __next__).
    """

    def __init__(self, category):
        """
        Инициализация итератора.

        Args:
            category: Объект класса Category, товары которого нужно перебирать
        """
        self._category = category
        self._index = 0  # Текущий индекс при итерации

    def __iter__(self):
        """
        Магический метод, возвращающий итератор.
        Необходим для совместимости с протоколом итератора.
        """
        return self

    def __next__(self):
        """
        Магический метод, возвращающий следующий элемент при итерации.

        Returns:
            Следующий товар из категории

        Raises:
            StopIteration: Когда товары в категории закончились
        """
        # Получаем список товаров категории
        products = self._category.products_list

        # Проверяем, не вышли ли мы за пределы списка
        if self._index < len(products):
            # Получаем текущий товар
            product = products[self._index]
            # Увеличиваем индекс для следующего вызова
            self._index += 1
            # Возвращаем товар
            return product
        else:
            # Если товары закончились, сбрасываем индекс и выбрасываем исключение
            self._index = 0
            raise StopIteration


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

    def __str__(self):
        """
        Магический метод для строкового представления категории.
        Возвращает строку в формате: "Название категории, количество продуктов: 200 шт."
        """
        # Вычисляем общее количество продуктов в категории
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity

        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """
        Магический метод, делающий категорию итерируемой.
        Возвращает объект итератора для перебора товаров.
        """
        return CategoryIterator(self)

    def add_product(self, product: Product):
        """Метод для добавления товара в категорию"""
        self.__products.append(product)
        # Увеличиваем общий счетчик товаров при добавлении нового продукта
        Category.product_count += 1

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

    @property
    def products(self):
        """
        Геттер для получения списка товаров в отформатированном виде.
        Теперь использует магический метод __str__ класса Product.
        Возвращает строку с информацией о каждом товаре.
        """
        products_str = ""
        for product in self.__products:
            # Преобразуем объект продукта в строку с помощью str(product)
            # что автоматически вызывает метод __str__ класса Product
            products_str += str(product) + "\n"
        return products_str.strip()  # Убираем последний перенос строки

    @property
    def products_list(self):
        """Геттер для получения списка товаров (для внутреннего использования)"""
        return self.__products

