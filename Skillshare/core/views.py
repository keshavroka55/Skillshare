from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import UserProfile,Chat,Follow
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm,ChartForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q




# Create your views here.
def core_page(request):
    return render (request,'core_page.html')

@login_required
def settings(request):
    return render (request,'profile/setting.html')

@login_required
def profile(request):
    return render (request,'profile.html')


def SignUp_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request,'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile/profile.html', {
        'user': request.user,
    })

@login_required
def my_profile_view(request):
    return redirect('view_profile', user_id=request.user.id)


@login_required
def inspect_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    followers = Follow.objects.filter(following=profile_user)
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    
    return render(request, 'profile/profile_view.html', {
        'profile_user': profile_user,
        'followers': followers,
        'is_following': is_following
    })


@login_required
def profile_edit(request):
    # Ensure the user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')  # or another profile view

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'profile/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

# password change 
def custom_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password was changed successfully!')
            # return redirect('change')  # your custom success page
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'profile/change_password.html', {'form': form})

@login_required
def send_message(request, user_id):
    receiver = get_object_or_404(User,id = user_id) # error: missing one positional argument.
    
    messages = Chat.objects.filter(
        sender__in= [request.user,receiver],
        receiver__in= [request.user,receiver]
    ).order_by('timestamp')
    if request.method == 'POST':
        form = ChartForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False) # create a message object but not save in the database.
            msg.sender = request.user
            msg.receiver = receiver 
            msg.save()
            return redirect('send',user_id=receiver.id)
    else:
        form = ChartForm()
    users = User.objects.exclude(id=request.user.id)
    return render (request, 'chat/send_message.html',{'users':users,'form': form,'messages':messages,'receiver':receiver,'user':request.user})

@login_required
def select_user_to_chat(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/select_user.html', {'users': users})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def search_profile(request):
    query = request.GET.get('q')
    results = []

    if query:
        query = query.strip().lower()

        all_profiles = UserProfile.objects.all()
        print("---- ALL PROFILES ----")
        for profile in all_profiles:
            print(profile.user, "| skills:", profile.skills_i_have)

        results =  UserProfile.objects.filter(
            Q(skills_i_have__icontains=f'{query},') |
            Q(skills_i_have__icontains=f', {query}') |
            Q(skills_i_have__icontains=f', {query},') |
            Q(skills_i_have__iexact=query)

    )

    if request.user.is_authenticated:
        results = results.exclude(user= request.user) # exclude the search user.
    return render(request,'search_profile.html',{'results':results,'query':query})


