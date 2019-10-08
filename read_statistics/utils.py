import datetime
from django.db.models import Sum   #求和
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.utils import timezone


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        #总阅读加1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        #当天阅读数
        date = timezone.now().date()   #now().date() now在filter中会自动把时间去掉所以加 date
        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readdetail.read_num += 1
        readdetail.save()
    return key


def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))  #把date装换成字符串
        read_datails = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_datails.aggregate(read_num_sum=Sum('read_num'))   #sum求和
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

def get_todat_hot_data(content_type):    #今天热门阅读
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today)
    return read_details.order_by('-read_num')[:7]  #对参数进行由大到小排序,取前7条

def get_yesterday_hot_date(content_type):  #昨天热门阅读
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday)
    return read_details.order_by('-read_num')[:7]

