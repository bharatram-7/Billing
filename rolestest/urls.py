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
    path('login/', auth_views.LoginView.as_view(template_name="authentication/login.html",
                                                         authentication_form=UserLoginForm,
                                                         redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menu/', ActiveMenuList.as_view(), name='menu'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('orders/', views.Orders.as_view(), name='order'),
    path('orders/<int:pk>', views.OrderItems.as_view(), name='order_detail'),
    path('orders/pending/', views.StaffOrders.as_view(), name='staff_orders'),
    path('admin/users/', views.UsersView.as_view(), name='users'),
    path('admin/users/<int:pk>', views.UserDetailsView.as_view(), name='view_user'),
    path('admin/users/new', views.createStaff, name='add_user'),
    path('api/v1/menu/active', views.MenuList.as_view(), name='active_menu_items'),
    path('api/v1/cart/', views.ViewCartWithItem.as_view(), name='view_cart'),
    path('api/v1/cartitem/', views.ViewCartItem.as_view(), name='view_cart_item'),
    path('api/v1/cartitem/<int:pk>', views.ModifyCartItem.as_view(), name='modify_cart_item'),
    path('api/v1/createorder/', views.CreateOrderWithItems.as_view(), name='create_order'),
    path('api/v1/orders/', views.OrderList.as_view(), name='view_order'),
    path('api/v1/orders/<int:pk>', views.OrderWithItemsDetail.as_view(), name='view_order_detail'),
    path('api/v1/updateorder/<int:pk>', views.OrderUpdate.as_view(), name='update_order'),
    path('api/v1/purchaseditems/', views.PurchasedItemList.as_view(), name='view_purchased_items'),
    path('api/v1/users/', views.UserList.as_view(), name='user_list'),
    path('api/v1/users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)