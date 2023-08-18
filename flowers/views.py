from django import forms
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from flowers.models import Product, Order
from django.core.paginator import Paginator
from more_itertools import chunked
from django.contrib.auth import views as auth_views, authenticate, login


DATA = {}


def view_flowers(request):
    operation = None
    if request.GET['cardNum']:
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
    context = {'operation': operation}
    return render(request, "flowers/index.html", context)


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
    return render(request, "flowers/quiz.html")


def view_quiz_step(request):
    return render(request, "flowers/quiz-step.html")


def view_result(request):
    return render(request, "flowers/result.html")


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
