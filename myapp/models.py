from django.db import models

# Create your models here.



class day(models.Model):
    # name   = models.CharField(max_length=20,verbose_name='name')
    index  = models.CharField(max_length=20,verbose_name='index',primary_key=True)
    open   = models.CharField(max_length=20)
    close  = models.CharField(max_length=20)
    high   = models.CharField(max_length=20)
    low    = models.CharField(max_length=20)
    vol    = models.CharField(max_length=20)
    amount = models.CharField(max_length=20)

    class Meta:
        db_table = 'day000001'  # 指明数据库表名
        # verbose_name = '图书'  # 在admin站点中显示的名称
        # verbose_name_plural = verbose_name  # 显示的复数名称
