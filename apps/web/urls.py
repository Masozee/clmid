from django.urls import path

from .views import (
    web_home_view,

)

app_name = "web"
urlpatterns = [
    # calendar
    path("", view=web_home_view, name="home"),
    

]