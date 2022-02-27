from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta():
        model = Article
        fields = ["title","content","article_image"]

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        widgets = {
            'comment_content': forms.Textarea(attrs={'cols': 80, 'rows': 5})
        }
        fields = ["comment_author","comment_content"]