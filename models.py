from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Категория объявления"""
    name = models.CharField('Название категории', max_length=100, unique=True)
    slug = models.SlugField('Слаг', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ad(models.Model):
    """Объявление"""
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('inactive', 'Неактивно'),
    ]

    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads', verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads', verbose_name='Автор')
    image = models.ImageField('Изображение', upload_to='ads_images/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='active')
    views = models.PositiveIntegerField('Просмотры', default=0)
    contact_email = models.EmailField('Контактный email', blank=True, null=True)
    contact_phone = models.CharField('Контактный телефон', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increment_views(self):
        """Увеличить счётчик просмотров"""
        self.views += 1
        self.save(update_fields=['views'])
