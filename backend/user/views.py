from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination


from .permissions import *
from user.models import *
from .serializers import *

# Create your views here.


@api_view(['Get'])
def endpoints(request):
    data = [
        '/user', '/user:<username>',
        '/instructor', '/instructor:<username>',
        '/courses', '/courses:<title>',
        'reviews', 'reviews:<course>'
        '/blog', '/blog:<title>',
        '/carts', '/cartitems',
    ]
    return Response(data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ------------------------------------- User ------------------------------


class UserListCreateApiView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = {
        'username': ['icontains'],
        'email': ['icontains'],
    }

    def create(self, request, *args, **kwargs):
        request.data['is_student'] = True
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        users = CustomUser.objects.filter(is_student=True)
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)


class UserRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class UserProfileViewSet(ModelViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,  ListModelMixin):
    queryset = StudentProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class ProfileUserViewSet(ModelViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset based on the user_profile lookup
        user_profile_id = self.kwargs.get('user_pk')
        return CustomUser.objects.filter(studentprofile__id=user_profile_id)


#  ------------------------------------------ Instructor ---------------------------


class InstructorListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = InstructorSerializer
    pagination_class = PageNumberPagination

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = {
        'username': ['icontains'],
        'email': ['icontains'],
    }

    def create(self, request, *args, **kwargs):
        request.data['is_instructor'] = True
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        users = CustomUser.objects.filter(is_instructor=True)
        serializer = InstructorSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)


class InstructorRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = InstructorSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class InstructorProfileViewSet(ModelViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,  ListModelMixin):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated]


class ProfileInstructorViewSet(ModelViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin):
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset based on the user_profile lookup
        user_profile_id = self.kwargs.get('user_pk')
        return CustomUser.objects.filter(instructorprofile__id=user_profile_id)

#  ------------------------------------------ Course ---------------------------


class CourseCreateListApiView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsStudent]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['instructor__username', 'title']

    def perform_create(self, serializer):
        user = self.request.user
        if user.groups.filter(name='Instructor').exists():
            # Handle instructor's action
            serializer.save(instructor=user)
        elif user.groups.filter(name='Student').exists():
            # Handle student's action
            # Give an error message to students
            raise PermissionDenied("You are not allowed to create courses.")

        return super().perform_create(serializer)

#  ------------------------------------------ Cart ---------------------------


class CartViewSet(ModelViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    # Use detail=False for actions not tied to a specific cart
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, completed=False)

        course_id = request.data.get('course_id')

        if course_id:
            course = Course.objects.get(pk=course_id)

            # Check if the course is already in the cart
            if cart.items.filter(course=course).exists():
                raise APIException("Course is already in the cart")

            Cartitems.objects.create(cart=cart, course=course)

            return Response({"detail": "Item added to cart"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Use detail=False for actions not tied to a specific cart
    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        user = request.user  # Get the authenticated user
        cart = Cart.objects.filter(user=user, completed=False).first()

        course_id = request.data.get('course_id')

        if cart and course_id:
            try:
                item = Cartitems.objects.get(cart=cart, course_id=course_id)
                item.delete()
                return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
            except Cartitems.DoesNotExist:
                return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------ WatchList ------------------------------------
class WatchListViewSet(ModelViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        user = request.user
        watchlist, created = WatchList.objects.get_or_create(user=user)

        course_id = request.data.get('course_id')

        if course_id:
            course = Course.objects.get(pk=course_id)

            # Check if the course is already in the cart
            # if watchlist.items.filter(course=course).exists():
            #     raise APIException("Course is already in the Watchlist")

            Watchitems.objects.create(watchlist=watchlist, course=course)

            return Response({"detail": "Item added to WatchList"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        user = request.user
        watchlist = WatchList.objects.filter(user=user).first()

        course_id = request.data.get('course_id')

        if watchlist and course_id:
            try:
                item = Watchitems.objects.get(
                    watchlist=watchlist, course_id=course_id)
                item.delete()
                return Response({"detail": "Item removed from Watchlist"}, status=status.HTTP_204_NO_CONTENT)
            except Watchitems.DoesNotExist:
                return Response({"error": "Item not found in Watchlist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------ Reviews -----------------------------------------------------
class ReviewViewSet(ModelViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')

        if course_id:
            course = Course.objects.get(pk=course_id)
            Review.objects.create(user=user, course=course,
                                  rating=rating, comment=comment)
            return Response({"detail": "Review added"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)
