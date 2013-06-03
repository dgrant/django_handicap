from django.conf.urls.defaults import *
from handicap.scores.models import Score
from handicap.scores.models import Course

from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.create_update import create_object, update_object
from django.contrib.auth.decorators import login_required

score_dict = {
    'queryset': Score.objects.all(),
}
course_dict = {
    'queryset': Course.objects.all(),
}

urlpatterns = patterns('',

    #All of these patterns are caught below "/score"
    #List all scores
    url(r'^$',
        'handicap.scores.views.score_list',
        name='score_list'),
    #Show a single score using generic object_detail view
    url(r'^(?P<object_id>\d+)/$',
        login_required(object_detail),
        score_dict,
        name='score_view'),
    #Create a new score
    url(r'^add/$',
        'handicap.scores.views.score_add_update', name='score_add'),
    #Update a single score using the score_edit view
    url(r'^(?P<score_id>\d+)/edit/$',
        'handicap.scores.views.score_add_update', name='score_update'),

    #list courses
    (r'^course/$', 'handicap.scores.views.course_list'),
    #view one course
    (r'^course/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', course_dict),
    #create a new course
    (r'^course/add/$', 'handicap.scores.views.course_add'),
    #update a course
    (r'^course/(?P<course_id>\d+)/edit/$', 'course_edit'),
    
    ##view one course
    #(r'^course/(?P<course_id>\d+)/$', 'course_detail'),
    
)
