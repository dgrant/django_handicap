from handicap.scores.models import *
from random import randint
from string import ascii_lowercase
from datetime import date

from django.contrib.auth.models import User

#Delete all users, keep the admin though
for u in User.objects.all():
    if u.username != 'admin' and u.is_superuser != True and u.is_staff != True:
        u.delete()

u1 = User.objects.create_user('david', 'davidgrant@gmail.com', 'nasha')
u1.first_name = 'David'
u1.last_name = 'Grant'
u1.save()
print "Created User:", u1
u2 = User.objects.create_user('test', 'test@gmail.com', 'test')
u2.first_name = 'Test'
u2.last_name = 'Test'
u2.save()
print "Created User:", u2

g1 = Golfer(user=u1)
g1.save()
print "Created Golfer:", g1
g2 = Golfer(user=u2)
g2.save()
print "Created Golfer:", g2

#delete all courses
for c in Course.objects.all():
    c.delete()
#make some courses   
courses=['Fraserview','Langara','Marine Drive','McCleery','Musquem','Point Grey','Queen Elizabeth','Rupert Park','Shaughnessy','Stanley Park','University Golf Club','Green Meadows','Fairway Village','Pine Crest','Royal Oaks']
for course in courses:
    c = Course(name=course)
    c.save()

#make 4 tees for each course
colours=['black','blue','red','green','white','gold']
for c in Course.objects.all():
    for i in xrange(randint(2,5)):
        c.tee_set.create(teeName=colours[randint(0,len(colours)-1)],
                         rating=randint(65,74),
                         slope=randint(100,140))

#add about 30 scores
for i in xrange(20):
    tees = Tee.objects.all()
    random_tee = tees[randint(0,len(tees)-1)]
    random_tee.score_set.create(date=date(2006,randint(1,12),randint(1,28)),
                                score=randint(80,110),
                                isUsedInHandicap=False,
                                golfer=g1)
