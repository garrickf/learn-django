# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404

from .models import Question

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context) # with this shortcut, we no longer need to import HttpResponse or loader!

def detail(request, question_id):
	# idiom for get object or 404
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question}) # context is inside

def results(request, question_id):
	response = "You're looking at the results of question %s"
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("You're voting on question %s" % question_id)