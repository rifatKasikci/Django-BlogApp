from django.shortcuts import get_object_or_404, redirect, render, HttpResponse,reverse
from .forms import ArticleForm, CommentForm
from django.contrib import messages
from .models import Article,Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,"index.html")

def articles(request):
    
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request,"articles.html",{"articles":articles})

    articles = Article.objects.all()
    context = {
        "articles":articles
    }
    return render(request,"articles.html",context)

def about(request):
    return render(request,"about.html")

def article_detail(request,id):
    article = get_object_or_404(Article,id=id)
    comments = article.comments.all()
    form = CommentForm()
    form.full_clean()
    return render(request,"articledetail.html",{"article":article,"comments":comments,"form":form})

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles":articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url="user:login")
def add_article(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    context = {
        "form":form
    }
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.content = article.content.replace("<script>","<pre class='prettyprint'>")
        article.content = article.content.replace("</script>","</pre>")
        article.save()
        messages.success(request,"Makale Oluşturuldu!")
        return redirect("index")
    return render(request,"addarticle.html",context)

@login_required(login_url="user:login")
def update_article(request,id):
    article = get_object_or_404(Article,id=id,author=request.user)
    form = ArticleForm(request.POST or None, request.FILES or None,instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.content = article.content.replace("<script>","<pre class='prettyprint'>")
        article.content = article.content.replace("</script>","</pre>")
        article.save()
        messages.success(request,"Makale Güncellendi!")
        return redirect("index")

    context = {
        "form":form
    }
    return render(request,"updatearticle.html",context)  

@login_required(login_url="user:login")
def delete_article(request,id):
    article = get_object_or_404(Article,id=id,author=request.user)
    article.delete()
    messages.success(request,"Makale silindi!")
    return redirect("index")    

def add_comment(request,id):
    article = get_object_or_404(Article, id=id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        new_comment = Comment(comment_author=comment_author,comment_content=comment_content)
        new_comment.article = article
        new_comment.save()
        return redirect(reverse("article:articledetail",kwargs={"id":id}))
    return redirect(reverse("article:articledetail",kwargs={"id":id}))
    # return redirect(reverse("article:articledetail",kwargs={"id":id}))   