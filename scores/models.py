import sys

from django.db import models
from django.contrib.auth.models import User

class Golfer(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   index = models.DecimalField(max_digits=4, decimal_places=2, null=True)

   def __str__(self):
       return self.user.first_name + ' ' + self.user.last_name + " (index: " + str(self.index) +")"

class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Tee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teeName = models.CharField(max_length=10)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    slope = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return str(self.course) + ' ' + self.teeName + ' tee (' + str(self.rating) + ', ' + str(self.slope) + ')'

class Score(models.Model):
    golfer = models.ForeignKey(Golfer, on_delete=models.CASCADE)
    date = models.DateField()
    tee = models.ForeignKey(Tee, on_delete=models.CASCADE)
    score = models.IntegerField()
    isUsedInHandicap = models.BooleanField()

    def get_absolute_url(self):
        # TODO: use reverse here
        return ('score_view',
                ([str(self.id)]),)

    def __unicode__(self):
        s = ''
        s += str(self.score)
        s += ' at ' + str(self.tee)
        s += ' on ' + str(self.date)
        s += ' by ' + str(self.golfer)
        if self.isUsedInHandicap == True:
            s += ' * '
        return s

    class Meta:
        ordering = ('-date',)
