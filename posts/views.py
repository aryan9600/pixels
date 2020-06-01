from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from posts.forms import PostCreateForm


@login_required
def create_post(request):
	if request.method == 'POST':
		form = PostCreateForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			new_item = form.save(commit=False)
			new_item.user = request.user
			new_item.save()
			messages.success(request, "Post uploaded successfully")
			return redirect(new_item.get_absolute_url())
	else:
		form = PostCreateForm()
	
