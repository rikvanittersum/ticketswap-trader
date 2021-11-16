from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("my_tickets/", views.my_tickets, name="my_tickets"),
    path("buy_tickets/", views.buy_tickets, name="buy_tickets"),
    path("buy/", views.buy, name="buy"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("past_events/", views.passed_events, name="past_events"),
    path("advice/", views.advicer, name="advice")
]