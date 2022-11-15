from django.db import models
from django.utils.translation import gettext as _

from api.models import User, Item
from mixins.models import (
    TimeStampMixin,
    IsActiveMixin,
)


class Wishlist(TimeStampMixin, IsActiveMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlists',
        verbose_name=_('User'),
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='wishlists',
        verbose_name=_('Item'),
    )

    class Meta:
        verbose_name = _('Wishlist')
        verbose_name_plural = _('Wishlists')
        unique_together = ('user', 'item')

    def __str__(self):
        return f'{self.user} - {self.item}'

