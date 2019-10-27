from django.shortcuts import render
from django.views.generic import UpdateView, ListView, FormView
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import UserRequest
from .forms import ServiceForm
from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    return render(request, "homepage.html")


# class UserRequestView(BSModalCreateView):
#     template_name ='/template/service_pop_op.html'


class ServicetypeView(BSModalCreateView):
    model = UserRequest
    form_class = ServiceForm
    template_name ='/templates/service.html'
    success_message = 'service was chosen.'
    success_url = reverse_lazy('index')



class SchoolView(BSModalCreateView):

    model = UserRequest
    template_name ='/templates/school.html'

class CuisinetypeView(BSModalCreateView):
    model = UserRequest
    template_name = '/templates/cuisine.html'

# class ItemListView(ListView):
#     model = UserRequest
#     template_name = '/item_list.html'
#
#     def get_queryset(self):
#         return UserRequest.objects.all()
#
#
# class ItemUpdateView(UpdateView):
#     model = UserRequest
#     form_class = UserRequestForm
#     template_name = 'myapp/item_edit_form.html'
#
#     def dispatch(self, *args, **kwargs):
#         self.item_id = kwargs['pk']
#         return super(ItemUpdateView, self).dispatch(*args, **kwargs)
#
#     def form_valid(self, form):
#         form.save()
#         item = UserRequest.objects.get(id=self.item_id)
#         return HttpResponse(render_to_string('/item_edit_form_success.html', {'item': item}))