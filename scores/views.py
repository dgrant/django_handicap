from .models import Score, Course, Golfer
from .forms import ScoreForm
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext

from django.core.paginator import Paginator

from django.views.generic.list_detail import object_list

def score_list(request):
    PAGINATE_BY=20
    scores = Score.objects.filter(golfer__user__id=request.user.id)
    paginator = Paginator(scores, PAGINATE_BY)

    page = request.GET.get('page', 1)
    try:
        page_number = int(page)
    except ValueError:
        if page == 'last':
            page_number = paginator.num_pages
        else:
            # Page is not 'last', nor can it be converted to an int.
            raise Http404

    try:
        page_obj = paginator.page(page_number)
    except InvalidPage:
        raise Http404

    index, whichOnes = _calculateHandicap(scores)
    whichOnes = whichOnes[(page_number-1)*PAGINATE_BY:(page_number)*PAGINATE_BY]
    c = RequestContext(request, {
        'score_list': list(zip(page_obj.object_list, whichOnes)),
        'whichOnes': whichOnes,
        'page_obj': page_obj,
        'index': index,
    })


#    return object_list(request,
#                       queryset=my_scores,
#                       paginate_by=PAGINATE_BY,
#                       extra_context={'index': index, 'whichOnes': whichOnes},
#                       )
    model = scores.model
    template_name = "%s/%s_list.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = loader.get_template(template_name)
    return HttpResponse(t.render(c))

def _calculateHandicap(all_scores):
    """
    Calculate handicap from a list of scores and return the handicap and the an array that contains 0 or 1 at
    position i if score i was used in calculating the handicap
    """

    # Get the first 20 scores
    scores_subset = all_scores[:20]
    differentials = []
    for i, aScore in enumerate(scores_subset):
        differentials.append(((float(aScore.score) - float(aScore.tee.rating)) * float(aScore.tee.slope) / 113.0, i))

    #differentials will be at most 20 scores currently
    differentials.sort()
    howMany = len(differentials)
    if howMany < 5:
        numUse = 0
    elif howMany < 7:
        numUse = 1
    elif howMany < 9:
        numUse = 2
    elif howMany < 11:
        numUse = 3
    elif howMany < 13:
        numUse = 4
    elif howMany < 15:
        numUse = 5
    elif howMany < 17:
        numUse = 6
    elif howMany < 18:
        numUse = 7
    elif howMany < 19:
        numUse = 8
    elif howMany < 20:
        numUse = 9
    else:
        numUse = 10
    whichOnesUsed = [False for x in range(howMany)]
    for i in range(numUse):
        whichOnesUsed[differentials[i][1]] = True
    #undecorate. THIS IS UGLY, fix this
    for i in range(len(differentials)):
        differentials[i] = differentials[i][0]
    if numUse == 0:
        currHandicap = 0
    else:
        currHandicap = sum(differentials[:numUse])/float(numUse)
        currHandicap = round(currHandicap*10)/10.0
    while len(whichOnesUsed) < len(all_scores):
        whichOnesUsed.append(False)
    return currHandicap, whichOnesUsed

@login_required
def score_add_update(request, score_id=None):
    if request.method == 'POST':
        #Reconstruct a form with the POST data
        form = ScoreForm(request.POST)
        if form.is_valid():
            new_score = form.save(commit=False)

            #Make sure it gets owned by the right golfer
            golfer = Golfer.objects.get(user__id=request.user.id)
            new_score.golfer = golfer

            #Finally save the model
            new_score.save()
            return HttpResponseRedirect("/score/%i/" % new_score.id)
        else:
            return render_to_response('scores/score_form.html', {'form': form})
    else:
        # create form
        if score_id:
            form = ScoreForm(instance=Score.objects.get(id=score_id))
        else:
            form = ScoreForm()
        # create template and pass in form
        return render_to_response('scores/score_form.html', {'form': form})

def course_list(request):
   courses = Course.objects.all()
   assert(False, str(courses))
   resp = render_to_response('scores/course_list.html', {'object_list': courses})
   #resp['X-Debug'] = str(courses)
   return resp

def course_add(request):
    """
    FIXME: merge this and one below into two
    """
    manipulator = Course.AddManipulator()

    if request.method == 'POST':
        # If data was POSTed, we're trying to create a new Place.
        new_data = request.POST.copy()
        # Check for errors.
        errors = manipulator.get_validation_errors(new_data)

        if not errors:
            # No errors. This means we can save the data!
            manipulator.do_html2python(new_data)
            new_course = manipulator.save(new_data)

            # Redirect to the object's "edit" page. Always use a redirect
            # after POST data, so that reloads don't accidently create
            # duplicate entires, and so users don't see the confusing
            # "Repost POST data?" alert box in their browsers.
            return HttpResponseRedirect("/score/course/%i/" % new_course.id)
    else:
        # No POST, so we want a brand new form without any data or errors.
        errors = new_data = {}

    # Create the FormWrapper, template, context, response.
    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('scores/course_form.html', {'form': form})
