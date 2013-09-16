from django.db import models
from django.contrib.auth.models import User

class Micropost(models.Model):
    content = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = ('micropost')
        verbose_name_plural = ('microposts')

    def __unicode__(self):
        pass

