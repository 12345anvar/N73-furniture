from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.models import BaseModel


class Author(BaseModel):
    full_name = models.CharField(
        max_length=128,
        verbose_name=_("Full name")
    )
    image = models.ImageField(
        upload_to='authors/',
        verbose_name=_("Image")
    )
    about = models.CharField(
        max_length=255,
        verbose_name=_("About")
    )
    professions = models.CharField(
        max_length=128,
        verbose_name=_("Professions")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active")
    )

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'authors'
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class Category(BaseModel):
    title = models.CharField(
        max_length=128,
        verbose_name=_("Title")
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        null=True,
        blank=True,
        verbose_name=_("Parent category")
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'categories'
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Tag(BaseModel):
    title = models.CharField(
        max_length=128,
        verbose_name=_("Title")
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tags'
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class BlogStatus(models.TextChoices):
    PUBLISHED = "PUBLISHED", _("Published")
    DRAFT = "DRAFT", _("Draft")
    DELETED = "DELETED", _("Deleted")


class Blog(BaseModel):
    title = models.CharField(
        max_length=128,
        verbose_name=_("Title")
    )
    short_description = models.CharField(
        max_length=255,
        verbose_name=_("Short description")
    )
    image = models.ImageField(
        upload_to='blogs/',
        null=True,
        blank=True,
        verbose_name=_("Image")
    )
    long_description = models.TextField(
        verbose_name=_("Long description")
    )
    status = models.CharField(
        max_length=20,
        choices=BlogStatus,
        default=BlogStatus.DRAFT,
        verbose_name=_("Status")
    )
    categories = models.ManyToManyField(
        Category,
        related_name='blogs',
        verbose_name=_("Categories")
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='blogs',
        verbose_name=_("Tags")
    )
    authors = models.ManyToManyField(
        Author,
        related_name='blogs',
        verbose_name=_("Authors")
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blogs'
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
