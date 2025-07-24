from django.contrib import admin
from .models import Author, Category, Post, Comment, Subscriber
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
import csv



@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'slug', 'slug_en')
    prepopulated_fields = {'slug': ('name',), 'slug_en': ('name_en',)}

    fieldsets = (
        ('Türkçe İçerik', {
            'fields': ('name', 'slug')
        }),
        ('İngilizce İçerik (Opsiyonel)', {
            'classes': ('collapse',),
            'fields': ('name_en', 'slug_en')
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'category')
    search_fields = ('title', 'content', 'author__user__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('status', '-created_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author__user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = Author.objects.get(user=request.user)
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('blog.can_publish_post'):
            limited_choices = [
                ('draft', _('Taslak')),
                ('awaiting_approval', _('Onay Bekliyor')),
            ]
            form.base_fields['status'].choices = limited_choices
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj:
            readonly_fields = ['created_at', 'updated_at', 'views']
            if not request.user.has_perm('blog.can_change_author'):
                readonly_fields.append('author')
            return readonly_fields
        return ['created_at', 'updated_at', 'views']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            if not request.user.is_superuser:
                kwargs["queryset"] = Author.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

    approve_comments.short_description = "Seçili yorumları onayla"


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    list_filter = ('created_at',)
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Seçili aboneleri CSV olarak dışa aktar"
