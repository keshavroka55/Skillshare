from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Connectionk
from connect.models import models
from django.db.models import Q
from django.contrib import messages


def home(request):
    return render(request,'test.html')

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude self

    # Get current user's accepted connections (friends)
    current_user_connections = Connectionk.objects.filter(
        (Q(from_user=request.user) | Q(to_user=request.user)) & Q(status='accepted')
    )

    # Build a set of connected user IDs (friends of current user)
    current_user_ids = set()
    for conn in current_user_connections:
        if conn.from_user == request.user:
            current_user_ids.add(conn.to_user.id)
        else:
            current_user_ids.add(conn.from_user.id)

    # For each user in the list
    for user in users:
        # Get their accepted connections
        user_connections = Connectionk.objects.filter(
            (Q(from_user=user) | Q(to_user=user)) & Q(status='accepted')
        )

        # Build a set of IDs for that user's connections
        user_connection_ids = set()
        for conn in user_connections:
            if conn.from_user == user:
                user_connection_ids.add(conn.to_user.id)
            else:
                user_connection_ids.add(conn.from_user.id)

        # Fix: Typo in variable name (was conneted_user_ids)
        user.is_connected = user.id in current_user_ids  # ✅ Check if this user is already a friend

        # Mutual = common IDs between my friends and their friends
        user.mutual_connections_count = len(current_user_ids & user_connection_ids)

    return render(request, 'user_list.html', {'users': users})


@login_required
def send_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    connection, created = Connectionk.objects.get_or_create(from_user=request.user, to_user=to_user)
    if created:
        messages.success(request, f"Connection request sent to {to_user.username}!")
    else:
        messages.info(request, f"You've already sent a connection request to {to_user.username}.")

    return redirect('user_list')

@login_required
def handle_request(request, connection_id, action):
    connection = get_object_or_404(Connectionk, id=connection_id)
    if connection.to_user == request.user:
        if action == 'accept':
            connection.status = 'accepted'
        elif action == 'decline':
            connection.status = 'declined'
        connection.save()
    return redirect('received_requests')

@login_required
def received_requests(request):
    requests = Connectionk.objects.filter(to_user=request.user, status='pending')
    return render(request, 'receive_request.html', {'requests': requests})


# to view your connections

@login_required
def my_connections_view(request):
    user = request.user
    connections = Connectionk.objects.filter(
        Q(from_user=user) | Q(to_user=user),
        status='accepted'
    )

    # To get the connected user (not the logged-in one)
    connected_users = []
    for conn in connections:
        if conn.from_user == user:
            connected_users.append(conn.to_user)
        else:
            connected_users.append(conn.from_user)

    return render(request, 'my_connections.html', {
        'connected_users': connected_users
    })

