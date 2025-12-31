from datetime import datetime, timedelta
import pytz
from django.utils import timezone
from events.models import Event

def find_available_slots(user_ids, duration_minutes, days_ahead=7):
    """
    Find available meeting slots for multiple users
    
    Args:
        user_ids: List of user IDs to schedule for
        duration_minutes: Duration of meeting in minutes
        days_ahead: Number of days to look ahead (default: 7)
    
    Returns:
        List of available datetime slots in UTC
    """
    if not user_ids:
        return []
    
    from users.models import User
    
    # Get users
    users = User.objects.filter(id__in=user_ids)
    if len(users) != len(user_ids):
        return []  # Some users don't exist
    
    # Calculate time range
    now = timezone.now()
    end_date = now + timedelta(days=days_ahead)
    
    # Get busy events for all users
    busy_events = Event.objects.filter(
        owner__in=users,
        event_type='busy',
        end_time__gte=now,
        start_time__lte=end_date
    ).select_related('owner')
    
    # Group events by user
    user_events = {}
    for user in users:
        user_events[user.id] = [
            event for event in busy_events if event.owner_id == user.id
        ]
    
    # Find common availability
    available_slots = []
    current_time = now.replace(minute=0, second=0, microsecond=0)
    
    # Check every 30 minutes
    while current_time + timedelta(minutes=duration_minutes) <= end_date:
        slot_end = current_time + timedelta(minutes=duration_minutes)
        slot_available = True
        
        for user in users:
            # Check user's working hours in their timezone
            user_tz = pytz.timezone(user.timezone)
            user_local_time = current_time.astimezone(user_tz)
            
            # Skip if outside working hours
            if not (user.working_hours_start <= user_local_time.time() <= user.working_hours_end):
                slot_available = False
                break
            
            # Check for busy events
            for event in user_events.get(user.id, []):
                if event.start_time < slot_end and event.end_time > current_time:
                    slot_available = False
                    break
            
            if not slot_available:
                break
        
        if slot_available:
            available_slots.append(current_time)
        
        current_time += timedelta(minutes=30)
    
    return available_slots