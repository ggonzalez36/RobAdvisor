from django.urls import path

from . import views

app_name = "roboadvisor"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:company_id>/", views.detail, name="detail"),
    path("<int:company_id>/prediction/", views.createPrediction, name="prediction"),
    path("<int:company_id>/graph/", views.graph, name="graph"),
    path("<int:company_id>/predicted/", views.graphPrediction, name="graphPrediction"),
    path("account/", views.account, name="account"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("register/", views.register, name="register"),
    path("welcome/", views.welcome, name="welcome"),
    path("profile/", views.profile, name="profile"),
    path("asset/<int:assetId>/", views.stockDetails, name="stockDetails"),
]
