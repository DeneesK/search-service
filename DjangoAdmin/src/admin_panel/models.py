import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField('text', blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    rubrics = ArrayField(models.TextField())

    def __str__(self) -> str:
        return str(self.text[:30])

    class Meta:
        db_table = "public\".\"posts"
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
