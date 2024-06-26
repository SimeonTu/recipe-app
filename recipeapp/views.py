from django.shortcuts import render, redirect
from django.contrib import messages
# Django authentication libraries
from django.contrib.auth import authenticate, login, logout
# Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm
from recipes.forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

# define register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()  # Save the form and get the new user instance

            # Authenticate the user programmatically
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # Authenticate the user
            
            if user is not None:
                login(request, user)  # Log the user in

                # Use Django messaging framework to provide a message indicating a successful registration and login
                messages.success(request, 'You have successfully registered and were logged in.')

                return redirect('home')  # Redirect to a home page or dashboard instead of login page
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

# define a function view called login_view that takes a request from user
def login_view(request):
    # initialize:
    # error_message to None
    error_message = None
    # form object with username and password fields
    form = AuthenticationForm()

    # when user hits "login" button, then POST request is generated
    if request.method == 'POST':
        # read the data sent by the form via POST request
        form = AuthenticationForm(data=request.POST)

        # check if form is valid
        if form.is_valid():
            username = form.cleaned_data.get('username')  # read username
            password = form.cleaned_data.get('password')  # read password

            # use Django authenticate function to validate the user
            user = authenticate(username=username, password=password)
            if user is not None:  # if user is authenticated
               # then use pre-defined Django function to login
                login(request, user)

                # use Django messaging framework to provide a message indicating a successfull login to the template
                # in the base.html template, we'll use bootstrap to display a Toast using the message data
                messages.success(request, 'You have successfully logged in.')

                # & send the user to desired page
                return redirect('home')
        else:  # in case of error
            error_message = 'ooops.. something went wrong'  # print error message

    # prepare data to send from view to template
    context = {
        'form': form,  # send the form data
        'error_message': error_message  # and the error_message
    }
    # load the login page using "context" information
    return render(request, 'auth/login.html', context)


# define a function view called logout_view that takes a request from user


def logout_view(request):
    # the use pre-defined Django function to logout
    logout(request)

    # toast indicating a successfull login
    messages.success(request, 'You have successfully logged out.')

    # after logging out go to login form (or whichever page you want)
    return redirect('home')
