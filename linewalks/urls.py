from django.urls    import path, include

urlpatterns = [
    path('temp', include('temp.urls')),
]
