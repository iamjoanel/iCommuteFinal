from django.db import models

from route.models import Route
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, editable=False)
    comment = models.CharField(max_length=140)
    approved = models.BooleanField(default=False, editable=False)
    route = models.ForeignKey(Route)
    date_posted = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "feedbacks"
        ordering = ['date_posted']

    def __unicode__(self):
        return "posted by: %s posted on: %s" % (self.user, self.rating, str(self.date_posted))
