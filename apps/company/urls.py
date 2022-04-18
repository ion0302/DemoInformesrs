from rest_framework.routers import DefaultRouter

from apps.company.views import CompanyViewSet, PlanLogViewSet

router = DefaultRouter()
router.register('planlogs', PlanLogViewSet, basename='planlogs')
router.register('companies', CompanyViewSet, basename='companies')

urlpatterns = router.urls
