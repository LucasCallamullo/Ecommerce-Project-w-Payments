

from django.template.loader import render_to_string


def get_render_htmls(carrito, cart_view):
    
    # renderizar el nuevo html del widget que vamos a integrar con js al html
    context = {'carrito': carrito}
    widget_html = render_to_string('cart/cart_items.html', context)
    
    # solo renderizar la vista del carrito en caso de que estemos en la pagina del carrito
    cart_view_html = None
    if cart_view:
        cart_view_html = render_to_string('cart/table_cart_detail.html', context)
    
    return widget_html, cart_view_html