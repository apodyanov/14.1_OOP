import pytest
from main import Product, Category


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта"""
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


@pytest.fixture
def sample_category(sample_product):
    """Фикстура для создания тестовой категории"""
    category = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    category.add_product(sample_product)  # Используем новый метод add_product
    return category


@pytest.fixture
def product_data():
    """Фикстура с данными для создания продукта через класс-метод"""
    return {
        'name': 'Xiaomi Redmi Note 11',
        'description': '1024GB, Синий',
        'price': 31000.0,
        'quantity': 14
    }


def test_product_initialization(sample_product):
    """Тест проверки инициализации объекта класса Product"""
    assert sample_product.name == "Samsung Galaxy S23 Ultra"
    assert sample_product.description == "256GB, Серый цвет, 200MP камера"
    assert sample_product.price == 180000.0  # Используем геттер
    assert sample_product.quantity == 5


def test_product_price_getter_setter():
    """Тест проверки геттера и сеттера для цены"""
    product = Product("Тест", "Описание", 100.0, 5)

    # Проверка геттера
    assert product.price == 100.0

    # Проверка сеттера с корректной ценой
    product.price = 150.0
    assert product.price == 150.0

    # Проверка сеттера с нулевой ценой
    product.price = 0
    assert product.price == 150.0  # Цена не должна измениться

    # Проверка сеттера с отрицательной ценой
    product.price = -50.0
    assert product.price == 150.0  # Цена не должна измениться


def test_product_new_product_classmethod(product_data):
    """Тест проверки класс-метода new_product"""
    product = Product.new_product(product_data)

    assert isinstance(product, Product)
    assert product.name == "Xiaomi Redmi Note 11"
    assert product.description == "1024GB, Синий"
    assert product.price == 31000.0
    assert product.quantity == 14


def test_product_new_product_with_duplicate_check(product_data):
    """Тест проверки класс-метода new_product с обнаружением дубликата"""
    # Создаем первый продукт
    product1 = Product.new_product(product_data)

    # Создаем список существующих продуктов
    existing_products = [product1]

    # Создаем дубликат с более высокой ценой и дополнительным количеством
    duplicate_data = {
        'name': 'Xiaomi Redmi Note 11',  # То же имя
        'description': '1024GB, Красный',  # Другое описание
        'price': 32000.0,  # Более высокая цена
        'quantity': 5  # Дополнительное количество
    }

    # Вызываем класс-метод с проверкой дубликатов
    result = Product.new_product(duplicate_data, existing_products)

    # Проверяем, что вернулся тот же объект (не новый)
    assert result is product1
    # Проверяем, что количество увеличилось
    assert result.quantity == 19  # 14 + 5
    # Проверяем, что цена обновилась на максимальную
    assert result.price == 32000.0


def test_product_new_product_with_lower_price_duplicate(product_data):
    """Тест проверки класс-метода new_product с дубликатом с меньшей ценой"""
    # Создаем первый продукт
    product1 = Product.new_product(product_data)

    existing_products = [product1]

    # Создаем дубликат с меньшей ценой
    duplicate_data = {
        'name': 'Xiaomi Redmi Note 11',
        'description': '1024GB, Зеленый',
        'price': 30000.0,  # Меньшая цена
        'quantity': 3
    }

    result = Product.new_product(duplicate_data, existing_products)

    # Проверяем, что вернулся тот же объект
    assert result is product1
    # Проверяем, что количество увеличилось
    assert result.quantity == 17  # 14 + 3
    # Проверяем, что цена НЕ обновилась (осталась большей)
    assert result.price == 31000.0


def test_category_initialization(sample_category):
    """Тест проверки инициализации объекта класса Category"""
    assert sample_category.name == "Смартфоны"
    assert sample_category.description == (
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    # Проверяем через геттер products
    assert len(sample_category.products.split('\n')) == 1  # products возвращает строку


def test_category_private_products_attribute(sample_category):
    """Тест проверки, что атрибут __products действительно приватный"""
    # Проверяем, что нет прямого доступа к __products
    all_attrs = dir(sample_category)
    assert "__products" not in all_attrs, "Приватный атрибут не должен быть напрямую доступен"

    # Проверяем, что есть только публичный интерфейс
    assert "products" in all_attrs, "Должен быть доступен публичный геттер products"

    # Проверяем, что через публичный интерфейс можно получить данные
    assert isinstance(sample_category.products, str)

    # Дополнительно можно проверить, что данные действительно есть
    if sample_category.products != "В категории нет товаров":
        assert "Samsung" in sample_category.products


def test_category_products_property_format(sample_category, sample_product):
    """Тест проверки формата вывода геттера products"""
    products_str = sample_category.products

    # Проверяем, что строка содержит информацию о продукте в нужном формате
    expected_format = f"{sample_product.name}, {sample_product.price} руб. Остаток: {sample_product.quantity} шт."
    assert expected_format in products_str


def test_add_product_method():
    """Тест проверки метода add_product"""
    category = Category("Тест", "Описание")
    product = Product("Тестовый товар", "Описание", 100.0, 5)

    # Используем метод add_product
    category.add_product(product)

    # Проверяем через геттер
    products_str = category.products
    assert "Тестовый товар, 100.0 руб. Остаток: 5 шт." in products_str


def test_category_count_increase(sample_category):
    """Тест проверки увеличения счетчика категорий"""
    initial_count = Category.category_count

    # Создаем категорию без сохранения в переменную
    Category("Телевизоры", "Современные телевизоры")

    assert Category.category_count == initial_count + 1
    assert Category.category_count > 0


def test_product_count_increase():
    """Тест проверки увеличения счетчика продуктов"""
    initial_product_count = Category.product_count

    # Создаем продукт
    product1 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Создаем категорию и добавляем продукт через метод add_product
    category = Category("Смартфоны", "Бюджетные смартфоны")
    category.add_product(product1)

    # Проверяем, что счетчик увеличился на 1
    assert Category.product_count == initial_product_count + 1


def test_product_count_with_duplicate_addition(product_data):
    """Тест проверки счетчика продуктов при добавлении дубликата"""
    initial_count = Category.product_count

    category = Category("Тест", "Описание")

    # Добавляем первый продукт
    product1 = Product.new_product(product_data)
    category.add_product(product1)
    assert Category.product_count == initial_count + 1

    # Пытаемся добавить дубликат через add_product_with_check
    duplicate_data = {
        'name': 'Xiaomi Redmi Note 11',
        'description': 'Другое описание',
        'price': 32000.0,
        'quantity': 5
    }

    # Используем специальный метод для добавления с проверкой
    result = category.add_product_with_check(duplicate_data)

    # Проверяем, что счетчик НЕ увеличился (так как дубликат не добавил новый объект)
    assert Category.product_count == initial_count + 1
    # Но количество товара должно увеличиться
    assert result.quantity == 19


def test_category_without_products():
    """Тест проверки создания категории без товаров"""
    category = Category("Пустая категория", "Категория без товаров")

    assert category.name == "Пустая категория"
    assert category.description == "Категория без товаров"

    # Проверяем, что возвращается либо пустая строка, либо сообщение о пустой категории
    products_output = category.products
    assert products_output == "" or products_output == "В категории нет товаров"


def test_multiple_products_in_category():
    """Тест проверки категории с несколькими товарами"""
    product1 = Product("Товар 1", "Описание 1", 100.0, 10)
    product2 = Product("Товар 2", "Описание 2", 200.0, 20)
    product3 = Product("Товар 3", "Описание 3", 300.0, 30)

    category = Category("Тестовая категория", "Описание")
    category.add_product(product1)
    category.add_product(product2)
    category.add_product(product3)

    products_str = category.products
    assert "Товар 1, 100.0 руб. Остаток: 10 шт." in products_str
    assert "Товар 2, 200.0 руб. Остаток: 20 шт." in products_str
    assert "Товар 3, 300.0 руб. Остаток: 30 шт." in products_str


def test_category_products_are_product_objects(sample_category):
    """Тест проверки, что в списке товаров категории хранятся объекты Product"""
    # Используем вспомогательный геттер для получения списка объектов
    products_list = sample_category.products_list  # Добавьте этот геттер в класс Category

    # Проверяем, что каждый элемент является экземпляром класса Product
    for product in products_list:
        assert isinstance(product, Product)

    # Проверяем наличие всех необходимых атрибутов
    if products_list:
        product = products_list[0]
        assert hasattr(product, "name")
        assert hasattr(product, "description")
        assert hasattr(product, "price")
        assert hasattr(product, "quantity")


def test_add_product_to_category():
    """Тест проверки добавления объекта Product в категорию через метод add_product"""
    # Создаем продукт
    new_product = Product("iPhone 15", "128GB, Black", 120000.0, 3)

    # Создаем категорию
    category = Category("Смартфоны", "Разные смартфоны")

    # Добавляем продукт в категорию через метод
    category.add_product(new_product)

    # Проверяем через геттер
    products_str = category.products
    assert "iPhone 15, 120000.0 руб. Остаток: 3 шт." in products_str

    # Также проверяем через вспомогательный геттер
    products_list = category.products_list
    assert len(products_list) == 1
    assert isinstance(products_list[0], Product)
    assert products_list[0].name == "iPhone 15"
    assert products_list[0].price == 120000.0
