from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from .models import FormTemplate, User, Question

# Create your views here.
def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect username or password.')
            return redirect('index')
    else:
        return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address')
            return redirect('signup')

        if password != confirmpassword:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, ', '.join(e.messages))
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')

        user = User.objects.create_user(username=email, email=email, password=password)
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('index')

    return render(request, 'signup.html')

@login_required
def usersettings(request):
    return render(request, 'usersettings.html')

@login_required
def editform(request, form_id):
    form_template = get_object_or_404(FormTemplate, id=form_id)
    if form_template.user != request.user: # Only the forms attached to the user can be accessed
        return HttpResponseForbidden("You don't have permission to access this form.")

    questions = Question.objects.filter(template=form_template)

    question_list = []
    for question in questions:
        question_list.append(question.question)

        return render(request, 'editform.html', {'form_template': form_template, 'questions': question_list})



@login_required
def dashboard(request):
    form_templates = FormTemplate.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'form_templates': form_templates})

@login_required
def create_default_form_template(request):
    if request.method == 'POST':
        title = 'Untitled Form'
        body = 'Form description'
        user = request.user
        FormTemplate.objects.create(title=title, body=body, user=user)
        return redirect('dashboard')
    return render(request, 'dashboard.html')

@login_required
def edit_template_title(request, form_id):
    form_template = get_object_or_404(FormTemplate, id=form_id)
    if form_template.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this form.")

    return render(request, 'editform.html', {'form_template': form_template, 'editing': True})

@login_required
def save_template_title(request, form_id):
    form_template = get_object_or_404(FormTemplate, id=form_id)
    if form_template.user != request.user:
        return HttpResponseForbidden("You don't have permission to save this form.")

    if request.method == 'POST':
        form_template.title = request.POST.get('title')
        form_template.save()
        return redirect('editform', form_id=form_template.id)

    return HttpResponseBadRequest("Invalid request method.")

@login_required
def create_question(request, form_id):
    if request.method == 'POST':
        title = 'New Question'
        template = get_object_or_404(FormTemplate, id=form_id)
        Question.objects.create(template=template, question=title)
        return redirect('editform', form_id=form_id)
    return redirect('editform', form_id=form_id)