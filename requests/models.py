from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Request(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    count = models.IntegerField(blank=True, null=True, default=1)
    is_done = models.BooleanField(default=False, editable=False)
    requested_by = models.ForeignKey(User, editable=False)

    class Meta:
        db_table = 'requests'

    def __unicode__(self):
        return "Origin: %s Destination: %s" % (self.origin, self.destination)
