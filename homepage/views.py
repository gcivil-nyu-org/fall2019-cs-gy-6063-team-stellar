from django.shortcuts import render, render_to_response
from . import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, "homepage.html")


userrequest = {
    "request_tpye": "N/a",
    "school": "N/a",
    "department": "N/a",
    "cuisine": "N/a",
}


def servicetype(request):
    # import pdb
    # pdb.set_trace()
    print("in service tpye")
    if request.method == "POST":
        print("in post")
        service_form = forms.TypeOfServiceModalForm(request.POST)

        print(request.POST.get("serviceSelect"))
        error = service_form.errors.get_json_data()
        if service_form.is_valid():
            print("service form is valid")
            print(service_form.cleaned_data["serviceSelect"])
            userrequest["service_type"] = str(
                service_form.cleaned_data["serviceSelect"]
            )
            print(userrequest["service_type"])
            return render(request, "homepage.html")
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
        school_form = forms.SchoolModalForm(request.POST)

        print(request.POST.get("school"))
        print(request.POST.get("department"))
        error = school_form.errors.get_json_data()
        if school_form.is_valid():
            print("school form is valid")
            print(school_form.cleaned_data["school"])
            userrequest["school"] = str(school_form.cleaned_data["school"])
            userrequest["department"] = str(school_form.cleaned_data["department"])
            return render(request, "homepage.html")
            # return render_to_response('homepage.html', {
            #     'form': service_form,
            # })
        errordict = {}
        for key in error:
            error_message = error[key]
            messagetext = error_message[0]["message"]
            errordict[key] = messagetext
        errordict["service_form"] = school_form
        return render(request, "service_pop_up.html.html", errordict)
    else:
        print("not post")
        signup_form = forms.TypeOfServiceModalForm()
        return render(request, "service_pop_up.html")



def cuisine(request):
    # import pdb
    # pdb.set_trace()
    print("in service tpye")
    if request.method == "POST":
        print("in post")
        cuisine_form = forms.CuisineModalForm(request.POST)

        print(request.POST.get("cuisine"))
        error = cuisine_form.errors.get_json_data()
        if cuisine_form.is_valid():
            print("cuisine_form is valid")
            print(cuisine_form.cleaned_data["cuisine"])
            userrequest["cuisine"] = str(cuisine_form.cleaned_data["cuisine"])
            return render(request, "homepage.html")
            # return render_to_response('homepage.html', {
            #     'form': service_form,
            # })
        errordict = {}
        for key in error:
            error_message = error[key]
            messagetext = error_message[0]["message"]
            errordict[key] = messagetext
        errordict["service_form"] = cuisine_form
        return render(request, "service_pop_up.html.html", errordict)
    else:
        print("not post")
        signup_form = forms.TypeOfServiceModalForm()
        return render(request, "service_pop_up.html")

#
# class CuisinetypeView(BSModalCreateView):
#     model = UserRequest
#     template_name = '/templates/cuisine.html'
