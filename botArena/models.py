from django.db import models
import datetime
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Game(models.Model):
    name = models.CharField(max_length=200)
    leader = models.CharField(max_length=200, default='None')
    leader_score = models.IntegerField(default=0)
    source = models.FileField(upload_to='game_src/', default='game_src/none.py')
    interface = models.CharField(max_length=200, default='None')
    description = models.CharField(max_length=40, default='Add description')

    def __str__(self):
        return self.name


class Bot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    creator_name = models.CharField(max_length=200)
    result = models.IntegerField(default=0)
    source = models.FileField(upload_to='bots_src/', default='bots_src/none.py')
    url_source = models.URLField(default='https://spbstubotarena.s3.eu-central-1.amazonaws.com/mindfield.txt')

    def __str__(self):
        return self.creator_name + "_" + str(self.id) + "_" + str(self.game.name)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
