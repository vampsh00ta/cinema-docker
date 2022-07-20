from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from .manager import CustomerManager
from django.db import models
from django.utils import timezone
from django.conf import settings

class Customer(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField('username', max_length=256)
    firstName = models.CharField('Имя', max_length=256,null=True)
    secondName = models.CharField('Фамилия', max_length=256,null=True)
    is_active = models.BooleanField(default=True)
    account_type = models.CharField("Тип", max_length=30)
    admin = models.BooleanField(default=False)
    verif_time = models.DateTimeField(null=True)
    fav_films = models.ManyToManyField("Film")
    fav_serials= models.ManyToManyField("Serial")
    fav_episodes= models.ManyToManyField("Episode")



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomerManager()

    def has_perm(self, perm, obj=None):
        if self.admin:
            return True

    def has_module_perms(self, app_label):
        if self.admin:
            return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        if self.account_type == 'mod' or self.account_type == 'admin':
            return True
        return False
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class Country(models.Model):
    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    name = models.CharField('Страна производства', max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    name = models.CharField('Жанр', max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField('Категория', max_length=50)

    def __str__(self):
        return self.name


class Film(models.Model):
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    year_of_release = models.IntegerField()
    date_of_adding = models.DateField(default=timezone.now)
    category = models.ManyToManyField(Category, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    country = models.ManyToManyField(Country, blank=True)
    person_who_added = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    screensaver_reference = models.URLField()
    magnet_reference = models.CharField('magnet link', max_length=300)
    def __str__(self):
        return self.name


class Serial(models.Model):
    class Meta:
        verbose_name = "Сериал"
        verbose_name_plural = "Сериалы"

    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    category = models.ManyToManyField(Category)
    genre = models.ManyToManyField(Genre)
    date_of_creation = models.IntegerField()
    country = models.ManyToManyField(Country)
    date_of_adding = models.DateTimeField(default=timezone.now)
    person_who_added = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    screensaver_reference = models.URLField()


class Season(models.Model):
    class Meta:
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"

    serial_parent = models.ForeignKey(Serial, on_delete=models.CASCADE)
    person_who_added = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    number_of_season = models.IntegerField()


class Episode(models.Model):
    class Meta:
        verbose_name = "Эпизод"
        verbose_name_plural = "Эпизоды"

    season_parent = models.ForeignKey(Season, on_delete=models.CASCADE)
    person_who_added = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    number_of_series = models.IntegerField()
    #   time_field = models.TimeField() #продолжительность в секундах; может не понадобиться
    magnet_reference = models.URLField()


class Comment(models.Model):
    author = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    rating = models.SmallIntegerField()
    to_film = models.ForeignKey(Film, on_delete=models.CASCADE)
    to_serial = models.ForeignKey(Serial, on_delete=models.CASCADE)

    def check_comment(self):
        if Comment.to_film is None and Comment.to_serial is None:
            return False
        else:
            return True


class Trailer(models.Model):
    class Meta:
        verbose_name = "Трейлер"
        verbose_name_plural = "Трейлеры"

    film_pk = models.ForeignKey(Film, blank=True, null=True, on_delete=models.SET_NULL)
    serial_pk = models.ForeignKey(Serial, blank=True, null=True, on_delete=models.SET_NULL)
    season_pk = models.ForeignKey(Season, blank=True, null=True, on_delete=models.SET_NULL)
    episode_pk = models.ForeignKey(Episode, blank=True, null=True, on_delete=models.SET_NULL)
    reference = models.URLField()

    def check_reference(self):
        quantity_of_not_null = 0
        if self.film_pk is not None:
            quantity_of_not_null += 1
        if self.serial_pk is not None:
            quantity_of_not_null += 1
        if self.episode_pk is not None:
            quantity_of_not_null += 1
        if self.season_pk is not None:
            quantity_of_not_null += 1
        if quantity_of_not_null != 1:
            return False
        return True






