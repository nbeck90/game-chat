from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import permalink


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    friends = models.ManyToManyField('Profile', symmetrical=True,
                                       related_name='friends', null=True,
                                       blank=True)
    blocking = models.ManyToManyField('Profile', symmetrical=False,
                                      related_name='_blocking', null=True,
                                      blank=True)
    picture = models.ImageField(
        upload_to='photos/', null=True, blank=True, default='photos/link.jpg')
    slug = models.CharField(max_length=32, unique=True, blank=True)

    Created_room = False
    chat_room_name = models.CharField(max_length=64, unique=True, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self):
        self.slug = slugify(self.user.username)
        super(Profile, self).save()

    @permalink
    def get_absolute_url(self):
        return ('profile', None, {'slug': self.slug})

    def friending(self, other_profile):
        return self.friends.add(other_profile)

    def unfriending(self, other_profile):
        return self.friends.remove(other_profile)

    def get_friends(self):
        return Profile.objects.filter(Q(friends=self) & ~Q(blocking=self) & ~Q(_blocking=self))

    def block(self, other_profile):
        return self.blocking.add(other_profile)

    def unblock(self, other_profile):
        return self.block.remove(other_profile)

    def room_status(self, name=None):
        if self.chat_room_name:
            self.Created_room = True
        else:
            self.chat_room_name = name
        return self.Created_room



