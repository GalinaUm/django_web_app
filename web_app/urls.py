from django.urls import path
from web_app.apps import WebAppConfig
# from web_app.views import

app_name = WebAppConfig.name


urlpatterns = [
    # path('catalog/home/', HomeView.as_view(), name='home'),
    # path('catalog/contacts/', ContactView.as_view(), name='contacts'),
    # path('', ProductListView.as_view(), name='product_list'),
    # path('catalog/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    # path('catalog/create/', ProductCreateView.as_view(), name='product_create'),
    # path('catalog/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    # path('catalog/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]