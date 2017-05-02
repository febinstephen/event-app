from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from events import views as account_views


urlpatterns = [
    url(r'^$', account_views.IndexView.as_view(), name='index'),
    url(r'^login/$', auth_views.login, {
        'template_name': 'login.html'}, name="user_login"),
    url(r'^logout/$', auth_views.logout_then_login,
        name="user_logout"),
    url(r'^(?P<pk>[0-9]+)/user/$', account_views.ProfileView.as_view(), name='profile'),
    url(r'^register/$', account_views.RegistrationView.as_view(), name='register'),

    # CRUD operations in Event model
    url(r'^(?P<user_id>[0-9]+)/create_event/$',
        account_views.EventCreateView.as_view(), name='create_event'),
    url(r'^event/(?P<pk>[0-9]+)/$',
        account_views.EventDetailView.as_view(), name='event_detail'),
    url(r'^event/(?P<pk>[0-9]+)/delete/$',
        account_views.EventDeleteView.as_view(), name='delete_event'),
    url(r'^event/(?P<pk>[0-9]+)/update/$',
        account_views.EventUpdateView.as_view(), name='update_event'),
    url(r'^(?P<pk>[0-9]+)/events/$',
        account_views.EventListView.as_view(), name='events'),
]
