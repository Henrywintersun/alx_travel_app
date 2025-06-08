from django.contrib import admin
from .models import Listing, Review, Booking


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'listing_type', 'location', 'price_per_night', 'is_available', 'owner', 'created_at']
    list_filter = ['listing_type', 'is_available', 'created_at']
    search_fields = ['title', 'location', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'description', 'listing_type')
        }),
        ('Pricing & Availability', {
            'fields': ('price_per_night', 'max_guests', 'is_available')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Additional Info', {
            'fields': ('amenities', 'owner')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['listing', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['listing__title', 'reviewer__username', 'comment']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Review Information', {
            'fields': ('id', 'listing', 'reviewer', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing', 'guest', 'check_in', 'check_out', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at', 'check_in']
    search_fields = ['guest__username', 'listing__title']
    readonly_fields = ['id', 'created_at', 'updated_at', 'duration_days']
    list_per_page = 25
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('id', 'listing', 'guest', 'status')
        }),
        ('Stay Details', {
            'fields': ('check_in', 'check_out', 'duration_days', 'guests_count')
        }),
        ('Pricing', {
            'fields': ('total_price',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
