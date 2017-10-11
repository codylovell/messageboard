# from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post
from django.contrib.auth.decorators import login_required #Requires user to be logged in to view certain pages

def home(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})
	
def board_topics(request, pk):
	# If board doesn't exist, raise a 404 instead of 500. Test created for this as well.
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user  # <- here
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user  # <- and here
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
	
def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})
	
@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
	
# def about(request):
    # # do something...
    # return render(request, 'about.html')

# def about_company(request):
    # # do something else...
    # # return some data along with the view...
    # return render(request, 'about_company.html', {'company_name': 'Simple Complex'})