from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ProfileForm, DetailForm, UserForm
from .models import Profile, Details

IMAGE_FILE_TYPES = ['png','jpg','jpeg']

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'studentsprofile/login.html')
    else:
        profiles = Profile.objects.filter(user=request.user)
        detail_result = Details.objects.all()
        query = request.GET.get("q")
        if query:
            profiles = profiles.filter(
                Q(email__icontains=query)
            ).distinct()
            detail_result = detail_result.filter(
                Q(detail_result__icontains=query)
            ).distinct()
            return render(request, 'studentsprofile/index.html', {
                'profiles': profiles,
                'details': detail_result,
            })
        else:
            return render(request, 'studentsprofile/index.html', {'profiles': profiles})

def detail(request, profile_id):
    form = DetailForm(request.POST or None, request.FILES or None)
    profile = get_object_or_404(Profile, pk=profile_id)
    if form.is_valid():
        profile = Profile._meta.all()
        for s in profile:
            if s.profile_id == form.cleaned_data.get("profile"):
                context = {
                    'profile': profile,
                    'form': form,
                    'error_message': 'You already added that profile',
                }
                return render(request, 'studentsprofile/create_detail.html', context)
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'studentsprofile/create_detail.html', context)


def create_profile(request):
    if not request.user.is_authenticated():
        return render(request, 'studentsprofile/login.html')
    else:
        form = ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.profile_logo = request.FILES['profile_logo']
            file_type = profile.profile_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'profile': profile,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'studentsprofile/create_profile.html', context)
            profile.save()
            return render(request, 'studentsprofile/detail.html', {'profile': profile})
        context = {
            "form": form,
        }
        return render(request, 'studentsprofile/create_profile.html', context)

def create_detail(request, profile_id):
    form = DetailForm(request.POST or None, request.FILES or None)
    profile = get_object_or_404(Profile, pk=profile_id)
    if form.is_valid():
        profiles_songs = profile.details_set.all()
        for s in profiles_songs:
            if s.profile_id == form.cleaned_data.get("profile_id"):
                context = {
                    'profile': profile,
                    'form': form,
                    'error_message': 'Already added this Profile',
                }
                return render(request, 'studentsprofile/create_detail.html', context)
        details = form.save(commit=False)
        details.profile = profile


def delete_profile(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    profile.delete()
    profile = Profile.objects.filter(user=request.user)
    return render(request, 'studentsprofile/index.html', {'profile': profile})


def delete_detail(request, profile_id, detail_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    details = Details.objects.get(pk=detail_id)
    details.delete()
    return render(request, 'studentsprofile/detail.html', {'profile': profile})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'studentsprofile/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profiles = Profile.objects.filter(user=request.user)
                return render(request, 'studentsprofile/index.html', {'profile': profiles})
            else:
                return render(request, 'studentsprofile/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'studentsprofile/login.html', {'error_message': 'Invalid login'})
    return render(request, 'studentsprofile/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profiles = Profile.objects.filter(user=request.user)
                return render(request, 'studentsprofile/index.html', {'profile': profiles})
    context = {
        "form": form,
    }
    return render(request, 'studentsprofile/register.html', context)

def log_detail(request, profile_id):
    if not request.user.is_authenticated():
        return render(request, 'studentsprofile/login.html')
    else:
        user = request.user
        profile = get_object_or_404(Profile, pk=profile_id)
        return render(request, 'studentsprofile/log_detail.html', {'profile': profile, 'user': user})
