from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from pixels.decorators import ajax_required
from posts.forms import PostCreateForm
from posts.models import Post


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

	return render(request, 'posts/post/edit.html', {'section': 'posts', 'form': form})


@login_required
def post_detail_view(request, id, slug):
	post = get_object_or_404(Post, id=id, slug=slug)
	return render(request, 'posts/post/detail.html', {'section': 'posts', 'post': post})


@require_POST
@login_required
@ajax_required
def like_post(request):
	post_id = request.POST.get('id')
	action = request.POST.get('action')
	if post_id and action:
		try:
			post = Post.objects.get(id=post_id)
			if action == 'like':
				post.liked_by.add(request.user)
			else:
				post.liked_by.remove(request.user)
			return JsonResponse({'status': 'OK'})
		except:
			pass
	return JsonResponse({'status': 'Error'})


@login_required
def posts_list(request):
	posts = Post.objects.all()
	paginator = Paginator(posts, 8)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse('')
		posts = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request, 'posts/post/list_ajax.html', {'section': 'posts', 'posts': posts})
	return render(request,
	              'posts/post/list.html',
	              {'section': 'posts', 'posts': posts})
