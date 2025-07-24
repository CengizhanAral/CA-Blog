import math
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.utils import translation



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Kullanıcı"))
    bio = models.TextField(_("Hakkında"), blank=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Instagram URL")
    twitter_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="X (Twitter) URL")
    facebook_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Facebook URL")
    linkedin_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="LinkedIn URL")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Yazar")
        verbose_name_plural = _("Yazarlar")


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Kategori Adı (Türkçe)"))
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    name_en = models.CharField(max_length=100, verbose_name=_("Kategori Adı (İngilizce)"), blank=True, null=True)
    slug_en = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.name_en and not self.slug_en:
            self.slug_en = slugify(self.name_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        current_language = translation.get_language()
        if current_language == 'en' and self.slug_en:
            return reverse('blog:category_posts', kwargs={'category_slug': self.slug_en})
        return reverse('blog:category_posts', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = _("Kategori")
        verbose_name_plural = _("Kategoriler")


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Taslak')),
        ('awaiting_approval', _('Onay Bekliyor')),
        ('published', _('Yayınlandı')),
    )

    title = models.CharField(max_length=200, verbose_name=_("Başlık (Türkçe)"))
    content = RichTextField(verbose_name=_("İçerik (Türkçe)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Başlık (İngilizce)"), blank=True, null=True)
    content_en = RichTextField(verbose_name=_("İçerik (İngilizce)"), blank=True, null=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts', verbose_name=_("Yazar"))
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name=_("Kategori"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma Tarihi"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Güncellenme Tarihi"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name=_("Durum"))
    views = models.PositiveIntegerField(default=0, verbose_name=_("Görüntülenme Sayısı"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title.replace('ı', 'i').replace('İ', 'i'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_reading_time(self):
        plain_text = strip_tags(self.content)
        word_count = len(plain_text.split())
        reading_time = math.ceil(word_count / 120)
        return reading_time

    class Meta:
        verbose_name = _("Yazı")
        verbose_name_plural = _("Yazılar")
        ordering = ['-created_at']
        permissions = [
            ("can_publish_post", "Can publish post"),
            ("can_change_author", "Can change post author"),
        ]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Yazı"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Kullanıcı"))
    name = models.CharField(max_length=80, verbose_name=_("İsim"))
    email = models.EmailField(verbose_name=_("E-posta"))
    body = models.TextField(verbose_name=_("Yorum"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma Tarihi"))
    active = models.BooleanField(default=True, verbose_name=_("Aktif"))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name=_("Ana Yorum"))

    class Meta:
        verbose_name = _("Yorum")
        verbose_name_plural = _("Yorumlar")
        # ordering = ['created_at'] # Yorumlara yanıt verme özelliği yokken kullanılır.

    def __str__(self):
        return f'{self.name} tarafından {self.post} yazısına yapılan yorum'


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name=_("E-posta Adresi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Abonelik Tarihi"))

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("Bülten Abonesi")
        verbose_name_plural = _("Bülten Aboneleri")
        ordering = ['-created_at']