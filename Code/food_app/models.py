from django.db import models
from django.utils.text import slugify

class Food(models.Model):
    TYPES = [
        ('drinks', 'Beverage'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]

    food_type = models.CharField(max_length=20, choices=TYPES, verbose_name='Food Type')

    name = models.CharField(max_length=20, verbose_name='Food Name')

    price = models.PositiveIntegerField(verbose_name='Food Price')

    description = models.TextField(verbose_name='Food Description',default='No description provided.')

    image = models.ImageField(upload_to='Foods', verbose_name='Food Image',
                              help_text='Images should be in the size of 800x480 pixels')

    slug = models.SlugField(blank=True, unique=True, verbose_name='Slug',
                            help_text='This field is automatically populated')

    update_at = models.DateTimeField(verbose_name='Last Updated Date', auto_now=True)
    date = models.DateTimeField(verbose_name='Creation Date', auto_now_add=True)

    availability = models.BooleanField(default=True, verbose_name='Availability')
    status = models.BooleanField(default=False, verbose_name='Status', help_text='Publication status on the website')

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super(Food, self).save()

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'


class Comment(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='comments', verbose_name='Food',
                             help_text='Which food is this comment about')

    name = models.CharField(max_length=20, verbose_name='Name and Surname')

    email = models.EmailField(verbose_name='Email', null=True)

    text = models.TextField(verbose_name='Comment Text')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', verbose_name='Reply to Comment',
                               help_text='If this comment is a reply to another comment, it will be filled', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')

    def __str__(self):
        return self.text[:10]

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
