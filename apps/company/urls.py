from rest_framework.routers import DefaultRouter

from apps.company.views import PlanViewSet, RuleViewSet

router = DefaultRouter()
router.register('plans', PlanViewSet, basename='plans')
router.register('rules', RuleViewSet, basename='rules')

urlpatterns = router.urls
