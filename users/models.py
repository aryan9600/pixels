from django.conf import settings
from django.db import models


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	dob = models.DateTimeField(blank=True, null=True)
	profile_picture = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

	def __str__(self):
		return f"Profile of {self.user.username}"
