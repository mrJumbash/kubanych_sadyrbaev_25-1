from django.shortcuts import render
from products.models import Product, Hashtag

# Create your views here.

def main_page_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')

def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()

        context = {
            'products': [
                {
                    'id': product.id,
                    'title': product.title,
                    'image': product.image,
                    'rating': product.rating,
                    'hashtags': product.hashtags.all(),
                    'price': product.price
                } for product in products
            ]
        }

        return render(request, 'products/products.html', context=context)

def hashtag_view(request):
    if request.method == 'GET':
        hashtags = Hashtag.objects.all()

        context = {
            "hashtags": hashtags
        }

        return render(request, 'products/hashtags.html', context=context)
