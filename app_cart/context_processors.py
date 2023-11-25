from app_cart.cart import Cart


def get_cart(request) -> dict:
    """ Передаем корзину в контекст """
    return {'cart': Cart(request)}
