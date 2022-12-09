from django.db import models
from django.utils.timezone import now

# Create your models here.
class Deal(models.Model):
    # list_index = models.IntegerField(primary_key=True)
    image = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=False)
    link = models.CharField(max_length=200)
    # reply_count = models.IntegerField()
    # up_count = models.IntegerField()
    upload_date = models.DateTimeField(default=now)
    category = models.CharField(max_length=10, null=True, default="")
    price = models.IntegerField(null = True)
    site = models.CharField(max_length=20, default=0)
    
    # class Meta:
    #     verbose_name_plural = "핫딜 게시글 모음"
    def __str__(self):
        return f"{self.title} -- {self.link}--{self.upload_date}"