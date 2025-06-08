from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Review, Booking


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model - used for displaying user information
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model
    """
    owner = UserSerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'listing_type', 'price_per_night',
            'location', 'latitude', 'longitude', 'amenities', 'max_guests',
            'is_available', 'owner', 'average_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'average_rating', 'created_at', 'updated_at']
    
    def validate_price_per_night(self, value):
        """Validate that price per night is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0.")
        return value
    
    def validate_max_guests(self, value):
        """Validate that max guests is positive"""
        if value <= 0:
            raise serializers.ValidationError("Max guests must be greater than 0.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model
    """
    reviewer = UserSerializer(read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'listing', 'listing_title', 'reviewer', 'rating',
            'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'listing_title', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        """Validate that rating is between 1 and 5"""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate(self, data):
        """Validate that user hasn't already reviewed this listing"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            listing = data.get('listing')
            
            # Check if this is a new review (not an update)
            if not self.instance:
                existing_review = Review.objects.filter(
                    listing=listing, 
                    reviewer=user
                ).exists()
                
                if existing_review:
                    raise serializers.ValidationError(
                        "You have already reviewed this listing."
                    )
        
        return data


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model
    """
    guest = UserSerializer(read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'guest', 'check_in', 'check_out',
            'guests_count', 'total_price', 'status', 'duration_days',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'guest', 'listing_title', 'duration_days', 
            'created_at', 'updated_at'
        ]
    
    def validate(self, data):
        """Custom validation for booking data"""
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        listing = data.get('listing')
        guests_count = data.get('guests_count')
        
        # Validate check-out is after check-in
        if check_out <= check_in:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )
        
        # Validate guests count doesn't exceed listing capacity
        if listing and guests_count > listing.max_guests:
            raise serializers.ValidationError(
                f"Number of guests ({guests_count}) exceeds maximum capacity "
                f"of {listing.max_guests} for this listing."
            )
        
        # Validate listing is available
        if listing and not listing.is_available:
            raise serializers.ValidationError(
                "This listing is currently not available for booking."
            )
        
        return data
    
    def validate_guests_count(self, value):
        """Validate that guests count is positive"""
        if value <= 0:
            raise serializers.ValidationError("Number of guests must be greater than 0.")
        return value
    
    def validate_total_price(self, value):
        """Validate that total price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Total price must be greater than 0.")
        return value
