from django.db import models
from apps.users.models import User
from config.base_model import BaseModel
from django.utils import timezone
from config.choices import *
from apps.packages.utils import update_tarif, send_message


class WarehouseData(BaseModel):
    usa_address_1 = models.CharField('Адрес 1', max_length=255, blank=True)
    usa_address_2 = models.CharField('Адрес 2', max_length=255, blank=True)
    usa_city = models.CharField('Город', max_length=255, blank=True)
    usa_state = models.CharField('Штат', max_length=255, blank=True)
    usa_zip_code = models.CharField('Почтовый индекс', max_length=10, blank=True)
    usa_phone = models.CharField('Номер телефона', max_length=20, blank=True)
    
    # turkey_city = models.CharField('Город', max_length=255, blank=True)
    # turkey_rayon = models.CharField('Район', max_length=255, blank=True)
    # turkey_quarter = models.CharField('Квартал', max_length=255, blank=True)
    # turkey_address = models.CharField('Адрес', max_length=255, blank=True)
    # turkey_post_code = models.CharField('Почтовый индекс', max_length=10, blank=True)
    # turkey_phone = models.CharField('Номер телефона', max_length=20, blank=True)
    
    china_address = models.CharField('Адрес', max_length=255, blank=True)
    china_phone = models.CharField('Номер телефона', max_length=20, blank=True)
    china_region = models.CharField('Регион', max_length=255, blank=True)
    china_detail_address = models.CharField('Детальный адрес', max_length=255, blank=True)
    china_post_code = models.CharField('Почтовый индекс', max_length=10, blank=True)
    
    # japan_city = models.CharField('Город', max_length=255, blank=True)
    # japan_address = models.CharField('Адрес', max_length=255, blank=True)
    # japan_post_code = models.CharField('Почтовый индекс', max_length=10, blank=True)
    # japan_phone = models.CharField('Номер телефона', max_length=20, blank=True)
    
    def __str__(self):
        return 'Данные складов'

    class Meta:
        verbose_name = 'Данные складов'
        verbose_name_plural = 'Данные складов'
        

class Store(BaseModel):
    name = models.CharField('Название магазина', max_length=255, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['-created_at']
        

class Reys(BaseModel):
    year = models.CharField('Год', max_length=255, blank=True)
    number = models.CharField('Номер', max_length=255, blank=True)
    
    def __str__(self):
        return f'{self.year} - {self.number}'
    
    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['-created_at']
        
        
class Package(BaseModel):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент', related_name='packages', blank=True, null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Получатель', related_name='packages_recipient', blank=True, null=True)
    status = models.CharField('Статус', max_length=255, blank=True, choices=STATUS_CHOICES, default='Проверяется')
    warehouse = models.CharField('Склад', max_length=255, blank=True, choices=WAREHOUSE_CHOICES)
    reys = models.ForeignKey(Reys, on_delete=models.CASCADE, verbose_name='Рейс', related_name='packages', blank=True, null=True)
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
    delivery_cost = models.DecimalField('Стоимость доставки', blank=True, null=True, decimal_places=2, max_digits=10)

    system_comment = models.TextField('Системный комментарий', blank=True, null=True)
    client_comment = models.TextField('Комментарий клиента', blank=True, null=True)
    cladovshik_comment = models.TextField('Комментарий кладовщика', blank=True, null=True)
    manager_comment = models.TextField('Комментарий менеджера', blank=True, null=True)
    
    whole_summa = models.DecimalField('Сумма', blank=True, null=True, decimal_places=2, max_digits=10)
    whole_summa_eur = models.DecimalField('Сумма в евро', blank=True, null=True, decimal_places=2, max_digits=10)
    date_on_warehouse = models.DateTimeField('Дата на складе', blank=True, null=True)
    
    def __str__(self):
        return f'{self.client} - {self.recipient}'
    
    def save(self, *args, **kwargs):
        if self.tracking_number and self.__class__.objects.filter(tracking_number=self.tracking_number).exclude(pk=self.id).exists():
            raise ValueError('Трек номер уже существует')
        
        old_instance = None
        old_status = None
        
        if self.pk:
            old_instance = self.__class__.objects.filter(pk=self.pk).first()
            
        if old_instance:
            old_status = getattr(old_instance, "status", None)
            if self.status == "На складе" and old_status != "На складе":
                self.date_on_warehouse = timezone.now()

        if self.final_weight:
            update_tarif(self)

        send_message(self, old_status)
        
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
    length = models.FloatField('Длина', blank=True, null=True)
    width = models.FloatField('Ширина', blank=True, null=True)
    height = models.FloatField('Высота', blank=True, null=True)
    volume_weight = models.FloatField('Обьемный вес', blank=True, null=True)
    
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
    code = models.CharField('Код', max_length=255, blank=True)
    brutto = models.FloatField('Брутто', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары' 
        ordering = ['-created_at']


class PackageDetail(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name='Посылка', related_name='package_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='package_details')
    price = models.DecimalField('Цена', blank=True, null=True, decimal_places=2, max_digits=10)
    count = models.IntegerField('Количество', blank=True, null=True)
    summa = models.DecimalField('Сумма', blank=True, null=True, decimal_places=2, max_digits=10)
    summa_eur = models.DecimalField('Сумма в евро', blank=True, null=True, decimal_places=2, max_digits=10)

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


class AWB(BaseModel):   
    number = models.CharField('Номер', max_length=255, blank=True)
    count_place = models.IntegerField('Количество мест', blank=True, null=True)
    weight = models.FloatField('Вес', blank=True, null=True)
    reys = models.ForeignKey(Reys, on_delete=models.CASCADE, verbose_name='Рейс', related_name='awbs', blank=True, null=True)
    date = models.DateTimeField('Дата', blank=True, null=True)
    warehouse = models.CharField('Склад', max_length=255, blank=True, choices=WAREHOUSE_CHOICES)
    sender = models.CharField('Отправитель', max_length=255, blank=True)
    recipient = models.CharField('Получатель', max_length=255, blank=True)
    comment = models.TextField('Комментарий', blank=True)
    image = models.ImageField('Фото', upload_to='awb_images/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.number}'
    
    class Meta:
        verbose_name = 'AWB'
        verbose_name_plural = 'AWB'
        ordering = ['-created_at']
        
    
class AWBFile(BaseModel):
    awb = models.ForeignKey(AWB, on_delete=models.CASCADE, verbose_name='AWB', related_name='awb_files')
    file = models.FileField('Файл', upload_to='awb_files/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.awb}'
    
    class Meta:
        verbose_name = 'Файл AWB'
        verbose_name_plural = 'Файлы AWB'
