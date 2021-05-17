from django import template

register = template.Library()


def product_list(product, wishlist):
    context = {
        "product": product,
        "wishlist":wishlist,
    }
    return context
register.inclusion_tag('tags/product_list.html')(product_list)

def navbar(user,cart, wishlist):
    context = {
        'user':user,
        'cart':cart,
        'wishlist':wishlist,
    }
    return context
register.inclusion_tag('tags/navbar.html')(navbar)

@register.inclusion_tag('tags/footer.html', takes_context=False)
def footer():
    context = {
        "product": "footer",
    }
    return context

