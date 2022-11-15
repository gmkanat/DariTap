from django.db import models
from django.utils.translation import gettext as _

from mixins.models import (
    TimeStampMixin,
    IsActiveMixin,
)


class Category(TimeStampMixin, IsActiveMixin):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    image = models.ImageField(
        upload_to='categories',
        verbose_name=_('Image'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Image(TimeStampMixin, IsActiveMixin):
    image = models.ImageField(
        upload_to='images',
        verbose_name=_('Image'),
    )

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return self.image.url


class Item(TimeStampMixin, IsActiveMixin):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Price'),
        default=0,
    )
    images = models.ManyToManyField(
        Image,
        related_name='items',
        verbose_name=_('Images'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Category'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __str__(self):
        return self.name
