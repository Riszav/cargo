from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField('Страна', max_length=255, blank=True)
    is_active = models.BooleanField('Активна', default=True)

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class User(AbstractUser):
    client_id = models.CharField('ID клиента', max_length=255, blank=True)
    last_name = models.CharField('Фамилия', max_length=255, blank=True)
    first_name = models.CharField('Имя', max_length=255, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна', blank=True, null=True)
    address = models.CharField('Адрес', max_length=255, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=255, blank=True)
    email = models.EmailField('Почта', max_length=255, blank=True)
    tarif_usa = models.CharField('Тариф США', max_length=255, blank=True)
    tarif_usa_value = models.IntegerField('', blank=True, null=True)
    tarif_turkey = models.CharField('Тариф Турция', max_length=255, blank=True)
    tarif_turkey_value = models.IntegerField('', blank=True, null=True)
    tarif_china = models.CharField('Тариф Китай', max_length=255, blank=True)
    tarif_china_value = models.IntegerField('', blank=True, null=True)
    tarif_japan = models.CharField('Тариф Япония', max_length=255, blank=True)
    tarif_japan_value = models.IntegerField('', blank=True, null=True)
    inn = models.CharField('ИНН', max_length=255, blank=True)
    status = models.CharField('Статус', max_length=255, blank=True)
    passport_number = models.CharField('Номер удостоверения личности', max_length=255, blank=True)
    passport_date = models.DateField('Дата выдачи удостоверения личности', blank=True, null=True)
    passport_place = models.CharField('Кем выдан', max_length=255, blank=True)
    passport_image_1 = models.ImageField('Фото удостоверения личности', upload_to='passport_images/', blank=True)
    passport_image_2 = models.ImageField('Фото удостоверения личности', upload_to='passport_images/', blank=True)
    contract = models.CharField('Договор', max_length=255, blank=True)
    is_admin = models.BooleanField('Админ', default=False)

    def __str__(self):
        return f'{self.last_name} {self.first_name}' if self.last_name or self.first_name else f'{self.username}'
    
    class Meta: 
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    

