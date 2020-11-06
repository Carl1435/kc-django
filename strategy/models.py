from django.db import models

# Create your models here.

class strategy(models.Model):
    # name   = models.CharField(max_length=20,verbose_name='name')
    strategy_id = models.CharField(max_length=20, verbose_name='strategy_id',primary_key=True)
    strategy_name  = models.CharField(max_length=20, verbose_name='strategy_name')
    strategy_train_start  = models.CharField(max_length=20, verbose_name='strategy_train_start')
    strategy_train_end   = models.CharField(max_length=20, verbose_name='strategy_train_end')
    strategy_verify_start    = models.CharField(max_length=20, verbose_name='strategy_verify_start')
    strategy_verify_end   = models.CharField(max_length=20, verbose_name='strategy_verify_end')
    strategy_vol_start = models.CharField(max_length=20, verbose_name='strategy_vol_start')
    strategy_vol_end = models.CharField(max_length=20, verbose_name='strategy_vol_end')
    strategy_amo_start = models.CharField(max_length=20, verbose_name='strategy_amo_start')
    strategy_amo_end = models.CharField(max_length=20, verbose_name='strategy_amo_end')
    strategy_Model_choose = models.CharField(max_length=20, verbose_name='strategy_Model_choose')
    strategy_epoch_num_choose = models.CharField(max_length=20, verbose_name='strategy_epoch_num_choose')
    MSE = models.CharField(max_length=20, verbose_name='MSE')
    strategy_state=models.CharField(max_length=20, verbose_name='strategy_state')
    if_high = models.CharField(max_length=20, verbose_name='if_high')
    if_low = models.CharField(max_length=20, verbose_name='if_low')
    if_open = models.CharField(max_length=20, verbose_name='if_open')
    if_vol = models.CharField(max_length=20, verbose_name='if_vol')
    if_amo = models.CharField(max_length=20, verbose_name='if_amo')

    class Meta:
        db_table = 'strategy'  # 指明数据库表名
        # verbose_name = '图书'  # 在admin站点中显示的名称
        # verbose_name_plural = verbose_name  # 显示的复数名称
class strategy_code(models.Model):
    # name   = models.CharField(max_length=20,verbose_name='name')
    id =models.CharField(max_length=20, verbose_name='id',primary_key=True)
    strategy_name= models.CharField(max_length=20, verbose_name='strategy_name')
    Code_ID = models.CharField(max_length=20, verbose_name='Code_ID')
    pre_close  = models.CharField(max_length=20, verbose_name='pre_close')
    mse = models.CharField(max_length=20, verbose_name='mse')
    open_start=models.CharField(max_length=20, verbose_name='open_start')
    class Meta:
        db_table = 'strategy_code'

class  day_table(models.Model):
    # name   = models.CharField(max_length=20,verbose_name='name')
    day_Code    = models.CharField(max_length=20, verbose_name='day_Code',primary_key=True)
    day_avg_vol = models.CharField(max_length=20, verbose_name='day_avg_vol')
    day_avg_amo = models.CharField(max_length=20, verbose_name='day_avg_amo')


    class Meta:
        db_table = 'day_table1'