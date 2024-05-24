from django.urls import path
from .views import (
    ItemListView, ItemDetailView, ItemCreatView, 
    ShopListView, ShopDetailView, ShopCreateView,

    OrderDetailView, OrderDetailView2, OrderQuantityUpdateView, OrderListView,
    OrderItemDeleteView, OrderItemListView, OrderUpdateView, OrderDeleteView,
    CreateCouponView, CouponDetailView, PaymentView, 
    OrderDashboardView, TotalSumView, AddToCartView, AddCouponView,

    AddressListView, AddressCreateView, AddressUpdateView, AddressDeleteView, 
    AddressDetailView, AddressDefaultAPIView,

    TagListView, TagDetailView, AddCategoryToItemAPIView,
    CategoryListView, CategoryDetailView, SubCategoryView, SubCategoryDetailView,
    AttributeDetailView, AttributeView, AttributeChildView,
    ItemAttributeListView, ItemAttributeDetailView, ItemAttributeCreateView,
    VariationCreateView, VariationListView, VariationDetailView, UpdateItemVariation, 
    AttributeChildDetailView, VariationClassificationAPIView
)

urlpatterns = [
    path('addresses/', AddressListView.as_view()),
    path('addresses/create/', AddressCreateView.as_view()),
    path('addresses/<pk>/update/', AddressUpdateView.as_view()),
    path('addresses/<pk>/defualt/', AddressDefaultAPIView.as_view()),
    path('addresses/<pk>/delete/',AddressDeleteView.as_view()),
    path('addresses/<pk>/detail/',AddressDetailView.as_view()),

    path('shops/', ShopListView.as_view()),
    path('shops-create/', ShopCreateView.as_view()),
    path('shop-detail/<pk>/', ShopDetailView.as_view()),
    
    path('tag-list/', TagListView.as_view()),
    path('tag/<pk>/', TagDetailView.as_view()),
    path('category-list/', CategoryListView.as_view()),
    path('categories/<pk>/', CategoryDetailView.as_view()),
    path('sub-categories/', SubCategoryView.as_view()),
    path('sub-categories/<pk>/', SubCategoryDetailView.as_view()),

    path('products/', ItemListView.as_view()),
    path('products-create/', ItemCreatView.as_view()),
    path('products/<pk>/', ItemDetailView.as_view()),
    path('product-category/<pk>/', AddCategoryToItemAPIView.as_view()),

    path('attributes/', AttributeView.as_view()),
    path('attributes/<pk>/', AttributeDetailView.as_view()),

    path('attributes-child/', AttributeChildView.as_view()),
    path('attributes-child/<pk>/', AttributeChildDetailView.as_view()),

    path('item-attributes-list/', ItemAttributeListView.as_view()),
    path('item-attributes-create/', ItemAttributeCreateView.as_view()),
    path('item-attributes/<pk>/', ItemAttributeDetailView.as_view()),

    path('variation-list/', VariationListView.as_view()),
    path('variation-create/', VariationCreateView.as_view()),
    path('variation/<pk>/', VariationDetailView.as_view()),

    path('update_item_variation/', UpdateItemVariation.as_view()),
    path('variations/classification/', VariationClassificationAPIView.as_view()),


    path('add-to-cart/<pk>/', AddToCartView.as_view()),
    path('order/update-quantity/<pk>/', OrderQuantityUpdateView.as_view()),
    path('order/delete/', OrderDeleteView.as_view()),
    path('order-summary/', OrderDetailView.as_view()),
    path('order-detail/<pk>/', OrderDetailView2.as_view()),
    path('checkout/', PaymentView.as_view()),

    path('create-coupon/', CreateCouponView.as_view()),
    path('detail-coupon/<pk>/', CouponDetailView.as_view()),
    path('add-coupon/', AddCouponView.as_view()),
    
    path('order-items-list/', OrderItemListView.as_view()),
    path('order-items/<pk>/delete/', OrderItemDeleteView.as_view()),
    
    path('order-list/', OrderListView.as_view()),
    path('order-dash/', OrderDashboardView.as_view()),
    path('order-rider-sum/<pk>/', TotalSumView.as_view()),
    path('order/<pk>/', OrderUpdateView.as_view()),
]