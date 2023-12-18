from django.core.exceptions import ObjectDoesNotExist
from .models import Recipe, Timecate, Diffcate
from detail.models import LikeModel
from post.models import Recipe
from recommend.models import RecommendModel
from user.models import UserModel
from django.core.paginator import Paginator
from django.shortcuts import render,redirect 
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/main')
    else:
        return redirect('/signin')


def view_main(request):
    try:
        target_reco = RecommendModel.objects.get(id=request.session['latestRecipe'])
    except:
        target_reco = RecommendModel.objects.get(id=2)

    try:
        reco_main_id = int((target_reco.reco1.strip('()').split(',')[0])) + 1
        reco_main = Recipe.objects.get(id=reco_main_id)
        # main_ingredients와 sub_ingredients 필드를 사용합니다.
        main_ing = reco_main.main_ingredients.split(',')[:5]
        sub_ing = reco_main.sub_ingredients.split(',')[:5]
    except ObjectDoesNotExist:
        # reco_main 또는 Recipe에서 레코드를 찾을 수 없을 때의 처리
        reco_main = None
        main_ing = None
        sub_ing = None

    # 템플릿 컨텍스트에 reco_main과 함께 main_ing, sub_ing 추가
    context = {
        'reco_main': reco_main, 
        'main_ing': main_ing, 
        'sub_ing': sub_ing
    }

    # 추천 레시피 리스트 생성
    reco_list = []
    for reco in [target_reco.reco2, target_reco.reco3, target_reco.reco4, target_reco.reco5]:
        try:
            reco_id = int(reco.strip('()').split(',')[0]) + 1
            reco_recipe = Recipe.objects.get(id=reco_id)
            reco_list.append(reco_recipe)
        except ObjectDoesNotExist:
            pass

    return render(request, 'main.html', {
        'reco_main': reco_main, 
        'reco_recipes': reco_list, 
        'main_ing': main_ing, 
        'sub_ing': sub_ing
    })




def view_search(request):
    total = Recipe.objects.count()
    latest_num = Recipe.objects.latest('id').id

    all_recipes = Recipe.objects.get_queryset().order_by('-id').values('id', 'title', 'img_url', 'img_file', 'author_id')
    all_recipe = []

    for index in range(1, latest_num+1):

        try:
            like_num = LikeModel.objects.filter(like_recipe_id=index).count()
            target_recipe = all_recipes.get(id=index)
            target_recipe['like_num'] = like_num
            all_recipe.append(target_recipe)

            if like_num == 1:
                pass
        except:
            pass

    searched=0

    try:
        if request.session['filter_type'] == "filters":
            if request.session['filter_name'] == "10분":
                filter_value = Recipe.objects.filter(timecost="10분 이내").values()
            elif request.session['filter_name'] == "20분":
                filter_value = Recipe.objects.filter(timecost="20분 이내").values()
            elif request.session['filter_name'] == "30분":
                filter_value = Recipe.objects.filter(timecost="30분 이내").values()
            elif request.session['filter_name'] == "60분":
                filter_value = Recipe.objects.filter(timecost="60분 이내").values()
            elif request.session['filter_name'] == "상":
                filter_value = Recipe.objects.filter(difficulty="중급").values()
            elif request.session['filter_name'] == "중":
                filter_value = Recipe.objects.filter(difficulty="초급").values()
            elif request.session['filter_name'] == "하":
                filter_value = Recipe.objects.filter(difficulty="아무나").values()
            elif request.session['filter_name'] == "most_popular":
                filter_value = sorted(all_recipe, key=lambda d: d['like_num'])
                filter_value.reverse()
            elif request.session['filter_name'] == "most_recent":
                filter_value = all_recipe
                filter_value.reverse()
            using_recipes =filter_value
        elif request.session['filter_type'] == "searched":
            using_recipes = Recipe.objects.filter(title__contains=request.session['filter_name']) or Recipe.objects.filter(author__username__contains=request.session['filter_name'])
            searched=request.session['filter_name']

    except:
        using_recipes = all_recipe
        using_recipes.reverse()

    # 페이지네이션 
    paginator = Paginator(using_recipes, 15)
    page_number = request.GET.get('page')
    p_recipe = paginator.page(page_number).object_list
    page_obj = paginator.page(page_number)
    page_index = []
    page_digit = len(str(page_obj.number-1))
    if page_digit == 1:
        page_firstNum = 0
    if page_digit == 3:
        page_firstNum = int(str(page_obj.number-1)[:2])
    else:
        page_firstNum = int(str(page_obj.number - 1)[0])
    for page in range(1, 11):
        page = page_firstNum * 10 + page
        page_index.append(page)

    # 페이지네이션 

    timecost = ["10분", "20분", "30분", "60분"]
    difficulty = ["상", "중", "하"]
    doc = {
        'recipes': p_recipe,
        'timecost': timecost,
        'difficulty': difficulty,
        'page_obj': page_obj,
        'page_index': page_index,
        'searched': searched,
    }
    
    if request.method == 'GET':
        return render(request, 'list.html', doc)

def searching(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '')
        #세션 저장
        request.session['filter_name'] = searched
        request.session['filter_type'] = "searched"

        return redirect('/search/?page=1')

def view_filter(request):
    if request.method == 'POST':
        timecost_value = request.POST.get('timecost', '')
        difficulty_value = request.POST.get('difficulty', '')
        mostfilter_value = request.POST.get('most_filter', '')

        request.session['filter_name'] = timecost_value or difficulty_value or mostfilter_value
        request.session['filter_type'] = "filters"
        request.session['edit'] = True
        return redirect('/search/?page=1')


def upload_recipes(request):
    if request.method == 'GET':
        try:
            #세션이 있다면
            is_update = request.session['update']
            #아이디로 레시피 가져오기
            target_recipe = Recipe.objects.get(id=request.session['myrecipe'])
        except:
            #세션이 없다면
            is_update = False
            target_recipe = ''
        ur_user = request.user.is_authenticated

        if ur_user:
            timecate = Timecate.objects.all()
            diffcate = Diffcate.objects.all()
            return render(request, 'upload.html',
                          {'timecost': timecate,
                           'difficulty': diffcate,
                           'is_update': is_update,
                           'target_recipe':target_recipe
                           })
        else:
            return redirect('/')

    elif request.method == 'POST':
        author_id = request.user.id
        title = request.POST.get('title', '')
        img_file = request.FILES.get('img_url', '')
        timecost = request.POST.get('timecost', '')
        difficulty = request.POST.get('difficulty', '')
        cookstep = request.POST.get('cookstep', '')
        main_ingredients = request.POST.get('main_ingredients', '')
        sub_ingredients = request.POST.get('sub_ingredients', '')

        my_post = Recipe.objects.create(author_id=author_id, title=title, img_file=img_file, timecost=timecost,
                                        difficulty=difficulty, cookstep=cookstep, main_ingredients=main_ingredients, sub_ingredients=sub_ingredients)
        my_post.save()
        return redirect('/')
