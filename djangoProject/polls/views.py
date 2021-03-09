from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Question, Choice, Game


def logging_test(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('polls:home', args=()))

            # Redirect to a success page.
            ...
        else:
            return render(request, 'polls/login.html', {'error_message': "Wrong username or password.", })
            # Return an 'invalid login' error message.

            ...
    return render(request, 'polls/login.html')


def home(request):
    game_list = Game.objects.order_by('-name')[:5]
    context = {'game_list': game_list}
    if request.user.is_authenticated:
        return render(request, 'polls/home.html', context)
    else:
        return render(request, 'polls/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'polls/login.html')


def game(request, name):
    if request.user.is_authenticated:
        return render(request, 'polls/game.html', {'name': name})
    else:
        return render(request, 'polls/login.html')


def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, 'no_email', password)
        user.save()
        return render(request, 'polls/login.html')

    return render(request, 'polls/registration.html')


# def logout(request):
#     return render(request, 'polls/logout.html')


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
