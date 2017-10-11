# from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from .forms import NewTopicForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post

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

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
	
# def about(request):
    # # do something...
    # return render(request, 'about.html')

# def about_company(request):
    # # do something else...
    # # return some data along with the view...
    # return render(request, 'about_company.html', {'company_name': 'Simple Complex'})