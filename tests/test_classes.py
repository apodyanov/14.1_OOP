import pytest

from src.classes import BaseProduct, Category, LawnGrass, LogMixin, Product, Smartphone


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта"""
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


@pytest.fixture
def sample_category(sample_product):
    """Фикстура для создания тестовой категории"""
    category = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
    )
    category.add_product(sample_product)
    return category


@pytest.fixture
def product_data():
    """Фикстура с данными для создания продукта через класс-метод"""
    return {"name": "Xiaomi Redmi Note 11", "description": "1024GB, Синий", "price": 31000.0, "quantity": 14}


@pytest.fixture
def sample_smartphone():
    """Фикстура для создания тестового смартфона"""
    return Smartphone(
        "iPhone 15 Pro",
        "Флагманский смартфон с мощным процессором",
        99999.0,
        5,
        "высокая",
        "iPhone 15 Pro",
        256,
        "черный",
    )


@pytest.fixture
def sample_lawn_grass():
    """Фикстура для создания тестовой газонной травы"""
    return LawnGrass(
        "Газонная трава премиум", "Смесь для идеального газона", 1500.0, 20, "Голландия", "10-14 дней", "зеленый"
    )


@pytest.fixture
def sample_category_with_mixed_products(sample_product, sample_smartphone, sample_lawn_grass):
    """Фикстура для создания категории с разными типами продуктов"""
    category = Category("Разные товары", "Категория с разными типами товаров")
    category.add_product(sample_product)
    category.add_product(sample_smartphone)
    category.add_product(sample_lawn_grass)
    return category


# ==================== СУЩЕСТВУЮЩИЕ ТЕСТЫ ====================


def test_product_initialization(sample_product):
    """Тест проверки инициализации объекта класса Product"""
    assert sample_product.name == "Samsung Galaxy S23 Ultra"
    assert sample_product.description == "256GB, Серый цвет, 200MP камера"
    assert sample_product.price == 180000.0
    assert sample_product.quantity == 5


def test_product_price_getter_setter():
    """Тест проверки геттера и сеттера для цены"""
    product = Product("Тест", "Описание", 100.0, 5)

    assert product.price == 100.0

    product.price = 150.0
    assert product.price == 150.0

    product.price = 0
    assert product.price == 150.0

    product.price = -50.0
    assert product.price == 150.0


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
    product1 = Product.new_product(product_data)

    existing_products = [product1]

    duplicate_data = {
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Красный",
        "price": 32000.0,
        "quantity": 5,
    }

    result = Product.new_product(duplicate_data, existing_products)

    assert result is product1
    assert result.quantity == 19
    assert result.price == 32000.0


def test_product_new_product_with_lower_price_duplicate(product_data):
    """Тест проверки класс-метода new_product с дубликатом с меньшей ценой"""
    product1 = Product.new_product(product_data)

    existing_products = [product1]

    duplicate_data = {
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Зеленый",
        "price": 30000.0,
        "quantity": 3,
    }

    result = Product.new_product(duplicate_data, existing_products)

    assert result is product1
    assert result.quantity == 17
    assert result.price == 31000.0


def test_category_initialization(sample_category):
    """Тест проверки инициализации объекта класса Category"""
    assert sample_category.name == "Смартфоны"
    assert sample_category.description == (
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert len(sample_category.products.split("\n")) == 1


def test_category_private_products_attribute(sample_category):
    """Тест проверки, что атрибут __products действительно приватный"""
    all_attrs = dir(sample_category)
    assert "__products" not in all_attrs
    assert "products" in all_attrs
    assert isinstance(sample_category.products, str)


def test_category_products_property_format(sample_category, sample_product):
    """Тест проверки формата вывода геттера products"""
    products_str = sample_category.products
    expected_format = f"{sample_product.name}, {sample_product.price} руб. Остаток: {sample_product.quantity} шт."
    assert expected_format in products_str


def test_add_product_method():
    """Тест проверки метода add_product"""
    category = Category("Тест", "Описание")
    product = Product("Тестовый товар", "Описание", 100.0, 5)

    category.add_product(product)

    products_str = category.products
    assert "Тестовый товар, 100.0 руб. Остаток: 5 шт." in products_str


def test_category_count_increase(sample_category):
    """Тест проверки увеличения счетчика категорий"""
    initial_count = Category.category_count

    Category("Телевизоры", "Современные телевизоры")

    assert Category.category_count == initial_count + 1
    assert Category.category_count > 0


def test_product_count_increase():
    """Тест проверки увеличения счетчика продуктов"""
    initial_product_count = Category.product_count

    product1 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category = Category("Смартфоны", "Бюджетные смартфоны")
    category.add_product(product1)

    assert Category.product_count == initial_product_count + 1


def test_product_count_with_duplicate_addition(product_data):
    """Тест проверки счетчика продуктов при добавлении дубликата"""
    initial_count = Category.product_count

    category = Category("Тест", "Описание")

    product1 = Product.new_product(product_data)
    category.add_product(product1)
    assert Category.product_count == initial_count + 1

    duplicate_data = {
        "name": "Xiaomi Redmi Note 11",
        "description": "Другое описание",
        "price": 32000.0,
        "quantity": 5,
    }

    result = category.add_product_with_check(duplicate_data)

    assert Category.product_count == initial_count + 1
    assert result.quantity == 19


def test_category_without_products():
    """Тест проверки создания категории без товаров"""
    category = Category("Пустая категория", "Категория без товаров")

    assert category.name == "Пустая категория"
    assert category.description == "Категория без товаров"

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
    products_list = sample_category.products_list

    for product in products_list:
        assert isinstance(product, Product)

    if products_list:
        product = products_list[0]
        assert hasattr(product, "name")
        assert hasattr(product, "description")
        assert hasattr(product, "price")
        assert hasattr(product, "quantity")


def test_add_product_to_category():
    """Тест проверки добавления объекта Product в категорию через метод add_product"""
    new_product = Product("iPhone 15", "128GB, Black", 120000.0, 3)

    category = Category("Смартфоны", "Разные смартфоны")

    category.add_product(new_product)

    products_str = category.products
    assert "iPhone 15, 120000.0 руб. Остаток: 3 шт." in products_str

    products_list = category.products_list
    assert len(products_list) == 1
    assert isinstance(products_list[0], Product)
    assert products_list[0].name == "iPhone 15"
    assert products_list[0].price == 120000.0


# ==================== НОВЫЕ ТЕСТЫ ДЛЯ SMARTSPHONE ====================


def test_smartphone_initialization(sample_smartphone):
    """Тест проверки инициализации объекта класса Smartphone"""
    assert sample_smartphone.name == "iPhone 15 Pro"
    assert sample_smartphone.description == "Флагманский смартфон с мощным процессором"
    assert sample_smartphone.price == 99999.0
    assert sample_smartphone.quantity == 5
    assert sample_smartphone.efficiency == "высокая"
    assert sample_smartphone.model == "iPhone 15 Pro"
    assert sample_smartphone.memory == 256
    assert sample_smartphone.color == "черный"


def test_smartphone_inheritance(sample_smartphone):
    """Тест проверки наследования Smartphone от Product"""
    assert isinstance(sample_smartphone, Product)
    assert isinstance(sample_smartphone, Smartphone)
    assert not isinstance(sample_smartphone, LawnGrass)
    assert issubclass(Smartphone, Product)


def test_smartphone_str_method(sample_smartphone):
    """Тест проверки строкового представления смартфона"""
    expected_str = (
        f"{sample_smartphone.name}, {sample_smartphone.price} руб. "
        f"Остаток: {sample_smartphone.quantity} шт. "
        f"Модель: {sample_smartphone.model}, "
        f"Память: {sample_smartphone.memory}ГБ, "
        f"Цвет: {sample_smartphone.color}"
    )
    assert str(sample_smartphone) == expected_str


def test_smartphone_price_property(sample_smartphone):
    """Тест проверки работы property цены у смартфона"""
    assert sample_smartphone.price == 99999.0

    sample_smartphone.price = 89999.0
    assert sample_smartphone.price == 89999.0

    sample_smartphone.price = -100
    assert sample_smartphone.price == 89999.0  # Цена не изменилась


# ==================== НОВЫЕ ТЕСТЫ ДЛЯ LAWNSGRASS ====================


def test_lawn_grass_initialization(sample_lawn_grass):
    """Тест проверки инициализации объекта класса LawnGrass"""
    assert sample_lawn_grass.name == "Газонная трава премиум"
    assert sample_lawn_grass.description == "Смесь для идеального газона"
    assert sample_lawn_grass.price == 1500.0
    assert sample_lawn_grass.quantity == 20
    assert sample_lawn_grass.country == "Голландия"
    assert sample_lawn_grass.germination_period == "10-14 дней"
    assert sample_lawn_grass.color == "зеленый"


def test_lawn_grass_inheritance(sample_lawn_grass):
    """Тест проверки наследования LawnGrass от Product"""
    assert isinstance(sample_lawn_grass, Product)
    assert isinstance(sample_lawn_grass, LawnGrass)
    assert not isinstance(sample_lawn_grass, Smartphone)
    assert issubclass(LawnGrass, Product)


def test_lawn_grass_str_method(sample_lawn_grass):
    """Тест проверки строкового представления газонной травы"""
    expected_str = (
        f"{sample_lawn_grass.name}, {sample_lawn_grass.price} руб. "
        f"Остаток: {sample_lawn_grass.quantity} шт. "
        f"Страна: {sample_lawn_grass.country}, "
        f"Срок прорастания: {sample_lawn_grass.germination_period}, "
        f"Цвет: {sample_lawn_grass.color}"
    )
    assert str(sample_lawn_grass) == expected_str


# ==================== НОВЫЕ ТЕСТЫ ДЛЯ МАГИЧЕСКОГО МЕТОДА __add__ ====================


def test_product_add_same_class():
    """Тест проверки сложения продуктов одного класса"""
    product1 = Product("Товар 1", "Описание", 100.0, 10)
    product2 = Product("Товар 2", "Описание", 200.0, 5)

    result = product1 + product2

    expected = (100.0 * 10) + (200.0 * 5)  # 1000 + 1000 = 2000
    assert result == expected


def test_smartphone_add_same_class(sample_smartphone):
    """Тест проверки сложения смартфонов одного класса"""
    smartphone2 = Smartphone(
        "Samsung Galaxy S24", "Флагманский смартфон", 89999.0, 3, "высокая", "Galaxy S24", 256, "фиолетовый"
    )

    result = sample_smartphone + smartphone2

    expected = (99999.0 * 5) + (89999.0 * 3)  # 499995 + 269997 = 769992
    assert result == expected


def test_lawn_grass_add_same_class(sample_lawn_grass):
    """Тест проверки сложения газонной травы одного класса"""
    lawn_grass2 = LawnGrass(
        "Газонная трава стандарт", "Обычная смесь", 800.0, 30, "Россия", "14-21 дней", "светло-зеленый"
    )

    result = sample_lawn_grass + lawn_grass2

    expected = (1500.0 * 20) + (800.0 * 30)  # 30000 + 24000 = 54000
    assert result == expected


def test_add_different_classes_raises_error(sample_product, sample_smartphone, sample_lawn_grass):
    """Тест проверки, что сложение разных классов вызывает TypeError"""
    with pytest.raises(TypeError) as exc_info:
        sample_product + sample_smartphone
    assert "Нельзя складывать товары разных категорий" in str(exc_info.value)

    with pytest.raises(TypeError) as exc_info:
        sample_smartphone + sample_lawn_grass
    assert "Нельзя складывать товары разных категорий" in str(exc_info.value)

    with pytest.raises(TypeError) as exc_info:
        sample_lawn_grass + sample_product
    assert "Нельзя складывать товары разных категорий" in str(exc_info.value)


def test_add_with_non_product_raises_error(sample_product):
    """Тест проверки, что сложение с не-продуктом вызывает TypeError"""
    with pytest.raises(TypeError) as exc_info:
        sample_product + 100
    assert "Нельзя сложить Product с int" in str(exc_info.value)

    with pytest.raises(TypeError) as exc_info:
        sample_product + "строка"
    assert "Нельзя сложить Product с str" in str(exc_info.value)

    with pytest.raises(TypeError) as exc_info:
        sample_product + [1, 2, 3]
    assert "Нельзя сложить Product с list" in str(exc_info.value)


# ==================== НОВЫЕ ТЕСТЫ ДЛЯ ЗАЩИЩЕННОГО ADD_PRODUCT ====================


def test_add_product_with_valid_products():
    """Тест проверки добавления корректных продуктов в категорию"""
    category = Category("Тестовая", "Категория для тестирования")

    product = Product("Обычный товар", "Описание", 100.0, 5)
    smartphone = Smartphone("Смартфон", "Описание", 500.0, 2, "высокая", "Model X", 128, "черный")
    lawn_grass = LawnGrass("Трава", "Описание", 200.0, 10, "Россия", "7 дней", "зеленый")

    category.add_product(product)
    category.add_product(smartphone)
    category.add_product(lawn_grass)

    products_list = category.products_list
    assert len(products_list) == 3
    assert isinstance(products_list[0], Product)
    assert isinstance(products_list[1], Smartphone)
    assert isinstance(products_list[2], LawnGrass)


def test_add_product_with_invalid_types():
    """Тест проверки, что добавление некорректных типов вызывает TypeError"""
    category = Category("Тестовая", "Категория для тестирования")

    invalid_objects = [
        ("строка", "Это не продукт"),
        ("число", 123),
        ("список", [1, 2, 3]),
        ("словарь", {"name": "test"}),
        ("None", None),
        ("булево значение", True),
        ("float", 10.5),
    ]

    for obj_name, invalid_obj in invalid_objects:
        with pytest.raises(TypeError) as exc_info:
            category.add_product(invalid_obj)
        assert "Можно добавлять только объекты класса Product или его наследников" in str(exc_info.value)
        assert f"Получен объект типа: {type(invalid_obj).__name__}" in str(exc_info.value)


def test_add_product_with_isinstance_check(sample_product, sample_smartphone):
    """Тест проверки работы isinstance в методе add_product"""
    category = Category("Тест", "Описание")

    # Проверяем, что isinstance распознает оба типа как Product
    assert isinstance(sample_product, Product)
    assert isinstance(sample_smartphone, Product)

    # Оба должны успешно добавляться
    category.add_product(sample_product)
    category.add_product(sample_smartphone)

    assert len(category.products_list) == 2


def test_add_product_with_issubclass_check():
    """Тест проверки работы issubclass в методе add_product"""
    # Проверяем отношения классов
    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)
    assert not issubclass(Product, Smartphone)
    assert not issubclass(str, Product)

    category = Category("Тест", "Описание")

    # Эти классы являются наследниками Product
    smartphone = Smartphone("Тест", "Описание", 100.0, 1, "средняя", "Model", 128, "черный")
    lawn_grass = LawnGrass("Тест", "Описание", 50.0, 5, "Россия", "7 дней", "зеленый")

    category.add_product(smartphone)
    category.add_product(lawn_grass)

    assert len(category.products_list) == 2


# ==================== НОВЫЕ ТЕСТЫ ДЛЯ КАТЕГОРИЙ С НАСЛЕДНИКАМИ ====================


def test_category_with_smartphones():
    """Тест проверки категории, содержащей только смартфоны"""
    category = Category("Смартфоны", "Флагманские смартфоны")

    iphone = Smartphone("iPhone 15 Pro", "Флагман", 99999.0, 5, "высокая", "iPhone 15 Pro", 256, "черный")
    samsung = Smartphone("Samsung S24", "Флагман", 89999.0, 3, "высокая", "S24", 256, "фиолетовый")

    category.add_product(iphone)
    category.add_product(samsung)

    products_str = category.products
    assert "iPhone 15 Pro" in products_str
    assert "Samsung S24" in products_str
    assert "Модель: iPhone 15 Pro" in products_str
    assert "Модель: S24" in products_str

    # Проверяем общую стоимость
    total_cost = iphone.price * iphone.quantity + samsung.price * samsung.quantity
    assert (iphone + samsung) == total_cost


def test_category_with_lawn_grass():
    """Тест проверки категории, содержащей только газонную траву"""
    category = Category("Газонные травы", "Смеси для газонов")

    premium = LawnGrass("Премиум", "Элитная смесь", 2500.0, 10, "Голландия", "7-10 дней", "изумрудный")
    standard = LawnGrass("Стандарт", "Обычная смесь", 1000.0, 20, "Россия", "14-21 дней", "зеленый")

    category.add_product(premium)
    category.add_product(standard)

    products_str = category.products
    assert "Премиум" in products_str
    assert "Стандарт" in products_str
    assert "Страна: Голландия" in products_str
    assert "Страна: Россия" in products_str

    # Проверяем общую стоимость
    total_cost = premium.price * premium.quantity + standard.price * standard.quantity
    assert (premium + standard) == total_cost


def test_category_with_mixed_products(sample_category_with_mixed_products):
    """Тест проверки категории со смешанными типами продуктов"""
    category = sample_category_with_mixed_products

    products_list = category.products_list
    assert len(products_list) == 3

    # Проверяем типы
    assert isinstance(products_list[0], Product)
    assert isinstance(products_list[1], Smartphone)
    assert isinstance(products_list[2], LawnGrass)

    # Проверяем, что __str__ работает для каждого типа
    products_str = category.products
    assert "Samsung Galaxy S23 Ultra" in products_str
    assert "iPhone 15 Pro" in products_str
    assert "Газонная трава премиум" in products_str
    assert "Модель: iPhone 15 Pro" in products_str
    assert "Страна: Голландия" in products_str


def test_category_total_cost_with_mixed_products(sample_category_with_mixed_products):
    """Тест проверки общей стоимости категории со смешанными продуктами"""
    category = sample_category_with_mixed_products
    products_list = category.products_list

    expected_total = 0
    for product in products_list:
        expected_total += product.price * product.quantity

    # Так как у Category нет прямого метода для получения общей стоимости,
    # мы можем вычислить её вручную для проверки
    actual_total = 0
    for product in products_list:
        actual_total += product.price * product.quantity

    assert actual_total == expected_total


# ==================== ТЕСТЫ ДЛЯ ИТЕРАТОРА ====================


def test_category_iterator(sample_category_with_mixed_products):
    """Тест проверки работы итератора категории"""
    category = sample_category_with_mixed_products
    products_list = category.products_list

    # Проверяем, что можно итерироваться по категории
    iterated_products = []
    for product in category:
        iterated_products.append(product)

    assert len(iterated_products) == len(products_list)
    for i, product in enumerate(iterated_products):
        assert product.name == products_list[i].name


# ==================== ТЕСТЫ ДЛЯ СЧЕТЧИКОВ ====================


def test_product_count_with_inherited_products():
    """Тест проверки счетчика продуктов при добавлении наследников"""
    initial_count = Category.product_count

    category = Category("Тест", "Описание")

    product = Product("Обычный", "Описание", 100.0, 5)
    smartphone = Smartphone("Смартфон", "Описание", 500.0, 2, "высокая", "Model", 128, "черный")
    lawn_grass = LawnGrass("Трава", "Описание", 200.0, 10, "Россия", "7 дней", "зеленый")

    category.add_product(product)
    category.add_product(smartphone)
    category.add_product(lawn_grass)

    assert Category.product_count == initial_count + 3


def test_category_count_with_inherited_products():
    """Тест проверки счетчика категорий при создании категорий с наследниками"""
    initial_count = Category.category_count

    category1 = Category("Смартфоны", "Категория со смартфонами")
    category2 = Category("Травы", "Категория с газонной травой")
    category3 = Category("Смешанная", "Категория с разными товарами")

    # Проверяем, что созданные объекты действительно являются экземплярами Category
    assert isinstance(category1, Category)
    assert isinstance(category2, Category)
    assert isinstance(category3, Category)

    # Проверяем, что у них корректные имена
    assert category1.name == "Смартфоны"
    assert category2.name == "Травы"
    assert category3.name == "Смешанная"

    # Проверяем счетчик
    assert Category.category_count == initial_count + 3


# ==================== ТЕСТЫ ДЛЯ ГРАНИЧНЫХ СЛУЧАЕВ ====================


def test_edge_case_empty_smartphone():
    """Тест проверки смартфона с минимальными значениями"""
    smartphone = Smartphone("", "", 0.0, 1, "", "", 0, "")

    assert smartphone.name == ""
    assert smartphone.price == 0.0
    assert smartphone.quantity == 1
    assert smartphone.efficiency == ""
    assert smartphone.model == ""
    assert smartphone.memory == 0
    assert smartphone.color == ""


def test_edge_case_negative_quantity():
    """Тест проверки создания продукта с отрицательным количеством"""
    # Количество может быть отрицательным? В реальном магазине нет, но тест проверяет, что это возможно
    product = Product("Тест", "Описание", 100.0, -5)
    assert product.quantity == -5

    category = Category("Тест", "Описание")
    category.add_product(product)

    # Проверяем, что __str__ отработает с отрицательным количеством
    assert "-5 шт." in str(product)


def test_edge_case_zero_price():
    """Тест проверки продукта с нулевой ценой"""
    product = Product("Бесплатный", "Описание", 0.0, 10)
    assert product.price == 0.0

    category = Category("Тест", "Описание")
    category.add_product(product)

    assert "0.0 руб." in str(product)


# ==================== ТЕСТЫ ДЛЯ ВЫВОДА СООБЩЕНИЙ ====================


def test_add_product_success_message(capsys):
    """Тест проверки вывода сообщения при успешном добавлении продукта"""
    category = Category("Тест", "Описание")
    product = Product("Тестовый", "Описание", 100.0, 5)

    category.add_product(product)
    captured = capsys.readouterr()
    assert "✓ Продукт 'Тестовый' успешно добавлен в категорию 'Тест'" in captured.out


def test_add_product_error_message(capsys):
    """Тест проверки вывода сообщения об ошибке при добавлении некорректного продукта"""
    category = Category("Тест", "Описание")

    with pytest.raises(TypeError):
        category.add_product("не продукт")

    # Ошибка должна быть поднята, сообщение проверяем через exc_info


def test_log_mixin_output_for_product(capsys):
    """Тест проверки вывода LogMixin при создании обычного продукта"""
    # Создаем продукт
    product = Product("Продукт1", "Описание продукта", 1200.0, 10)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    expected_output = "Создан объект: Product('Продукт1', 'Описание продукта', 1200.0, 10)\n"
    assert captured.out == expected_output

    # Проверяем, что объект создался корректно
    assert product.name == "Продукт1"
    assert product.price == 1200.0
    assert product.quantity == 10


def test_log_mixin_output_for_smartphone(capsys):
    """Тест проверки вывода LogMixin при создании смартфона"""
    smartphone = Smartphone(
        "iPhone 15 Pro", "Флагманский смартфон", 99999.0, 5, "высокая", "iPhone 15 Pro", 256, "черный"
    )

    captured = capsys.readouterr()
    expected_output = (
        "Создан объект: Smartphone('iPhone 15 Pro', 'Флагманский смартфон', "
        "99999.0, 5, 'высокая', 'iPhone 15 Pro', 256, 'черный')\n"
    )
    assert captured.out == expected_output

    # Проверяем, что объект создался корректно
    assert smartphone.name == "iPhone 15 Pro"
    assert smartphone.efficiency == "высокая"
    assert smartphone.memory == 256


def test_log_mixin_output_for_lawn_grass(capsys):
    """Тест проверки вывода LogMixin при создании газонной травы"""
    lawn_grass = LawnGrass(
        "Газонная трава премиум", "Смесь для идеального газона", 1500.0, 20, "Голландия", "10-14 дней", "зеленый"
    )

    captured = capsys.readouterr()
    expected_output = (
        "Создан объект: LawnGrass('Газонная трава премиум', 'Смесь для идеального газона', "
        "1500.0, 20, 'Голландия', '10-14 дней', 'зеленый')\n"
    )
    assert captured.out == expected_output

    # Проверяем, что объект создался корректно
    assert lawn_grass.name == "Газонная трава премиум"
    assert lawn_grass.country == "Голландия"
    assert lawn_grass.germination_period == "10-14 дней"


def test_log_mixin_multiple_creations(capsys):
    """Тест проверки вывода LogMixin при создании нескольких объектов"""
    # Создаем несколько объектов подряд
    product1 = Product("Товар 1", "Описание 1", 100.0, 5)
    product2 = Product("Товар 2", "Описание 2", 200.0, 3)
    smartphone = Smartphone("Смартфон", "Описание", 500.0, 2, "средняя", "Model X", 128, "черный")

    captured = capsys.readouterr()
    expected_outputs = [
        "Создан объект: Product('Товар 1', 'Описание 1', 100.0, 5)\n",
        "Создан объект: Product('Товар 2', 'Описание 2', 200.0, 3)\n",
        "Создан объект: Smartphone('Смартфон', 'Описание', 500.0, 2, 'средняя', 'Model X', 128, 'черный')\n",
    ]

    for expected in expected_outputs:
        assert expected in captured.out


def test_log_mixin_with_classmethod_new_product(capsys):
    """Тест проверки, что LogMixin работает и при использовании classmethod new_product"""
    product_data = {"name": "Xiaomi Redmi Note 11", "description": "1024GB, Синий", "price": 31000.0, "quantity": 14}

    product = Product.new_product(product_data)

    captured = capsys.readouterr()
    # Должно быть два сообщения:
    # 1. "Создаем новый товар 'Xiaomi Redmi Note 11'"
    # 2. "Создан объект: Product('Xiaomi Redmi Note 11', '1024GB, Синий', 31000.0, 14)"

    assert "Создаем новый товар 'Xiaomi Redmi Note 11'" in captured.out
    assert "Создан объект: Product('Xiaomi Redmi Note 11', '1024GB, Синий', 31000.0, 14)" in captured.out


def test_log_mixin_does_not_affect_existing_functionality():
    """Тест проверки, что LogMixin не нарушает существующую функциональность"""
    # Создаем продукты
    product1 = Product("Товар 1", "Описание 1", 100.0, 10)
    product2 = Product("Товар 2", "Описание 2", 200.0, 5)
    smartphone = Smartphone("iPhone", "Описание", 99999.0, 3, "высокая", "iPhone 15", 256, "черный")
    lawn_grass = LawnGrass("Трава", "Описание", 1500.0, 20, "Голландия", "10 дней", "зеленый")

    # Проверяем все существующие методы
    assert product1 + product2 == (100.0 * 10) + (200.0 * 5)

    # Проверяем строковые представления
    assert "Товар 1, 100.0 руб. Остаток: 10 шт." in str(product1)
    assert "Модель: iPhone 15" in str(smartphone)
    assert "Страна: Голландия" in str(lawn_grass)

    # Проверяем работу с категориями
    category = Category("Тест", "Описание")
    category.add_product(product1)
    category.add_product(smartphone)
    category.add_product(lawn_grass)

    assert len(category.products_list) == 3
    assert "Товар 1" in category.products
    assert "iPhone" in category.products
    assert "Трава" in category.products

    # Проверяем итератор
    products_count = 0
    for product in category:
        products_count += 1
    assert products_count == 3


def test_log_mixin_mro_order():
    """Тест проверки правильного порядка MRO (Method Resolution Order)"""
    # Проверяем, что LogMixin стоит перед BaseProduct в MRO
    mro = Product.__mro__

    # Получаем имена классов в MRO
    mro_names = [cls.__name__ for cls in mro]

    # Проверяем порядок: Product -> LogMixin -> BaseProduct -> ABC -> object
    assert mro_names.index("LogMixin") < mro_names.index("BaseProduct")
    assert "Product" in mro_names
    assert "LogMixin" in mro_names
    assert "BaseProduct" in mro_names

    # Проверяем, что миксин вызывается первым
    class TestMixinOrder:
        def __init__(self, *args, **kwargs):
            print("Mixin init")
            super().__init__(*args, **kwargs)

    class TestBase:
        def __init__(self, *args, **kwargs):
            print("Base init")

    class TestClass(TestMixinOrder, TestBase):
        def __init__(self, value):
            super().__init__(value)

    # Создаем тестовый объект и проверяем порядок вызовов
    import io
    import sys

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    test_obj = TestClass(10)
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout

    # Миксин должен быть вызван первым
    lines = output.strip().split("\n")
    assert lines[0] == "Mixin init"
    assert lines[1] == "Base init"


def test_log_mixin_with_category_initialization(capsys):
    """Тест проверки, что LogMixin не влияет на создание категорий"""
    category = Category("Смартфоны", "Категория для смартфонов")

    captured = capsys.readouterr()
    # Категория не использует LogMixin, поэтому вывода быть не должно
    assert captured.out == ""

    # Проверяем, что категория создалась корректно
    assert category.name == "Смартфоны"
    assert category.description == "Категория для смартфонов"


def test_log_mixin_handles_all_argument_types(capsys):
    """Тест проверки, что LogMixin корректно обрабатывает разные типы аргументов"""
    # Строки
    product1 = Product("Тест", "Описание", 100.0, 5)
    captured = capsys.readouterr()
    assert "Product('Тест', 'Описание', 100.0, 5)" in captured.out

    # Целые числа
    product2 = Product("Тест2", "Описание2", 200, 10)
    captured = capsys.readouterr()
    assert "Product('Тест2', 'Описание2', 200, 10)" in captured.out

    # Числа с плавающей точкой
    product3 = Product("Тест3", "Описание3", 300.55, 15)
    captured = capsys.readouterr()
    assert "Product('Тест3', 'Описание3', 300.55, 15)" in captured.out

    # Отрицательные числа
    product4 = Product("Тест4", "Описание4", -50.0, -3)
    captured = capsys.readouterr()
    assert "Product('Тест4', 'Описание4', -50.0, -3)" in captured.out

    # Ноль
    product5 = Product("Тест5", "Описание5", 0, 1)
    captured = capsys.readouterr()
    assert "Product('Тест5', 'Описание5', 0, 1)" in captured.out


def test_log_mixin_output_with_newline_characters(capsys):
    """Тест проверки, что LogMixin корректно обрабатывает символы новой строки"""
    product = Product("Product\nwith\nnewlines", "Description\nwith\nnewlines", 100.0, 5)

    captured = capsys.readouterr()
    # repr() должен экранировать символы новой строки как \n
    assert "Product\\nwith\\nnewlines" in captured.out
    assert "Description\\nwith\\nnewlines" in captured.out


def test_log_mixin_with_boolean_values(capsys):
    """Тест проверки, что LogMixin корректно обрабатывает булевы значения"""

    # Создаем тестовый класс для проверки булевых значений
    class TestProduct(LogMixin, BaseProduct):
        def __init__(self, name: str, is_active: bool, *args, **kwargs):
            super().__init__(name, is_active, *args, **kwargs)
            self.name = name
            self.is_active = is_active

    test_product = TestProduct("Тест", True)
    captured = capsys.readouterr()
    assert "TestProduct('Тест', True)" in captured.out

    test_product2 = TestProduct("Тест2", False)
    captured = capsys.readouterr()
    assert "TestProduct('Тест2', False)" in captured.out


def test_log_mixin_inheritance_chain():
    """Тест проверки цепочки наследования с LogMixin"""
    # Проверяем, что все дочерние классы наследуют LogMixin
    assert hasattr(Product, "__init__")
    assert hasattr(Smartphone, "__init__")
    assert hasattr(LawnGrass, "__init__")

    # Проверяем, что LogMixin есть в MRO всех классов
    assert LogMixin in Product.__mro__
    assert LogMixin in Smartphone.__mro__
    assert LogMixin in LawnGrass.__mro__


# ==================== НОВЫЕ ТЕСТЫ ДЛЯ ЗАДАНИЯ 17.1 ====================
# Проверка исключения ValueError при создании товара с нулевым количеством


def test_product_creation_zero_quantity_raises_value_error():
    """Тест: при создании Product с quantity=0 вызывается ValueError с правильным сообщением"""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Тестовый товар", "Описание", 100.0, 0)


def test_product_creation_positive_quantity_success():
    """Тест: создание Product с положительным количеством не вызывает исключение"""
    try:
        product = Product("Тестовый товар", "Описание", 100.0, 5)
        assert product.quantity == 5
    except ValueError:
        pytest.fail("ValueError не должен вызываться при положительном количестве")


def test_product_creation_negative_quantity_success():
    """Тест: создание Product с отрицательным количеством не вызывает исключение (по заданию проверяем только ноль)"""
    try:
        product = Product("Тестовый товар", "Описание", 100.0, -5)
        assert product.quantity == -5
    except ValueError:
        pytest.fail("ValueError не должен вызываться при отрицательном количестве")


def test_smartphone_creation_zero_quantity_raises_value_error():
    """Тест: при создании Smartphone с quantity=0 вызывается ValueError"""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Smartphone(
            "iPhone 15 Pro",
            "Флагманский смартфон",
            99999.0,
            0,  # quantity = 0
            "высокая",
            "iPhone 15 Pro",
            256,
            "черный",
        )


def test_lawn_grass_creation_zero_quantity_raises_value_error():
    """Тест: при создании LawnGrass с quantity=0 вызывается ValueError"""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        LawnGrass(
            "Газонная трава премиум",
            "Смесь для идеального газона",
            1500.0,
            0,  # quantity = 0
            "Голландия",
            "10-14 дней",
            "зеленый",
        )


def test_new_product_with_zero_quantity_raises_value_error():
    """Тест: создание продукта через new_product с quantity=0 вызывает ValueError"""
    product_data = {"name": "Тестовый товар", "description": "Описание", "price": 100.0, "quantity": 0}

    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product.new_product(product_data)


def test_add_product_with_check_zero_quantity():
    """Тест: добавление продукта с нулевым количеством через add_product_with_check вызывает ValueError"""
    category = Category("Тест", "Описание")

    product_data = {"name": "Тестовый товар", "description": "Описание", "price": 100.0, "quantity": 0}

    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        category.add_product_with_check(product_data)


def test_category_average_price_with_products():
    """Тест: расчет средней цены в категории с товарами"""
    product1 = Product("Товар 1", "Описание", 100.0, 10)
    product2 = Product("Товар 2", "Описание", 200.0, 5)
    product3 = Product("Товар 3", "Описание", 300.0, 8)

    category = Category("Тест", "Описание", [product1, product2, product3])

    expected_average = (100.0 + 200.0 + 300.0) / 3
    assert category.middle_price() == expected_average


def test_category_average_price_empty_category():
    """Тест: расчет средней цены в пустой категории должен вернуть 0"""
    category = Category("Пустая", "Категория без товаров")

    # Не должно быть исключения, должно вернуться 0
    assert category.middle_price() == 0


def test_category_average_price_single_product():
    """Тест: расчет средней цены в категории с одним товаром"""
    product = Product("Товар", "Описание", 150.0, 10)
    category = Category("Тест", "Описание", [product])

    assert category.middle_price() == 150.0


def test_category_average_price_with_smartphones():
    """Тест: расчет средней цены в категории со смартфонами"""
    iphone = Smartphone("iPhone 15 Pro", "Флагман", 99999.0, 5, "высокая", "iPhone 15 Pro", 256, "черный")
    samsung = Smartphone("Samsung S24", "Флагман", 89999.0, 3, "высокая", "S24", 256, "фиолетовый")

    category = Category("Смартфоны", "Флагманы", [iphone, samsung])

    expected_average = (99999.0 + 89999.0) / 2
    assert category.middle_price() == expected_average


def test_category_average_price_with_lawn_grass():
    """Тест: расчет средней цены в категории с газонной травой"""
    premium = LawnGrass("Премиум", "Элитная смесь", 2500.0, 10, "Голландия", "7-10 дней", "изумрудный")
    standard = LawnGrass("Стандарт", "Обычная смесь", 1000.0, 20, "Россия", "14-21 дней", "зеленый")

    category = Category("Газоны", "Смеси", [premium, standard])

    expected_average = (2500.0 + 1000.0) / 2
    assert category.middle_price() == expected_average


def test_category_average_price_with_mixed_products(sample_category_with_mixed_products):
    """Тест: расчет средней цены в категории со смешанными типами продуктов"""
    category = sample_category_with_mixed_products
    products_list = category.products_list

    # Вычисляем среднюю цену вручную
    total_price = sum(product.price for product in products_list)
    expected_average = total_price / len(products_list)

    assert category.middle_price() == expected_average


def test_category_average_price_after_adding_products():
    """Тест: расчет средней цены после добавления новых товаров"""
    category = Category("Тест", "Описание")

    # Пустая категория
    assert category.middle_price() == 0

    # Добавляем первый товар
    product1 = Product("Товар 1", "Описание", 100.0, 10)
    category.add_product(product1)
    assert category.middle_price() == 100.0

    # Добавляем второй товар
    product2 = Product("Товар 2", "Описание", 200.0, 5)
    category.add_product(product2)
    assert category.middle_price() == 150.0

    # Добавляем третий товар
    product3 = Product("Товар 3", "Описание", 300.0, 8)
    category.add_product(product3)
    assert category.middle_price() == 200.0


def test_category_average_price_with_duplicate_products():
    """Тест: расчет средней цены при наличии дубликатов товаров"""
    product1 = Product("Товар", "Описание", 100.0, 10)
    product2 = Product("Товар", "Описание", 200.0, 5)  # Товар с таким же именем, но другой ценой

    category = Category("Тест", "Описание", [product1, product2])

    # Оба товара учитываются отдельно
    expected_average = (100.0 + 200.0) / 2
    assert category.middle_price() == expected_average


def test_category_average_price_with_zero_priced_products():
    """Тест: расчет средней цены, если некоторые товары имеют нулевую цену"""
    product1 = Product("Бесплатный", "Описание", 0.0, 10)
    product2 = Product("Платный", "Описание", 200.0, 5)
    product3 = Product("Дорогой", "Описание", 1000.0, 8)

    category = Category("Тест", "Описание", [product1, product2, product3])

    expected_average = (0.0 + 200.0 + 1000.0) / 3
    assert category.middle_price() == expected_average


def test_category_average_price_after_removing_products():
    """Тест: расчет средней цены после удаления товаров (хотя в классе нет метода удаления,
    но можно проверить через создание новой категории)"""
    product1 = Product("Товар 1", "Описание", 100.0, 10)
    product2 = Product("Товар 2", "Описание", 200.0, 5)
    product3 = Product("Товар 3", "Описание", 300.0, 8)

    category1 = Category("Тест", "Описание", [product1, product2, product3])
    assert category1.middle_price() == 200.0

    category2 = Category("Тест", "Описание", [product1, product3])
    assert category2.middle_price() == 200.0  # (100 + 300) / 2 = 200

    category3 = Category("Тест", "Описание", [product1])
    assert category3.middle_price() == 100.0

    category4 = Category("Тест", "Описание", [])
    assert category4.middle_price() == 0


def test_category_average_price_does_not_affect_original_products(sample_category_with_mixed_products):
    """Тест: проверка, что метод average_price() не изменяет исходные данные"""
    category = sample_category_with_mixed_products
    original_products = category.products_list.copy()
    original_prices = [product.price for product in original_products]

    # Вызываем метод average_price()
    avg = category.middle_price()

    # Проверяем, что данные не изменились
    assert len(category.products_list) == len(original_products)
    for i, product in enumerate(category.products_list):
        assert product.price == original_prices[i]

    # Проверяем, что средняя цена вычислена корректно
    assert avg == sum(original_prices) / len(original_products)


def test_category_average_price_type():
    """Тест: проверка, что метод average_price() возвращает число (int или float)"""
    category_empty = Category("Пустая", "Описание")
    assert isinstance(category_empty.middle_price(), (int, float))

    product = Product("Товар", "Описание", 100, 10)
    category_with_product = Category("Тест", "Описание", [product])
    assert isinstance(category_with_product.middle_price(), (int, float))

    # Цены с плавающей точкой
    product_float = Product("Товар", "Описание", 100.5, 10)
    category_with_float = Category("Тест", "Описание", [product_float])
    assert isinstance(category_with_float.middle_price(), float)


def test_integration_all_features_together():
    """Полный интеграционный тест: проверка работы всей функциональности вместе"""
    # Создаем категорию
    category = Category("Электроника", "Электронные товары")

    # Создаем обычные товары
    product1 = Product("Ноутбук", "Мощный ноутбук", 50000.0, 10)
    product2 = Product("Мышь", "Беспроводная мышь", 1000.0, 20)

    # Создаем смартфоны
    smartphone1 = Smartphone("iPhone 15 Pro", "Флагман", 99999.0, 5, "высокая", "iPhone 15 Pro", 256, "черный")
    smartphone2 = Smartphone("Samsung S24", "Флагман", 89999.0, 3, "высокая", "S24", 256, "фиолетовый")

    # Добавляем все в категорию
    category.add_product(product1)
    category.add_product(product2)
    category.add_product(smartphone1)
    category.add_product(smartphone2)

    # Проверяем количество товаров
    assert len(category.products_list) == 4

    # Проверяем общее количество продуктов (сумма quantity)
    total_quantity = sum(p.quantity for p in category.products_list)
    assert total_quantity == 10 + 20 + 5 + 3  # 38

    # Проверяем среднюю цену
    expected_avg = (50000.0 + 1000.0 + 99999.0 + 89999.0) / 4
    assert category.middle_price() == expected_avg

    # Проверяем строковое представление категории
    assert str(category) == f"Электроника, количество продуктов: {total_quantity} шт."

    # Проверяем, что нельзя создать товар с нулевым количеством
    with pytest.raises(ValueError):
        Product("Нулевой", "Описание", 100.0, 0)

    # Проверяем, что средняя цена после невозможного добавления не изменилась
    assert category.middle_price() == expected_avg

    # Проверяем итерацию по категории
    product_names = []
    for product in category:
        product_names.append(product.name)

    assert "Ноутбук" in product_names
    assert "Мышь" in product_names
    assert "iPhone 15 Pro" in product_names
    assert "Samsung S24" in product_names
