from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from .models import Post
from .serializers import PostSerializer

basic_404_handler = lambda request: render(request, "static/404.html", {})

def error_404_view(request, exception):
    data = {}
    return render(request,'static/_404.html', data)

class AllPostsView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all().filter(hidden=False, force_hidden=False)

class SinglePostView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Post.objects.all().filter(id=self.kwargs['id'], hidden=False,
                                         force_hidden=False)
