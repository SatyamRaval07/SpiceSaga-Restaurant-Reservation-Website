from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Blog(models.Model):
    title = models.CharField(max_length=30, verbose_name='Title', unique=True)
    body = models.TextField(verbose_name='Text')
    image = models.ImageField(verbose_name='Blog Image', upload_to='Blog',
                              help_text='Image size should be 470x570 pixels')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Category', related_name='blog')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    tag = models.ManyToManyField('Tag', verbose_name='Tags', related_name='tag')
    situation = models.BooleanField(verbose_name='Publication Status', default=False)
    created_at = models.DateField(verbose_name='Creation Date', auto_now_add=True)
    update = models.DateTimeField(verbose_name='Last Updated Date', auto_now=True)
    slug = models.SlugField(blank=True, verbose_name='Slug',
                            help_text='This field is automatically populated')

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Blog, self).save()

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class Category(models.Model):
    title = models.CharField(max_length=25, verbose_name='Category Title', unique=True)
    slug = models.SlugField(blank=True, verbose_name='Slug',
                            help_text='This field is automatically populated')
    date = models.DateTimeField(verbose_name='Creation Date', auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Category, self).save()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    title = models.CharField(max_length=25, verbose_name='Tag Title', unique=True)
    slug = models.SlugField(blank=True, unique=True, verbose_name='Slug',
                            help_text='This field is automatically populated')
    date = models.DateTimeField(verbose_name='Creation Date', auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Tag, self).save()

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name='Article',
                             help_text='Which article is this comment for')
    name = models.CharField(max_length=20, verbose_name='Name')
    email = models.EmailField(verbose_name='Email', null=True)
    text = models.TextField(verbose_name='Comment Text')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', verbose_name='Reply to Comment',
                               help_text='If this comment is a reply to another comment, it is filled in', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')

    def __str__(self):
        return self.text[:10]

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
