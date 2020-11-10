from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'login/$', views.Login.as_view()),
    url(r'userinfo/$',views.Userinfo.as_view()),
    url(r'departments/$',views.Departments.as_view()),
    url(r'departments/(?P<pk>\w+)/$',views.Departments.as_view()),
    url(r'userlist/$',views.UserList.as_view()),
    url(r'userlist/(?P<pk>\w+)/$',views.UserList.as_view()),
    url(r'authorizedusers/$',views.AuthorizedUsers.as_view()),
    url(r'unauthorizedusers/$',views.UnauthorizedUsers.as_view()),
    url(r'device/$', views.Device.as_view()),
    url(r'device/(?P<pk>\w+)/$', views.Device.as_view()),
    url(r'failurewarning/$',views.FailureWarning.as_view()),
    url(r'cncstates/$',views.Cncstates.as_view()),
    url(r'cameraaddress/(?P<pk>\w+)/$',views.Cameraaddress.as_view()),
    url(r'shuju/(?P<devtype>\w+-\w+)/$', views.Shuju.as_view()),
]