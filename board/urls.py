from board.views import PostListView, PostView, PostWriteView
from django.conf.urls import url

urlpatterns = [
    url(r'^write/?$', PostWriteView.as_view(), name='post_write'),
    url(r'^modify/(?P<id>\d+)/?$', PostWriteView.as_view(), name='post_modify'),
    url(r'^delete/(?P<id>\d+)/?$', PostWriteView.as_view(), name='post_delete'),
    url(r'^(?P<name>\w+)/?$', PostListView.as_view(), name='post_list'),
    url(r'^(?P<name>\w+)/(?P<id>\d+)/?$', PostView.as_view(), name='post_detail'),
]