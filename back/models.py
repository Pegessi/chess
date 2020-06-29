from django.db import models


# Create your models here.
class Avatar(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    path = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'avatar'
        unique_together = (('id', 'path'),)


class Career(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    allgame = models.IntegerField(db_column='allGame')  # Field name made lowercase.
    wingame = models.IntegerField(db_column='winGame')  # Field name made lowercase.
    lossgame = models.IntegerField(db_column='lossGame')  # Field name made lowercase.
    winper = models.FloatField(db_column='winPer')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'career'


class Friend(models.Model):
    id = models.CharField(max_length=45)
    fri = models.CharField(max_length=45)
    recentdate = models.CharField(max_length=45)
    date = models.CharField(primary_key=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'friend'


class Message(models.Model):
    send = models.CharField(primary_key=True, max_length=45)
    receive = models.CharField(max_length=45)
    content = models.CharField(max_length=45)
    date = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'message'
        unique_together = (('send', 'receive', 'date'),)


class Passwar(models.Model):
    red = models.CharField(max_length=45)
    black = models.CharField(max_length=45)
    date = models.CharField(primary_key=True, max_length=45)
    win = models.CharField(max_length=45)
    runtime = models.CharField(db_column='runTime', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'passwar'


class Request(models.Model):
    send = models.CharField(max_length=45)
    receive = models.CharField(max_length=45)
    date = models.CharField(primary_key=True, max_length=45)
    flag = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'request'


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    password = models.CharField(max_length=45)
    sex = models.CharField(max_length=45)
    age = models.CharField(max_length=45)
    birth = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    level = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'user'


class War(models.Model):
    userid = models.CharField(primary_key=True, max_length=45)
    level = models.CharField(max_length=45)
    flag = models.CharField(max_length=45)
    date = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'war'


class Warhis(models.Model):
    userred = models.CharField(db_column='userRed', primary_key=True, max_length=45)  # Field name made lowercase.
    userblack = models.CharField(db_column='userBlack', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    date = models.CharField(max_length=45)
    winner = models.CharField(max_length=45)
    picpath = models.CharField(max_length=45)
    flag = models.CharField(max_length=45)  # Field name made lowercase.
    mesdata = models.TextField(db_column='mesData', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'warhis'
        unique_together = (('userred', 'date'),)
