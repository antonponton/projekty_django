from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from taggit.managers import TaggableManager

class Art(models.Model) :
    title = models.CharField(max_length=200, validators = [MinLengthValidator(2,"Title must be greater than 2 characters")])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='art_owned')
    type = models.ForeignKey('Type', on_delete=models.CASCADE, null=False)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_owned')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_arts')
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

class Type(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Type must be greater than 1 character")]
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='type_owned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'
    
class Fav(models.Model) :
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('art', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.art.title[:10])