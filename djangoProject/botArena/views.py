from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Question, Choice, Game


def logging_test(request):
    game_list = Game.objects.order_by('-name')[:5]
    context = {'game_list': game_list}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('botArena:home', args=()))

            # Redirect to a success page.
            ...
        else:
            context = {'game_list': game_list, 'error_message': "Wrong username or password."}
            return render(request, 'botArena/login.html', context)
            # Return an 'invalid login' error message.

            ...
    return render(request, 'botArena/login.html', context)


def home(request):
    game_list = Game.objects.order_by('-name')[:5]
    context = {'game_list': game_list}
    if request.user.is_authenticated:
        return render(request, 'botArena/home.html', context)
    else:
        return HttpResponseRedirect(reverse('botArena:login', args=()))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('botArena:login'))
    #return render(request, 'botArena/login.html')


def game(request, name):
    # Сделать через get object or 4o4?
    this_game = Game.objects.filter(name__startswith=name)
    print(this_game)
    if request.user.is_authenticated:
        return render(request, 'botArena/game.html', {'game': this_game[0]})
    else:
        return HttpResponseRedirect(reverse('botArena:login', args=()))


def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, 'no_email', password)
        user.save()
        return render(request, 'botArena/login.html')

    return render(request, 'botArena/registration.html')


# def logout(request):
#     return render(request, 'botArena/logout.html')

#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'botArena/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'botArena/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'botArena/results.html', {'question': question})
#
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'botArena/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('botArena:results', args=(question.id,)))
