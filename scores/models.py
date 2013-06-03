import sys

from django.db import models
from django.contrib.auth.models import User

class Golfer(models.Model):
   user = models.OneToOneField(User)
   index = models.DecimalField(max_digits=4, decimal_places=2, null=True)

   def __str__(self):
       return self.user.first_name + ' ' + self.user.last_name + " (index: " + str(self.index) +")"

class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Tee(models.Model):
    course = models.ForeignKey(Course)
    teeName = models.CharField(max_length=10)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    slope = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return unicode(self.course) + ' ' + self.teeName + ' tee (' + unicode(self.rating) + ', ' + unicode(self.slope) + ')'

class Score(models.Model):
    golfer = models.ForeignKey(Golfer)
    date = models.DateField()
    tee = models.ForeignKey(Tee)
    score = models.IntegerField()
    isUsedInHandicap = models.BooleanField()

    @models.permalink
    def get_absolute_url(self):
        return ('score_view',
                ([str(self.id)]),)

    def __unicode__(self):
        s = ''
        s += unicode(self.score)
        s += ' at ' + unicode(self.tee)
        s += ' on ' + unicode(self.date)
        s += ' by ' + unicode(self.golfer)
        if self.isUsedInHandicap == True:
            s += ' * '
        return s

    class Meta:
        ordering = ('-date',)
