from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.text import slugify

from django.conf import settings as conf
import re
import hmac
import base64
import hashlib
from time import time
from uuid import uuid4

def gen_uuid():
    return seed_uuid(uuid4().hex)

def seed_uuid(sessionid, length=32):
    hex = hashlib.md5(conf.SECRET_KEY + str(sessionid)).hexdigest()
    uid = hex.encode('base64')
    uid = re.sub("[^A-Z0-9]", "", uid.upper())
    if length < 4:
        length = 4
    if length > 128:
        length = 128
    while (len(uid) < length):
        uid = uid + seed_uuid(sessionid, 22)
    return uid[0:length]

def gen_secret_key():
    salt = seed_uuid(64)
    p = {'time': str(time()), 'salt': salt, 'secret': conf.SECRET_KEY}
    digest = hmac.new(urlencode(p), salt, digestmod=hashlib.sha256).hexdigest()
    return quote_plus(base64.b64encode(digest).strip('=='))

class ModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self._select_related = kwargs.pop('select_related', None)
        self._prefetch_related = kwargs.pop('prefetch_related', None)
        super(ModelManager, self).__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(ModelManager, self).get_queryset(*args, **kwargs).\
             exclude(deleted__isnull=False)
        if self._select_related:
            qs = qs.select_related(*self._select_related)
        if self._prefetch_related:
            qs = qs.prefetch_related(*self._prefetch_related)
        return qs

    def deleted(self, *args, **kwargs):
        qs = super(ModelManager, self).get_queryset(*args, **kwargs).\
            exclude(deleted__isnull=True)
        if self._select_related:
            qs = qs.select_related(*self._select_related)
        if self._prefetch_related:
            qs = qs.prefetch_related(*self._prefetch_related)
        return qs

    def delete(self):
        self.get_queryset().update(deleted=timezone.now())

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True, editable=False)

    objects = ModelManager()

    class Meta:
        abstract = True

class PasswordReset(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    token = models.CharField(
        max_length=128, unique=True, default=gen_secret_key, editable=False)
    is_active = models.BooleanField(default=True)

def profile_photo_upload(instance, filename):
    prefix = 'profiles/user-%s-%s-%s'
    return prefix % (
        instance.pk,
        slugify(instance.user.first_name),
        filename)

class Profile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile')
    photo = models.ImageField(
        blank=True, null=True, upload_to=profile_photo_upload)
    birthday = models.DateField(null=True)
    phone = models.CharField(null=True, max_length=11)

    def __str__(self):
        return self.user.email

class Position(BaseModel):
    name = models.CharField(max_length=45)

class State(BaseModel):
    name = models.CharField(max_length=45)

class City(BaseModel):
    state = models.ForeignKey(State, related_name='cities')
    name = models.CharField(max_length=45)

def logo_upload(instance, filename):
    prefix = 'teams/logo-%s-%s-%s'
    return prefix % (
        instance.pk,
        slugify(instance.name),
        filename)

class Team(BaseModel):
    city = models.ForeignKey(City, related_name='teams')
    logo = models.ImageField(
        blank=True, null=True, upload_to=logo_upload)
    name = models.CharField(max_length=50)
    foundation = models.DateField(null=True)
    president = models.CharField(max_length=50)

class Athlete(BaseModel):
    profile = models.ForeignKey(Profile)
    team = models.ForeignKey(Team)
    position = models.ForeignKey(Position)

class Arena(BaseModel):
    name = models.CharField(max_length=50)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

class Match(BaseModel):
    arena = models.ForeignKey(Arena, related_name='matches')
    home_team = models.ForeignKey(Team, related_name='home_matches')
    visitor_team = models.ForeignKey(Team, related_name='visitor_matches')
