from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Banner(models.Model):
    title = models.TextField('Заголовок')
    image = models.ImageField('Изображение', upload_to='banners/')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['id']
        

class AboutUs(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='about_us/')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'
        ordering = ['id']
        

class AboutUsPage(models.Model):
    text = CKEditor5Field('Текст', blank=True, null=True)
    image1 = models.ImageField('Изображение 1', upload_to='about_us_page/')
    image2 = models.ImageField('Изображение 2', upload_to='about_us_page/')

    def __str__(self):
        return 'Страница О нас'
    
    class Meta:
        verbose_name = 'Страница О нас'
        verbose_name_plural = 'Страница О нас'


class OurServices(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='our_services/')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Наши услуги'
        verbose_name_plural = 'Наши услуги'
        ordering = ['id']
        

class ApplicationSettings(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')
    email = models.EmailField('Email')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Настройки приложения'
        verbose_name_plural = 'Настройки приложения'
        ordering = ['id']
        

class Application(models.Model):
    name = models.CharField('Имя', max_length=255)
    phone = models.CharField('Телефон', max_length=255)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['id']


class FAQ(models.Model):
    question = models.TextField('Вопрос')
    answer = models.TextField('Ответ')
    
    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['id']
        
        
class Gallery(models.Model):
    image = models.ImageField('Изображение', upload_to='gallery/')
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'
        ordering = ['id']


class HowItWorks(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='how_it_works/')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Как это работает'
        verbose_name_plural = 'Как это работает'
        ordering = ['id']
    
    
WEIGHT_CHOICES = [
    ('0+', '0+'),
    ('100+', '100+'),
    ('200+', '200+'),
]
        
    
class PriceAndPayment(models.Model):
    weight = models.CharField('Вес', max_length=255, choices=WEIGHT_CHOICES)
    type_of_service = models.CharField('Тип услуги', max_length=255)    
    price_usa = models.CharField('Цена в США', max_length=255)
    price_turkey = models.CharField('Цена в Турции', max_length=255)
    price_china_air = models.CharField('Цена в Китай(Авиа)', max_length=255)
    price_china_car = models.CharField('Цена в Китай(Авто)', max_length=255)
    commission = models.CharField('Комиссия', max_length=255)
    
    def __str__(self):
        return f'{self.weight} кг, {self.type_of_service}'
    
    class Meta:
        verbose_name = 'Цена и оплата'
        verbose_name_plural = 'Цена и оплата'
        ordering = ['id']
        

class PaymentData(models.Model):
    subtitle = models.CharField('Подзаголовок', max_length=255)
    description = models.TextField('Описание')
    
    description_weight = models.CharField('Описание', max_length=255)
    text_weight = models.CharField('Текст', max_length=255)
    
    description_payment = models.CharField('Описание', max_length=255)
    
    def __str__(self):
        return self.subtitle
    
    class Meta:
        verbose_name = 'Данные оплаты'
        verbose_name_plural = 'Данные оплаты'
        ordering = ['id']


class News(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = CKEditor5Field('Описание', blank=True, null=True, config_name='external')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
        ordering = ['-id']


class PVZ(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    location = models.CharField('Локация', max_length=255)
    phone_number = models.CharField('Телефон', max_length=255)
    working_hours = models.CharField('Время работы', max_length=255)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'ПВЗ'
        verbose_name_plural = 'ПВЗ'
        ordering = ['id']

