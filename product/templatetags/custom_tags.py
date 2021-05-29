from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter



register = template.Library()



@register.filter
@stringfilter
def media_url(value):
    """Searches for {{ STATIC_URL }} and replaces it with the MEDIA_URL from settings.py"""
    return value.replace('{{ STATIC_URL }}', settings.STATIC_URL) 
media_url.is_safe = True

def product_list(product, wishlist):
    context = {
        "product": product,
        "wishlist":wishlist,
    }
    return context
register.inclusion_tag('tags/product_list.html')(product_list)

def filterForm(form):
    context = {
        "form": form,
    }
    return context
register.inclusion_tag('tags/filterForm.html')(filterForm)

def checkoutForm(form):
    context = {
        "form": form,
    }
    return context
register.inclusion_tag('tags/checkout_form.html')(checkoutForm)


def navbar(user,cart, wishlist, categories):
    context = {
        'user':user,
        'cart':cart,
        'wishlist':wishlist,
        'categories':categories,
    }
    return context
register.inclusion_tag('tags/navbar.html')(navbar)

def categories(categories):
    context = {
        "categories": categories,
    }
    return context
@register.inclusion_tag('tags/categories.html')(categories)



@register.inclusion_tag('tags/carousel.html', takes_context=False)
def carousel():
    context = {
        "product": "footer",
    }
    return context





@register.inclusion_tag('tags/explore.html', takes_context=False)
def explore():
    context = {
        "product": "footer",
    }
    return context


@register.inclusion_tag('tags/footer.html', takes_context=False)
def footer():
    context = {
        "product": "footer",
    }
    return context

