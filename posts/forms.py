from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from posts.models import Post


class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('url', 'image', 'caption')

	def clean_url(self):
		if self.cleaned_data['url']:
			url = self.cleaned_data['url']
			valid_extensions = ['jpg', 'jpeg', 'png']
			extension = url.rsplit('.', 1)[1].lower()
			if extension not in valid_extensions:
				raise forms.ValidationError('Only images with a .jpg/.jpeg and .png extension are supported')
			return url

	def save(self, force_insert=False, force_update=False, commit=True):
		if self.cleaned_data['url']:
			post = super().save(commit=False)
			image_url = self.cleaned_data['url']
			name = slugify(post.user) + slugify(post.created)
			extension = image_url.rsplit('.', 1)[1].lower()
			image_name = f'{name}.{extension}'
			response = request.urlopen(image_url)
			post.image.save(image_name, ContentFile(response.read()), save=False)
			if commit:
				post.save()
				return post
		super().save(commit=commit)
