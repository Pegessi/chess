from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
import json
import datetime
import time
from .models import User, War, Warhis, Avatar, Career, Passwar


# 对局接口

# 发起战局
@require_http_methods(['GET'])
def makeWar(request):
    response = {}
    try:
        user = request.GET.get('id')
        status = '未开始'
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        indexUser = User.objects.get(id=user)
        level = indexUser.level
        warInfo = {
            'id': user,
            'level': level,
            'flag': status,
            'date': currentTime
        }
        newWar = War(userid=user, level=level, flag=status, date=currentTime)
        newWar.save()
        newWarhis = Warhis(userred=user, date=currentTime, flag='未就绪')
        newWarhis.save()
        response['warInfo'] = warInfo
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 结束战局
@require_http_methods(['GET'])
def cancelWar(request):
    response = {}
    try:
        user = request.GET.get('id')
        delWar = War.objects.get(userid=user)
        delWar.delete()
        delWarHis = Warhis.objects.get(userred=user)
        delWarHis.delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 获取当前所有战局
@require_http_methods(['GET'])
def getAllWar(request):
    response = {}
    try:
        wars = War.objects.filter()
        warList = json.loads(serializers.serialize('json', wars))
        # print(warList)
        for i in range(0, len(warList)):
            owner = warList[i]['pk']
            avatar = Avatar.objects.get(id=owner)
            warList[i]['fields']['path'] = avatar.path
        response['warlist'] = warList
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 战局初始化
@require_http_methods(['GET'])
def enterWar(request):
    response = {}
    try:
        red = request.GET.get('owner')
        black = request.GET.get('id')
        war = Warhis.objects.get(userred=red)
        warOut = War.objects.get(userid=red)
        if red == black:
            # 进入者为红方
            if warOut.flag == '黑方就绪':
                warOut.flag = '进行中'
            else:
                warOut.flag = '红方就绪'
            if war.flag == '黑方就绪':
                war.flag = '就绪'
            else:
                war.flag = '红方就绪'
        else:
            # 进入者为黑方
            if warOut.flag == '红方就绪':
                warOut.flag = '进行中'
            else:
                warOut.flag = '黑方就绪'
            war.userblack = black
            if war.flag == '红方就绪':
                war.flag = '就绪'
            else:
                war.flag = '黑方就绪'
        # war.flag = '就绪'
        war.save()
        warOut.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 返回战局信息
@require_http_methods(['GET'])
def updateWar(request):
    response = {}
    try:
        # time.sleep(1)
        id = request.GET.get('id')
        aim = request.GET.get('aim')
        # print(id,aim)
        if aim == 'null':
            # 红方
            war = Warhis.objects.get(userred=id)
            if war.flag != '就绪':
                # 红方进入黑方未进入
                avatarRed = Avatar.objects.get(id=war.userred)
                userRed = User.objects.get(id=war.userred)
                warInfo = {
                    'red': war.userred,
                    'black': war.userblack,
                    'date': war.date,
                    'winner': war.winner,
                    'picpath': war.picpath,
                    'flag': war.flag,
                    'avatarRed': avatarRed.path,
                    # 'avatarBlack': avatarBlack.path,
                    'redLevel': userRed.level,
                    'check': 'red'
                    # 'blackLevel': userBlack.level
                }
            else:
                # 都进入
                avatarRed = Avatar.objects.get(id=war.userred)
                userRed = User.objects.get(id=war.userred)
                avatarBlack = Avatar.objects.get(id=war.userblack)
                userBlack = User.objects.get(id=war.userblack)
                warInfo = {
                    'red': war.userred,
                    'black': war.userblack,
                    'date': war.date,
                    'winner': war.winner,
                    'picpath': war.picpath,
                    'flag': war.flag,
                    'avatarRed': avatarRed.path,
                    'avatarBlack': avatarBlack.path,
                    'redLevel': userRed.level,
                    'check': 'red',
                    'blackLevel': userBlack.level
                }
        else:
            # 黑方
            war = Warhis.objects.get(userblack=id)
            if war.flag == '就绪':
                # 双方进入
                avatarBlack = Avatar.objects.get(id=war.userblack)
                userBlack = User.objects.get(id=war.userblack)
                avatarRed = Avatar.objects.get(id=war.userred)
                userRed = User.objects.get(id=war.userred)
                warInfo = {
                    'red': war.userred,
                    'black': war.userblack,
                    'date': war.date,
                    'winner': war.winner,
                    'picpath': war.picpath,
                    'flag': war.flag,
                    'avatarRed': avatarRed.path,
                    'avatarBlack': avatarBlack.path,
                    'redLevel': userRed.level,
                    'blackLevel': userBlack.level,
                    'check': 'black'
                }
            else:
                # 黑方进入红方未进入
                avatarBlack = Avatar.objects.get(id=war.userblack)
                userBlack = User.objects.get(id=war.userblack)
                warInfo = {
                    'red': war.userred,
                    'black': war.userblack,
                    'date': war.date,
                    'winner': war.winner,
                    'picpath': war.picpath,
                    'flag': war.flag,
                    # 'avatarRed': avatarRed.path,
                    'avatarBlack': avatarBlack.path,
                    # 'redLevel': userRed.level,
                    'blackLevel': userBlack.level,
                    'check': 'black'
                }
        # warInfo = {
        #     'red': war.userred,
        #     'black': war.userblack,
        #     'date': war.date,
        #     'winner': war.winner,
        #     'picpath': war.picpath,
        #     'flag': war.flag,
        #     'avatarRed': avatarRed.path,
        #     # 'avatarBlack': avatarBlack.path,
        #     'redLevel': userRed.level,
        #     'flag': 'black'
        #     # 'blackLevel': userBlack.level
        # }
        response['warInfo'] = warInfo
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(str(e))
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 中途退出战局
@require_http_methods(['GET'])
def quitWar(request):
    response = {}
    try:
        id = request.GET.get('id')
        aim = request.GET.get('aim')
        # 找到对局
        if aim == 'null':
            war = Warhis.objects.get(userred=id)
            if war.flag == '黑方离场':
                war.delete()
            else:
                war.flag = '红方离场'
                war.save()
            if War.objects.filter(userid=id):
                warOut = War.objects.get(userid=id)
                warOut.delete()
        else:
            war = Warhis.objects.get(userblack=id)
            if war.flag == '红方离场':
                war.delete()
            else:
                war.flag = '黑方离场'
                war.save()
            if War.objects.filter(userid=aim):
                warOut = War.objects.get(userid=aim)
                warOut.delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 发送消息
@require_http_methods(['POST'])
def sendMessage(request):
    response = {}
    try:
        # 请求body中包括json信息 解码 封装为字典 调用
        pack = request.body.decode('utf-8')
        print(pack)
        print(type(pack))
        mesData = json.loads(pack)
        print(type(mesData))
        print(mesData)
        print(len(mesData))
        red = request.GET.get('red')
        black = request.GET.get('black')
        send = request.GET.get('send')
        war = Warhis.objects.get(userred=red, userblack=black)
        war.mesdata = pack
        # print(war.mesdata)
        war.save()
        # print(request.GET.get('send'))
        # print(mesData[0]['words'])
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 接收消息
@require_http_methods(['GET'])
def recMessage(request):
    response = {}
    try:
        red = request.GET.get('red')
        black = request.GET.get('black')
        # send = request.GET.get('send')
        war = Warhis.objects.get(userred=red, userblack=black)
        index = str(war.mesdata)
        print('rec')
        mesData = json.loads(index)
        print(type(mesData))
        print(mesData)
        print(len(mesData))
        response['mesData'] = mesData
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(str(e))
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 更新生涯
@require_http_methods(['GET'])
def updateCareer(request):
    response = {}
    try:
        user = request.GET.get('id')
        winner = request.GET.get('win')
        car = Career.objects.get(id=user)
        use = User.objects.get(id=user)
        car.allgame = int(car.allgame) + 1
        if user == winner:
            car.wingame = int(car.wingame) + 1
        else:
            car.lossgame = int(car.lossgame) + 1
        if int(car.wingame) != 0:
            car.winper = float(car.wingame) / float(car.allgame)
        if 10 < int(car.allgame) <= 20:
            use.level = '入门'
            use.save()
        elif 20 < int(car.allgame) <= 40:
            use.level = '初级'
            use.save()
        elif 40 < int(car.allgame) <= 60:
            use.level = '中级'
            use.save()
        elif 60 < int(car.allgame) <= 100:
            use.level = '高级'
            use.save()
        elif int(car.allgame) > 100:
            use.level = '大师'
            use.save()
        car.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 更新历史对局
@require_http_methods(['GET'])
def updatePass(request):
    response = {}
    try:
        red = request.GET.get('red')
        black = request.GET.get('black')
        winner = request.GET.get('win')
        run = request.GET.get('run')
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        newPass = Passwar(red=red, black=black, win=winner, date=currentTime, runtime=run)
        newPass.save()
        print(newPass)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(str(e))
        response['msg'] = str(e)
        response['error_num'] = 1
        return JsonResponse(response)


# 获取历史对局
@require_http_methods(['GET'])
def getPass(request):
    response = {}
    try:
        id = request.GET.get('id')

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(str(e))
        response['msg'] = str(e)
        response['error_num'] = 1
        return JsonResponse(response)
