from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'ts', 'author', 'title', 'text', 'use_img', 'image_url')

    def get_author(self, obj):
        return obj.author.username

    def get_image_url(self, obj):
        if obj.use_img:
            return obj.image_url
        else:
            return None
