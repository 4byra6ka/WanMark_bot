from PIL import Image
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

NULLABLE = {'blank': True, 'null': True}


class MainMenuBot(models.Model):
    """Модель главное меню"""
    name = models.CharField(max_length=255, verbose_name="Имя меню")
    title = models.TextField(verbose_name="Описание", **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Главное меню бота'
        verbose_name_plural = 'Главные меню бота'
        ordering = ["id"]


class SubMenuBot(models.Model):
    """Модель подменю меню"""
    name = models.CharField(max_length=255, verbose_name="Серия дверей")
    title = models.TextField(verbose_name="Описание", **NULLABLE)
    link_main_menu = models.ForeignKey('MainMenuBot', on_delete=models.CASCADE, verbose_name='Главное меню', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Подменю бота'
        verbose_name_plural = 'Подменю бота'


class DoorCardBot(models.Model):
    """Модель карточка двери"""
    name = models.CharField(max_length=255, verbose_name="Имя модели")
    title = models.TextField(verbose_name="Описание", **NULLABLE)
    link_submenu = models.ForeignKey("SubMenuBot", on_delete=models.CASCADE, verbose_name='Подменю', **NULLABLE)
    link_main_menu = models.ForeignKey('MainMenuBot', on_delete=models.CASCADE, verbose_name='Главное меню', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Карточка двери'
        verbose_name_plural = 'Карточки дверей'


class ImageTitleDoorCardBot(models.Model):
    """Модель титульной картинки для карточки двери"""
    link_door_card = models.ForeignKey("DoorCardBot", on_delete=models.CASCADE, verbose_name='Карточка двери')
    image = models.ImageField(upload_to='wanmark/imagetitle', verbose_name='Изображение')

    def __str__(self):
        return f'Титульная картинка: {self.id}'

    class Meta:
        verbose_name = 'Титульная картинка'
        verbose_name_plural = 'Титульные картинки'


@receiver(pre_delete, sender=ImageTitleDoorCardBot)
def image_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)


class InstallDoorCardBot(models.Model):
    """Модель установленных дверей для карточки двери"""
    link_door_card = models.ForeignKey("DoorCardBot", on_delete=models.CASCADE, verbose_name='Карточка двери')
    name = models.CharField(max_length=255, verbose_name="Название кнопки")
    title = models.TextField(verbose_name="Описание", **NULLABLE)

    def __str__(self):
        return f'Установленная дверь: {self.title}'

    class Meta:
        verbose_name = 'Установленная дверь'
        verbose_name_plural = 'Установленные двери'


class ImageInstallDoorCardBot(models.Model):
    """Модель изображения установленных дверей для карточки двери"""
    link_install_door_card = models.ForeignKey("InstallDoorCardBot", on_delete=models.CASCADE, verbose_name='Установленные двери', **NULLABLE)
    image = models.ImageField(upload_to='wanmark/imageinstall', verbose_name='Изображение')

    def __str__(self):
        return f'Установленная дверь картинка: {self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            with Image.open(self.image.path) as img:
                img.load()

            if img.height > 1080 or img.width > 1920:
                new_height = 720
                new_width = int(new_height / img.height * img.width)
                img = img.resize((new_width, new_height))
                img.save(self.image.path)

    class Meta:
        verbose_name = 'Изображение установленной двери'
        verbose_name_plural = 'Изображения установленных дверей'


@receiver(pre_delete, sender=ImageInstallDoorCardBot)
def image_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)


class SettingsBot(models.Model):
    main_title = models.TextField(verbose_name="Описание", **NULLABLE)
    main_image = models.ImageField(upload_to='wanmark', verbose_name='Изображение')
    on_contact = models.BooleanField(verbose_name='Отображать контакты в меню', default=False)
    contact_button = models.CharField(max_length=255, verbose_name="Название кнопки", **NULLABLE)
    contact_title = models.TextField(verbose_name="Описание", **NULLABLE)
    on_application = models.BooleanField(verbose_name='Отображать заявку в меню', default=False)
    application_button = models.CharField(max_length=255, verbose_name="Название кнопки", **NULLABLE)
    on_subscription = models.BooleanField(verbose_name='Отображать подписка на рассылку в меню', default=False)
    subscription_button = models.CharField(max_length=255, verbose_name="Название кнопки", **NULLABLE)
    on_mail = models.BooleanField(verbose_name='Включить рассылку', default=False)
    mail_hostname = models.CharField(max_length=255, verbose_name="Сервер исходящей почты (SMTP-сервер)", **NULLABLE)
    mail_port = models.PositiveIntegerField(verbose_name='Порт', default=465, **NULLABLE)
    mail_username = models.CharField(max_length=255, verbose_name="Электронный адрес", **NULLABLE)
    mail_password = models.CharField(max_length=255, verbose_name="Пароль", **NULLABLE)
    mail_use_tls = models.BooleanField(verbose_name='Защита соединения TLS/SSL', default=True)
    mail_email_to = models.CharField(max_length=255, verbose_name="Электронный адрес получателя рассылки ", **NULLABLE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.main_image:
            with Image.open(self.main_image.path) as img:
                img.load()

            if img.height > 1080 or img.width > 1920:
                new_height = 720
                new_width = int(new_height / img.height * img.width)
                img = img.resize((new_width, new_height))
                img.save(self.main_image.path)

    def __str__(self):
        return 'Настройки бота'

    class Meta:
        verbose_name = 'настройки бота'
        verbose_name_plural = 'Настройки бота'


@receiver(pre_delete, sender=SettingsBot)
def image_model_delete(sender, instance, **kwargs):
    if instance.main_image.name:
        instance.main_image.delete(False)


class NewsletterBot(models.Model):
    """Модель рассылки новостей через web интерфейс"""
    title = models.TextField(verbose_name="Описание")
    count_all = models.PositiveIntegerField(verbose_name='Общее кол-во', **NULLABLE)
    count_delivered = models.PositiveIntegerField(verbose_name='Доставленное кол-во', **NULLABLE)
    status = models.PositiveIntegerField(verbose_name='Статус отправки', default=0, **NULLABLE)
    send_date = models.DateTimeField(verbose_name='Дата рассылки', **NULLABLE)
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Рассылка новости: {self.id}'

    class Meta:
        verbose_name = 'рассылка новости'
        verbose_name_plural = 'Рассылки новостей'
        ordering = ["-id"]


class ImageNewsletterBot(models.Model):
    """Модель изображения для рассылки новостей"""
    link_newsletter = models.ForeignKey("NewsletterBot", on_delete=models.CASCADE, verbose_name='Рассылка новостей')
    image = models.ImageField(upload_to='wanmark/imagenewsletter', verbose_name='Изображение')

    def __str__(self):
        return f'{self.id} Изображение рассылки новостей: {self.link_newsletter}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            with Image.open(self.image.path) as img:
                img.load()

            if img.height > 1080 or img.width > 1920:
                new_height = 720
                new_width = int(new_height / img.height * img.width)
                img = img.resize((new_width, new_height))
                img.save(self.image.path)

    class Meta:
        verbose_name = 'Изображение рассылки новостей'
        verbose_name_plural = 'Изображения рассылки новостей'


@receiver(pre_delete, sender=ImageNewsletterBot)
def image_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)
