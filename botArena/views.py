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
    game_list = Game.objects.order_by('-name')[:7]
    context = {'game_list': game_list, 'next': next_to}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(request.POST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_to == "":
                return home(request)  # HttpResponseRedirect(reverse('botArena:home', args=()))
            else:
                return HttpResponseRedirect(next_to)
        else:
            context = {'game_list': game_list, 'error_message': "Wrong username or password."}
            # return render(request, 'botArena/login.html', context)
            return home(request,
                        error="Wrong username or password.")  # HttpResponseRedirect(reverse('botArena:home', args=()))
    return home(request)  # HttpResponseRedirect(reverse('botArena:home', args=()))
    # return render(request, 'botArena/login.html', context)


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


def home(request, error=None):
    # if not request.user.is_authenticated:
    #    return HttpResponseRedirect(reverse('botArena:login', args=()))
    game_list = Game.objects.order_by('-name')[:7]
    if error:
        context = {'game_list': game_list, 'err_msg': error}
    else:
        context = {'game_list': game_list}
    return render(request, 'botArena/home.html', context)


def logout_view(request):
    logout(request)
    # return HttpResponseRedirect(reverse('botArena:login'))
    return home(request)  # HttpResponseRedirect(reverse('botArena:home', args=()))


# @login_required()
def game(request, name):
    # Сделать через get object or 4o4?
    games = Game.objects.filter(name__startswith=name)
    this_game = games[0]
    all_text = ""
    with open('media/' + str(this_game.long_description), 'r') as txt:
        lines = txt.readlines()
        all_text = "".join(lines)
    description = all_text  # this_game.long_description.read()
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
                # return render(request, 'botArena/registration.html', {"error_message": err_msg})
                return home(request,
                            error="User name is too long")  # HttpResponseRedirect(reverse('botArena:home', args=()))
            if len(password) < 5:
                err_msg = "Password too short"
                return home(request, error=err_msg)  # HttpResponseRedirect(reverse('botArena:home', args=()))
                # return render(request, 'botArena/registration.html', {"error_message": err_msg})
            user = User.objects.create_user(username, email, password)
            user.save()
        else:
            err_msg = "User already exist"
            return home(request, error=err_msg)  # HttpResponseRedirect(reverse('botArena:home', args=()))
            # return render(request, 'botArena/registration.html', {"error_message": err_msg})
        # return render(request, 'botArena/login.html')
        return home(request)  # HttpResponseRedirect(reverse('botArena:home', args=()))

    # return render(request, 'botArena/registration.html')
    return home(request)  # HttpResponseRedirect(reverse('botArena:home', args=()))


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
    if not os.path.exists(str(this_bot.source)):  # upload bot if we dont have prev temp file
        print("upload new File!")
        url = this_bot.url_source
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(urlopen(url).read())
        # bot_code = temp_file.read()
        this_bot.source = str(temp_file.name)
        temp_file.close()
        this_bot.save()

    working_source = str(this_bot.source)
    # working_source = 'bot_src/pacman/my_pacman_bot.py'
    with open(working_source, 'r') as f:
        bot_code = f.read()
    game_code = this_game.source.read()

    loc = {}
    import math

    exec(bot_code, {"__builtins__": {'__name__': __name__, 'math': math, '__build_class__': __build_class__,
                                     'randint': randint}, 'range': range, 'len': len}, loc)
    bot_class = loc['Bot']
    loc = {}
    exec(game_code, None, loc)
    game_class = loc['Game']
    bot = bot_class()
    game = game_class(bot=bot)
    
    if request.method == "GET":
        game_cond = request.GET.get("game_cond")

        if game_cond == "start":
            print('game start')
            game.start_game()
            state = game.get_state()
            # Не понял, че за приколы с field'ом, поэтому
            # просто возвращаю полученный словарь состояния
            
            request.session['game_state'] = state

            return HttpResponse(json.dumps(state), content_type='json')
        if game_cond == "running":
            print('game running')
            incoming_state = request.GET.get("inner_state")
            game = game_class(state=request.session['game_state'], bot=bot)

            game.user_input(user_action=incoming_state)
            game.bot_move()

            new_state = game.get_state()

            request.session['game_state'] = new_state

            # Раньше победитель приходил со стороны клиента
            # будем требовать, чтобы в состоянии игры всегда было поле 'winner'
            # принимающее одно из значений: 'player', 'bot', 'draw', 'none'
            # это нужно добавить в спички и крестики нолики
            # могу и я добавить, когда проснусь
            # Еще мне показалось, что this_bot.save() в конце функции
            # был лишним. Верни его, если это не так.
            if new_state['winner'] != 'none':
                if new_state['winner'] == 'bot':
                    this_bot.result = 1 + this_bot.result
                    if this_game.leader_score < this_bot.result:
                        this_game.leader_score = this_bot.result
                        this_game.leader = this_bot.creator_name
                        this_game.save()
                    this_bot.save()
                this_bot.all_games_count = 1 + this_bot.all_game_count
                this_bot.save()
            
            return HttpResponse(json.dumps(new_state), content_type='json')

    return render(request, this_game.interface)


@login_required()
def bot_view(request, game_name, creator_name, id):
    return render(request, 'botArena/bot.html', {'game_name': game_name, 'bot_id': id})


@login_required()
def download_bot(request, game_name):
    # content = open("botArena/templates/botArena/" + str(game_name) + "_bot.py").read()
    # return HttpResponse(content, content_type='text/plain', filename='example_bot_code.txt')
    response = HttpResponse(open("botArena/templates/botArena/" + str(game_name) + "_bot.py", 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=example_bot.py'
    return response


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
        post_values['url_source'] = request.POST['url_source']
        post_values['game'] = this_game[0]
        post_values['creator_name'] = request.user.username
        bot = Bot(game=this_game[0], creator_name=request.user.username,
                  url_source=request.POST['url_source'])
        bot.save()
        return HttpResponseRedirect(reverse('botArena:game', args=(name,)))
        # form = BotForm(post_values, request.FILES)
        # print(form)
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, 'Committee Podcast Was Created',
        #                      "alert alert-success alert-dismissible")
        #     # return HttpResponseRedirect(reverse('botArena:home', args=()))
        #
        # # Если форма не валидная
        # else:
        #     form = BotForm()
        #     return render(request, 'botArena/new_game.html', {'game_name': name, 'form': form, 'error_message': "Error "
        #                                                                                                         "occurs"})
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
