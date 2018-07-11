from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    ts = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    text = models.TextField()
    use_img = models.BooleanField(default=False)
    image_url = models.URLField(max_length=200, null=True, blank=True, default=None)
    hidden = models.BooleanField(default=False)
    force_hidden = models.BooleanField(default=False)
    force_readonly = models.BooleanField(default=False)

    def __str__(self):
        return "Post #{0} | {1}".format(self.id, self.title)

    def __repr__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        if self.image_url == None:
            self.use_img = False
        else:
            self.use_img = True

        super(Post, self).save(*args, **kwargs)
