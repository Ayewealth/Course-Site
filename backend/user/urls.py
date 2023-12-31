from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views

router = DefaultRouter()
router.register('user-profile', views.UserProfileViewSet)
router.register('instructor-profile', views.InstructorProfileViewSet)
router.register('cart', views.CartViewSet)
router.register('watch-list', views.WatchListViewSet)
router.register('reviews', views.ReviewViewSet)

userprofile_router = routers.NestedDefaultRouter(
    router, 'user-profile', lookup='user'
)
userprofile_router.register(
    'user', views.ProfileUserViewSet, basename='user-profile-user'
)

instructorprofile_router = routers.NestedDefaultRouter(
    router, 'instructor-profile', lookup='user'
)
instructorprofile_router.register(
    'user', views.ProfileInstructorViewSet, basename='instructor-profile-user'
)

urlpatterns = [
    path('', include(router.urls)),

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.endpoints),

    # ------------------------------- User -------------------------------------

    path('users/', views.UserListCreateApiView.as_view()),
    path('users/<str:pk>/',
         views.UserRetrieveUpdateDestroyApiView.as_view(), name='user'),

    path('', include(userprofile_router.urls)),

    # ---------------------------------- Instructor --------------------------------

    path('instructor/', views.InstructorListCreateView.as_view()),
    path('instructor/<str:pk>',
         views.InstructorRetrieveUpdateDestroyApiView.as_view(), name='instructor'),

    path('', include(instructorprofile_router.urls)),

    # -------------------------------------- Course -------------------------------------

    path('courses/', views.CourseCreateListApiView.as_view()),
    path('courses/<str:pk>/', views.CourseRetrieveUpdateDestroyApiView.as_view()),
    path('courses/popular', views.PopularCoursesApiView.as_view(), name='popular-courses'),
    path('courses/trending', views.TrendingCoursesApiView.as_view(), name='trending-courses'),
    path('courses/new', views.NewCoursesApiView.as_view(), name='new-courses'),

    # -------------------------------------- Category --------------------------------
    path('categories/', views.CategoryCreateListApiView.as_view()),
    path('categories/<str:pk>/', views.CategoryRetrieveUpdateDestroyApiView.as_view(), name='category-detail'),
    path('categories/<str:pk>/subcategories/', views.SubcategoryListView.as_view(), name='subcategory-list'),
    path('categories/<str:pk>/subcategories/<str:name>/', views.SubcategoryDetailView.as_view(), name='subcategory-detail'),
    path('categories/<str:pk>/subcategories/<str:name>/courses/', views.CourseListBySubcategoryView.as_view(), name='course-list-by-subcategory'),
]
