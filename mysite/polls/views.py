# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse

from .models import Question, Choice

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context) # with this shortcut, we no longer need to import HttpResponse or loader!

def detail(request, question_id):
	# idiom for get object or 404
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question}) # context is inside

def results(request, question_id):
    # response = "You're looking at the results of question %s"
	# return HttpResponse(response % question_id)
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	# return HttpResponse("You're voting on question %s" % question_id)
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# redisp. voting form
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice."
			})
	else:
		selected_choice.votes += 1 # careful: race condition (if two vote at same time)
		selected_choice.save()
		# return HttpResponseRedirect
		return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))