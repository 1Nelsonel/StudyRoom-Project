from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Blog, Room, Topic, Message, User, Curriculam, Comment
from .forms import RoomForm, UserForm


from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm  # add this


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Invalid User')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials!!!')
    context = {'page': page}
    return render(request, 'base/login.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, 'User logged out!!!')
    return redirect('login')


def registerPage(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(
            request, "Unsuccessful registration, please valid credentials!!!")
    form = NewUserForm()
    return render(request=request, template_name="base/register.html", context={"register_form": form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def rooms(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/rooms.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    curriculam = room.curriculam_set.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)

        messages.success(request, 'Message sent!!!')
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants, 'curriculam': curriculam}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST' and request.FILES['image']:
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            image=request.FILES['image'],
        )
        messages.success(request, 'Room created!!!')
        return redirect('create-room')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/create-room.html', context)


@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        messages.warning(request, 'Invalid request!! ')
        return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        messages.success(request, 'Room updated')
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/update-room.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.warning(request, 'Invalid request!!! ')
        return redirect('home')

    if request.method == 'POST':
        room.delete()
        messages.warning(request, 'Room deleted')
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        messages.warning(request, 'Invalid request!! ')
        return redirect('home')

    if request.method == 'POST':
        message.delete()
        messages.warning(request, 'Message deleted')
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            messages.success(request, 'Profile Updated Successfully')
            return redirect('update-user')

    return render(request, 'base/update-user.html', {'form': form})


def blogs(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(body__icontains=q)
    )

    topics = Topic.objects.all()
    blog_count = blogs.count()
    blog_comments = Comment.objects.filter(Q(blog__topic__name__icontains=q))

    context = {'blogs': blogs, 'topics': topics,
               'blog_comments': blog_comments, 'blog_count': blog_count}
    return render(request, 'base/blogs.html', context)


def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    blog_messages = room.message_set.all()
   
    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            blog=blog,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)

        messages.success(request, 'Message sent!!!')
        return redirect('room', pk=room.id)

    context = {'blog': blog, 'blog_messages': blog_messages}
    return render(request, 'base/blogs.html', context)


def contact(request):
    context = {}
    return render(request, 'base/contact.html', context)


def about(request):
    context = {}
    return render(request, 'base/about.html', context)


def service(request):
    context = {}
    return render(request, 'base/service.html', context)


def faq(request):
    context = {}
    return render(request, 'base/faq.html', context)
