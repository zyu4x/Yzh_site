from django.shortcuts import render
from .models import LikeCount, LikeRecord
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist

def SuccessResponse(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'you were not login')
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')

    is_like = request.GET.get('is_like')

    if is_like == 'true':
        #要点赞
        like_record, create =LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if create:
            #未点赞
            like_count, create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)

        else:
            #以点过赞不能重复点赞
            return ErrorResponse(402, 'you were liked')
    else:
        #取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            #有点赞过取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            #点赞总数减1
            like_count, create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not create:
                like_count.like_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(403, 'data error')

            pass
        else:
            #没有点赞过不能取消
            return ErrorResponse(403, 'you were not liked')

