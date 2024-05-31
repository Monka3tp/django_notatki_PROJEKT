from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Opublikowany')
    )
    PRIORITY_CHOICES = (
        (0, "Wazne"),
        (1, "Standard"),
    )

    title = models.CharField(max_length=250)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notatki_posts')
    # text = models.TextField(default="tekst")
    body = models.TextField(default="Tutaj wpisz tekst")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='published')


    class Meta:
        ordering = ('priority',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notatki:post_detail', args=[self.publish.year,
                                                    self.publish.strftime('%m'),
                                                    self.publish.strftime('%d'),
                                                    self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"Notatka zaktualizowana przez {self.name}"
