"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    cart = Cart()
    test_product = Product("pen", 11, "This is a pen", 770)
    cart.add_product(product=test_product, buy_count=14)
    return cart


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(quantity=910) is True
        assert product.check_quantity(quantity=1010) is False

    def test_product_buy(self, product):
        product.buy(quantity=50)
        assert product.check_quantity(quantity=950) is True

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError, match="Продуктов не хватает"):
            product.buy(quantity=5000)


class TestCart:

    def test_add_product(self, cart: Cart, product: Product, buy_count=10):
        cart.add_product(product=product, buy_count=buy_count)
        assert len(cart.products) == 2
        assert cart.products[product] == buy_count

    def test_remove_product_remove_count_is_none(self, cart: Cart, product: Product):
        cart.add_product(product=product, buy_count=25)
        assert len(cart.products) == 2
        cart.remove_product(product=product)
        assert len(cart.products) == 1

    def test_remove_product_remove_count_is_greater(self, cart: Cart,
                                                    product: Product,
                                                    remove_count=31):
        cart.add_product(product=product, buy_count=25)
        assert len(cart.products) == 2
        cart.remove_product(product=product, remove_count=remove_count)
        assert len(cart.products) == 1

    def test_remove_product_remove_count_is_less(self, cart: Cart,
                                                 product: Product,
                                                 remove_count=7):
        cart.add_product(product=product, buy_count=25)
        product_start_count = cart.products[product]
        assert len(cart.products) == 2
        cart.remove_product(product=product, remove_count=remove_count)
        assert len(cart.products) == 2
        assert cart.products[product] == product_start_count - remove_count

    def test_clear(self, cart: Cart):
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart: Cart, product: Product, buy_count=25):

        assert cart.get_total_price() == 11*14
        cart.add_product(product=product, buy_count=buy_count)
        assert cart.get_total_price() == 11 * 14 + 100*25

    def test_buy_ok(self, cart: Cart):
        cart.buy()
        assert len(cart.products) == 0

    def test_buy_not_ok(self, cart: Cart, product: Product, buy_count=2005):
        cart.add_product(product=product, buy_count=buy_count)
        with pytest.raises(ValueError, match="Продуктов не хватает"):
            cart.buy()
