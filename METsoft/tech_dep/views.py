from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, TemplateView
from rest_framework import viewsets

from prod_reports.models import Pocastord
from .forms import OrderUpdateForm
from .models import Order
from .serializers import OrderSerializers


class OrdersView(TemplateView):
    template_name = 'tech_dep/orders.html'

    def dispatch(self, request, *args, **kwargs):
        last_poc_kokila = Pocastord.objects.using('kokila').last()
        last_poc_orders = Order.objects.last()

        if last_poc_kokila.pk > last_poc_orders.id_poc:
            items = Pocastord.objects.using('kokila').filter(pk__gt=last_poc_orders.id_poc - 50)
            for item in items:
                Order.objects.update_or_create(
                    id_poc=item.id,
                    defaults={
                        'numer_met': item.porder.met_no,
                        'company': item.porder.zamawiajacy.company,
                        'cast_name': item.cast_name,
                        'cast_pcs': item.cast_pcs,
                        'pict_number': item.pict_number,
                        'cust_material': item.cust_material,
                        'termin_klienta': item.porder.customer_date,
                        'model': item.model,
                        'rawcast': item.rawcast,
                        'painting': item.painting,
                        'mechrough': item.mechrough,
                        'mechfine': item.mechfine,
                        'marketing': item.porder.wprowadzajacy,
                        'ord_in': item.created_at,
                    }
                )
        return super().dispatch(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    """ Register of orders processed by Technology Department. """
    queryset = Order.objects.all()
    serializer_class = OrderSerializers


class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Updating records from register of orders. """
    model = Order
    form_class = OrderUpdateForm
    success_url = '/tech/orders/'
    permission_required = ['tech_dep.change_order']

    def form_valid(self, form):
        """ Set order finish date. """
        if form.instance.status.id != 2:
            form.instance.ord_out = datetime.today()
        else:
            form.instance.ord_out = None
        return super().form_valid(form)




