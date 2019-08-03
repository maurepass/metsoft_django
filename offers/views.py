from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from rest_framework import viewsets

from .forms import (DetailCreateForm, DetailSeachingForm, DetailUpdateForm,
                    OfferCreateUpdateForm, OfferDetailsForm, OfferNoticeForm)
from .models import Detail, Material, Notice, Offer
from .serializers import DetailSerializer, MaterialSerializer, OfferSerializer


def test(request):
    return render(request, 'offers/test.html')


def index_offer(request):
    return render(request, 'offers/index_offers.html')


def details_index(request):
    return render(request, 'offers/details_index.html')


@login_required
def offer_notices_update(request):
    notices = Notice.objects.first()
    if request.method == 'POST':
        form = OfferNoticeForm(request.POST, instance=notices)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('offers'))
    form = OfferNoticeForm(instance=notices)
    return render(request, 'offers/notice_form.html', {'form': form})


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class DetailViewSet(viewsets.ModelViewSet):
    queryset = Detail.objects.exclude(offer__status__in=[1])
    serializer_class = DetailSerializer


class OfferCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Offer
    form_class = OfferCreateUpdateForm
    permission_required = ['offers.add_offer']

    def get_initial(self):
        """ Set in form the next offer number """
        initial = super().get_initial()
        offer = Offer.objects.last()
        last_no, ending = offer.offer_no.split('/')
        try:
            new_no = int(last_no) + 1
        except:
            new_no = last_no
        initial['offer_no'] = '{}/{}'.format(new_no, ending)

        return initial

    def form_valid(self, form):
        """ Before create the new offer add default notices """
        notice = Notice.objects.first()
        form.instance.notices = notice.content
        return super().form_valid(form)


class OfferUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Offer
    form_class = OfferCreateUpdateForm
    permission_required = ['offers.change_offer']


def offer_print_view(request, pk):
    offer = Offer.objects.get(pk=pk)
    details = offer.detail_set.all()
    prep_det = offer.prepare_details()
    context = {
        'offer': offer,
        'details': details,
        'tolerances': prep_det['tolerances'],
        'tapers': prep_det['tapers'],
        'atest': prep_det['atest'],
        'machining': prep_det['machining'],
    }
    return render(request, 'offers/offer_print.html', context)


class MaterialListView(ListView):
    model = Material


def materials(request):
    return render(request, 'offers/material_list.html')


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Material
    fields = ['material', 'mat_group']
    permission_required = ['offers.add_material']


class MaterialUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Material
    fields = ['material', 'mat_group']
    permission_required = ['offers.change_material']


@login_required
def offer_detail_view(request, pk):
    this_offer = Offer.objects.get(pk=pk)

    if request.method == 'POST' and 'new_notices' not in request.POST:
        offer_form = OfferDetailsForm(request.POST, instance=this_offer)
        if offer_form.is_valid():
            offer_form.save()
            if 'status' in offer_form.changed_data:
                return redirect('offers')

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
    model = Detail
    form_class = DetailCreateForm
    permission_required = ['offer.add_detail']

    def get_initial(self):
        initial = super().get_initial()
        initial['quality_class'] = 'VT – poziom 4 wg ISO 11971:2008'
        initial['required'] = 'wł. wytrz., skł. chem.'
        initial['atest'] = '3.1 wg PN-EN 10204'

        if 'steel' in self.request.GET:
            initial['yeld'] = 50
            initial['fr_chormite'] = 1
            initial['tolerances'] = 'ISO 8062-DCTG13 RMAG H'
            initial['heat_treat'] = 'normalizacja'

        if 'iron' in self.request.GET:
            initial['yeld'] = 75
            initial['fr_chormite'] = 0
            initial['tolerances'] = 'ISO 8062-DCTG12 RMAG H'
            initial['heat_treat'] = 'brak'

        return initial

    def form_valid(self, form):
        offer = Offer.objects.get(pk=self.kwargs.get('pk'))
        form.instance.offer = offer
        offer.positions_amount += 1
        offer.save()
        return super().form_valid(form)


class DetailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Detail
    form_class = DetailUpdateForm
    pk_url_kwarg = 'det_pk'
    permission_required = ['offers.change_detail']

    def dispatch(self, request, *args, **kwargs):
        if 'new-detail' in request.POST:
            pk = self.kwargs.get('pk')
            offer = Offer.objects.get(pk=pk)
            new_detail = DetailUpdateForm(request.POST)
            new_detail.instance.offer = offer
            if new_detail.is_valid():
                new_detail.save()
                offer.positions_amount += 1
                offer.save()
                return redirect('offer-details', pk=pk)
        return super().dispatch(request, *args, **kwargs)


class DetailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Detail
    pk_url_kwarg = 'det_pk'
    permission_required = ['offers.delete_detail']

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        offer = Offer.objects.get(pk=pk)
        offer.positions_amount -= 1
        offer.save()
        return reverse('offer-details', kwargs={'pk': pk})


def details_searching(request):
    if request.method == 'POST':
        if request.POST['cast_name'] or request.POST['drawing_no'] or request.POST['offer_no']:
            objects = Detail.objects.filter(
                cast_name__icontains=request.POST.get('cast_name'),
                drawing_no__icontains=request.POST.get('drawing_no'),
                offer__offer_no__icontains=request.POST.get('offer_no')
            ).order_by('-id')
            return render(request, 'offers/detail_searching_results.html', {'objects': objects})

    return render(request, 'offers/detail_searching_form.html', {'form': DetailSeachingForm})
