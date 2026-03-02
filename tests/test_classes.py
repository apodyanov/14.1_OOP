import pytest
from main import Product, Category


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта"""
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


@pytest.fixture
def sample_category(sample_product):
    """Фикстура для создания тестовой категории"""
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [sample_product],
    )


def test_product_initialization(sample_product):
    """Тест проверки инициализации объекта класса Product"""
    assert sample_product.name == "Samsung Galaxy S23 Ultra"
    assert sample_product.description == "256GB, Серый цвет, 200MP камера"
    assert sample_product.price == 180000.0
    assert sample_product.quantity == 5


def test_category_initialization(sample_category):
    """Тест проверки инициализации объекта класса Category"""
    assert sample_category.name == "Смартфоны"
    assert sample_category.description == (
        "Смартфоны, как средство не только коммуникации, " "но и получения дополнительных функций для удобства жизни"
    )
    assert len(sample_category.products) == 1


def test_category_count_increase(sample_category):
    """Тест проверки увеличения счетчика категорий"""
    initial_count = Category.category_count

    # Создаем новую категорию
    category2 = Category("Телевизоры", "Современные телевизоры", [])

    assert Category.category_count == initial_count + 1
    assert Category.category_count > 0


def test_product_count_increase(sample_category):
    """Тест проверки увеличения счетчика продуктов"""
    initial_product_count = Category.product_count

    # Создаем продукт и новую категорию с этим продуктом
    product1 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    category2 = Category("Смартфоны", "Бюджетные смартфоны", [product1])

    assert Category.product_count == initial_product_count + 1
    assert Category.product_count > 0


def test_category_without_products():
    """Тест проверки создания категории без товаров"""
    category = Category("Пустая категория", "Категория без товаров")

    assert category.name == "Пустая категория"
    assert category.description == "Категория без товаров"
    assert len(category.products) == 0


def test_multiple_products_in_category():
    """Тест проверки категории с несколькими товарами"""
    product1 = Product("Товар 1", "Описание 1", 100.0, 10)
    product2 = Product("Товар 2", "Описание 2", 200.0, 20)
    product3 = Product("Товар 3", "Описание 3", 300.0, 30)

    category = Category("Тестовая категория", "Описание", [product1, product2, product3])

    assert len(category.products) == 3
    assert category.products[0].name == "Товар 1"
    assert category.products[1].name == "Товар 2"
    assert category.products[2].name == "Товар 3"


def test_category_products_are_product_objects(sample_category):
    """Тест проверки, что в списке товаров категории хранятся объекты Product"""

    # Проверяем, что каждый элемент в списке products является экземпляром класса Product
    for product in sample_category.products:
        assert isinstance(product, Product)

    # Также можно проверить, что у объектов есть все необходимые атрибуты Product
    if sample_category.products:
        product = sample_category.products[0]
        assert hasattr(product, "name")
        assert hasattr(product, "description")
        assert hasattr(product, "price")
        assert hasattr(product, "quantity")


def test_add_product_to_category():
    """Тест проверки добавления объекта Product в категорию"""

    # Создаем продукт
    new_product = Product("iPhone 15", "128GB, Black", 120000.0, 3)

    # Создаем категорию
    category = Category("Смартфоны", "Разные смартфоны")

    # Добавляем продукт в категорию (как объект)
    category.products.append(new_product)

    # Проверяем, что добавился именно объект Product
    assert len(category.products) == 1
    assert isinstance(category.products[0], Product)
    assert category.products[0].name == "iPhone 15"
    assert category.products[0].price == 120000.0
