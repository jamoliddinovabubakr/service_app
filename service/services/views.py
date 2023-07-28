from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from services.models import Subscription
from django.db.models import Prefetch, F, Sum
from services.serializers import SubscrioptionSerializer
from clients.models import Client

class SubscriptionView(ReadOnlyModelViewSet):
    # queryset = Subscription.objects.all().prefetch_related('client').prefetch_related('client__user ')
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')),
    ).annotate(price=F('service__full_price') - 
                        F('service__full_price') * F('plan__discount_percent') / 100.00)

    serializer_class = SubscrioptionSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response = super().list(request=request, *args, **kwargs)

        
        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data
        
        return response