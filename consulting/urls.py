from django.urls import path
from .views import (consulting, consusers, consteammembership, consservices, consconversation, \
                    conscontactmessage,telegrammessage,consuseradd,
                    consblogpost, conschatrequests,conshistory
    # consservicemembership
                    )

urlpatterns = [
    path('consulting/', consulting, name='consulting'),
    path('consusers/',consusers,name='consusers'),
    path('conschatrequests/',conschatrequests,name='conschatrequests'),
    path('consteammemberships/',consteammembership,name='consteammemberships'),
    path('consservices/',consservices,name='consservices'),
    path('consconversation/',consconversation,name='consconversation'),
    path('conscontactmessages/',conscontactmessage,name='conscontactmessages'),
    path('conscomments/',conscontactmessage,name='conscomments'),
    path('consblogposts/',consblogpost,name='consblogposts'),
    path('conshistory/',conshistory,name='conshistory'),
    path('constelegram/',telegrammessage,name='constelegram'),
    path('consaddstaff/',consuseradd,name='addstaff'),


    # path('consservicememberships/',consservicemembership,name='consservicememberships'),
]
