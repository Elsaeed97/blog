from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


class Post(models.Model):
    author = models.ForeignKey(
        get_user_model(), verbose_name=_("Author"), on_delete=models.CASCADE
    )
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title
