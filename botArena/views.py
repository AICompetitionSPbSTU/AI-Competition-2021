import ctypes
import os
import boto3
import json
from builtins import __build_class__
from random import seed, randint, choice
from botocore.config import Config
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import BotForm, GameForm
from .models import Question, Choice, Game, Bot
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from multiprocessing import Process
from threading import Thread, enumerate
from django.core.cache import cache


def logging_test(request):
    next_to = ""
    # print(request.POST, request.GET)

    if request.GET:
        next_to = request.GET['next']
    # print(next_to)
    game_list = Game.objects.order_by('-name')
    context = {'game_list': game_list, 'next': next_to}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(request.POST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_to == "":
                return HttpResponseRedirect(reverse('botArena:home', args=()))
            else:
                return HttpResponseRedirect(next_to)
        else:
            context = {'game_list': game_list, 'error_message': "Wrong username or password."}
            return render(request, 'botArena/login.html', context)
    return render(request, 'botArena/login.html', context)


@login_required()
def creating_game_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('botArena:login', args=()))
    # TODO проверку на существование такой игры.
    if request.method == "POST":
        # name = request.POST['name']
        # leader = request.POST['leader']
        # score = 0
        # new_game = Game(name=name, leader=leader, leader_score=score)
        # new_game.save()
        print(request.POST, request.FILES)
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('botArena:home', args=()))
        # Если форма не валидная
        # print(form)
        form = GameForm()
        return render(request, 'botArena/new_game.html', {'form': form, 'error_message': "Error occurs"})
    form = GameForm()
    return render(request, 'botArena/new_game.html', {'form': form})


def home(request):
    # if not request.user.is_authenticated:
    #    return HttpResponseRedirect(reverse('botArena:login', args=()))
    game_list = Game.objects.order_by('-name')[:7]
    context = {'game_list': game_list}
    return render(request, 'botArena/home.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('botArena:login'))


@login_required()
def game(request, name):
    # Сделать через get object or 4o4?
    games = Game.objects.filter(name__startswith=name)
    this_game = games[0]
    description = this_game.long_description.read()
    # print(this_game)
    return render(request, 'botArena/game.html', {'game': this_game, 'description': description})


def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        # user = authenticate(request, username=username, password=password)
        duplicate_users = User.objects.filter(username=username)
        if not duplicate_users:
            if len(username) > 50:
                err_msg = "User name is too long"
                return render(request, 'botArena/registration.html', {"error_message": err_msg})
            if len(password) < 5:
                err_msg = "Password too short"
                return render(request, 'botArena/registration.html', {"error_message": err_msg})
            user = User.objects.create_user(username, email, password)
            user.save()
        else:
            err_msg = "User already exist"
            return render(request, 'botArena/registration.html', {"error_message": err_msg})
        return render(request, 'botArena/login.html')

    return render(request, 'botArena/registration.html')


@login_required()
def sign_s3(request):
    S3_BUCKET = os.environ.get('S3_BUCKET')  # heroku
    # S3_BUCKET = "spbstubotarena"
    # print(request)
    file_name = request.GET.get('file_name')
    file_type = request.GET.get('file_type')
    game_name = request.GET.get('game_name')
    # print("was here")
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'), region_name='eu-central-1')
    print(file_name)
    print(file_type)
    print(game_name)
    user = request.user.username
    file_name = user + "_" + game_name + "_" + file_name
    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key="bot_src/" + file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {'acl': "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )
    print(presigned_post)
    path_url = "https://spbstubotarena.s3.eu-central-1.amazonaws.com/bot_src/"
    data = json.dumps({
        'data': presigned_post,
        'url': path_url + file_name,
    })
    return HttpResponse(data, content_type='json')


@login_required()
def playground_bot(request, game_name, bot_id):
    # print('playground_bot')
    games = Game.objects.filter(name__startswith=game_name)
    this_game = games[0]
    this_bot = this_game.bot_set.filter(pk=bot_id)[0]
    if not os.path.exists(str(this_bot.source)):  # upload bot if we dont have prev temp file
        print("upload new File!")
        url = this_bot.url_source
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(urlopen(url).read())
        # bot_code = temp_file.read()
        this_bot.source = temp_file.name
        temp_file.close()

    working_source = str(this_bot.source)
    # print(working_source)

    # with open('media/bots_src/matches_mybot.py', 'r') as f: # macthes bot debug
    # with open('media/bots_src/tic_tac_toe_mybot.py', 'r') as f:
    with open(working_source, 'r') as f:
        bot_code = f.read()

        game_code = this_game.source.read()

        loc = {}
        import math
        # print(bot_code)
        exec(bot_code, {"__builtins__": {'__name__': __name__, 'math': math, '__build_class__': __build_class__,
                                         'randint': randint}, 'range': range}, loc)
        bot_class = loc['Bot']  # ой еще тут нужно сделать парсинг имени класса, ну за идеальный час успеешь
        loc = {}
        exec(game_code, None, loc)
        game_class = loc['Game']
        bot = bot_class()
        game = game_class(bot=bot)
    if request.method == "GET":
        game_cond = request.GET.get("game_cond")
        if game_cond == "start":
            print('game start')
            ##            url = this_bot.url_source

            ##            temp_file = NamedTemporaryFile(delete=True)
            ##            temp_file.write(urlopen(url).read())
            ##            bot_code = temp_file.read()
            ##            temp_file.close()

            state = game.get_state()

            data = json.dumps({'inner_state': state['field']})
            print('состояние', state['field'])

            request.session['game_state'] = game.get_state()

            return HttpResponse(data, content_type='json')
        if game_cond == "running":
            print('game running')
            incoming_state = request.GET.get("inner_state")
            game = game_class(state=request.session['game_state'], bot=bot)

            # user_took = game.get_state() - int(state)

            # print('user took:', user_took)

            game.user_input(user_action=incoming_state)
            game.bot_move()

            new_state = game.get_state()

            print('new state:', new_state)

            data = json.dumps({'inner_state': new_state['field']})  # 'number'
            request.session['game_state'] = new_state

            return HttpResponse(data, content_type='json')
    print(this_game.interface)
    return render(request, this_game.interface)


@login_required()
def bot_view(request, game_name, creator_name, id):
    return render(request, 'botArena/bot.html', {'game_name': game_name, 'bot_id': id})


@login_required()
def creating_bot_view(request, name):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('botArena:login', args=()))
    # print(name)
    # TODO get game or 404
    this_game = Game.objects.filter(name__startswith=name)
    if request.method == "POST":
        # print(request.POST)
        post_values = request.POST.copy()
        post_values['game'] = this_game[0]
        post_values['creator_name'] = request.user.username
        form = BotForm(post_values, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Committee Podcast Was Created',
                             "alert alert-success alert-dismissible")
            # return HttpResponseRedirect(reverse('botArena:home', args=()))

        # Если форма не валидная
        else:
            form = BotForm()
            return render(request, 'botArena/new_game.html', {'game_name': name, 'form': form, 'error_message': "Error "
                                                                                                                "occurs"})
    form = BotForm()

    return render(request, 'botArena/new_bot.html', {'game_name': name, 'form': form, })


# expected new page
def about_view(request):
    return render(request, 'botArena/about.html')  # some space


@login_required()
def playing_game_view(request, game_name):
    games = Game.objects.filter(name__startswith=game_name)
    this_game = games[0]
    bots = this_game.bot_set.all()
    if not bots:
        return HttpResponseRedirect(reverse('botArena:game', args=(game_name,)))
    print(bots)
    i_choose = choice(bots)
    return HttpResponseRedirect(reverse('botArena:playground', args=(game_name, i_choose.id)))
    # return render(request, this_game.interface)

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
#     question = get_object_or_404(Question, pk=question_id
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
