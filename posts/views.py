import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from actions.utils import create_action
from pixels.decorators import ajax_required
from posts.forms import PostCreateForm
from posts.models import Post

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


@login_required
def create_post(request):
	if request.method == 'POST':
		form = PostCreateForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			new_item = form.save(commit=False)
			new_item.user = request.user
			new_item.save()
			create_action(request.user, 'uploaded post', new_item)
			messages.success(request, "Post uploaded successfully")
			return redirect(new_item.get_absolute_url())
	else:
		form = PostCreateForm()

	return render(request, 'posts/post/edit.html', {'section': 'posts', 'form': form})


@login_required
def post_detail_view(request, id, slug):
	post = get_object_or_404(Post, id=id, slug=slug)
	total_views = r.incr(f'image:{post.id}:views')
	r.zincrby('image_ranking', 1, image.id)
	return render(request, 'posts/post/detail.html', {'section': 'posts', 'post': post, 'total_views': total_views})


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
				create_action(request.user, 'likes', post)
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
	return render(request, 'posts/post/list.html', {'section': 'posts', 'posts': posts})


@login_required
def image_ranking(request):
    # get image ranking dictionary
    post_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    post_ranking_ids = [int(id) for id in post_ranking]
    # get most viewed images
    most_viewed = list(Post.objects.filter(
                           id__in=post_ranking_ids))
    most_viewed.sort(key=lambda x: post_ranking_ids.index(x.id))
    return render(request,
                  'posts/post/ranking.html',
                  {'section': 'images',
                   'most_viewed': most_viewed})