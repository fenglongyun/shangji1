from django.conf.urls import url
from api.views import indexviews
from api.views.simcard.simcard import Simcard
from api.views.admin import account
from api.views.device.views import UpdateDevPic, StateDevView 
from api.views.admin.digitalCockpit import workbench

urlpatterns = [
    url(r'login/$', indexviews.Login.as_view()),
    url(r'register/$', indexviews.Register.as_view()),
    url(r'getmenutree/$', indexviews.GetMenuTree.as_view()),
    url(r'companysdepartments/$',indexviews.CompanysDepartments.as_view()),
    url(r'userinfo/$',indexviews.Userinfo.as_view()),
    url(r'departments/$',indexviews.Departments.as_view()),
    url(r'departments/(?P<pk>\w+)/$',indexviews.Departments.as_view()),
    url(r'userlist/$',indexviews.UserList.as_view()),
    url(r'userlist/(?P<pk>\w+)/$',indexviews.UserList.as_view()),
    url(r'device/$', indexviews.Device.as_view()),
    url(r'device/(?P<pk>\w+)/$', indexviews.Device.as_view()),
    url(r'failurewarning/$',indexviews.FailureWarning.as_view()),
    url(r'baojing/$',indexviews.BaoJing.as_view()),
    url(r'cncstates/$',indexviews.Cncstates.as_view()),
    url(r'cameraaddress/(?P<pk>\w+)/$',indexviews.Cameraaddress.as_view()),
    url(r'shuju/(?P<devtype>\w+-\w+)/$', indexviews.Shuju.as_view()),
    url(r'devpic/(?P<pk>\d+)/$', UpdateDevPic.as_view()), #设备图片修改接口


    url(r'^authorizedusers/$',account.AuthorizedUsers.as_view()),
    url(r'^authorizeduser/(?P<pk>\d+)/$',account.AuthorizedUser.as_view()),
    url(r'^authorizeduser/$',account.AuthorizedUser.as_view()),
    url(r'^unauthorizedusers/$',account.UnauthorizedUsers.as_view()),
    url(r'^unauthorizedUser/(?P<pk>\d+)/$',account.UnauthorizedUser.as_view()),
    url(r'^menulist/$',account.Menulist.as_view()),
    url(r'^menutree/$',account.Menutree.as_view()),
    url(r'^userauthorization/(?P<pk>\d+)/$', account.UserAuthorization.as_view()),
    url(r'^usermenus/(?P<pk>\d+)/$', account.UserMenus.as_view()),
    url(r'^shujuTest/$', indexviews.ShujuTest.as_view()),
    url(r'^shujuTest/(?P<devtype>\w+-\w+)/$', indexviews.ShujuTest.as_view()),

    # sim 卡接口：
    url(r'^simCard/$', Simcard.as_view()),
    

    # 设备接口：
    url(r'^statedev/(?P<cncstate>\w+)/(?P<devnum>\w+)/$', StateDevView.as_view()),  #根据cncstate值不同，列出不同状态的设备
]