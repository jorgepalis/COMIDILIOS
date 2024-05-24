from django.contrib import admin

from .models import (
    Item, OrderItem, Order, Payment, Coupon, Refund,
    Address, Shop, Category, Variation,
    Attribute, AttributeChild, Tags, SubCategory,
    ItemAttribute
)


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'rider',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'ordered',
                    'item',
                    'quantity'
                    ]
    list_display_links = [
        'user'
    ]
    list_filter = ['ordered'
                   ]
    search_fields = [
        'user__username'
    ]

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'address',
        'lng',
        'lat',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type']
    search_fields = ['user', 'address', 'lat', 'lng', 'zip']

class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_discount']
    list_filter = ['is_discount']
    search_fields = ['name']


admin.site.register(Variation)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(ItemAttribute)
admin.site.register(AttributeChild)
admin.site.register(Attribute)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)