from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

class Art(models.Model) :
    title = models.CharField(max_length=200, validators = [MinLengthValidator(2,"Title must be greater than 2 characters")])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='art_owned')
    type = models.ForeignKey('Type', on_delete=models.CASCADE, null=False)

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