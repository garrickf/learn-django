# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase

import datetime
from django.utils import timezone
from django.urls import reverse
from .models import Question

# Create your tests here. Note: chenged upper level directory name to allow tests to run!
class QuestionMethodTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() should return False for 
		questions whose pub_date is in the future.
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() should return False for 
		questions that are older than a day.
		"""
		time = timezone.now() - datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() should return True for 
		questions published recently (an hour ago).
		"""
		time = timezone.now() - datetime.timedelta(hours=1)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), True)

def create_question(question_text, days):
	"""
	creates a question with the given parameters text and 
	offset (negative for the past, positive for the future)
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):

	def test_index_view_with_no_questions(self):
		"""
		if no questions exist, check status code, context
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_a_past_question(self):
		"""
		Questions with a pub_date in the past should be displayed on the
		index page.
		"""
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_index_view_with_a_future_question(self):
		"""
		Questions with a pub_date in the future should not be displayed on
		the index page.
		"""
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_future_question_and_past_question(self):
		"""
		Even if both past and future questions exist, only past questions
		should be displayed.
		"""
		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_index_view_with_two_past_questions(self):
		"""
		The questions index page may display multiple questions.
		"""
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question 2.>', '<Question: Past question 1.>']
		)

class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
		"""
		The detail view of a question with a pub_date in the future should
		return a 404 not found.
		"""
		future_question = create_question(question_text='Future question.', days=5)
		url = reverse('polls:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_question(self):
		"""
		The detail view of a question with a pub_date in the past should
		display the question's text.
		"""
		past_question = create_question(question_text='Past Question.', days=-5)
		url = reverse('polls:detail', args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)