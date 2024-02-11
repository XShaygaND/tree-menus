from django.db import models
from django.utils.text import slugify

class Menu(models.Model):
    """Class for representing menus"""

    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.url = f'/menu/{self.name}/'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Class for representing menu items"""

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=False)
    depth = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.parent:
            self.depth = self.parent.depth + 1

        self.url = self.set_item_url()
            
        super().save(*args, **kwargs)

    def set_item_url(self):
        if self.parent:
            return self.parent.url + slugify(self.title) + '/'
        
        return '/' + '/'.join(('menu', slugify(self.menu.name), slugify(self.title))) + '/'

    def __str__(self):
        return self.menu.name + ' | ' + self.title

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
