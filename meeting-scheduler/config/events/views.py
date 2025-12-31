# events/views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # For demo - change to IsAuthenticated later
    
    def get_queryset(self):
        return Event.objects.all()
    
    def perform_create(self, serializer):
        from users.models import User
        
        # Try to get user from request (if authenticated)
        if self.request.user.is_authenticated:
            print(f"Using authenticated user: {self.request.user.username}")
            user = self.request.user
        else:
            # For demo: use first available user
            print("No authenticated user, using first available user")
            user = User.objects.first()
            if not user:
                # Create a demo user if none exists
                user = User.objects.create(
                    username='demo_owner',
                    email='demo@owner.com',
                    timezone='UTC',
                    password='demo123'  # Plain text for demo
                )
        
        # Save event with owner
        serializer.save(owner=user)
        print(f"Event created with owner: {user.username}")