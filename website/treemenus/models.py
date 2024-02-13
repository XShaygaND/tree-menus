from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class MenuItem(models.Model):
    """Class for representing menu items"""

    name = models.CharField(max_length=99)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    depth = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        """Modifies the depth and the url of the object pre-save"""

        if self.parent:
            self.depth = self.parent.depth + 1

        self.url = self.get_item_url()

        super().save(*args, **kwargs)

    def clean(self):
        """Modifies object's name and raises a `ValidationError` if the parent is not relative"""

        if not self.name:
            if self.parent:
                self.name = self.parent.name

        if self.parent and not self.name == self.parent.name:
            raise ValidationError(
                {'parent': "Parent must be in the same menu as menu item"})

    def get_item_url(self):
        """Returns the correct url for the item"""

        if self.parent:
            return self.parent.url + slugify(self.title) + '/'

        return '/' + '/'.join(('menu', slugify(self.name), slugify(self.title))) + '/'

    def __str__(self):
        return self.name + ' | ' + self.title

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
