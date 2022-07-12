from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog_posts",default=User)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    image = models.FileField(upload_to="images/")
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)    # ordering yangi qoshilgan obektlar oxiriga qoshiladi
        verbose_name_plural = 'Postlar'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])



# # Coment yozish
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True) # # null=True, email ixtiyoriy yozish bo'sh qosa majburiy boladi
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # # BooleanField() chekbox


    class Meta:
        ordering = ('created',) # # qavus ichida xar doim 2 ta obekt bolish shart! vergul qoyilish shart!
        verbose_name_plural = "Commentlar"

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"