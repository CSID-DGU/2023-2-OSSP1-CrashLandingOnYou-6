from django.shortcuts import render, redirect
from detail.models import LikeModel
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import CommentModel
from post.models import Recipe
from recommend.models import RecommendModel
from user.models import UserModel


# Create your views here.
def view_detail(request, id):
    me = request.user.id
    target_recipe = Recipe.objects.get(id=id)
    target_like = LikeModel.objects.filter(like_recipe=id)
    target_user_list = [like.like_me_id for like in target_like]

    iLikeThis = me in target_user_list

    all_comment = CommentModel.objects.filter(comment_recipe=id).order_by('-created_at')

    # 타겟 재료 정제 (main_ingredients와 sub_ingredients로 분리)
    target_main_ing = target_recipe.main_ingredients.split(',')  # 메인 재료
    target_sub_ing = target_recipe.sub_ingredients.split(',')  # 서브 재료

    # 타겟 순서 정제
    target_step = target_recipe.cookstep.split(',')
    del target_step[-1]

    try:
        is_update = request.session['commentupdate']
        target_comment = CommentModel.objects.get(id=request.session['mycomment'])
    except:
        is_update = False
        target_comment = ''

    return render(request, 'detail.html', {
        'recipe': target_recipe,
        'like_status': iLikeThis,
        'comment': all_comment,
        'main_ing_list': target_main_ing,
        'sub_ing_list': target_sub_ing,
        'cookstep_list': target_step,
        'reco_list': [],
        'is_update': is_update,
        'target_comment': target_comment
    })


@login_required
def like_post(request, id):
    me = request.user
    recipe = Recipe.objects.get(id=id)
    target_like = LikeModel.objects.filter(like_me=me, like_recipe=recipe)

    if target_like:
        target_like.delete()
    else:
        target_like = LikeModel()
        target_like.like_me = me
        target_like.like_recipe = recipe
        target_like.save()
    return redirect(f'/detail/{id}')


@login_required
def comment_post(request, id):
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        me = request.user
        recipe = Recipe.objects.get(id=id)
        target_comment = CommentModel.objects.filter(comment_me=me, comment_recipe=recipe)
        comment_content = request.POST.get('comment', '')

        makecomment = CommentModel()
        makecomment.comment_me = me
        makecomment.comment_recipe = recipe
        makecomment.comment_content = comment_content
        makecomment.save()
        return redirect(f'/detail/{id}')


@login_required
def comment_delete(request, id):
    all_comment = CommentModel.objects.get(id=id)
    target_recipe = all_comment.comment_recipe.id
    all_comment.delete()
    return redirect(f'/detail/{target_recipe}')


@login_required
def comment_update(request, id):
    commentupdate = True

    all_comment = CommentModel.objects.get(id=id)
    target_recipe = str(all_comment.comment_recipe_id)
    all_comment = str(CommentModel.objects.get(id=id).id)

    request.session['commentupdate'] = commentupdate
    request.session['mycomment'] = all_comment
    return redirect(f'/detail/{target_recipe}')



@login_required
def comment_update_end(request, id):
    if request.method == 'POST':
        all_comment = CommentModel.objects.get(id=id)
        target_recipe = str(all_comment.comment_recipe_id)
        all_comment.comment_content = request.POST.get('comment')
        all_comment.save()
        commentupdate = False
        request.session['commentupdate'] = commentupdate
        return redirect(f'/detail/{target_recipe}')

