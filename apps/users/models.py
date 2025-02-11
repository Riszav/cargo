from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


STATUS_RECIPIENT = (    
    ('Проверяется', 'Проверяется'),
    ('Отклонен', 'Отклонен'),
    ('Подтвержден', 'Подтвержден'),
)


STATUS_TARIF = (    
    ('Новичок', 'Новичок'),
    ('VIP', 'VIP'),
)


class Country(models.Model):
    name = models.CharField('Страна', max_length=255, blank=True)
    is_active = models.BooleanField('Активна', default=True)

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['is_active',]


class User(AbstractUser):
    client_id = models.CharField('ID клиента', max_length=255, blank=True)
    last_name = models.CharField('Фамилия', max_length=255, blank=True)
    first_name = models.CharField('Имя', max_length=255, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна', blank=True, null=True)
    phone_number = models.CharField('Номер телефона', max_length=255, blank=True, null=True)
    email = models.EmailField('Почта', max_length=255, blank=True, null=True)
    
    tarif_usa = models.CharField('Тариф США', max_length=255, blank=True, choices=STATUS_TARIF, default='Новичок')
    tarif_usa_value = models.FloatField('', blank=True, null=True, default=11)
    tarif_usa_weight = models.FloatField('Тариф США: Вес', blank=True, null=True)
    tarif_turkey = models.CharField('Тариф Турция', max_length=255, blank=True, choices=STATUS_TARIF, default='Новичок')
    tarif_turkey_value = models.FloatField('', blank=True, null=True, default=5.44)
    tarif_turkey_weight = models.FloatField('Тариф Турция: Вес', blank=True, null=True)
    tarif_china = models.CharField('Тариф Китай', max_length=255, blank=True, choices=STATUS_TARIF, default='Новичок')
    tarif_china_value = models.FloatField('', blank=True, null=True, default=3.40)
    tarif_china_weight = models.FloatField('Тариф Китай: Вес', blank=True, null=True)
    tarif_japan = models.CharField('Тариф Япония', max_length=255, blank=True, choices=STATUS_TARIF, default='Новичок')
    tarif_japan_value = models.FloatField('', blank=True, null=True, default=20)
    tarif_japan_weight = models.FloatField('Тариф Япония: Вес', blank=True, null=True)
    
    is_admin = models.BooleanField('Админ', default=False)  
    is_manager = models.BooleanField('Менеджер', default=False)
    username = models.CharField('Логин', max_length=255, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager() 
    
    def save(self, *args, **kwargs):
        if User.objects.filter(email=self.email).exclude(id=self.id).exists():
            raise ValueError('Пользователь с такой почтой уже существует')
        elif User.objects.filter(phone_number=self.phone_number).exclude(id=self.id).exists():
            raise ValueError('Пользователь с таким номером телефона уже существует')
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.last_name or self.first_name:
            return f'{self.last_name} {self.first_name}' 
        elif self.email:
            return f'{self.email}'
        else:
            return f'{self.phone_number}'
    
    class Meta: 
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']
    

class Recipient(models.Model):
    last_name = models.CharField('Фамилия', max_length=255, blank=True)
    first_name = models.CharField('Имя', max_length=255, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна', blank=True, null=True)
    address = models.CharField('Адрес', max_length=255, blank=True)
    status_recipient = models.CharField('Статус получателя', max_length=255, choices=STATUS_RECIPIENT, default='Проверяется')
    passport_number = models.CharField('Номер удостоверения личности', max_length=255, blank=True)
    passport_place = models.CharField('Кем выдан', max_length=255, blank=True)
    passport_date = models.DateField('Дата выдачи удостоверения личности', blank=True, null=True)
    passport_end_date = models.DateField('Дата окончания удостоверения личности', blank=True, null=True)
    inn = models.CharField('ИНН', max_length=255, blank=True)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    passport_image_1 = models.ImageField('Фото удостоверения личности', upload_to='passport_images/', blank=True)
    passport_image_2 = models.ImageField('Фото удостоверения личности', upload_to='passport_images/', blank=True)
    portret_image = models.ImageField('Портрет', upload_to='portret_images/', blank=True)
    contract = models.CharField('Договор', max_length=255, blank=True)
    
    main_recipient = models.BooleanField('Основной получатель', default=False)
    comment_for_manager = models.TextField('Комментарий для менеджера', blank=True)
    comment_for_client = models.TextField('Комментарий для клиента', blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='recipients', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.main_recipient:
            Recipient.objects.filter(user=self.user).update(main_recipient=False)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['-created_at']
