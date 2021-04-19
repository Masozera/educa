from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)


app_name = 'courses'

urlpatterns = [
    path('subjects/',views.SubjectListView.as_view(),name='subject_list'),
    path('subjects/<pk>/',views.SubjectDetailView.as_view(),name='subject_detail'),
    #path('courses/<pk>/enroll/', views.CourseEnrollView.as_view(),name='course_enroll'), # Theoretically, you could now perform a POST request to enroll the current useron a course. However, you need to be able to identify the user and prevent unauthenticated users from accessing this view. Let's see how API authentication and permissions work.
    path('', include(router.urls))
]