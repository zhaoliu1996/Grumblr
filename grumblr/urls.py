from django.conf.urls import include, url
import grumblr.views

urlpatterns = [

               url('^', include('django.contrib.auth.urls')),
               url(r'^$', grumblr.views.main, name='main'),
               url(r'^global_stream$', grumblr.views.global_stream, name='global_stream'),
               
               url(r'^register$', grumblr.views.register, name='register'),
               url(r'^logout$', grumblr.views.logout_view, name='logout'),
               url(r'^confirm-registration/(?P<user_id>\d+)/(?P<token>[A-Za-z0-9\-]+)$',
                   grumblr.views.confirm_registration, name='confirm'),
               url(r'^delete_post$', grumblr.views.delete_post), # not yet implement
               url(r'^profile/(?P<user_id>\d+)$', grumblr.views.profile, name='profile'),
               url(r'^avatar/(?P<user_id>\d+)$', grumblr.views.get_avatar, name='avatar'),
               url(r'^edit', grumblr.views.edit_profile,name='edit'),
               url(r'^follow/(?P<user_id>\d+)$', grumblr.views.add_following, name='add_following'),
               url(r'^unfollow/(?P<user_id>\d+)$', grumblr.views.remove_following, name='remove_following'),
               url(r'^following', grumblr.views.following_stream, name='following_stream'),
               url(r'^update_new_post$', grumblr.views.get_new_posts_json,name='get_new_posts_json'),
               url(r'^add-comment/(?P<post_id>\d+)$', grumblr.views.add_comment,name='add_comment'),





	
]
