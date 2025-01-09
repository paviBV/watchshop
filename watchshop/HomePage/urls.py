from django.contrib import admin
from django.urls import path
from .views import home,ShowProduct,AddWatch
from .views import AddRatingComment, EditRatingComment, DeleteRatingComment
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name="home"),
    path('login/', views.LoginPage, name='login'),
    # path('reviews/<int:pk>', views.Reviews, name='reviews'),

    path('reviews/<int:pk>', views.Reviews.as_view(), name='reviews'),

    path('rate_product/<int:pk>', AddRatingComment.as_view(), name='rate_product'),
    path('edit_comment/<int:pk>/', EditRatingComment.as_view(), name='edit_comment'),
    path('delete_comment/<int:pk>/', DeleteRatingComment.as_view(), name='delete_comment'),
    # path('rate_product/<int:product_id>', views.add_rating_comment, name='rate_product'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', views.LogoutPage, name='logout'),
    path('product/<str:pk>',ShowProduct, name='product'),
    path('addWatch/', AddWatch, name='addWatch'),
    path('editWatch/<int:pk>', views.EditWatch, name='editWatch'),
    path('deleteWatch/<int:pk>', views.DeleteWatch, name='deleteWatch'),
    path('search_product/',views.SearchProduct, name="search_product")

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)