from django.urls import path
from .views import consulting, consusers, consabouts, consteammembership, consservices, consconversation, \
    conscontactmessage, consblogpost, consservicemembership

urlpatterns = [
    path('consulting/', consulting, name='consulting'),
    path('consusers/',consusers,name='consusers'),
    path('consabouts/',consabouts,name='consabouts'),
    path('consteammemberships/',consteammembership,name='consteammemberships'),
    path('consservices/',consservices,name='consservices'),
    path('consconversation/',consconversation,name='consconversation'),
    path('conscontactmessages/',conscontactmessage,name='conscontactmessages'),
    path('conscomments/',conscontactmessage,name='conscomments'),
    path('consblogposts/',consblogpost,name='consblogposts'),
    path('consservicememberships/',consservicemembership,name='consservicememberships'),
]
