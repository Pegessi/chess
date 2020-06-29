from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
import json
from .models import User, Career, Avatar, Passwar
import random
import base64
from suds.client import Client

# 登录&用户管理接口

# http://localhost:8888/AliYunChessAvatarStore_war/service/chessImageStore?wsdl
# http://39.98.48.34:2233/AliYunChessAvatarStore_war/service/chessImageStore?wsdl
# 阿里云web服务初始化
imageService = Client('http://39.98.48.34:2233/AliYunChessAvatarStore_war/service/chessImageStore?wsdl')

# 登录检验
@require_http_methods(['GET'])
def loginCheck(request):
    response = {}
    flag = ''
    try:
        user = 'ini'
        pwd = 'ini'
        if request.GET:
            user = request.GET.get('username')
            pwd = request.GET.get('password')
        # 查询语句
        if User.objects.filter(id=user):
            userSQL = User.objects.get(id=user)
            name = userSQL.id
            pwds = userSQL.password
            if user == name and pwd == pwds:
                flag = 'true'
            elif user == name and pwd != pwds:
                flag = 'false'
        else:
            flag = "none"
        response['msg'] = 'success'
        response['error_num'] = 0
        response['flag'] = flag
        response['token'] = str(random.randint(1000, 10000))
        # username = User(user_name=request.GET.get('username'))
        # username.save()
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 注册用户
@require_http_methods(['POST'])
def logon(request):
    response = {}
    try:
        # 请求body中包括json信息 解码 封装为字典 调用
        pack = request.body.decode('utf-8')
        userData = json.loads(pack)
        birthday = str(userData['birth']).split('T')[0]
        # 2001-06-07T16:00:00.000Z
        # print(userData)
        newUser = User(id=userData['name'], password=userData['password'], sex=userData['sex'], age=userData['age'],
                       birth=birthday, email=userData['email'], level='小白')
        newUser.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 用户名查重
@require_http_methods(['GET'])
def checkID(request):
    response = {}
    try:
        user = request.GET.get('username')
        flag = ''
        if User.objects.filter(id=user):
            flag = 'exists'
        else:
            flag = 'new'
        response['flag'] = flag
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 获取用户信息
@require_http_methods(['GET'])
def getUserData(request):
    response = {}
    try:
        user = request.GET.get('id')
        indexUser = User.objects.get(id=user)
        userData = {
            'id': indexUser.id,
            'sex': indexUser.sex,
            'age': indexUser.age,
            'birth': indexUser.birth,
            'email': indexUser.email,
            'level': indexUser.level,
            'password': indexUser.password
        }
        if userData['birth'] == '':
            userData['birth'] = '未填写'
        response['userdata'] = userData
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 获取用户生涯信息
@require_http_methods(['GET'])
def getUserCareer(request):
    response = {}
    try:
        user = request.GET.get('id')
        # print(user)
        userData = {}
        indexCareer = Career.objects.get(id=user)
        userData['allGame'] = indexCareer.allgame
        userData['winGame'] = indexCareer.wingame
        userData['lossGame'] = indexCareer.lossgame
        userData['winPer'] = indexCareer.winper
        response['userdata'] = userData
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 修改用户信息
@require_http_methods(['POST'])
def changeUserData(request):
    response = {}
    try:
        pack = request.body.decode('utf-8')
        userData = json.loads(pack)
        birthday = str(userData['birth']).split('T')[0]
        user = User.objects.get(id=userData['name'])
        user.password = userData['password']
        user.sex = userData['sex']
        user.age = userData['age']
        user.birth = birthday
        user.email = userData['email']
        user.save()
        if userData['base'] != 'null':
            base = str(userData['base']).split(',')[1]
            # base为不带表头的base64数据
            para = imageService.factory.create('storeImg')
            para['arg0'] = base
            para.arg1 = userData['name']
            # 调用web服务将图片base64字符串上传
            imageService.service.storeImg(base, userData['name'] + '.jpg')
            imgPath = 'http://39.98.48.34:2233/userImg/' + userData['name'] + '.jpg'
            userAvatar = Avatar(id=userData['name'], path=imgPath)
            userAvatar.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 返回用户头像
@require_http_methods(['GET'])
def getAvatar(request):
    response = {}
    try:
        user = request.GET.get('id')
        avatar = Avatar.objects.get(id=user)
        path = avatar.path
        response['path'] = path
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 返回历史对局
@require_http_methods(['GET'])
def getPassWar(request):
    response = {}
    try:
        user = request.GET.get('id')
        print(user)
        redWar = Passwar.objects.filter(red=user)
        blackWar = Passwar.objects.filter(black=user)
        redList = json.loads(serializers.serialize('json', redWar))
        blackList = json.loads(serializers.serialize('json', blackWar))
        response['redList'] = redList
        response['blackList'] = blackList
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(str(e))
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)