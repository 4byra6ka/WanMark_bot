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


class ImageInstallDoorCardBot(models.Model):
    """Модель изображения установленных дверей для карточки двери"""
    link_door_card = models.ForeignKey("DoorCardBot", on_delete=models.CASCADE, verbose_name='Карточка двери')
    image = models.ImageField(upload_to='wanmark/imageinstall', verbose_name='Изображение')

    def __str__(self):
        return f'Установленная дверь картинка: {self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:  # check if image exists before resize
            with Image.open(self.image.path) as img:
                img.load()
            # img = Image.open(self.report_image.path)

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


class DescriptionMainMenuBot(models.Model):
    title = models.TextField(verbose_name="Описание", **NULLABLE)
    image = models.ImageField(upload_to='wanmark', verbose_name='Изображение')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:  # check if image exists before resize
            with Image.open(self.image.path) as img:
                img.load()
            # img = Image.open(self.report_image.path)

            if img.height > 1080 or img.width > 1920:
                new_height = 720
                new_width = int(new_height / img.height * img.width)
                img = img.resize((new_width, new_height))
                img.save(self.image.path)

    def __str__(self):
        return 'Описание главного меню'

    class Meta:
        verbose_name = 'описание главного меню'
        verbose_name_plural = 'Описание главного меню'


@receiver(pre_delete, sender=DescriptionMainMenuBot)
def image_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)
