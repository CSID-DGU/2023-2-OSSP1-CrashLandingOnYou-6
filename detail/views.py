#from urllib import request
from django.shortcuts import render, redirect
from detail.models import LikeModel
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import CommentModel
from post.models import Recipe
from recommend.models import RecommendModel
from user.models import UserModel
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render, get_object_or_404
from .models import Recipe, LikeModel, CommentModel

def view_detail(request, id):
    # 현재 로그인한 사용자의 ID를 가져옵니다.
    user_id = request.user.id if request.user.is_authenticated else None

    # 선택한 레시피를 가져옵니다.
    target_recipe = get_object_or_404(Recipe, id=id)

    # 해당 레시피에 대한 좋아요 정보를 가져옵니다.
    target_like = LikeModel.objects.filter(like_recipe=id)
    target_user_list = [like.like_me_id for like in target_like]

    # 사용자가 해당 레시피를 좋아하는지 확인합니다.
    user_likes_this = user_id in target_user_list

    # 해당 레시피에 대한 모든 댓글을 가져옵니다.
    all_comments = CommentModel.objects.filter(comment_recipe=id).order_by('-created_at')

    # 레시피의 재료와 조리 순서를 분리합니다.
    target_main_ingredients = target_recipe.main_ingredients.split(',') if target_recipe.main_ingredients else []
    target_sub_ingredients = target_recipe.sub_ingredients.split(',') if target_recipe.sub_ingredients else []
    target_cook_steps = target_recipe.cookstep.split(',') if target_recipe.cookstep else []

    # 유사 레시피 찾기
    clicked_main_ingredients = set(target_recipe.main_ingredients.split(', '))
    clicked_classification = target_recipe.classification
    clicked_sub_ingredients = set(target_recipe.sub_ingredients.split(', '))

    filtered_recipes = Recipe.objects.filter(
        main_ingredients__in=clicked_main_ingredients,
        classification=clicked_classification
    ).exclude(id=id)

    def calculate_similarity(recipe):
        recipe_sub_ingredients = set(recipe.sub_ingredients.split(', '))
        return len(clicked_sub_ingredients.intersection(recipe_sub_ingredients))

    sorted_recipes = sorted(filtered_recipes, key=calculate_similarity, reverse=True)
    top_similar_recipes = sorted_recipes[:5]

    context = {
        'recipe': target_recipe,
        'like_status': user_likes_this,
        'comment': all_comments,
        'main_ingredients_list': target_main_ingredients,
        'sub_ingredients_list': target_sub_ingredients,
        'cook_steps_list': target_cook_steps,
        'similar_recipes': top_similar_recipes
    }

    return render(request, 'detail.html', context)



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