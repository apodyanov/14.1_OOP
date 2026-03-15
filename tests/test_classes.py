import pytest

from src.classes import Category, CategoryIterator, Product


# Фикстуры для создания тестовых данных
@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта"""
    return Product("Тестовый продукт", "Тестовое описание", 100.0, 10)


@pytest.fixture
def sample_products():
    """Фикстура для создания списка тестовых продуктов"""
    return [
        Product("Продукт 1", "Описание 1", 100.0, 5),
        Product("Продукт 2", "Описание 2", 200.0, 3),
        Product("Продукт 3", "Описание 3", 300.0, 2),
    ]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура для создания тестовой категории"""
    return Category("Тестовая категория", "Тестовое описание категории", sample_products)


# Тесты для класса Product
class TestProduct:
    """Тесты для класса Product"""

    def test_product_initialization(self, sample_product):
        """Тест инициализации продукта"""
        assert sample_product.name == "Тестовый продукт"
        assert sample_product.description == "Тестовое описание"
        assert sample_product.price == 100.0
        assert sample_product.quantity == 10

    def test_price_getter_setter(self, sample_product):
        """Тест геттера и сеттера цены"""
        # Проверка начальной цены
        assert sample_product.price == 100.0

        # Проверка установки корректной цены
        sample_product.price = 150.0
        assert sample_product.price == 150.0

        # Проверка установки некорректной цены (должен вывести сообщение, но не изменить цену)
        sample_product.price = -50.0
        assert sample_product.price == 150.0  # Цена не должна измениться

        sample_product.price = 0
        assert sample_product.price == 150.0  # Цена не должна измениться

    def test_product_str(self, sample_product):
        """Тест строкового представления продукта"""
        expected_str = "Тестовый продукт, 100.0 руб. Остаток: 10 шт."
        assert str(sample_product) == expected_str

    def test_product_add(self):
        """Тест сложения продуктов"""
        product_a = Product("Товар A", "Описание A", 100.0, 10)
        product_b = Product("Товар B", "Описание B", 200.0, 2)

        # Проверка сложения продуктов
        total = product_a + product_b
        expected_total = 100.0 * 10 + 200.0 * 2  # 1000 + 400 = 1400
        assert total == expected_total

        # Проверка сложения с другими продуктами
        product_c = Product("Товар C", "Описание C", 50.0, 5)
        total2 = product_b + product_c
        expected_total2 = 200.0 * 2 + 50.0 * 5  # 400 + 250 = 650
        assert total2 == expected_total2

    def test_new_product_creation(self):
        """Тест создания нового продукта через класс-метод"""
        product_data = {"name": "Новый продукт", "description": "Новое описание", "price": 500.0, "quantity": 7}

        product = Product.new_product(product_data)
        assert product.name == "Новый продукт"
        assert product.description == "Новое описание"
        assert product.price == 500.0
        assert product.quantity == 7

    def test_new_product_with_duplicate(self, sample_products):
        """Тест обработки дубликатов при создании продукта"""
        # Создаем дубликат существующего продукта
        duplicate_data = {
            "name": "Продукт 1",  # Совпадает с именем первого продукта из фикстуры
            "description": "Новое описание",
            "price": 150.0,  # Цена выше существующей
            "quantity": 3,
        }

        # Создаем продукт с проверкой на дубликаты
        product = Product.new_product(duplicate_data, sample_products)

        # Должен вернуться существующий продукт с обновленными данными
        assert product.name == "Продукт 1"
        assert product.price == 150.0  # Цена должна обновиться на максимальную
        assert product.quantity == 8  # 5 (было) + 3 (новых) = 8

    def test_new_product_with_lower_price_duplicate(self, sample_products):
        """Тест обработки дубликата с более низкой ценой"""
        duplicate_data = {
            "name": "Продукт 2",  # Существующий продукт с ценой 200.0
            "description": "Новое описание",
            "price": 150.0,  # Цена ниже существующей
            "quantity": 4,
        }

        product = Product.new_product(duplicate_data, sample_products)

        # Цена не должна обновиться (остается максимальная)
        assert product.price == 200.0
        assert product.quantity == 7  # 3 (было) + 4 (новых) = 7


# Тесты для класса Category
class TestCategory:
    """Тесты для класса Category"""

    def test_category_initialization(self, sample_category, sample_products):
        """Тест инициализации категории"""
        assert sample_category.name == "Тестовая категория"
        assert sample_category.description == "Тестовое описание категории"
        assert len(sample_category.products_list) == 3
        assert sample_category.products_list == sample_products

    def test_category_counters(self, sample_category):
        """Тест счетчиков категорий и продуктов"""
        # Сохраняем текущие значения счетчиков
        initial_category_count = Category.category_count
        initial_product_count = Category.product_count

        # Создаем новую категорию
        new_category = Category("Новая категория", "Описание", [])

        # Проверяем увеличение счетчиков
        assert Category.category_count == initial_category_count + 1
        assert Category.product_count == initial_product_count  # Не изменился, т.к. товаров нет

        # Создаем продукт и добавляем в категорию
        product = Product("Тест", "Описание", 100.0, 1)
        new_category.add_product(product)

        # Проверяем увеличение счетчика продуктов
        assert Category.product_count == initial_product_count + 1

    def test_add_product(self, sample_category):
        """Тест добавления продукта в категорию"""
        initial_count = len(sample_category.products_list)
        initial_product_count = Category.product_count

        new_product = Product("Новый продукт", "Новое описание", 300.0, 5)
        sample_category.add_product(new_product)

        assert len(sample_category.products_list) == initial_count + 1
        assert sample_category.products_list[-1] == new_product
        assert Category.product_count == initial_product_count + 1

    def test_add_product_with_check_new(self, sample_category):
        """Тест добавления нового продукта с проверкой на дубликаты"""
        initial_count = len(sample_category.products_list)

        product_data = {
            "name": "Совершенно новый продукт",
            "description": "Описание нового продукта",
            "price": 400.0,
            "quantity": 2,
        }

        product = sample_category.add_product_with_check(product_data)

        assert len(sample_category.products_list) == initial_count + 1
        assert product.name == "Совершенно новый продукт"
        assert product.price == 400.0
        assert product.quantity == 2

    def test_add_product_with_check_duplicate(self, sample_category):
        """Тест добавления дубликата продукта с проверкой"""
        initial_count = len(sample_category.products_list)

        # Данные дубликата существующего продукта
        product_data = {
            "name": "Продукт 1",  # Существующий продукт
            "description": "Обновленное описание",
            "price": 250.0,  # Более высокая цена
            "quantity": 3,
        }

        product = sample_category.add_product_with_check(product_data)

        # Количество продуктов не должно увеличиться (обновился существующий)
        assert len(sample_category.products_list) == initial_count
        assert product.quantity == 8  # 5 (было) + 3 (новых) = 8
        assert product.price == 250.0  # Цена обновилась

    def test_category_str(self, sample_category):
        """Тест строкового представления категории"""
        # В категории 3 продукта с количеством: 5, 3, 2 = всего 10
        expected_str = "Тестовая категория, количество продуктов: 10 шт."
        assert str(sample_category) == expected_str

    def test_products_property(self, sample_category, sample_products):
        """Тест геттера products (строковое представление всех продуктов)"""
        expected_output = (
            "Продукт 1, 100.0 руб. Остаток: 5 шт.\n"
            "Продукт 2, 200.0 руб. Остаток: 3 шт.\n"
            "Продукт 3, 300.0 руб. Остаток: 2 шт."
        )
        assert sample_category.products == expected_output


# Тесты для класса CategoryIterator
class TestCategoryIterator:
    """Тесты для класса CategoryIterator"""

    def test_iterator_creation(self, sample_category):
        """Тест создания итератора"""
        iterator = CategoryIterator(sample_category)
        assert isinstance(iterator, CategoryIterator)
        assert iterator._category == sample_category
        assert iterator._index == 0

    def test_iterator_iter_method(self, sample_category):
        """Тест метода __iter__ итератора"""
        iterator = CategoryIterator(sample_category)
        # Метод __iter__ должен возвращать сам итератор
        assert iterator.__iter__() is iterator

    def test_iterator_next_method(self, sample_category, sample_products):
        """Тест метода __next__ итератора"""
        iterator = CategoryIterator(sample_category)

        # Должен вернуть продукты по порядку
        assert next(iterator) == sample_products[0]
        assert iterator._index == 1

        assert next(iterator) == sample_products[1]
        assert iterator._index == 2

        assert next(iterator) == sample_products[2]
        assert iterator._index == 3

        # При попытке получить следующий продукт должно быть исключение StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

        # Индекс должен сброситься после StopIteration
        assert iterator._index == 0

    def test_category_iter_method(self, sample_category):
        """Тест метода __iter__ категории"""
        # Метод __iter__ категории должен возвращать итератор
        iterator = iter(sample_category)
        assert isinstance(iterator, CategoryIterator)
        assert iterator._category == sample_category

    def test_category_in_for_loop(self, sample_category, sample_products):
        """Тест использования категории в цикле for"""
        collected_products = []
        for product in sample_category:
            collected_products.append(product)

        # Должны быть собраны все продукты в правильном порядке
        assert collected_products == sample_products
        assert len(collected_products) == 3

    def test_iterator_with_empty_category(self):
        """Тест итератора с пустой категорией"""
        empty_category = Category("Пустая", "Описание", [])

        # Проверка в цикле for
        products_in_loop = []
        for product in empty_category:
            products_in_loop.append(product)

        assert len(products_in_loop) == 0

        # Проверка через явный итератор
        iterator = iter(empty_category)
        with pytest.raises(StopIteration):
            next(iterator)

    def test_multiple_iterations(self, sample_category):
        """Тест множественных итераций по одной категории"""
        # Первая итерация
        first_iteration = [p for p in sample_category]

        # Вторая итерация (должна работать заново)
        second_iteration = [p for p in sample_category]

        # Обе итерации должны дать одинаковый результат
        assert first_iteration == second_iteration
        assert len(first_iteration) == 3
        assert len(second_iteration) == 3

    def test_iterator_independence(self, sample_category):
        """Тест независимости разных итераторов одной категории"""
        iterator1 = iter(sample_category)
        iterator2 = iter(sample_category)

        # Продвигаем первый итератор
        next(iterator1)
        assert iterator1._index == 1
        assert iterator2._index == 0  # Второй итератор не должен измениться

        # Продвигаем второй итератор
        next(iterator2)
        assert iterator1._index == 1
        assert iterator2._index == 1

        # Продвигаем первый итератор дальше
        next(iterator1)
        assert iterator1._index == 2
        assert iterator2._index == 1


# Интеграционные тесты
class TestIntegration:
    """Интеграционные тесты для проверки взаимодействия классов"""

    def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        # Создаем продукты
        product1 = Product("Ноутбук", "Игровой ноутбук", 100000.0, 3)
        product2 = Product("Мышь", "Беспроводная мышь", 5000.0, 10)
        product3 = Product("Клавиатура", "Механическая клавиатура", 15000.0, 5)

        # Создаем категорию
        category = Category("Компьютеры", "Компьютерная периферия", [product1, product2])

        # Проверяем счетчики
        assert Category.category_count > 0
        assert Category.product_count >= 13  # 3 + 10

        # Добавляем продукт
        category.add_product(product3)

        # Проверяем строковое представление
        assert "Компьютеры" in str(category)

        # Проверяем сложение продуктов
        total_value = product1 + product2
        expected = 100000.0 * 3 + 5000.0 * 10  # 300000 + 50000 = 350000
        assert total_value == expected

        # Проверяем итерацию
        products_in_category = []
        for product in category:
            products_in_category.append(product)

        assert len(products_in_category) == 3
        assert products_in_category[0].name == "Ноутбук"
        assert products_in_category[1].name == "Мышь"
        assert products_in_category[2].name == "Клавиатура"

        # Проверяем добавление с проверкой дубликатов
        duplicate_data = {"name": "Мышь", "description": "Новая беспроводная мышь", "price": 6000.0, "quantity": 5}

        updated_product = category.add_product_with_check(duplicate_data)
        assert updated_product.quantity == 15  # 10 + 5
        assert updated_product.price == 6000.0  # Обновилась на максимальную

        # Проверяем общую стоимость после обновления
        new_total = product1 + updated_product
        expected_new = 100000.0 * 3 + 6000.0 * 15  # 300000 + 90000 = 390000
        assert new_total == expected_new


# Тесты для проверки старых требований (чтобы убедиться, что они не сломались)
class TestLegacyRequirements:
    """Тесты для проверки, что старая функциональность работает"""

    def test_category_counters_legacy(self):
        """Тест счетчиков категорий и продуктов (старая функциональность)"""
        # Сбрасываем счетчики для чистоты теста
        Category.category_count = 0
        Category.product_count = 0

        # Создаем продукты
        p1 = Product("p1", "d1", 100, 5)
        p2 = Product("p2", "d2", 200, 3)

        # Создаем первую категорию с продуктами
        category1 = Category("category1", "description1", [p1, p2])
        assert Category.category_count == 1
        assert Category.product_count == 2  # 2 продукта в списке
        assert len(category1.products_list) == 2  # Проверяем, что продукты действительно добавлены

        # Создаем вторую категорию без продуктов
        category2 = Category("category2", "description2", [])
        assert Category.category_count == 2
        assert Category.product_count == 2  # Не изменилось
        assert len(category2.products_list) == 0  # Проверяем, что категория пустая

        # Добавляем продукт во вторую категорию
        category2.add_product(p1)
        assert Category.product_count == 3  # Увеличилось на 1
        assert len(category2.products_list) == 1  # Проверяем, что продукт добавлен
        assert category2.products_list[0] == p1  # Проверяем, что добавлен правильный продукт

        # Проверяем, что первая категория не изменилась
        assert len(category1.products_list) == 2
        assert category1.products_list[0] == p1
        assert category1.products_list[1] == p2

    def test_price_validation_legacy(self):
        """Тест валидации цены (старая функциональность)"""
        product = Product("Тест", "Описание", 100, 5)

        # Попытка установить отрицательную цену
        product.price = -50
        assert product.price == 100  # Цена не изменилась

        # Попытка установить нулевую цену
        product.price = 0
        assert product.price == 100  # Цена не изменилась

        # Установка корректной цены
        product.price = 150
        assert product.price == 150

    def test_new_product_creation_legacy(self):
        """Тест создания продукта через класс-метод (старая функциональность)"""
        data = {"name": "Тест", "description": "Описание", "price": 100, "quantity": 5}
        product = Product.new_product(data)

        assert isinstance(product, Product)
        assert product.name == "Тест"
        assert product.price == 100
        assert product.quantity == 5
