from django.conf.urls import url
from api import views

urlpatterns = [
    
    url(r'login/$', views.Login.as_view()),
    url(r'userinfo/$',views.Userinfo.as_view()),
    url(r'userlist/$',views.UserList.as_view()),
    url(r'userlist/(?P<pk>\w+)/$',views.UserList.as_view()),
    url(r'device/$', views.Device.as_view()),
    url(r'device/(?P<pk>\w+)/$', views.Device.as_view()),
    url(r'cncstates/$',views.Cncstates.as_view()),
    url(r'cameraaddress/(?P<pk>\w+)/$',views.Cameraaddress.as_view()),
    url(r'shuju/(?P<devtype>\w+-\w+)/$', views.Shuju.as_view()),
]