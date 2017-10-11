"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from boards import views
#Give alias to avoid clashing with boards views name
from accounts import views as accounts_views

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),

    url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
    url(r'^admin/', admin.site.urls),
]

	
	# url(r'^about/$', views.about, name='about'), # Ensure simple URLs like 'about' go before super-inclusive names like the one below. Someone could sign up with the name 'about' that would match first since it's looking for users right off the root URL.
	# url(r'^(?P<username>[\w.@+-]+)/$', views.user_profile, name='user_profile'),
	# url(r'^about/company/$', views.about_company, name='about_company'),
    # url(r'^about/author/$', views.about_author, name='about_author'),
    # url(r'^privacy/$', views.privacy_policy, name='privacy_policy'),

#  Sidenote: Consider creating unique paths for users, like u/david on reddit or /@david on Twitter

# This is the anatomy of the url function:

# def url(regex, view, kwargs=None, name=None):
     # ...
# regex: A regular expression for matching URL patterns in strings. Note that these regular expressions do not search GET or POST parameter. In a request to http://127.0.0.1:8000/boards/?page=2 only /boards/ will be processed.

# view: A view function used to process the user request for a matched URL. It also accepts the return of the django.conf.urls.include function, which is used to reference an external urls.py file. You can, for example, use it to define a set of app specific URLs, and include it in the root URLconf using a prefix. We will explore more on this concept later on.

# kwargs: Arbitrary keyword arguments that’s passed to the target view. It is normally used to do some simple customization on reusable views. We don’t use it very often.

# name: A unique identifier for a given URL. This is a very important feature. Always remember to name your URLs. With this, you can change a specific URL in the whole project by just changing the regex. So it’s important to never hard code URLs in the views or templates, and always refer to the URLs by its name.