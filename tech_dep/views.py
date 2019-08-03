import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views.generic import UpdateView
from rest_framework import viewsets

from offers.models import Detail, MaterialGroup, Offer, OfferStatus
from prod_reports.models import Pocastord

from .forms import OfferStatsForm, OrderUpdateForm
from .models import Order
from .serializers import OrderSerializers


def orders(request):
    last_poc_kokila = Pocastord.objects.using('kokila').last()
    last_poc_orders = Order.objects.last()

    if last_poc_kokila.pk > last_poc_orders.id_poc:
        items = Pocastord.objects.using('kokila').filter(pk__gt=last_poc_orders.id_poc - 50)
        for item in items:
            Order.objects.update_or_create(
                id_poc=item.id,
                defaults={
                    'numer_met': item.porder.numer_met,
                    'company': item.porder.zamawiajacy.company,
                    'cast_name': item.cast_name,
                    'cast_pcs': item.cast_pcs,
                    'pict_number': item.pict_number,
                    'cust_material': item.cust_material,
                    'termin_klienta': item.porder.termin_klienta,
                    'model': item.model,
                    'rawcast': item.rawcast,
                    'painting': item.painting,
                    'mechrough': item.mechrough,
                    'mechfine': item.mechfine,
                    'marketing': item.porder.wprowadzajacy,
                    'ord_in': item.created_at,
                }
            )
    return render(request, 'tech_dep/orders.html')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers


class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    form_class = OrderUpdateForm
    success_url = '/tech/orders/'
    permission_required = ['tech_dep.change_order']

    def get_context_data(self, **kwargs):
        if self.object.model:
            self.object.model = 'TAK'
        if self.object.rawcast:
            self.object.rawcast = 'TAK'
        if self.object.painting:
            self.object.painting = 'TAK'
        if self.object.mechrough:
            self.object.mechrough = 'TAK'
        if self.object.mechfine:
            self.object.mechfine = 'TAK'
        return super().get_context_data(**kwargs)


@login_required
@permission_required('offers')
def tech_dep_statistics(request):

    date_stats_to = datetime.date.today()
    date_stats_from = datetime.date(date_stats_to.year, date_stats_to.month, 1)

    if request.method == "POST":
        form = OfferStatsForm(request.POST)
        date_stats_from = datetime.datetime.strptime(request.POST['date_stats_from'], '%d.%m.%Y')
        date_stats_to = datetime.datetime.strptime(request.POST['date_stats_to'], '%d.%m.%Y')
    else:
        form = OfferStatsForm(initial={'date_stats_from': date_stats_from, 'date_stats_to': date_stats_to})

    # get required data
    offers = Offer.objects.filter(date_tech_out__gt=date_stats_from, date_tech_out__lt=date_stats_to)
    tech_users = Group.objects.get(pk=2).user_set.all()
    offer_statuses = OfferStatus.objects.all()
    mat_groups = MaterialGroup.objects.all()
    details = Detail.objects.filter(offer__date_tech_out__gt=date_stats_from, offer__date_tech_out__lt=date_stats_to)

    # stats for offers per technologist
    tech_stats = []
    of_amt, det_amt, in_time_amt = 0, 0, 0

    for index, tech in enumerate(tech_users):
        tech_stats.append({
            'tech': tech.first_name,
            'amount': 0,
            'avg_days': 0,
            'in_time': 0,
            'det_amt': 0,
        })
        for offer in offers:
            if tech.pk == offer.user_tech.pk:
                tech_stats[index]['amount'] += 1
                tech_stats[index]['avg_days'] += offer.days_amount
                if offer.days_amount < 8:
                    tech_stats[index]['in_time'] += 1
                    in_time_amt += 1
                tech_stats[index]['det_amt'] += offer.positions_amount
                of_amt += 1
                det_amt += offer.positions_amount

    # stats for offers per status
    statuses_stats = []
    of_stat_amt = 0

    for index, status in enumerate(offer_statuses):
        statuses_stats.append({
            'status': status.offer_status,
            'amount': 0,
        })
        for offer in offers:
            if offer.status.pk == status.pk:
                statuses_stats[index]['amount'] += 1
                of_stat_amt += 1

    # stats for details per material group
    detail_stats = []
    det_mat_amt = 0
    for index, mat_group in enumerate(mat_groups):
        detail_stats.append({
            'mat_group': mat_group.mat_group,
            'amount': 0,
        })
        for detail in details:
            if detail.mat.mat_group.pk == mat_group.pk:
                detail_stats[index]['amount'] += 1
                det_mat_amt += 1

    context = {
        "tech_stats": tech_stats,
        "statuses_stats": statuses_stats,
        "detail_stats": detail_stats,
        "of_amt": of_amt,
        "in_time_amt": in_time_amt,
        "det_amt": det_amt,
        "det_mat_amt": det_mat_amt,
        "of_stat_amt": of_stat_amt,
        "form": form,
    }

    return render(request, 'tech_dep/stats.html', context)
