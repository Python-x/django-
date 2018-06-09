# @Time    : 18-6-5 下午2:19
# @Author  : wengwenyu
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from .views import index, list1, Search, detail

urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^list/$',list1, name='list1'),
    url(r'^search/$', Search.as_view(),name='search'),
    url(r'^tags/(?P<tid>\d*)/$', list1, name='tags'),
    url(r'^cat/(?P<cid>\d*)/$', list1, name='cat'),
    url(r'^detail/(?P<pid>\d*)/$', detail, name='detail'),
]
