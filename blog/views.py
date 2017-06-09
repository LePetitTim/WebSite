from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
import bs4
import urllib3
import time

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
# Create your views here.

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def getLastDate():
    try:
        fileRead = open("D:\\WebSite\\blog\\static\\txt\\date.txt", "r")
    except FileNotFoundError:
        return 0
    date = fileRead.readlines()[-1]
    return date


def setActualDate():
    fileWrite = open("D:\\WebSite\\blog\\static\\txt\\date.txt", "w")
    fileWrite.write(str(time.gmtime(time.time())[0]) + "/" + str(time.gmtime(time.time())[1]) + "/" + str(
        time.gmtime(time.time())[2]))

def uptodate(request):
    requests = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer+head+neck&retmax=1000000&usehistory=y"
    #fichier = open("D:\\WebSite\\blog\\static\\txt\\pdim.txt", "a")
    #fichier.write("")
    http = urllib3.PoolManager()
    urllib3.disable_warnings()
    tab = []
    fichierread = open("D:\\WebSite\\blog\\static\\txt\\pdim.txt", "r")
    for line in fichierread.readlines():
        tab.append(line.replace('\n', ""))
    lastDate = getLastDate()
    requests = requests + "&mindate=" + str(lastDate) + "&maxdate=2017/06/7"
    requesthttp = http.request("GET", requests)
    texte = str(requesthttp.data)
    soup = bs4.BeautifulSoup(texte, "html.parser")
    fichier = open("D:\\WebSite\\blog\\static\\txt\\pdim.txt", "a")

    string = ""
    for p in soup.find_all('id'):
        if str(p.get_text()) not in tab:
            fichier.write(str(p.get_text()) + "\n")
            string = string + " " +str(p.get_text())
            #return render('test', {'tableau': tableau} )
    setActualDate()
    tableau='1 2 3 4 5 6 7'
    return render(request,'blog/test.html', {'tableau': string })
    #return redirect()

def test(request):
    return render(request,'blog/test.html', {'tableau': []})

def nltk(request):
    return render(request,'blog/nltk.html', {})