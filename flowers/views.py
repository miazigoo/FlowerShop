import random
import stripe
from http import HTTPStatus
from django import forms
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View

from flowers.models import Product, Order, ProductCategory, PriceCategory
from django.core.paginator import Paginator
from more_itertools import chunked
from django.contrib.auth import views as auth_views, authenticate, login
from django.conf import settings
from django.views import View
from django.views.generic.base import TemplateView


DATA = {}
QUIZ = {}


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "flowers/success.html"


class CancelView(TemplateView):
    template_name = "flowers/cancel.html"


def get_product(request):
    category = None
    product = None
    if QUIZ.get('CATEGORY_PK') and QUIZ.get('CATEGORY_PK') != '0':
        category = ProductCategory.objects.get(pk=int(QUIZ['CATEGORY_PK']))
    try:
        if request.GET['FROM'] == '0' and request.GET['UP_TO'] == '0':
            if category:
                products = Product.objects.filter(category=category)
                product_pk = random.randint(0, len(products))
                product = products[product_pk]
            else:
                products = Product.objects.all().count()
                product_pk = random.randint(1, products)
                product = Product.objects.get(pk=product_pk)
        elif request.GET['FROM'] == '0' and request.GET['UP_TO'] != '0':
            up_to = int(request.GET['UP_TO'])
            if category:
                products = Product.objects.filter(category=category, price__range=(0, up_to))
                product_pk = random.randint(0, len(products))
                product = products[product_pk]
            else:
                products = Product.objects.filter(price__range=(0, up_to))
                product_pk = random.randint(0, len(products))
                product = products[product_pk]
        elif request.GET['FROM'] != '0' and request.GET['UP_TO'] != '0':
            up_to = int(request.GET['UP_TO'])
            from_to = int(request.GET['FROM'])
            if category:
                products = Product.objects.filter(category=category, price__range=(from_to, up_to))
                product_pk = random.randint(0, len(products))
                product = products[product_pk]
            else:
                products = Product.objects.filter(price__range=(from_to, up_to))
                product_pk = random.randint(0, len(products))
                product = products[product_pk]
        elif request.GET['FROM'] != '0' and request.GET['UP_TO'] == '0':
            from_to = int(request.GET['FROM'])
            if category:
                products = Product.objects.filter(category=category, price__gte=from_to)
                product_pk = random.randint(0, len(products))
                product = products[product_pk]
            else:
                products = Product.objects.filter(price__gte=from_to)
                product_pk = random.randint(0, len(products))
                product = products[product_pk]
    except IndexError as err:
        product = None
    return product


def view_flowers(request):
    operation = None
    if request.GET.get('cardNum'):
        product = DATA['product']
        Order.objects.create(
            phone_number=DATA['phone'],
            firstname=DATA['name'],
            address=DATA['address'],
            comment=DATA['order_time'],
            product=product,
            price=product.price,
        )
        print('SUCCESS')
        operation = 'Оплата прошла успешно. Менеджер свяжется с вами для уточнения заказа.'
        DATA.clear()
        # checkout_session = stripe.checkout.Session.create(
        #     line_items=[
        #         {
        #             # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
        #             'price': 'price_1Ngt61IOnXKDlGzlxcyrYLxM',
        #             'quantity': 1,
        #         },
        #     ],
        #     mode='payment',
        #     success_url='{}{}'.format(settings.DOMAIN_NAME, reverse_lazy('ViewSuccess')),
        #     cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse_lazy('ViewCancel')),
        # )
        #
        # return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)
    context = {'operation': operation}
    return render(request, "flowers/index.html", context)


def view_success(request):
    return render(request, "flowers/success.html")


def view_cancel(request):
    return render(request, "flowers/cancel.html")


def view_contacts(request):
    return render(request, "flowers/contacts.html")


def view_catalog(request):
    columns_count = 2
    flowers = Product.objects.all()

    page_columns = list(chunked(flowers, columns_count))
    context = {
        'page_columns': page_columns,
    }
    return render(request, "flowers/catalog.html",  context)


def view_card(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, "flowers/card.html", context)


def view_consultation(request):
    return render(request, "flowers/consultation.html")


def view_order(request):
    if request.GET:
        pk = request.GET['PK']
        product = get_object_or_404(Product, pk=pk)
        DATA['product'] = product
    
    return render(request, "flowers/order.html")


def view_order_step(request):
    if request.GET:
        DATA['name'] = request.GET['fname']
        DATA['phone'] = request.GET['tel']
        DATA['address'] = request.GET['adres']
        DATA['order_time'] = request.GET['orderTime']
    return render(request, "flowers/order-step.html")


def view_quiz(request):
    categories = ProductCategory.objects.all()
    context = {'categories': categories}
    return render(request, "flowers/quiz.html", context)


def view_quiz_step(request):
    cat_prices = PriceCategory.objects.all()
    context = {'cat_prices': cat_prices}
    if request.GET:
        QUIZ['CATEGORY_PK'] = request.GET['CATEGORY_PK']
    print('CATEGORY_PK', request.GET['CATEGORY_PK'], type(request.GET['CATEGORY_PK']))
    return render(request, "flowers/quiz-step.html", context)


def view_result(request):
    product = get_product(request)
    print(product)
    context = {'product': product}
    QUIZ.clear()
    return render(request, "flowers/result.html", context)


def view_result2(request):
    return render(request, "flowers/result2.html")


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:
                    return redirect("ManagerView")
                return redirect("ViewFlowers")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff


@user_passes_test(is_manager, login_url='login')
def view_manager(request):
    orders = list(Order.objects.exclude(status=Order.READY).order_by('-status'))
    context = {'order_items': orders}
    return render(request, template_name='order_items.html', context=context)
