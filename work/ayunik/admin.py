from django.contrib import admin
from .models import PharmacySignUp,ClientSignUp,Feedback,CUserProfile,PUserProfile,SignUp,Advertisements
from .models import MedInfo,MedTrack,Query,TrackAdv,CartData,Transaction
admin.site.register(PharmacySignUp)
admin.site.register(CUserProfile)
admin.site.register(PUserProfile)
admin.site.register(ClientSignUp)
admin.site.register(Feedback)
admin.site.register(SignUp)
admin.site.register(MedInfo)
admin.site.register(MedTrack)
admin.site.register(Query)
admin.site.register(Advertisements)
admin.site.register(TrackAdv)
admin.site.register(CartData)
admin.site.register(Transaction)