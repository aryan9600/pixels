from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts_created', on_delete=models.CASCADE)
	caption = models.CharField(max_length=250, null=True, blank=True)
	slug = models.SlugField(max_length=250, blank=True)
	image = models.ImageField(upload_to='posts/%Y/%m/%d')
	url = models.URLField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True, db_index=True)
	liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
	total_likes = models.PositiveIntegerField(db_index=True, default=0)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.caption)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('posts:detail', args=[self.id, self.slug])
