from django.conf.urls import url, include
from back import views
from back import warManage
from back import friManage

urlpatterns = [
    # 用户中心相关接口
    url(r'^login_check$', views.loginCheck),         # 登录校验
    url(r'^logon', views.logon),                     # 注册接口
    url(r'^checkid', views.checkID),                 # 用户id查询接口
    url(r'^getuserdata', views.getUserData),         # 获取用户信息
    url(r'^getusercareer', views.getUserCareer),     # 获取用户生涯信息
    url(r'^changeUserData', views.changeUserData),   # 改变用户信息
    url(r'^getAvatar', views.getAvatar),             # 获取用户头像
    url(r'^getPass', views.getPassWar),              # 获取历史对局

    # 象棋战局相关接口
    url(r'^makewar', warManage.makeWar),             # 创建战局
    url(r'^cancelwar', warManage.cancelWar),         # 取消战局
    url(r'^getwar', warManage.getAllWar),            # 获取战局列表
    url(r'^enterwar', warManage.enterWar),           # 进入战局初始化
    url(r'^updatewar', warManage.updateWar),         # 更新对局信息
    url(r'^quitwar', warManage.quitWar),             # 中途退出战局
    url(r'^sendMes', warManage.sendMessage),         # 发送消息包
    url(r'^recMes', warManage.recMessage),           # 接收消息包
    url(r'^updateCareer', warManage.updateCareer),   # 更新生涯
    url(r'^updatePass', warManage.updatePass),       # 更新历史对局

    # 好友管理相关接口
    url(r'^sendReq', friManage.sendReq),             # 发送好友请求
    url(r'^selectSendReq', friManage.selectSendReq), # 获取发送的请求
    url(r'^selectRecReq', friManage.selectRecReq),   # 获取接收的请求
    url(r'^dealReq', friManage.dealReq),             # 处理请求
    url(r'^delReq', friManage.delReq),               # 删除请求
    url(r'^getFriList', friManage.getFriList),       # 获取好友列表
    url(r'^delFri', friManage.delFri),               # 删除好友
]
