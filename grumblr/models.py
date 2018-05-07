from django.db import models

#User class for built-in authentication module
from django.contrib.auth.models import User

class Post(models.Model):
	content = models.CharField(max_length=42)
	time = models.DateTimeField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def get_posts():
		return Post.objects.all().order_by('-time')

	@staticmethod
	def get_new_posts(five_seconds_before,present):
		return Post.objects.filter(time__range=[five_seconds_before,present]).order_by('time')
	
	def get_following_posts(users):
		return Post.objects.filter(user__in=users).order_by('-time')

class Profile(models.Model):
	owner = models.ForeignKey(User)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	age = models.IntegerField(null= True, blank=True)
	follow = models.ManyToManyField(User, related_name='follow', blank=True)
	bio = models.CharField(max_length=420, blank=True)
	photo = models.ImageField(upload_to="images", blank=True)
	follow = models.ManyToManyField(User, related_name='follow', blank=True)

	def __str__(self):
		return (self.first_name + self.last_name)

class Comment(models.Model):
    comment_text = models.CharField(max_length=200)
    comment_time = models.DateTimeField()
    comment_post = models.ForeignKey(Post,null=True)
    comment_user = models.ForeignKey(User,null=True)
    comment_username = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.comment_text

    @staticmethod
    def get_comments():
        return Comment.objects.all().order_by('comment_time')