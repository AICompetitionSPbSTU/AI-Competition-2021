import ctypes
import os
# import boto3
import json
from random import seed, randint
# from botocore.config import Config
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
    game_list = Game.objects.order_by('-name')[:5]
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
    this_game = Game.objects.filter(name__startswith=name)
    # print(this_game)
    return render(request, 'botArena/game.html', {'game': this_game[0]})


def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # user = authenticate(request, username=username, password=password)
        duplicate_users = User.objects.filter(username=username)
        if not duplicate_users:
            if len(username) > 50:
                err_msg = "User name is too long"
                return render(request, 'botArena/registration.html', {"error_message": err_msg})
            if len(password) < 5:
                err_msg = "Password too short"
                return render(request, 'botArena/registration.html', {"error_message": err_msg})
            user = User.objects.create_user(username, 'no_email', password)
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
    games = Game.objects.filter(name__startswith=game_name)
    this_game = games[0]
    this_bot = this_game.bot_set.filter(pk=bot_id)[0]
    print(this_bot.url_source)
    url = this_bot.url_source
    result = 0
    if url:
        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(urlopen(url).read())
        # print(temp_file.name)
        # print(urlopen(url).read())
        temp_file.read()
        # temp_file.close()
        with open(temp_file.name, 'r') as f:
            result = exec(f.read())
        # result = os.system('python '+temp_file.name)
        # result = temp_file.read()
        temp_file.close()

    return render(request, 'botArena/playground.html', {'bot_url': str(url), 'result': result})


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


def start_new_thread(function):
    def decorator(*args, **kwargs):
        _, name = args
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.name = name
        t.daemon = True
        t.start()

    return decorator


@start_new_thread
def run_game(src, user_name):
    # from django.db import connection
    # connection.close()
    # smt=''
    with src as f:
        result = exec(f.read())
    pass


def check_user_already_play(user_name):
    for t in enumerate():
        name = t.getName()
        if name == str(user_name):
            print("kill proc", name)
            #thread_id = t.native_id local
            print(dir(t))
            thread_id = t.ident # for heroku
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                             ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print('Exception raise failure')
            print("I kill him!!!")


@login_required()
def playing_game_view(request, game_name):
    for t in enumerate():
        print(t.getName())
    print('-' * 10)

    games = Game.objects.filter(name__startswith=game_name)
    this_game = games[0]
    if request.method == "GET":
        game_cond = request.GET.get("game_cond")
        if game_name == "tic_tac_toe":
            if game_cond == "start":
                check_user_already_play(request.user)
                src = this_game.source.open()
                run_game(src, request.user)
                print("run tic_tac for ", request.user)
                start = ['-1' for _ in range(9)]
                seed()
                data = json.dumps({'inner_state': start})
                return HttpResponse(data, content_type='json')
            if game_cond == "running":
                state = request.GET.get("inner_state").split(',')
                while True:
                    bot_choose = randint(0, 8)
                    # print(bot_choose)
                    # print("nigga")
                    if state[bot_choose] == '-1':
                        state[bot_choose] = '0'
                        break
                data = json.dumps({
                    'inner_state': state,
                })
                return HttpResponse(data, content_type='json')
        else:
            if game_cond == "start":
                check_user_already_play(request.user)
                src = this_game.source.open()
                seed()
                run_game(src, request.user)
                print("run matches for ", request.user)
                # os.system('python '+str(data)+" &")
                data = json.dumps({
                    'inner_state': 21,
                })
                return HttpResponse(data, content_type='json')

            if game_cond == "running":
                for t in enumerate():
                    print(t.getName())
                count = request.GET.get("inner_state")
                bot_choose = randint(1, 3)
                new_state = int(count) - bot_choose
                data = json.dumps({
                    'inner_state': new_state,
                })
                return HttpResponse(data, content_type='json')
    print(this_game.interface)
    return render(request, this_game.interface)

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
