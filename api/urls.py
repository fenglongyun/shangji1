from django.conf.urls import url
from api.views import adminviews,indexviews

urlpatterns = [
    url(r'login/$', indexviews.Login.as_view()),
    url(r'register/$', indexviews.Register.as_view()),
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
    
    url(r'^authorizedusers/$',adminviews.AuthorizedUsers.as_view()),
    url(r'^unauthorizedusers/$',adminviews.UnauthorizedUsers.as_view()),
    url(r'^menulist/$',adminviews.Menulist.as_view()),
    url(r'^menutree/$',adminviews.Menutree.as_view()),
    url(r'^userauthorization/(?P<pk>\d+)/$', adminviews.UserAuthorization.as_view()),
    url(r'^usermenus/(?P<pk>\d+)/$', adminviews.UserMenus.as_view()),


]