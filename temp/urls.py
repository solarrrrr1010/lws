from django.urls import path

from temp.views import Statistics, ConceptInfo

app_name = 'temp'
urlpatterns = [
    path('/statistics', Statistics.as_view()),
    path('/conceptinfo/', ConceptInfo.as_view()),
] 