from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import *
from .utils import round_to_5_stars


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username


        return token

# ---------------------------------------- User --------------------------------------------


class UserSerializer(ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user', lookup_field='pk')

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'name',
            'username',
            'email',
            'password',
            'url',
            'is_student',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    cart = serializers.SerializerMethodField(method_name='get_cart')
    watchlist = serializers.SerializerMethodField(method_name='get_watchlist')

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'profile_pics',
            'user',
            'bio',
            'cart',
            'watchlist'
        ]

    def get_cart(self, student_profile):
        cart = Cart.objects.filter(user=student_profile.user).first()
        if cart:
            return CartSerializer(cart, context=self.context).data
        return None

    def get_watchlist(self, student_profile):
        watchlist = WatchList.objects.filter(user=student_profile.user).first()
        if watchlist:
            return WatchListSerializer(watchlist, context=self.context).data
        return None

#  ---------------------------------------------- Instructor ---------------------------------


class InstructorSerializer(ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='instructor', lookup_field='pk')

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'name',
            'username',
            'email',
            'password',
            'url',
            'is_instructor',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


class InstructorProfileSerializer(ModelSerializer):
    user = InstructorSerializer(many=False, read_only=True)
    courses = serializers.SerializerMethodField(method_name='get_course')
    cart = serializers.SerializerMethodField(method_name='get_cart')
    watchlist = serializers.SerializerMethodField(method_name='get_watchlist')

    class Meta:
        model = InstructorProfile
        fields = [
            'id',
            'user',
            'bio',
            'cart',
            'watchlist',
            'bank_name',
            'account_name',
            'account_number',
            'courses',
        ]

    def get_cart(self, instructor_profile):
        cart = Cart.objects.filter(user=instructor_profile.user).first()
        if cart:
            return CartSerializer(cart, context=self.context).data
        return None

    def get_watchlist(self, instructor_profile):
        watchlist = WatchList.objects.filter(
            user=instructor_profile.user).first()
        if watchlist:
            return WatchListSerializer(watchlist, context=self.context).data
        return None

    def get_course(self, instructor_profile):
        courses = Course.objects.filter(instructor=instructor_profile.user)
        return CourseSerializer(courses, many=True, context=self.context).data


# ------------------------------ Course -----------------------

class CourseSerializer(ModelSerializer):
    instructor = InstructorSerializer(many=False, read_only=True)
    category = serializers.CharField(source="category.name")
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    students_purchased_count = serializers.SerializerMethodField(method_name='get_student_purchased_count')
    average_rating = serializers.SerializerMethodField(method_name='get_average_rating')

    class Meta:
        model = Course
        fields = [
            'id',
            'image',
            'title',
            'what_you_learn',
            'requirements',
            'description',
            'targeted_audience',
            'instructor',
            'category',
            'price',
            'duration_in_hours',
            'students_purchased_count',
            'average_rating',
            'reviews',
        ]
        read_only_fields = ['instructor']

    def get_reviews(self, course):
        reviews = Review.objects.filter(course=course)
        return ReviewSerializer(reviews, many=True, context=self.context).data
    
    def get_student_purchased_count(self, course):
        return course.get_student_purchased_count()
    
    def get_average_rating(self, course):
        average_rating = course.get_average_rating()
        if average_rating is not None:
            rounded_rating = round_to_5_stars(average_rating)
            return rounded_rating
        return None

# ------------------------------- Category --------------------

class CategorySerializer(serializers.ModelSerializer):
    # courses = serializers.SerializerMethodField(method_name='get_courses')

    class Meta:
        model = Category
        fields = '__all__'

    # def get_courses(self, category):
    #     category = Course.objects.filter(category=category)
    #     return CourseSerializer(category, many=True, context=self.context).data 

# ---------------------------- Cart------------------------------


class CartCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'image',
            'title',
            'instructor',
            'duration_in_hours',
            'price',
        ]


class CartSerializer(ModelSerializer):
    items = serializers.SerializerMethodField(method_name='get_items')
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')
    # total_quantity = serializers.SerializerMethodField(
    #     method_name='get_total_quantity')

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    def get_items(self, cart):
        items = Cartitems.objects.filter(cart=cart).select_related('course')

        # Create a dictionary to hold item quantities by course
        item_quantities = {}
        for item in items:
            course_id = item.course.id
            if course_id in item_quantities:
                item_quantities[course_id] += 1
            else:
                item_quantities[course_id] = 1

        # Serialize the items with their corresponding quantities
        serialized_items = []
        for course_id, quantity in item_quantities.items():
            course_item = {
                'course': CartCourseSerializer(item.course).data,
                'quantity': quantity
            }
            serialized_items.append(course_item)

        return serialized_items

    def get_total_price(self, cart):
        items = Cartitems.objects.filter(cart=cart)
        total_price = sum(item.course.price for item in items)
        return total_price

    # def get_total_quantity(self, cart):
    #     items = Cartitems.objects.filter(cart=cart)
    #     total_price = sum(item.quantity for item in items)
    #     return total_price


class CartItemSerializer(serializers.ModelSerializer):
    course = CartCourseSerializer()

    class Meta:
        model = Cartitems
        fields = '__all__'

# -------------------------------------- WatchList -------------------------


class WatchListSerializer(ModelSerializer):
    items = serializers.SerializerMethodField(method_name='get_items')

    class Meta:
        model = WatchList
        fields = [
            'id',
            'items',
        ]

    def get_items(self, watchlist):
        items = Watchitems.objects.filter(watchlist=watchlist)
        return WatchItemSerializer(items, many=True, context=self.context).data


class WatchItemSerializer(ModelSerializer):
    course = CartCourseSerializer()

    class Meta:
        model = Watchitems
        fields = '__all__'


# ---------------------------------------- Reviews ------------------------------------

class ReviewSerializer(ModelSerializer):
    user = serializers.CharField(source="user.name")
    course = serializers.CharField(source="course.title")

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'course',
            'rating',
            'comment',
        ]
