from django.shortcuts import render, redirect
from products.models import Product, Hashtag, Review
from .forms import ProductCreateForm, ReviewCreateForm
from products.constants import PAGINATION_LIMIT
from django.views.generic import ListView, CreateView, DetailView


class MainCBV(ListView):
    model = Product
    template_name = 'layouts/index.html'


class ProductCBV(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get(self, request, **kwargs):
        products = self.get_queryset()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search:
            products = products.filter(title__contains=search) | products.filter(description__contains=search)

        max_page = products.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        contex = {
            'products': [
                {
                    'id': product.id,
                    'title': product.title,
                    'image': product.image,
                    'quantity': product.quantity,
                    'price': product.price,
                    'hashtags': product.hashtags.all()
                } for product in products
            ],
            'user': request.user,
            'pages': range(1, max_page + 1)
        }

        return render(request, self.template_name, context=contex)


class HashtagsCBV(ListView):
    model = Hashtag
    template_name = 'products/hashtags.html'

    def get(self, request, **kwargs):
        hashtags = self.get_queryset()
        context = {
            'hashtags': hashtags
        }

        return render(request, self.template_name, context=context)


class ProductDetailCBV(DetailView, CreateView):
    model = Product
    template_name = 'products/detail.html'
    form_class = ReviewCreateForm
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'product': self.get_object(),
            'reviews': Review.objects.filter(product=self.get_object()),
            'form': kwargs.get('form', self.form_class)
        }

    def post(self, request, **kwargs):

        data = request.POST
        form = ReviewCreateForm(data=data)

        if form.is_valid():
            Review.objects.create(
                text=form.cleaned_data.get('text'),
                rate=form.cleaned_data.get('rate'),
                product_id=self.get_object().id
            )
            return redirect(f'/products/{self.get_object().id}/')

        return render(request, self.template_name, context=self.get_context_data(
            form=form
        ))


class CreateProductCBV(ListView, CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': self.form_class if not kwargs.get('form') else kwargs['form']
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, **kwargs):
        data, files = request.POST, request.FILES

        form = ProductCreateForm(data, files)

        if form.is_valid():
            Product.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                quantity=form.cleaned_data.get('quantity'),
                price=form.cleaned_data.get('price')
            )
            return redirect('/products')

        return render(request, self.template_name, context=self.get_context_data(
            form=form
        ))