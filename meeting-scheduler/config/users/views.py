# users/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import UserSerializer
from .models import User  # Import your User model

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Get the data
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        timezone = request.data.get('timezone', 'UTC')
        
        # Validate required fields
        if not username or not password or not email:
            return Response(
                {'error': 'Username, password, and email are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create user with hashed password
            user = User.objects.create(
                username=username,
                email=email,
                timezone=timezone,
                password=make_password(password)  # Hash the password!
            )
            
            # Auto-login after registration
            login(request, user)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        print(f"LOGIN ATTEMPT: username={username}")
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Find the user
            user = User.objects.get(username=username)
            print(f"User found: {user.username}")
            
            # Check password - use check_password for hashed passwords
            if check_password(password, user.password):
                print("Password is correct!")
                login(request, user)
                
                return Response({
                    'message': 'Login successful',
                    'user': UserSerializer(user).data
                })
            else:
                print("Password is incorrect")
                # For demo: also try direct comparison in case password isn't hashed
                if user.password == password:
                    print("Using direct password match (demo mode)")
                    login(request, user)
                    return Response({
                        'message': 'Login successful (demo mode)',
                        'user': UserSerializer(user).data
                    })
                
                return Response(
                    {'error': 'Invalid password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except User.DoesNotExist:
            print(f"User '{username}' does not exist")
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Login error: {e}")
            return Response(
                {'error': 'Login failed'},
                status=status.HTTP_400_BAD_REQUEST
            )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            # Hash password if it's being updated
            if 'password' in request.data:
                serializer.validated_data['password'] = make_password(request.data['password'])
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Optional: Add a simple view to check if user is authenticated
class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'authenticated': True,
            'user': UserSerializer(request.user).data
        })

# Optional: View to list all users (for demo)
class ListUsersView(APIView):
    permission_classes = [AllowAny]  # For demo only - should be IsAuthenticated in production
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            'total_users': users.count(),
            'users': serializer.data
        })