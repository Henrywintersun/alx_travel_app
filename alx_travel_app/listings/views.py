from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Listing, Review, Booking
from .serializers import ListingSerializer, ReviewSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing travel listings.
    
    Provides CRUD operations for listings with filtering, searching, and ordering capabilities.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['listing_type', 'is_available', 'location']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'price_per_night', 'title']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Set the owner to the current user when creating a listing."""
        serializer.save(owner=self.request.user)
    
    @swagger_auto_schema(
        method='get',
        responses={200: ListingSerializer(many=True)},
        operation_description="Get listings owned by the current user"
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_listings(self, request):
        """Get listings owned by the current user."""
        listings = self.queryset.filter(owner=request.user)
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        method='get',
        responses={200: ReviewSerializer(many=True)},
        operation_description="Get all reviews for a specific listing"
    )
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific listing."""
        listing = self.get_object()
        reviews = listing.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reviews.
    
    Allows users to create, read, update, and delete reviews for listings.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['rating', 'listing']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Set the reviewer to the current user when creating a review."""
        serializer.save(reviewer=self.request.user)
    
    @swagger_auto_schema(
        method='get',
        responses={200: ReviewSerializer(many=True)},
        operation_description="Get reviews created by the current user"
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_reviews(self, request):
        """Get reviews created by the current user."""
        reviews = self.queryset.filter(reviewer=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    
    Handles booking creation, retrieval, updates, and cancellation.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'listing']
    ordering_fields = ['created_at', 'check_in', 'check_out']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter bookings to only show those belonging to the current user."""
        return self.queryset.filter(guest=self.request.user)
    
    def perform_create(self, serializer):
        """Set the guest to the current user when creating a booking."""
        serializer.save(guest=self.request.user)
    
    @swagger_auto_schema(
        method='post',
        responses={200: openapi.Response('Booking cancelled successfully')},
        operation_description="Cancel a booking"
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking."""
        booking = self.get_object()
        
        if booking.status == 'cancelled':
            return Response(
                {'detail': 'Booking is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.status == 'completed':
            return Response(
                {'detail': 'Cannot cancel a completed booking.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        return Response({'detail': 'Booking cancelled successfully.'})
    
    @swagger_auto_schema(
        method='post',
        responses={200: openapi.Response('Booking confirmed successfully')},
        operation_description="Confirm a booking"
    )
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking."""
        booking = self.get_object()
        
        if booking.status != 'pending':
            return Response(
                {'detail': 'Only pending bookings can be confirmed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'confirmed'
        booking.save()
        
        return Response({'detail': 'Booking confirmed successfully.'})
