from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer


class CreateTaskView(APIView):
    def post(self, request):
        # Validate the input data using TaskSerializer
        serializer = TaskSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the task if valid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListView(APIView):
    def get(self, request):
        # Extract query parameters
        search_term = request.query_params.get('search', '')
        status_filter = request.query_params.get('status', None)
        
        # Start with all tasks
        tasks = Task.objects.all()

        # Apply search functionality based on task title
        if search_term:
            tasks = tasks.filter(title__icontains=search_term)

        # Apply filtering based on task status
        if status_filter is not None:
            if status_filter.lower() == 'pending':
                tasks = tasks.filter(status=False)
            elif status_filter.lower() == 'completed':
                tasks = tasks.filter(status=True)
            else:
                return Response({'error': 'Invalid status filter. Use "pending" or "completed".'}, status=status.HTTP_400_BAD_REQUEST)

        # Implement pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of tasks per page
        paginated_tasks = paginator.paginate_queryset(tasks, request)

        # Serialize the paginated tasks
        serializer = TaskSerializer(paginated_tasks, many=True)

        # Return paginated results
        return paginator.get_paginated_response(serializer.data)


class TaskDetailView(APIView):
    def get(self, request, pk):
        try:
            # Retrieve the specific task by primary key
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the task data
        serializer = TaskSerializer(task)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            # Retrieve the specific task by primary key
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Initialize the serializer with the task instance and the request data
        serializer = TaskSerializer(task, data=request.data, partial=True)  # partial=True allows updating only some fields
        
        # Validate and save the updated data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            # Retrieve the specific task by primary key
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the task
        task.delete()
        
        # Return a success response
        return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# registration,login and logout

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LogoutView(APIView):
    def post(self, request):
        # Here, you could implement logic to handle token blacklisting if you are using such a feature.
        # For stateless JWT, simply inform the client to remove the token.
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)