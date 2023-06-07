import random
import os

from django.db.models import Q
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from e_commerce.utils import unique_slug_generator

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename = new_filename, ext = ext) #old format
    #final_filename = f"{new_filename}{ext}" #syntax to python 3.6 and up

    return "products/{new_filename}/{final_filename}".format(
            new_filename = new_filename, 
            final_filename = final_filename
            )
    #return f"products/{new_filename}/{new_filename}" #syntax to python 3.6 and up

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)

    def featured(self):
        return self.filter(featured = True, active = True)
    
    def search(self, query):
        lookups = (Q(title__contains = query) | 
                   Q(description__contains = query) | 
                   Q(price__contains = query) |
                   Q(tag__title__icontains = query))
        return self.filter(lookups).distinct()      
    
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using = self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None
    
    def search(self, query):
        return self.get_queryset().active().search(query)

# Create your models here.
class Product(models.Model): #product_category
    title         = models.CharField(max_length=120)
    slug          = models.SlugField(blank = True, default = 'slug_padrao', unique = True)
    qtd           = models.IntegerField(default=1)
    description   = models.TextField()
    price         = models.DecimalField(decimal_places=2, max_digits=20, default=100.00)
    image         = models.ImageField(upload_to = 'products/',  null = True, blank = True)
    distribuidora = models.CharField(max_length=140, default='', blank=True, null=True)
    featured    = models.BooleanField(default = False)
    active      = models.BooleanField(default = True)
    timestamp   = models.DateTimeField(auto_now_add = True)
    
    objects = ProductManager()

    def get_absolute_url(self):
        #return "/produto/{slug}/".format(slug = self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender = Product)