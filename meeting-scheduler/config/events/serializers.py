from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'owner', 'owner_username', 
                 'start_time', 'end_time', 'event_type', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Check that start_time is before end_time.
        """
        if 'start_time' in data and 'end_time' in data:
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError("End time must be after start time")
        return data