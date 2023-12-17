from django.db import models
from user.models import UserModel

#Create your models here.
class Recipe(models.Model):
    class Meta:
        db_table = "recipe"
    def __str__(self):
        return self.title

    title = models.CharField(max_length=100, null=False)
    img_url = models.URLField(max_length=300, null=False, default='')
    timecost = models.CharField(max_length=10, null=True)
    difficulty = models.CharField(max_length=10, null=False) 
    #ingredient = models.TextField(null=False) 
    cookstep = models.TextField(null=False)
    ingredient = models.TextField(null=False)
    main_ingredients = models.TextField(null=False)
    sub_ingredients = models.TextField(null=False)


    author_id = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    img_file = models.ImageField(upload_to='uploads/', null=True)

    #수정한 부분
    n_main_ingredients = models.IntegerField(null=True)  # 정규화한 후 저장될 열
    n_sub_ingredients = models.IntegerField(null=True)  # 정규화한 후 저장될 열
    classification = models.CharField(max_length=50, null=True)  # CSV 파일에 있는 classification 열



class Timecate(models.Model):
    class Meta:
        db_table = "timecost"
    def __str__(self):
        return self.timecost
    timecost = models.CharField(max_length=50, default='')

class Diffcate(models.Model):
    class Meta:
        db_table = "difficulty"
    def __str__(self):
        return self.difficulty
    difficulty = models.CharField(max_length=50, default='')
