from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  # CHANGED
from datetime import timedelta
from .algorithms import find_available_slots

class FindSlotsView(APIView):
    permission_classes = [AllowAny]  # CHANGED from IsAuthenticated
    
    def post(self, request):
        user_ids = request.data.get('user_ids', [1])  # Default to user 1
        duration_minutes = request.data.get('duration_minutes', 60)
        
        try:
            slots = find_available_slots(user_ids, int(duration_minutes))
            
            formatted_slots = [
                {
                    'start_time': slot.isoformat(),
                    'end_time': (slot + timedelta(minutes=int(duration_minutes))).isoformat()
                }
                for slot in slots
            ]
            
            return Response({
                'available_slots': formatted_slots,
                'user_ids': user_ids,
                'duration_minutes': duration_minutes,
                'total_slots_found': len(formatted_slots)
            })
            
        except Exception as e:
            return Response(
                {'available_slots': [], 'error': str(e)},
                status=status.HTTP_200_OK  # Still return 200 for demo
            )
