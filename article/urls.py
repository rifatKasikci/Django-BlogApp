from django.contrib import admin
from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path('dashboard/',views.dashboard,name="dashboard"),
    path('add/',views.add_article,name="addarticle"),
    path('detail/<int:id>',views.article_detail,name="articledetail"),
    path('update/<int:id>',views.update_article,name="updatearticle"),
    path('delete/<int:id>',views.delete_article,name="deletearticle"),
    path('',views.articles,name="articles"),
    path('comment/<int:id>',views.add_comment,name="addcomment")
]