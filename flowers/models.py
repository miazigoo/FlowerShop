from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class PriceCategory(models.Model):
    from_price = models.IntegerField("От:", null=True, blank=True)
    up_to_price = models.IntegerField("До:", null=True, blank=True)

    class Meta:
        verbose_name = 'Категория цен'
        verbose_name_plural = 'Категории цен'


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='pictures')
    category = models.ManyToManyField(
        ProductCategory,
        verbose_name="Категории букетов",
        related_name="categories",
    )

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'

    def __str__(self):
        return f'Букет: {self.name}'





class Order(models.Model):
    NEW = 'new'
    DELIVERY = 'delivery'
    READY = 'ready'
    ORDER_STATUS = [
        (NEW, 'Необработанный'),
        (DELIVERY, 'Доставка'),
        (READY, 'Доставлен'),
    ]
    status = models.CharField(
        'Статус заказа',
        choices=ORDER_STATUS,
        default=NEW,
        max_length=20,
        db_index=True
    )
    firstname = models.CharField(
        'Имя',
        max_length=90
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон',
        db_index=True
    )

    address = models.CharField(
        'Адрес доставки',
        max_length=100,
    )
    comment = models.TextField(
        blank=True, verbose_name='Комментарий к заказу'
    )
    registration_date = models.DateTimeField(
        blank=True, null=True, verbose_name='Дата регистрации', db_index=True, auto_now=True
    )
    call_date = models.DateTimeField(
        blank=True, null=True, verbose_name='Дата звонка', db_index=True
    )
    delivery_date = models.DateTimeField(
        blank=True, null=True, verbose_name='Дата доставки', db_index=True
    )
    product = models.ForeignKey(
        Product,
        related_name='products',
        verbose_name="Букеты",
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    price = models.DecimalField(
        'Сумма',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(
            limit_value=0
        )], blank=True, null=True,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.phone_number}'






