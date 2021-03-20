from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm
from .views import ActiveMenuList, Checkout
from django.urls import path, reverse_lazy, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='root'),
    path('signup/', views.signup, name='signup'),
    path('activation/sent', views.activation_sent_view, name='activation_email_sent'),
    path('activation/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name="authentication/login.html",
                                                         authentication_form=UserLoginForm,
                                                         redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menu/', ActiveMenuList.as_view(), name='menu'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('orders/', views.Orders.as_view(), name='order'),
    path('orders/<int:pk>', views.OrderItems.as_view(), name='order_detail'),
    path('orders/<int:pk>/rating', views.OrderRatingView.as_view(), name='csat'),
    path('orders/pending/', views.StaffOrders.as_view(), name='staff_orders'),
    path('admin/users/', views.UsersView.as_view(), name='users'),
    path('admin/users/<int:pk>', views.UserDetailsView.as_view(), name='view_user'),
    path('admin/users/new', views.create_staff, name='add_user'),
    path('admin/menus/', views.MenusView.as_view(), name='view_all_menus'),
    path('admin/menus/<int:pk>', views.MenuDetailView.as_view(), name='menu_detail_view'),
    path('admin/menus/<int:menu_id>/items/<int:pk>', views.ItemDetailView.as_view(), name='item_detail_view'),
    path('api/v1/menus/', views.MenuList.as_view(), name='all_menus'),
    path('api/v1/menus/<int:pk>', views.MenuDetail.as_view(), name='modify_menu'),
    path('api/v1/menus/active', views.MenuWithItemList.as_view(), name='active_menu_items'),
    path('api/v1/items/<int:pk>', views.ItemDetail.as_view(), name='item_details'),
    path('api/v1/cart/', views.ViewCartWithItem.as_view(), name='view_cart'),
    path('api/v1/cartitems/', views.ViewCartItem.as_view(), name='view_cart_item'),
    path('api/v1/cartitems/<int:pk>', views.ModifyCartItem.as_view(), name='modify_cart_item'),
    path('api/v1/createorder/', views.CreateOrderWithItems.as_view(), name='create_order'),
    path('api/v1/orders/', views.OrderList.as_view(), name='view_order'),
    path('api/v1/orders/<int:pk>', views.OrderWithItemsDetail.as_view(), name='view_order_detail'),
    path('api/v1/orders/<int:pk>/rating', views.OrderRating.as_view(), name='rate_order'),
    path('api/v1/updateorder/<int:pk>', views.OrderUpdate.as_view(), name='update_order'),
    path('api/v1/users/', views.UserList.as_view(), name='user_list'),
    path('api/v1/users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)