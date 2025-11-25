# products/serializers.py

from rest_framework import serializers
from .models import Product
# Assuming these imports exist in your project structure
from .validators import validate_title_no_hello, unique_product_title 


class ProductSerializer(serializers.ModelSerializer):
    # 1. READ-ONLY USER FIELD (New)
    # Exposes the user's ID but prevents users from setting it directly.
    user = serializers.IntegerField(source='user.id', read_only=True) 

    # 2. WRITE-ONLY EMAIL FIELD (Custom Data)
    email = serializers.EmailField(write_only=True) 

    # 3. TITLE FIELD WITH CUSTOM VALIDATORS (New Validation)
    title = serializers.CharField(
        validators=[unique_product_title, validate_title_no_hello] 
    )

    # 4. DEFAULT FIELDS
    url = serializers.HyperlinkedIdentityField(
        view_name='products-detail',
        lookup_field='pk'
    )
    my_discount = serializers.SerializerMethodField(read_only=True)
    sale_price = serializers.ReadOnlyField(source='get_sale_price')

    class Meta:
        model = Product
        fields = [
            'id',
            'user',        # <-- New: Exposed user ID
            'url',
            'email',       # <-- New: Write-only field
            'title',       # <-- Uses re-declared field with custom validators
            'content',
            'price',
            'sale_price',
            'my_discount'
        ]

    # --- 5. OBJECT-LEVEL VALIDATION (Custom Business Logic) ---
    def validate(self, data):
        """
        Ensures content and title are not identical.
        Runs after field-level validators pass.
        """
        content = data.get('content', None)
        title = data.get('title', None)
        
        if content == title:
            # Raise ValidationError on the serializer instance
            raise serializers.ValidationError("Content and Title cannot be the same.")
        
        return data

    # --- 6. OVERRIDE create() (Handles custom 'email' field) ---
    def create(self, validated_data):
        # POP the custom field out before passing data to Product.objects.create()
        email = validated_data.pop('email') 
        
        # Call the parent's create method
        obj = super().create(validated_data)
        
        # Custom action
        print(f"[ACTION] Sending hypothetical email to: {email} regarding new product: {obj.title}") 
        
        return obj

    # --- 7. OVERRIDE update() (Handles custom 'email' field) ---
    def update(self, instance, validated_data):
        # POP the custom field out (optional in an update)
        email = validated_data.pop('email', None) 
        
        # Call the parent's update method
        instance = super().update(instance, validated_data)

        # Custom action
        if email:
             print(f"[ACTION] Sending notification to: {email} about product update: {instance.title}") 

        return instance
        
    # --- 8. SERIALIZER METHOD FIELD ---
    def get_my_discount(self, obj):
        if not hasattr(obj, 'id') or obj.id is None:
            return None
        try:
            return obj.get_discount()
        except AttributeError:
            return 0