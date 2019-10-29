from django.shortcuts import render
from . import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, "homepage.html")
#
# def user_service(request):
#     if request.method == 'POST':
#         form = forms.TypeOfServiceModalForm(request.POST)
#         if form.is_valid():
#             return
#


request = {
    "service_type" : "N/A",
    "school" : "N/a",
    "department" : "N/a",
    "cuisine" : "N/a",
}

# class Index(generic.ListView):
#     model = UserRequest
#     context_object_name = 'request'
#     template_name = 'homepage.html'


def servicetype(request):
    # import pdb
    # pdb.set_trace()
    print("in service tpye")
    if request.method == "POST":
        print("in post")
        service_form = forms.TypeOfServiceModalForm(request.POST)

        print(request.POST.get('serviceSelect'))
        error = service_form.errors.get_json_data()
        if service_form.is_valid():
            print("service form is valid")
            print(service_form.cleaned_data['serviceSelect'])
            return HttpResponseRedirect(reverse('serviceSelect'))
            # return HttpResponse(
            #     "We have received the service type "
            # )
        errordict = {}
        for key in error:
            error_message = error[key]
            messagetext = error_message[0]["message"]
            errordict[key] = messagetext
        errordict["service_form"] = service_form
        return render(request, "service.html", errordict)
    else:
        print("not post")
        signup_form = forms.TypeOfServiceModalForm()
        return render(request, "service.html")

#
#
#
# class SchoolView(BSModalCreateView):
#     model = UserRequest
#     template_name ='/templates/school.html'
#     success_message = 'school was chosen.'
#     success_url = reverse_lazy('index')
#
# class CuisinetypeView(BSModalCreateView):
#     model = UserRequest
#     template_name = '/templates/cuisine.html'
