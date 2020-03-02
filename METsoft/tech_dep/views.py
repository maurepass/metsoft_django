from datetime import datetime, timedelta, date

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, TemplateView
from rest_framework import viewsets

from offers.models import Offer
from prod_reports.models import Pocastord, Operation
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


class WZTDailyReport(TemplateView):
    """ Offers and orders to finish in technology department and nonconformities from last day"""
    template_name = 'tech_dep/wzt_daily_report.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if date.isoweekday(date.today()) == 1:
            completion_date = date.today() - timedelta(days=3)
        else:
            completion_date = date.today() - timedelta(days=1)

        context['offers'] = Offer.objects.filter(status_id=1).order_by('-id')
        context['orders'] = Order.objects.filter(status_id=2).order_by('-id')
        context['nonconformities'] = Operation.objects.filter(accordance=3, completion_date1=completion_date)

        return context




