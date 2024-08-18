from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('hello',views.hello),
    path('login',views.ulogin),
    path('register',views.register),
    path('logout',views.ulogout),
    path('index',views.index),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('pricefilter',views.pricefilter),
    path('search',views.search),
    path('product_detail/<pid>',views.product_detail),
    path('addtocart/<pid>',views.addtocart),
    path('cart',views.viewcart),
    path('update/<x>/<cid>',views.update),
    path('remove/<cid>',views.removecart),
    path('detail',views.detail),
    path('placeorder',views.placeorder),
    path('fetchorder',views.fetchorder),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.success),
    path("history",views.history),
    path('contact',views.contact),
    path('franchise',views.franchise),
    path('carrer',views.carrer),
    path('about',views.about),
    path('terms',views.terms),
    path('contact',views.contact),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
