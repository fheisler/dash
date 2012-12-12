from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user =      models.OneToOneField(User)
    zipcode =   models.CharField(max_length=5, null=True, blank=True)
    interests = models.CharField(max_length=400, null=True, blank=True)

    def list_interests(self):
        if self.interests is not None:
            return self.interests.split(",")
        else:
            return []

    '''
    def interests(self):
        interests = [i.text for i in self.interest_set.all()]
        return interests
    #TODO: specify default interests
    '''

'''
class Interest(models.Model):
    text =  models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(UserProfile, null=True, blank=True)
    def __unicode__(self):
        return self.text
'''

'''
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
'''
def create_user_profile(sender, **kwargs):
    u = kwargs["instance"]
    if not UserProfile.objects.filter(user=u):
        UserProfile(user=u).save()
post_save.connect(create_user_profile, sender=User)
