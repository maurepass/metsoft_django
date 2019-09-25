import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render, reverse
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView, FormView
from rest_framework import viewsets

from .forms import (DetailCreateForm, DetailSearchingForm, DetailUpdateForm,
                    OfferCreateUpdateForm, OfferDetailsForm, OfferNoticeForm, OfferStatsForm)
from .models import Detail, Material, Notice, Offer, OfferStatus, MaterialGroup
from .serializers import DetailSerializer, MaterialSerializer, OfferSerializer


class OfferNoticesUpdateView(LoginRequiredMixin, UpdateView):
    """ Changing default notices for offers"""
    template_name = 'offers/notice_form.html'
    form_class = OfferNoticeForm

    def get_object(self, queryset=None):
        return Notice.objects.first()

    def get_success_url(self):
        return reverse('offers')


class OfferViewSet(viewsets.ModelViewSet):
    """ All serialized offers"""
    queryset = Offer.objects.all().order_by('-id')
    serializer_class = OfferSerializer


class DetailViewSet(viewsets.ModelViewSet):
    """ All serialized details for finished offers (without details in offers currently in work)"""
    queryset = Detail.objects.exclude(offer__status__in=[1]).order_by('-id')  # without "W opracowaniu"
    serializer_class = DetailSerializer


class OfferCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Create a new offer"""
    model = Offer
    form_class = OfferCreateUpdateForm
    permission_required = ['offers.add_offer']

    def get_initial(self):
        """ Set in form the new offer number """
        initial = super().get_initial()
        last_offer = Offer.objects.last()
        last_no, ending = last_offer.offer_no.split('/')
        try:
            new_no = int(last_no) + 1
        except ValueError:
            new_no = last_no
        initial['offer_no'] = '{}/{}'.format(new_no, ending)

        return initial

    def form_valid(self, form):
        """ Before create the new offer add default notices """
        form.instance.notices = Notice.objects.first().content
        return super().form_valid(form)


class OfferUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Offer update"""
    model = Offer
    form_class = OfferCreateUpdateForm
    permission_required = ['offers.change_offer']


class OfferPrintView(TemplateView):
    """ Prepare view to print the offer """
    template_name = 'offers/offer_print.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer = Offer.objects.get(pk=kwargs.get('pk'))
        details = offer.detail_set.all()
        prep_det = offer.prepare_details()

        context['offer'] = offer
        context['details'] = details
        context['tolerances'] = prep_det['tolerances']
        context['tapers'] = prep_det['tapers']
        context['atest'] = prep_det['atest']
        context['machining'] = prep_det['machining'],

        return context


class MaterialViewSet(viewsets.ModelViewSet):
    """ All serialize materials """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Add a new material"""
    model = Material
    fields = ['material', 'mat_group']
    permission_required = ['offers.add_material']


class MaterialUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Update material """
    model = Material
    fields = ['material', 'mat_group']
    permission_required = ['offers.change_material']


class OfferDetailView(LoginRequiredMixin, TemplateView):
    """ Managing details belonged to a offer and editing notices"""
    def dispatch(self, request, *args, **kwargs):
        this_offer = Offer.objects.get(pk=kwargs.get('pk'))

        if request.method == 'POST' and 'new_notices' not in request.POST:
            offer_form = OfferDetailsForm(request.POST, instance=this_offer)
            if offer_form.is_valid():
                offer_form.save()
                if 'status' in offer_form.changed_data:
                    this_offer.offer_status_changed()
                    return redirect('offers')

        # loading default notices if users require them
        if 'new_notices' in request.POST:
            notices = Notice.objects.first()
            this_offer.notices = notices.content

        offer_form = OfferDetailsForm(instance=this_offer)
        details = this_offer.detail_set.all()

        context = {
            'offer': this_offer,
            'details': details,
            'offer_form': offer_form,
        }
        return render(request, 'offers/offer_details.html', context)


class DetailCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Create new detail from cast iron or steel"""
    model = Detail
    form_class = DetailCreateForm
    permission_required = ['offers.add_detail']

    def get_initial(self):
        initial = super().get_initial()

        if 'steel' in self.request.GET:
            initial['detail_yield'] = 50
            initial['fr_chormite'] = 1
            initial['tolerances'] = 'ISO 8062-DCTG13 RMAG H'
            initial['heat_treat'] = 'normalizacja'

        if 'iron' in self.request.GET:
            initial['detail_yield'] = 75
            initial['fr_chormite'] = 0
            initial['tolerances'] = 'ISO 8062-DCTG12 RMAG H'
            initial['heat_treat'] = 'brak'

        return initial

    def form_valid(self, form):
        """ Create new detail and increase positions amount in offer """
        offer = Offer.objects.get(pk=self.kwargs.get('pk'))
        form.instance.offer = offer
        offer.positions_amount += 1
        offer.save()
        return super().form_valid(form)


class DetailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Update detail or create new one based on current detail """

    model = Detail
    form_class = DetailUpdateForm
    pk_url_kwarg = 'det_pk'
    permission_required = ['offers.change_detail']

    def dispatch(self, request, *args, **kwargs):
        """ If 'new-detail' create new object and increase positions amount in the offer """
        if 'new-detail' in request.POST:
            pk = self.kwargs.get('pk')
            offer = Offer.objects.get(pk=pk)
            new_detail = DetailCreateForm(request.POST)
            new_detail.instance.offer = offer
            if new_detail.is_valid():
                new_detail.save()
                offer.positions_amount += 1
                offer.save()
                return redirect('offer-details', pk=pk)
        return super().dispatch(request, *args, **kwargs)


class DetailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ Remove detail from offer"""
    model = Detail
    pk_url_kwarg = 'det_pk'
    permission_required = ['offers.delete_detail']

    def get_success_url(self):
        """ After removing detail decrease positions amount in offer """
        pk = self.kwargs.get('pk')
        offer = Offer.objects.get(pk=pk)
        offer.positions_amount -= 1
        offer.save()
        return reverse('offer-details', kwargs={'pk': pk})


class DetailSearchingView(FormView):
    """ Find and show details based on given criteria """

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.POST['cast_name'] or request.POST['drawing_no'] or request.POST['offer_no']:
                objects = Detail.objects.filter(
                    cast_name__icontains=request.POST.get('cast_name'),
                    drawing_no__icontains=request.POST.get('drawing_no'),
                    offer__offer_no__icontains=request.POST.get('offer_no')
                ).order_by('-id')
                return render(request, 'offers/detail_searching_results.html', {'objects': objects})

        return render(request, 'offers/detail_searching_form.html', {'form': DetailSearchingForm})


class OffersStatisticsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """ Generate reports: offers per technologist, offers per status, details per material group."""
    permission_required = 'offers.view_offer'

    def dispatch(self, request, *args, **kwargs):
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

        return render(request, 'offers/stats.html', context)

