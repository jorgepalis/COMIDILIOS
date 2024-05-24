from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, ListCreateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
) 
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    ItemSerializer, OrderSerializer, ItemDetailSerializer, AddressSerializer,
    ItemAttributeSerializer, ItemAttributeDetailSerializer, ShopSerializer, OrderItemSerializer, CouponSerializer, 
    
    CategorySerializer, CategoryDetailSerializer, SubCategorySerializer,
    TagSerializer, 
    AttributeChildSerializer, AttributeSerializer, AttributeDetailSerializer,
    VariationDetailSerializer, VariationSerializer
)
from store.models import ( 
    Item, OrderItem, Order, Address, Variation,
    Payment, Coupon, Shop, Category, SubCategory,
    AttributeChild, Attribute, Tags, ItemAttribute
)
from Auth.models import User

import random
import string
from django.db.models import Q


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'
    # max_page_size = 100

class ShopCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class ShopListView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ShopSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Shop.objects.all().order_by("-id")

        # Filter based on request parameters
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
    
        is_discount = self.request.query_params.get('is_discount', None)
        if is_discount:
            queryset = queryset.filter(is_discount=is_discount)

        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            queryset = queryset.filter(
                Q(item__categories__id=category_id)
            ).distinct()

        # subcategory_id = self.request.query_params.get('subcategory_id', None)
        # if subcategory_id:
        #     queryset = queryset.filter(
        #         Q(item__categories__sub_categories__id=subcategory_id)
        #     ).distinct()

        subcategory_id = self.request.query_params.get('subcategory_id', None)
        if subcategory_id:
            # Get items with the given subcategory_id
            subcategory = SubCategory.objects.get(id=subcategory_id)
            items = Item.objects.filter(categories__sub_categories=subcategory)
            # Extract shop IDs from these items
            shop_ids = set()
            for item in items:
                if item.shop:
                    shop_ids.add(item.shop_id)
            # Filter shops by these IDs
            queryset = queryset.filter(id__in=shop_ids)

        return queryset
    
class ShopDetailView(APIView):
    def get_object(self, pk):
        try:
            return Shop.objects.get(id=pk)
        except Shop.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = ShopSerializer(obj)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = ShopSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    

class TagListView(APIView):
    def get(self, request):
        obj = Tags.objects.all()
        serialized_items = TagSerializer(obj, many=True)
        return Response(serialized_items.data)
    
    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class TagDetailView(APIView):
    def get_object(self, pk):
        try:
            return Tags.objects.get(id=pk)
        except Tags.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = TagSerializer(instance)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = TagSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status= HTTP_204_NO_CONTENT)

class CategoryListView(APIView):
    """ GET /category-list/?shop=1 """
    def get(self, request):
        shop_id = request.GET.get('shop', None)
        if shop_id:
            categories = Category.objects.filter(shop=shop_id)  # Filter by shop_id
        else:
            categories = Category.objects.all()

        serialized_items = CategoryDetailSerializer(categories, many=True)
        return Response(serialized_items.data)
    
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
class CategoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = CategoryDetailSerializer(instance)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = CategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status= HTTP_204_NO_CONTENT)

class SubCategoryView(APIView):
    def get(self, request):
        obj = SubCategory.objects.all()
        serialized_items = SubCategorySerializer(obj, many=True)
        return Response(serialized_items.data)
    
    def post(self, request, *args, **kwargs):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
class SubCategoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return SubCategory.objects.get(id=pk)
        except SubCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = SubCategorySerializer(instance)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = SubCategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status= HTTP_204_NO_CONTENT)

class AttributeView(APIView):
    def get(self, request):
        obj = Attribute.objects.all()
        serialized_items = AttributeDetailSerializer(obj, many=True)
        return Response(serialized_items.data)
    
    def post(self, request, *args, **kwargs):
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
class AttributeDetailView(APIView):
    def get_object(self, pk):
        try:
            return Attribute.objects.get(id=pk)
        except Attribute.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = AttributeSerializer(instance)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = AttributeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status= HTTP_204_NO_CONTENT)

class AttributeChildView(APIView):
    def get(self, request):
        obj = AttributeChild.objects.all()
        serialized_items = AttributeChildSerializer(obj, many=True)
        return Response(serialized_items.data)
    
    def post(self, request, *args, **kwargs):
        serializer = AttributeChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
class AttributeChildDetailView(APIView):
    def get_object(self, pk):
        try:
            return AttributeChild.objects.get(id=pk)
        except AttributeChild.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = AttributeChildSerializer(instance)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = AttributeChildSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status= HTTP_204_NO_CONTENT)


class ItemAttributeListView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ItemAttributeDetailSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ItemAttribute.objects.all().order_by("-id")

        # Filter based on request parameters
        item_id = self.request.query_params.get('item_id', None)
        if item_id:
            queryset = queryset.filter(item=item_id)

        attribute_id = self.request.query_params.get('attribute_id', None)
        if attribute_id:
            queryset = queryset.filter(attribute=attribute_id)
        
        return queryset

class ItemAttributeCreateView(APIView):
    def post(self, request, *args, **kwargs):
        item_obj = Item.objects.get(id=request.data.get("item"))
        attribute_obj = Attribute.objects.get(id=request.data.get("attribute"))
        
        ItemAttribute.objects.create(item=item_obj, attribute=attribute_obj)
       
        return Response({"message": "Successfull"}, status= HTTP_201_CREATED)
    
class ItemAttributeDetailView(APIView):
    def get_object(self, pk):
        try:
            return ItemAttribute.objects.get(id=pk)
        except ItemAttribute.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = ItemAttributeDetailSerializer(instance)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        print(request.data)
        serializer = ItemAttributeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status= HTTP_204_NO_CONTENT)


class VariationListView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VariationDetailSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Variation.objects.all().order_by("-id")

        # Filter based on request parameters
        attribute_id = self.request.query_params.get('attribute_id', None)
        if attribute_id:
            queryset = queryset.filter(attribute=attribute_id)
        
        return queryset

class VariationCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VariationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({"message": "Successfull"}, status= HTTP_201_CREATED)
    
class VariationDetailView(APIView):
    def get_object(self, pk):
        try:
            return Variation.objects.get(id=pk)
        except Variation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = VariationDetailSerializer(instance)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        print(request.data)
        serializer = VariationSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status= HTTP_204_NO_CONTENT)


class VariationClassificationAPIView(APIView):
    def get(self, request):
        # Fetch all variations
        variations = Variation.objects.all()

        # Dictionary to store variations classified by attribute
        variations_by_attribute = {}

        # Classify variations based on attribute
        for variation in variations:
            attribute_id = variation.attribute.id
            if attribute_id not in variations_by_attribute:
                variations_by_attribute[attribute_id] = []
            variations_by_attribute[attribute_id].append({
                'id': variation.id,
                'price': variation.price,
                # Add other fields if needed
            })

        # Return the classified variations as JSON response
        return Response(variations_by_attribute)
    
       
class UpdateItemVariation(APIView):
    def post(self, request, format=None):
        item_ids = request.data.get('item_ids', [])  # Assuming item_ids are passed in the request data
        variations_ids = request.data.get('variations_ids', [])  # Assuming variations_ids are passed in the request data
        
        print(request.data)
        
        if not item_ids:
            return Response({"error": "No item IDs provided"}, status=HTTP_400_BAD_REQUEST)
        
        if not variations_ids:
            return Response({"error": "No variations IDs provided"}, status=HTTP_400_BAD_REQUEST)
        
        try:
            items = Item.objects.filter(pk__in=item_ids)

            # Add variations to each item
            for item in items:
                item.variations.add(*variations_ids)
                item.save()
                
            return Response({"message": "Item vendor status and variations updated successfully"}, status=HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({"error": "One or more item IDs are invalid"}, status=HTTP_404_NOT_FOUND)
        

class ItemListView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ItemDetailSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user=self.request.user
        queryset = Item.objects.all().order_by("-id")
        # print(queryset)

        # if user.is_vendor:
        #     shop = Shop.objects.get(user=user)
        #     queryset = queryset.filter(shop_id=shop.id)


        # Filter based on request parameters
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        shop_id = self.request.query_params.get('shop_id', None)
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)

        tag_id = self.request.query_params.get('tag_id', None)
        if tag_id:
            tag = Tags.objects.get(id=tag_id)
            queryset = queryset.filter(tags=tag)
        
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            category = Category.objects.get(id=category_id)
            queryset = queryset.filter(categories=category)

        subcategory_id = self.request.query_params.get('subcategory_id', None)
        if subcategory_id:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            queryset = queryset.filter(categories__sub_categories=subcategory)
        
        return queryset

class ItemCreatView(APIView):
    def post(self, request, *args, **kwargs):
        # print(request.data)
        shop_id = request.data.get('shop')
        obj = None
        user = request.user
        if user.is_vendor:
            obj = Shop.objects.get(user=user)
        else:
            obj = Shop.objects.get(id=shop_id)


        serializer = ItemSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            serializer.validated_data['shop'] = obj  
            serializer.save()

            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
class ItemDetailView(APIView):
    def get_object(self, pk):
        try:
            return Item.objects.get(id=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = ItemDetailSerializer(instance)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = ItemSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status= HTTP_204_NO_CONTENT)


class AddCategoryToItemAPIView(APIView):

    def put(self, request, pk, format=None):
        try:
            category_data = request.data
            item = Item.objects.get(id=pk)
            IDs = None

            for category_or_combo in category_data:
                try:
                    category_id, subcategory_id = category_or_combo.split('-')
                    category_id = int(category_id)
                    subcategory_id = int(subcategory_id)
                    category = Category.objects.get(pk=category_id)
                    subcategory = category.sub_categories.get(pk=subcategory_id)

                    # Update selected_sub_categories_id if subcategory ID is not already present
                    if IDs:
                        id = IDs.split(',')
                        if category_or_combo not in id:
                            IDs += f",{category_or_combo}"
                    else:
                        IDs = category_or_combo

                    # Add category and update subcategory's isChecked (optional)
                    item.selected_cat_sub_categories_id = IDs
                    item.categories.add(category)
                    item.save()

                except (ValueError, Item.DoesNotExist, Category.DoesNotExist, SubCategory.DoesNotExist):
                    return Response({'error': 'Invalid data or object not found'}, status=HTTP_400_BAD_REQUEST)

            # Serialize and return the updated item (optional)
            # serializer = CategorySerializer(item.categories.all(), context={'request': request}, many=True)
            # return Response(serializer.data, status=HTTP_200_OK)

            return Response({'message': 'Categories and/or subcategories added successfully'}, status=HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        

class OrderItemListView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OrderItemSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = OrderItem.objects.all().order_by("-id")

        # Filter based on request parameters
        shop_id = self.request.query_params.get('shop_id', None)
        if shop_id:
            queryset = queryset.filter(item__shop_id=shop_id)

        ordered = self.request.query_params.get('ordered', None)
        if ordered:
            queryset = queryset.filter(ordered=True)
        
        
        return queryset

class OrderItemDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = OrderItem.objects.all()


# class AddToCartView(APIView):
#     def post(self, request, pk, *args, **kwargs):
#         item = get_object_or_404(Item, id=pk)
#         shop_instance = Shop.objects.get(id=item.shop.id)

#         order_qs = Order.objects.filter(user=request.user, ordered=False)
#         if order_qs.exists():
#             if order_qs[0].shop == shop_instance:
#                 print("Shop exist")
#             else:
#                 return Response({"message": "Invalid Shop received"}, status=HTTP_400_BAD_REQUEST)


#         order_item_qs = OrderItem.objects.filter(
#             item=item,
#             user=request.user,
#             ordered=False
#         )

#         if order_item_qs.exists():
#             order_item = order_item_qs.first()
#             order_item.quantity += 1
#             order_item.save()
#         else:
#             order_item = OrderItem.objects.create(
#                 item=item,
#                 user=request.user,
#                 ordered=False
#             )
#             order_item.save()

#         order_qs = Order.objects.filter(user=request.user, ordered=False)
#         if order_qs.exists():
#             order = order_qs[0]
#             if not order.items.filter(item__id=order_item.id).exists():
#                 order.items.add(order_item)
#                 return Response({"message": "Order Updated"}, status=HTTP_200_OK)
#         else:
#             ordered_date = timezone.now()
#             order = Order.objects.create(
#                 user=request.user, ordered_date=ordered_date, shop=shop_instance)
#             order.items.add(order_item)
#             return Response({"message": "Order Created"}, status=HTTP_200_OK)


class AddToCartView(APIView):
    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(Item, id=pk)
        shop_instance = Shop.objects.get(id=item.shop.id)
        
        # Extract variations from request data
        variations = request.data.get('variations', [])

        # Retrieve Variation instances
        variation_instances = []
        for variation_id in variations:
            variation = get_object_or_404(Variation, id=variation_id)
            variation_instances.append(variation)

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            if order_qs[0].shop == shop_instance:
                print("Shop exist")
            else:
                return Response({"message": "Invalid Shop received"}, status=HTTP_400_BAD_REQUEST)

        # Check for existing OrderItem with the same item and variations
        order_item_qs = OrderItem.objects.filter(
            item=item,
            user=request.user,
            ordered=False
        ).prefetch_related('item_variations')

        for order_item in order_item_qs:
            if set(order_item.item_variations.all()) == set(variation_instances):
                order_item.quantity += 1
                order_item.save()
                break
        else:
            # If no existing OrderItem is found, create a new one
            order_item = OrderItem.objects.create(
                item=item,
                user=request.user,
                ordered=False
            )
            order_item.item_variations.set(variation_instances)
            order_item.save()

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if not order.items.filter(id=order_item.id).exists():
                order.items.add(order_item)
                return Response({"message": "Order Updated"}, status=HTTP_200_OK)
            return Response({"message": "OrderItem quantity updated"}, status=HTTP_200_OK)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date, shop=shop_instance)
            order.items.add(order_item)
            return Response({"message": "Order Created"}, status=HTTP_200_OK)

class OrderQuantityUpdateView(APIView):
    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(Item, id=pk)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item_id=item.id).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order.items.remove(order_item)
                return Response(status=HTTP_200_OK)
            else:
                return Response({"message": "This item was not in your cart"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You do not have an active order"}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
        
            order.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class OrderDeleteView(APIView):
    def delete(self, request, format=None):
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            order.items.all().delete()
            order.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class OrderDashboardView(APIView):
    def get(self, request, format=None):
        queryset = Order.objects.all()

        being_delivered = queryset.filter(being_delivered=True).count()
        received = queryset.filter(received=True).count()
        all_order = queryset.count()

        response_data = {
            'pending': being_delivered,
            'completed': received,
            'total': all_order,
            'cancel': 0
        }
        return Response(response_data)

class TotalSumView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        queryset = Order.objects.filter(rider_id=pk, received=True)
        total_sum = 0

        serializer = OrderSerializer(queryset, many=True)
        for order_data in serializer.data:
            total_sum += order_data['total']  # Summing up the total from each order

        return Response({
            'total_sum': total_sum
        })
        
class OrderListView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Order.objects.all()

        # Filter based on request parameters
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            # queryset = queryset.filter(user_id=user_id, ordered=False, payment__isnull=True)
            queryset = queryset.filter(user_id=user_id)
        
        user_id_1 = self.request.query_params.get('user_id_1', None)
        if user_id_1:
            queryset = queryset.filter(user_id=user_id_1, ordered=True, payment__isnull=False)
        
        user_id_2 = self.request.query_params.get('user_id_2', None)
        if user_id_2:
            queryset = queryset.filter(user_id=user_id_2)
            
        rider_id = self.request.query_params.get('rider_id', None)
        if rider_id:
            queryset = queryset.filter(rider_id=rider_id)
            
        ordered_f = self.request.query_params.get('ordered_f', None)
        if ordered_f:
            queryset = queryset.filter(ordered=False)
            
        ordered_t = self.request.query_params.get('ordered_t', None)
        if ordered_t:
            queryset = queryset.filter(ordered=True)
            
        rider_t = self.request.query_params.get('rider_t', None)
        if rider_t:
            queryset = queryset.filter(rider__isnull=True)

        rider_f = self.request.query_params.get('rider_f', None)
        if rider_f:
            queryset = queryset.filter(rider__isnull=False)
        
        being_delivered = self.request.query_params.get('being_delivered', None)
        if being_delivered:
            queryset = queryset.filter(being_delivered=True)
        
        received = self.request.query_params.get('received', None)
        if received:
            queryset = queryset.filter(received=True)

        received_f = self.request.query_params.get('received_f', None)
        if received_f:
            queryset = queryset.filter(received=False)

        shop_id = self.request.query_params.get('shop_id', None)
        if shop_id:
            shop_instance = Shop.objects.get(id=shop_id)
            queryset = queryset.filter(items__item__shop=shop_instance)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        being_delivered = queryset.filter(being_delivered=True, received=False).count()
        received = queryset.filter(being_delivered=True, received=True).count()
        newOrder = queryset.filter(rider__isnull=True, received=False, being_delivered=False).count()

        # Order the queryset by id
        queryset = queryset.order_by('-id')

        total_sum = 0 

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for order_data in serializer.data:
                total_sum += order_data['total'] 

            response_data = {
                'results': serializer.data,
                'being_delivered': being_delivered,
                'received': received,
                'newOrder': newOrder,
                'total_sum': total_sum,
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        for order_data in serializer.data:
            total_sum += order_data['total'] 

        response_data = {
            'results': serializer.data,
            'being_delivered': being_delivered,
            'received': received,
            'newOrder': newOrder,
            'total_sum': total_sum,
        }

        return Response(response_data)

class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return order
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order")
            # return Response({"message": "You do not have an active order"}, status=HTTP_400_BAD_REQUEST)

class OrderDetailView2(APIView):
    def get(self, request, pk, format=None):
        try:
            order = Order.objects.get(id=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order")
            # return Response({"message": "You do not have an active order"}, status=HTTP_400_BAD_REQUEST)
        
class OrderUpdateView(APIView):
    def put(self, request, pk, format=None):
        inatance = Order.objects.get(id=pk)
        serializer = OrderSerializer(inatance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Order successfully assigned "} ,status=HTTP_200_OK)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        instance = Order.objects.get(id=pk)
        serializer = OrderSerializer(instance)
        instance.received = True
        instance.save()
        return Response({
            "message": "Order successfully completed!",
            "result": serializer.data
            } ,status=HTTP_200_OK)

class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        order = Order.objects.get(user=user, ordered=False)
        
        # create the payment
        payment = Payment()
        payment.user = user
        payment.amount = order.get_total()
        payment.save()

        # assign the payment to the order
        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()
            # pass

        order.ordered = True
        order.payment = payment
        order.ref_code = create_ref_code()
        order.save()

        return Response({"message": "Your order was successful!"} ,status=HTTP_200_OK)
        
class CreateCouponView(APIView):
    def get(self, request, format=None):
        queryset = Coupon.objects.all()
        serializerPqrs = CouponSerializer(queryset, many=True)
        return Response( serializerPqrs.data)

    def post(self, request, *args, **kwargs):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
class CouponDetailView(APIView):
    def put(self, request, pk, format=None):
        inatance = Coupon.objects.get(id=pk)
        serializer = CouponSerializer(inatance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        inatance = Coupon.objects.get(id=pk)
        inatance.delete()
        return Response(status= HTTP_200_OK)
                        
class AddCouponView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code', None)
        if code is None:
            return Response({"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST)
        order = Order.objects.get(
            user=self.request.user, ordered=False)
        coupon = get_object_or_404(Coupon, code=code)
        order.coupon = coupon
        order.save()
        return Response(status=HTTP_200_OK)


class AddressListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AddressSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user=self.request.user
        queryset = Address.objects.filter(user=user).order_by("-id")

        # Filter based on request parameters
        address_type = self.request.query_params.get('address_type', None)
        if address_type:
            queryset = queryset.filter(address_type=address_type)

        default = self.request.query_params.get('default', None)
        if default:
            queryset = queryset.filter(default=True)

        return queryset

class AddressCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = user  
            serializer.save()

            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
  
class AddressUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

class AddressDetailView(APIView):
    def get(self, request, pk, format=None):
        user = User.objects.get(id=pk)
        instance = Address.objects.get(user=user)
        serializer = AddressSerializer(instance)
        return Response(serializer.data)

class AddressDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Address.objects.all()

class AddressDefaultAPIView(APIView):
    def get(self, request, pk, format=None):
        user=request.user
        qs = Address.objects.filter(user=user)

        for data in qs:
            data.default = False
            data.save()

        instance = Address.objects.get(id=pk)
        instance.default = True
        instance.save()

        return Response("Successfully updated for instances", status=HTTP_200_OK)
    