# apps/cart/utils.py
def _get_cart(session):
    return session.get('cart', {})

def _save_cart(session, cart):
    session['cart'] = cart
    session.modified = True
