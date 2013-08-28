from django.db import models


class Fare(models.Model):
    mode = models.CharField(unique=True)
    base = models.DecimalField(max_digits=5, decimal_places=2)
    increment = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('Fare')
        verbose_name_plural = ('Fares')
        ordering = ['mode',]
        db_table = 'fares'

    def __unicode__(self):
        return "Mode: %s, Base: %0.2f, Increment: %0.2f" % (self.mode, self.base, self.increment)
