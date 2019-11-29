import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render, reverse
from django.views.generic import CreateView, DeleteView, UpdateView, FormView, DetailView
from rest_framework import viewsets

from . import forms
from .models import Detail, Material, Notice, Offer, OfferStatus, MaterialGroup
from .serializers import DetailSerializer, MaterialSerializer, OfferSerializer


class OfferNoticesUpdateView(LoginRequiredMixin, UpdateView):
    """ Changing default notices for offers"""
    template_name = 'offers/notice_form.html'
    form_class = forms.OfferNoticeForm

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
    form_class = forms.OfferCreateUpdateForm
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
    form_class = forms.OfferCreateUpdateForm
    permission_required = ['offers.change_offer']


class OfferPrintView(DetailView):
    """ Prepare view to print the offer """
    model = Offer
    template_name = 'offers/offer_print.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prep_det = self.object.prepare_details()
        context['details'] = self.object.detail_set.all()
        context['tolerances'] = prep_det['tolerances']
        context['tapers'] = prep_det['tapers']
        context['atest'] = prep_det['atest']
        context['machining'] = prep_det['machining']
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


class OfferDetailView(LoginRequiredMixin, FormView):
    """ Managing details belonged to a offer and editing notices"""

    def dispatch(self, request, *args, **kwargs):
        this_offer = Offer.objects.get(pk=kwargs.get('pk'))

        if request.method == 'POST' and 'new_notices' not in request.POST:
            offer_form = forms.OfferDetailsForm(request.POST, instance=this_offer)
            if offer_form.is_valid():
                offer_form.save()
                if 'status' in offer_form.changed_data:
                    this_offer.offer_status_changed()
                    return redirect('offers')

        # loading default notices if users require them
        if 'new_notices' in request.POST:
            notices = Notice.objects.first()
            this_offer.notices = notices.content

        offer_form = forms.OfferDetailsForm(instance=this_offer)
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
    form_class = forms.DetailCreateForm
    permission_required = ['offers.add_detail']

    def get_initial(self):
        initial = super().get_initial()
        initial['required'] = 'wł. wytrz., skł. chem.'

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
    form_class = forms.DetailUpdateForm
    pk_url_kwarg = 'det_pk'
    permission_required = ['offers.change_detail']

    def dispatch(self, request, *args, **kwargs):
        """ If 'new-detail' create new object and increase positions amount in the offer """
        if 'new-detail' in request.POST:
            offer = Offer.objects.get(pk=self.kwargs.get('pk'))
            new_detail = forms.DetailCreateForm(request.POST)
            new_detail.instance.offer = offer
            if new_detail.is_valid():
                new_detail.save()
                offer.positions_amount += 1
                offer.save()
                return redirect('offer-details', pk=offer.pk)
        return super().dispatch(request, *args, **kwargs)


class DetailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ Remove detail from offer"""
    model = Detail
    pk_url_kwarg = 'det_pk'
    permission_required = ['offers.delete_detail']

    def get_success_url(self):
        """ After removing detail decrease positions amount in offer """
        offer = Offer.objects.get(pk=self.kwargs.get('pk'))
        offer.positions_amount -= 1
        offer.save()
        return reverse('offer-details', kwargs={'pk': offer.pk})


class DetailSearchingView(FormView):
    """ Find and show details based on given criteria """
    form_class = forms.DetailSearchingForm
    template_name = 'offers/detail_searching_form.html'

    def post(self, request, *args, **kwargs):
        if request.POST['cast_name'] or request.POST['drawing_no'] or request.POST['offer_no']:
            objects = Detail.objects.filter(
                cast_name__icontains=request.POST.get('cast_name'),
                drawing_no__icontains=request.POST.get('drawing_no'),
                offer__offer_no__icontains=request.POST.get('offer_no')
            ).order_by('-id')
            return render(request, 'offers/detail_searching_results.html', {'objects': objects})

        return redirect('details-searching')


class OffersStatisticsView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    """ Generate reports: offers per technologist, offers per status, details per material group."""
    permission_required = 'offers.add_offer'

    @staticmethod
    def gen_report_offer_per_technologist(offers):
        """
        Generate report:
        - amount of offers prepared by every technologist
        - average time required to prepare offer by every technologist
        - amount of casting prepared by every technologist
        """
        tech_stats = []
        of_amt, det_amt, in_time_amt = 0, 0, 0
        technologists = Group.objects.get(pk=2).user_set.all()

        for index, tech in enumerate(technologists):
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

        return {'tech_stats': tech_stats, 'of_amt': of_amt, 'det_amt': det_amt, 'in_time_amt': in_time_amt}

    @staticmethod
    def gen_report_offer_per_statuses(offers):
        """ Generat report: amount of offers in every status"""
        statuses_stats = []
        of_stat_amt = 0
        offer_statuses = OfferStatus.objects.all()

        for index, status in enumerate(offer_statuses):
            statuses_stats.append({
                'status': status.offer_status,
                'amount': 0,
            })
            for offer in offers:
                if offer.status.pk == status.pk:
                    statuses_stats[index]['amount'] += 1
                    of_stat_amt += 1

        return {'statuses_stats': statuses_stats, 'of_stat_amt': of_stat_amt}

    @staticmethod
    def gen_report_details_per_mat_group(details):
        """ Generate report: amount of castings in every material group """
        detail_stats = []
        det_mat_amt = 0
        mat_groups = MaterialGroup.objects.all()

        for index, mat_group in enumerate(mat_groups):
            detail_stats.append({
                'mat_group': mat_group.mat_group,
                'amount': 0,
            })
            for detail in details:
                if detail.mat.mat_group.pk == mat_group.pk:
                    detail_stats[index]['amount'] += 1
                    det_mat_amt += 1
        return {'detail_stats': detail_stats, 'det_mat_amt': det_mat_amt}

    def dispatch(self, request, *args, **kwargs):
        date_stats_to = datetime.date.today()
        date_stats_from = datetime.date(date_stats_to.year, date_stats_to.month, 1)

        if request.method == "POST":
            form = forms.OfferStatsForm(request.POST)
            date_stats_from = request.POST.get('date_stats_from')
            date_stats_to = request.POST.get('date_stats_to')
        else:
            form = forms.OfferStatsForm(initial={'date_stats_from': date_stats_from, 'date_stats_to': date_stats_to})

        offers = Offer.objects.filter(date_tech_out__gt=date_stats_from, date_tech_out__lt=date_stats_to)
        details = Detail.objects.filter(offer__date_tech_out__gt=date_stats_from, offer__date_tech_out__lt=date_stats_to)

        context = {"form": form}
        context.update(self.gen_report_offer_per_technologist(offers))
        context.update(self.gen_report_offer_per_statuses(offers))
        context.update(self.gen_report_details_per_mat_group(details))

        return render(request, 'offers/stats.html', context)
