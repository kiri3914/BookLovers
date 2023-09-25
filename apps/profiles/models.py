from django.db import models
from django.db.models import Q
from django.urls import reverse

from apps.accounts.models import CustomUser
from apps.books.models import Genre



class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name='user_profile')
    profile_picture = models.ImageField(upload_to='profile/', blank=True, null=True)
    favorite_genres = models.ManyToManyField(Genre, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'profile_id': self.id})

    def __str__(self):
        return self.user.username

    @property
    def get_friends(self):
        user = self.user
        friends_added_by_user = Friend.objects.filter(Q(user=user, status='accepted'))
        friends_added_user = Friend.objects.filter(Q(friend=user, status='accepted'))
        # friends = Friend.objects.filter(
        #     Q(friend=user, status='accepted')
        #     | Q(user=user, status='accepted'))
        friends = (friends_added_by_user | friends_added_user).distinct()
        return friends


class Friend(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='friends')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='user_friends')

    status = models.CharField(max_length=10, choices=(('accepted', 'Принято'),
                                                      ('rejected', 'Отклонено'),
                                                      ('pending', 'Ожидание')),
                              default='pending')

    def __str__(self):
        return f'{self.user.username} - {self.friend.username} ({self.status})'
