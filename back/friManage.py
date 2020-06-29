from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
import datetime
import time
import json
from .models import User, Friend, Request, Avatar


# 好友管理接口


# 发送好友请求
@require_http_methods(['GET'])
def sendReq(request):
    response = {}
    try:
        send = request.GET.get('send')
        rec = request.GET.get('rec')
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        newReq = Request(send=send, receive=rec, date=currentTime, flag='未处理')
        newReq.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 删除好友请求
@require_http_methods(['GET'])
def delReq(request):
    response = {}
    try:
        send = request.GET.get('send')
        rec = request.GET.get('rec')
        req = Request.objects.get(send=send, receive=rec)
        req.delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 查询发送的好友请求
@require_http_methods(['GET'])
def selectSendReq(request):
    response = {}
    try:
        send = request.GET.get('send')
        reqList = Request.objects.filter(send=send)
        response['reqList'] = json.loads(serializers.serialize('json', reqList))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 查询接收的好友请求
@require_http_methods(['GET'])
def selectRecReq(request):
    response = {}
    try:
        rec = request.GET.get('rec')
        reqList = Request.objects.filter(receive=rec)
        response['reqList'] = json.loads(serializers.serialize('json', reqList))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 处理好友请求
@require_http_methods(['GET'])
def dealReq(request):
    response = {}
    try:
        send = request.GET.get('send')
        rec = request.GET.get('rec')
        flag = request.GET.get('flag')
        deal = Request.objects.get(send=send, receive=rec)
        deal.flag = flag
        deal.delete()
        if flag == '同意':
            currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            newFri = Friend(id=send, fri=rec, date=currentTime)
            newFri.save()
            time.sleep(1)
            currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            newFriToo = Friend(id=rec, fri=send, date=currentTime)
            newFriToo.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 获取好友列表
@require_http_methods(['GET'])
def getFriList(request):
    response = {}
    try:
        user = request.GET.get('id')
        friendList = Friend.objects.filter(id=user)
        friList = json.loads(serializers.serialize('json', friendList))
        for i in range(0, len(friList)):
            friID = friList[i]['fields']['fri']
            avatar = Avatar.objects.get(id=friID)
            user = User.objects.get(id=friID)
            friList[i]['fields']['avatarPath'] = avatar.path
            friList[i]['fields']['sex'] = user.sex
            friList[i]['fields']['age'] = user.age
            friList[i]['fields']['birth'] = user.birth
            friList[i]['fields']['email'] = user.email
            friList[i]['fields']['level'] = user.level
            friList[i]['pk'] = str(friList[i]['pk']).split(' ')[0]
        response['friendList'] = friList
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 删除好友
@require_http_methods(['GET'])
def delFri(request):
    response = {}
    try:
        user = request.GET.get('id')
        fri = request.GET.get('fri')
        delf1 = Friend.objects.get(id=user,fri=fri)
        delf1.delete()
        delf2 = Friend.objects.get(id=fri,fri=user)
        delf2.delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
