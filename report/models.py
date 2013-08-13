from django.db import models
from django.contrib.auth.models import User


class Report(models.Model):
    post = models.CharField(max_length=200)
    reporter = models.ForeignKey(User)
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ('Report')
        verbose_name_plural = ('Reports')

    def __unicode__(self):
        return "%s posted by: %s posted on: %s" % (self.post, self.reporter, self.post_date)

    def __repr__(self):
        return "%s posted by: %s posted on: %s" % (self.post, self.reporter, self.post_date)
