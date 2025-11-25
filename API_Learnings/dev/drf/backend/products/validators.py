# products/validators.py

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product # Assuming your models are accessible via relative import

# --- External Validator Function ---

def validate_title_no_hello(value):
    """
    Custom function-based validator to ensure the word 'hello' is not in the title.
    """
    if "hello" in value.lower():
        raise serializers.ValidationError(f"The word 'hello' is not allowed in the title.")
    return value


# --- External Validator Instance (Unique Check) ---

# This creates an instance of UniqueValidator targeted at the Product model's title field.
# We use 'iexact' (case-insensitive) lookup for a better uniqueness check, as seen in the video.
unique_product_title = UniqueValidator(
    queryset=Product.objects.all(),
    lookup='iexact', # Ensures case-insensitive checking 
    message="This product title already exists (case-insensitive)."
)