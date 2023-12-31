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
    description = models.TextField("Описание")
    short_description = models.TextField("Короткое описание", null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    structure = models.TextField("Состав", null=True, blank=True)
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

    def get_absolute_url(self):
        return f'/card/{self.pk}'


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


class Consultation(models.Model):
    NEW = 'new'
    READY = 'ready'
    ORDER_STATUS = [
        (NEW, 'Необработан'),
        (READY, 'Готов'),
    ]
    status = models.CharField(
        'Статус заказа',
        choices=ORDER_STATUS,
        default=NEW,
        max_length=20,
        db_index=True, null=True
    )
    firstname = models.CharField(
        'Имя',
        max_length=90, null=True
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон',
        db_index=True, null=True
    )
    registration_date = models.DateTimeField(
        blank=True, null=True, verbose_name='Дата регистрации', db_index=True, auto_now=True
    )
    call_date = models.DateTimeField(
        blank=True, null=True, verbose_name='Дата звонка', db_index=True
    )
    comment = models.TextField(
        blank=True, null=True, verbose_name='Комментарий к заявке'
    )

    class Meta:
        verbose_name = 'Заявку на консультацию'
        verbose_name_plural = 'Заявки на консультации'

    def __str__(self):
        return f'{self.firstname} {self.phone_number}'
