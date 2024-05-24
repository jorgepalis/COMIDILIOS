from rest_framework import serializers
from Auth.serializers import UserSerializer
from .models import (
    Address, Item, Order, OrderItem, Coupon, Tags, SubCategory,
    Payment, Shop, Category, Attribute, AttributeChild, ItemAttribute, Variation
)

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryDetailSerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)
    
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name', 'description']

class VariationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Variation
        fields = '__all__'

class VariationDetailSerializer(serializers.ModelSerializer):
    attribute = serializers.SerializerMethodField()
    child = serializers.SerializerMethodField()
    # item = serializers.SerializerMethodField()
    # child = AttributeChildSerializer(many=True)
    
    class Meta:
        model = Variation
        fields = '__all__'
    
    def get_attribute(self, obj):
        return AttributeDetailSerializer(obj.attribute).data
        
    def get_child(self, obj):
        return AttributeChildSerializer(obj.child).data
        
    # def get_item(self, obj):
    #     return ItemSerializer(obj.item).data
        

class AttributeChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeChild
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class AttributeDetailSerializer(serializers.ModelSerializer):
    attribute_child = AttributeChildSerializer(many=True)
    
    class Meta:
        model = Attribute
        fields = '__all__'


class ItemAttributeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ItemAttribute
        fields = '__all__'
    
class ItemAttributeDetailSerializer(serializers.ModelSerializer):
    attribute = serializers.SerializerMethodField()
    value = AttributeChildSerializer(many=True)
    item = serializers.SerializerMethodField()
    
    class Meta:
        model = ItemAttribute
        fields = '__all__'

    def get_attribute(self, obj):
        return AttributeDetailSerializer(obj.attribute).data
    
    def get_item(self, obj):
        return ItemSerializer(obj.item).data
    
        
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'amount', 'shop']

class ItemSerializer(serializers.ModelSerializer):
    shop = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'categories', 'description', 'attributes', 'tags', 'price', 'inventory', 'discount_price', 'image', 'shop']

    def get_shop(self, obj):
        return ShopSerializer(obj.shop).data
        
class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'item',
            'quantity',
            'final_price',
            'shop'
        )

    def get_item(self, obj):
        return ItemSerializer(obj.item).data
    
    def get_final_price(self, obj):
        return obj.get_final_price()

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'id',
            'user',
            'address',
            'lng',
            'lat',
            'zip',
            'address_type',
            'default'
        )

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    shop = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'rider',
            'order_items',
            'total',
            'ordered',
            'coupon',
            'being_delivered',
            'received',
            'ref_code',
            'address',
            'ordered_date',
            'shop'
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.items.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()

    def get_coupon(self, obj):
        if obj.coupon is not None:
            return CouponSerializer(obj.coupon).data
        return None
    
    def get_user(self, obj):
        return UserSerializer(obj.user).data
    
    def get_address(self, obj):
        default_address = obj.user.address_set.filter(default=True).first()
        if default_address:
            return AddressSerializer(default_address).data
        return None
    
    def get_shop(self, obj):
        return ShopSerializer(obj.shop).data

class ItemDetailSerializer(serializers.ModelSerializer):
    categories = CategoryDetailSerializer(many=True)
    tags = TagSerializer(many=True)
    variations = VariationDetailSerializer(many=True)
    attributes = AttributeDetailSerializer(many=True)
    shop = serializers.SerializerMethodField()
    # item_attributes = serializers.SerializerMethodField()
    attribute_variations = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"

    def get_shop(self, obj):
        return ShopSerializer(obj.shop).data
    
    # def get_attribute_variations(self, obj):
    #     attribute_variations = {}
    #     for variation in obj.variations.all():
    #         attribute_name = variation.attribute.name
    #         if attribute_name not in attribute_variations:
    #             attribute_variations[attribute_name] = []
    #         attribute_variations[attribute_name].append(VariationSerializer(variation).data)
    #     return attribute_variations

    def get_attribute_variations(self, obj):
        attribute_variations = []
        attribute_map = {}

        for variation in obj.variations.all():
            attribute_name = variation.attribute.name
            variation_data = VariationDetailSerializer(variation).data

            if attribute_name not in attribute_map:
                attribute_map[attribute_name] = {
                    'attribute_name': attribute_name,
                    'attribute_values': []
                }
                attribute_variations.append(attribute_map[attribute_name])

            attribute_map[attribute_name]['attribute_values'].append(variation_data)

        return attribute_variations
    
    # def get_item_attributes(self, obj):
    #     return ItemAttributeDetailSerializer(obj.itemattribute_set.all(), many=True).data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'amount',
            'timestamp'
        )