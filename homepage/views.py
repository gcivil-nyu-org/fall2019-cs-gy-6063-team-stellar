from django.shortcuts import render, render_to_response
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


userrequest = {
    "request_tpye": "N/a",
    "school": "N/a",
    "department": "N/a",
    "cuisine": "N/a",
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
            userrequest["service_type"] = str(service_form.cleaned_data['serviceSelect'])
            print(userrequest["service_type"])
            return render(request, 'homepage.html')
            # return render_to_response('homepage.html', {
            #     'form': service_form,
            # })
        errordict = {}
        for key in error:
            error_message = error[key]
            messagetext = error_message[0]["message"]
            errordict[key] = messagetext
        errordict["service_form"] = service_form
        return render(request, "service_pop_up.html.html", errordict)
    else:
        print("not post")
        signup_form = forms.TypeOfServiceModalForm()
        return render(request, "service_pop_up.html")

#

def school(request):
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
            type = service_form.cleaned_data['serviceSelect']
            request["service_type"] = type
            return render(request, 'homepage.html')
            # return render_to_response('homepage.html', {
            #     'form': service_form,
            # })
        errordict = {}
        for key in error:
            error_message = error[key]
            messagetext = error_message[0]["message"]
            errordict[key] = messagetext
        errordict["service_form"] = service_form
        return render(request, "service_pop_up.html.html", errordict)
    else:
        print("not post")
        signup_form = forms.TypeOfServiceModalForm()
        return render(request, "service_pop_up.html")
#
# class CuisinetypeView(BSModalCreateView):
#     model = UserRequest
#     template_name = '/templates/cuisine.html'
