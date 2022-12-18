from .routers import router
from django.urls import include, path, re_path
# from .views import SingleReviewViewSet, ReviewsAPIView

app_name = 'reviews'

urlpatterns = [
    path('v1/', include(router.urls)),

    # # re_path(r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)', ReviewViewSet),
    # # re_path(r'v1/titles/(?P<title_id>\d+)/reviews', AllReviewsViewSet)

    # path('v1/titles/<int:title_id>/reviews/', AllReviewsViewSet.as_view({'get': 'list'})),

    # path('v1/titles/<int:pk>/reviews/', AllReviewsViewSet.as_view({'get': 'retrieve'})),
    # path('v1/titles/<int:title_id>/reviews/', TestAPIView.as_view()),
    
    # path('v1/titles/<int:title_id>/reviews/<int:review_id>/', AllReviewsViewSet.as_view({'put': 'update'})),

    # path('v1/titles/<int:title_id>/reviews/<int:pk>/', SingleReviewViewSet.as_view({'get': 'retrieve'})),
    # path('v1/titles/<int:title_id>/reviews/', ReviewsAPIView.as_view()),

]
