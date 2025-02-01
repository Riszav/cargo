from django.db import models
from apps.users.models import User
from config.base_model import BaseModel
from django.utils import timezone


STATUS_CHOICES = [
    ('Проверяется', 'Проверяется'),
    ('Ждем на склад', 'Ждем на склад'),
    ('На складе', 'На складе'),
    ('Отправлена', 'Отправлена'),
    ('На обработке', 'На обработке'),
    ('Прибыла', 'Прибыла'),
    ('Доставлена заказчику', 'Доставлена заказчику'),
    ('Неправильный трекинг номер', 'Неправильный трекинг номер'),
    ('Возвращена отправителю', 'Возвращена отправителю'),
    ('Задержана на складе', 'Задержана на складе'),
    ('Отменена', 'Отменена'),
]

WAREHOUSE_CHOICES = [
    ('США', 'США'),
    ('Турция', 'Турция'),
    ('Китай', 'Китай'),
    ('Япония', 'Япония'),
]

TYPE_OF_PACKAGING_CHOICES = [
    ('Пакет', 'Пакет'),
    ('Коробка', 'Коробка'),
]

OPTIONS_OF_PACKAGING_CHOICES = [
    ('Отправить в почтовой упаковке', 'Отправить в почтовой упаковке'),
    ('Сохранить обувную коробку', 'Сохранить обувную коробку'),
]


class Store(BaseModel):
    name = models.CharField('Название магазина', max_length=255, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['-created_at']
        

class Package(BaseModel):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент', related_name='packages', blank=True, null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Получатель', related_name='packages_recipient', blank=True, null=True)
    status = models.CharField('Статус', max_length=255, blank=True, choices=STATUS_CHOICES)
    warehouse = models.CharField('Склад', max_length=255, blank=True, choices=WAREHOUSE_CHOICES)
    reys = models.CharField('Рейс', max_length=255, blank=True)
    summa = models.IntegerField('Сумма', blank=True, null=True)
    package_image = models.ImageField('Фото посылки', upload_to='package_images/', blank=True, null=True)
    label_image = models.ImageField('Фото лэйбла', upload_to='label_images/', blank=True, null=True)
    invoice_image = models.ImageField('Фото инвойса', upload_to='invoice_images/', blank=True, null=True)
    type_of_packaging = models.CharField('Тип упаковки', max_length=255, blank=True, choices=TYPE_OF_PACKAGING_CHOICES)
    options_of_packaging = models.CharField('Опции упаковки', max_length=255, blank=True, choices=OPTIONS_OF_PACKAGING_CHOICES)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Магазин', related_name='packages', blank=True, null=True)
    full_name = models.CharField('Фамилия и Имя', max_length=255, blank=True)
    weight_of_package = models.FloatField('Вес по складу', blank=True, null=True)
    tracking_number = models.CharField('Трек номер', max_length=255, blank=True)
    count_scans = models.IntegerField('Количество сканов', blank=True, null=True)
    
    final_weight = models.FloatField('Итоговый вес', blank=True, null=True)
    delivery_cost = models.IntegerField('Стоимость доставки', blank=True, null=True)
    manual_editing = models.BooleanField('Ручное редактирование', default=False)

    client_comment = models.TextField('Комментарий клиента', blank=True)
    admin_comment = models.TextField('Комментарий администратора', blank=True)
    
    date_on_warehouse = models.DateTimeField('Дата на складе', blank=True, null=True)
    
    def __str__(self):
        return f'{self.client} - {self.recipient}'
    
    def save(self, *args, **kwargs):
        if self.status == 'На складе' and self.instance.status != 'На складе':
            self.date_on_warehouse = timezone.now()
        if self.package_details.exists():
            self.summa = self.package_details.aggregate(models.Sum('price'))['price__sum'] or 0
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Посылка'
        verbose_name_plural = 'Посылки'
        ordering = ['-created_at']


class PackageWeight(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name='Посылка', related_name='package_weights')
    count_place = models.IntegerField('Количество мест', blank=True, null=True)
    weight = models.FloatField('Вес', blank=True, null=True)
    is_volume_weight = models.BooleanField('Обьемный вес', default=False)
    length = models.IntegerField('Длина', blank=True, null=True)
    width = models.IntegerField('Ширина', blank=True, null=True)
    height = models.IntegerField('Высота', blank=True, null=True)
    volume_weight = models.IntegerField('Обьемный вес', blank=True, null=True)
    
    def __str__(self):
        return f'{self.package} - {self.weight}'
    
    class Meta:
        verbose_name = 'Вес посылки'
        verbose_name_plural = 'Вес посылок'
        

class Category(BaseModel):
    name = models.CharField('Название', max_length=255, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-created_at']


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    name = models.CharField('Название', max_length=255, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


class PackageDetail(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name='Посылка', related_name='package_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='package_details')
    price = models.IntegerField('Цена', blank=True, null=True)
    count = models.IntegerField('Количество', blank=True, null=True)

    def __str__(self):
        return f'{self.product} - {self.count}'
    
    class Meta:
        verbose_name = 'Детали посылки'
        verbose_name_plural = 'Детали посылок'
        

class PackageImage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name='Посылка', related_name='package_images')
    image = models.ImageField('Фото', upload_to='package_images/', blank=True)
    
    def __str__(self):
        return f'{self.package}'
    
    class Meta:
        verbose_name = 'Фото посылки'
        verbose_name_plural = 'Фото посылок'


class Location(BaseModel):
    name = models.CharField('Название', max_length=255, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ['-created_at']


SCAN_TYPE_CHOICES = [
    ('Входящие', 'Входящие'),
    ('Исходящие', 'Исходящие'),
]   

class Scan(BaseModel):
    tracking_number = models.CharField('Трек номер', max_length=255, blank=True)
    tracking_number_2 = models.CharField('Трек номер 2', max_length=255, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер', related_name='scans')
    type = models.CharField('Тип', max_length=255, blank=True, choices=SCAN_TYPE_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Локация', related_name='scans', blank=True, null=True)
    
    def __str__(self):
        return f'{self.tracking_number} - {self.tracking_number_2}'
    
    class Meta:
        verbose_name = 'Скан'
        verbose_name_plural = 'Сканы'
        ordering = ['-created_at']
