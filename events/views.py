from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


from events.forms import UserForm, UserProfileForm, EventForm
from events.models import Event, UserProfile

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        return context


class ProfileView(TemplateView):

    template_name = "profile.html"

    def get_context_data(self, pk, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        user = get_object_or_404(User, pk=pk)
        if user.is_authenticated():
            pic = get_object_or_404(UserProfile, user=user)
        if pic:
            picture_url = pic.picture.url
            context['picture_url'] = picture_url
        return context


class RegistrationView(FormView):
    """ Registration Logic"""

    model = User
    form_class = UserForm
    second_form_class = UserProfileForm
    template_name = 'registration_crispy.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        # context['active_client'] = True
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        # context['active_client'] = True
        return context

    def get(self, request, *args, **kwargs):
        super(RegistrationView, self).get(request, *args, **kwargs)
        form = self.form_class
        form2 = self.second_form_class
        return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST, request.FILES)

        if form.is_valid() and form2.is_valid():
            userdata = form.save(commit=False)
            userdata.set_password(userdata.password)
            # used to set the password, but no longer necesarry
            userdata.save()
            userprofiledata = form2.save(commit=False)
            userprofiledata.user = userdata
            userprofiledata.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2))

    def get_success_url(self):
        return reverse('index')


class EventCreateView(CreateView):
    """ Creates an event"""
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.save()
        return super(CreateView, self).form_valid(form)


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"


class EventListView(ListView):
    model = Event
    paginate_by = 5
    template_name = "event_list.html"

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset()
        return qs.filter(user=self.request.user)


class EventUpdateView(UpdateView):
    model = Event
    fields = ['date', ]
    template_name = "event_form.html"


class EventDeleteView(DeleteView):
    """"""
    model = Event
    template_name = "event_confirm_delete.html"
    success_url = reverse_lazy('index')

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset()
        return qs.filter(user=self.request.user)
