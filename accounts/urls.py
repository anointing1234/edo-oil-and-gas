from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 

urlpatterns = [ 
    path('', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('privacy_policy/',views.privacy_policy,name='privacy_policy'),
    path('reservation/',views.reservation,name='reservation'),
    path('contact/',views.contact,name='contact'),
    path('reserve_seat/',views.reserve_seat,name='reserve_seat'),
    path('contact_view/',views.contact_view,name='contact_view'),
     path('sponsors/',views.sponsors,name='sponsors'),
     path('send_message/',views.send_message,name='send_message'),
     path('send_messages/',views.send_messages,name='send_messages'),
     path('decline/',views.decline,name='decline'),
     path('decline_message/',views.decline_message,name='decline_message'),
    path('exhibitors/',views.exhibitors,name='exhibitors'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
