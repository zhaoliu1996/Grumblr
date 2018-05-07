from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db import transaction
#Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

#Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

#forms
from grumblr.forms import *
from django.contrib.auth.forms import UserCreationForm

#Used to get time
import datetime
from django.utils import timezone

#for requeset
from django.http import HttpResponse, Http404

#for pictures
from mimetypes import guess_type

#for mails
from django.core.mail import send_mail

#for token email registration
from django.contrib.auth.tokens import default_token_generator

from grumblr.models import *

from .tokens import account_activation_token



def main(request):

	if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
		form = LoginForm(request.POST)

        # Check if the form is valid:
		if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect(global_stream)

			else:   
				
				return render(request, 'grumblr/login.html', {'form': form})


    # If this is a GET (or any other method) create the default form.
	else:
		form = LoginForm()
	print ('dd')
	return render(request, 'grumblr/login.html', {'form': form})


@login_required
def global_stream(request):
	items = Post.objects.all().order_by('-time')
	if request.method == 'POST':
		form = PostForm(request.POST)

		if form.is_valid() and len(form.cleaned_data['content'])<=42:
			new_post = Post.objects.create(content=form.cleaned_data['content'], time=timezone.now(), user=request.user)
			items = Post.objects.all().order_by('-time')

	my_profile = get_object_or_404(Profile, owner=request.user)
	context = {'items':items, 'form':PostForm(), 'profile':my_profile}
	return render(request, 'grumblr/global_stream.html', context)

@login_required
def profile(request, user_id):
	context = {}
	me=False
	following=None
	thisuser = get_object_or_404(User, id=user_id)
	current_profile = get_object_or_404(Profile, owner=thisuser)
	my_profile = get_object_or_404(Profile, owner=request.user)
	if thisuser==request.user:
		me = True
	try:
		following_user = my_profile.follow.all()
	except:
		following_user=[]
	if thisuser in following_user:
		following = True
	else:
		following = False
	post = Post.objects.filter(user=thisuser).order_by('-time')
	context['me'] = me
	context['following'] = following
	context['post'] = post
	context['profile'] = current_profile
	context['thisuser'] = thisuser
	return render(request, 'grumblr/profile.html', context)


@login_required
def delete_post(request):
	errors = []

	#  try to delete the item if an post mathcing the id
	try:
		post_to_delete = Post.objects.get(id=id, user=request.user)
		post_to_delete.delete()
	except ObjectDoesNotExist:
		errors.append('The post you want to delete do not exist')

	items = Post.objects.filter(user=request.user)
	context = {'items' : items, 'errors' : errors}
	return render(request, 'grumblr/global_stream.html', context)


@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == 'GET':
        my_profile = get_object_or_404(Profile, owner=request.user)
        form = ProfileForm(instance=my_profile) 
        context = {'form':form,'profile':my_profile}  
        return render(request, 'grumblr/edit_profile.html', context)
    my_profile = Profile.objects.select_for_update().get(owner=request.user)
    form = ProfileForm(request.POST, request.FILES, instance=my_profile)
    if not form.is_valid():
        context = {'form':form,'profile':my_profile} 
        return render(request, 'grumblr/edit_profile.html', context)
    form.save()
    my_profile.save()
        #after set new password, need to re-login.
    context = {'form':form,'profile':my_profile} 
    print("nv")
    return render(request, 'grumblr/edit_profile.html', context)




def register(request):
	context={}
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			firstname = form.cleaned_data.get('firstname')
			lastname = form.cleaned_data.get('lastname')
			email = form.cleaned_data.get('email')
			
			user = authenticate(username=username, password=raw_password)

			login(request, user)
			user.email = email
			user.save()

			token = default_token_generator.make_token(user)

			email_body="""
			Welcome to grumblr! Please click the link below to verify your email address and 
			complete the registration of your account: 

			http://%s%s
			"""%(request.get_host(),reverse('confirm',args=(user.id,token)))
			send_mail(subject="Verify your email address",
						message=email_body,
						from_email="zhao666666666@gmail.com",
						recipient_list=[user.email])
			context['email']=form.cleaned_data['email']



			new_profile = Profile(first_name = firstname, 
                                  last_name = lastname,
                                  owner = user)
			new_profile.save()
			return HttpResponse('Please confirm your email address to complete the registration')
	
	context['form'] = RegisterForm()
	return render(request, 'grumblr/registration.html', context)

def confirm_registration(request, user_id, token):
	user = get_object_or_404(User, id=user_id)
	if not default_token_generator.check_token(user, token):
		raise Http404
	user.is_active = True
	user.save()
	return redirect(global_stream)


@login_required
@transaction.atomic
def add_following(request, user_id):
	my_profile = get_object_or_404(Profile, owner=request.user)
	add_following_user = get_object_or_404(User, id=user_id)
	if my_profile.follow.filter(id=user_id).count()==0:
		my_profile.follow.add(add_following_user)
		my_profile.save()
	return redirect(reverse('profile', kwargs={'user_id': user_id}))

@login_required
@transaction.atomic
def remove_following(request, user_id):
	my_profile = get_object_or_404(Profile, owner=request.user)
	remove_following_user = get_object_or_404(User, id=user_id)
	if my_profile.follow.filter(id=user_id).count()==1:
		my_profile.follow.remove(remove_following_user)
		my_profile.save()
	return redirect(reverse('profile', kwargs={'user_id': user_id}))

@login_required
@transaction.atomic
def following_stream(request):
	my_profile = get_object_or_404(Profile, owner=request.user)
	following = my_profile.follow.all()
	context = {'post': Post.objects.filter(user__in=following).order_by('-time')}
	context['profile'] = my_profile
	return render(request, 'grumblr/following_stream.html', context)

@login_required
@transaction.atomic
def get_avatar(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_profile = get_object_or_404(Profile, owner=user)
    if not current_profile.photo:
        current_profile.photo='grumblr/media/avatar1.png'
        print("1")
        return HttpResponse(current_profile.photo)
    content_type = guess_type(current_profile.photo.name)
    return HttpResponse(current_profile.photo, content_type=content_type)

#update new post without refresh.
@login_required
@transaction.atomic
def get_new_posts_json(request):
    time_now = timezone.now()
    five_seconds_before = time_now-datetime.timedelta(seconds=5)
    update_posts = Post.get_new_posts(five_seconds_before,time_now)
    response_text = serializers.serialize('json',update_posts)
    return HttpResponse(response_text,content_type='application/json')

@login_required
@transaction.atomic
def add_comment(request,post_id):
    current_post = get_object_or_404(post, id=post_id)
    form = Comment_form(request.POST)
    if not form.is_valid():
        raise Http404
    else:
        new_comment=Comment(comment_text=request.POST['comment_text'],comment_user=request.user,comment_time=timezone.now(),
                            comment_post=current_post,comment_username=request.user.username)
        new_comment.save()
        response_text = serializers.serialize('json',[new_comment,])
    return HttpResponse(response_text,content_type='application/json')


@login_required
def logout_view(request):
	logout(request)
	return redirect(main)



