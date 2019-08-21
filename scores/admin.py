from .models import Course, Golfer, Score, Tee
from django.contrib import admin

class TeeInline(admin.TabularInline):
    model = Tee
    extra = 3

class CourseAdmin(admin.ModelAdmin):
    inlines = [TeeInline]

class ScoreAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['date', 'tee', 'score', 'isUsedInHandicap']}),
    ]
    list_display = ('date', 'tee', 'score', 'golfer')
    list_filter = ['date', 'golfer']
    date_hierarchy = 'date'


admin.site.register(Course, CourseAdmin)
admin.site.register(Golfer)
admin.site.register(Score, ScoreAdmin)
