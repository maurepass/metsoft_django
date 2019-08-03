import datetime

from django.db.models import F, Max, Q, Sum
from django.shortcuts import render
from rest_framework import viewsets

from .forms import CzasWykonaniaForm
from .models import Cast, Operation
from .serializers import CastSerializer, OperationSerializer


def zalania(request):
    return render(request, 'prod_reports/zalania.html')


class ZalaniaViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict=6)
    serializer_class = OperationSerializer


def zaformowania(request):
    return render(request, 'prod_reports/zaformowania.html')


class ZaformowaniaViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict=5)
    serializer_class = OperationSerializer


def odbiory(request):
    return render(request, 'prod_reports/odbiory.html')


class OdbioryViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict=38)
    serializer_class = OperationSerializer


def uwagi(request):
    return render(request, 'prod_reports/uwagi.html')


class UwagiViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(notes__regex=r'\w+')
    serializer_class = OperationSerializer


def badania_ndt(request):
    return render(request, 'prod_reports/badania_ndt.html')


class BadaniaNDTViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict__in=[10, 21, 22, 24, 25, 26, 28, 56])
    serializer_class = OperationSerializer


def niezgodnosci(request):
    return render(request, 'prod_reports/niezgodnosci.html')


class NiezgodnosciViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(accordance=3)
    serializer_class = OperationSerializer


def inserted_data(request):
    casts = (
        Operation.objects
        .values('cast')
        .annotate(
            id=Max('cast_id'),
            nr_met=Max('cast__porder__numer_met'),
            customer=Max('cast__customer'),
            cast_name=Max('cast__cast_name'),
            picture_number=Max('cast__picture_number'),
            nr_odlewu=Max('parameter_value1', filter=Q(opdict_id=5)),
            nr_wytopu=Max('parameter_value1', filter=Q(opdict_id=6)),
            temp_zalewania=Max('parameter_value2', filter=Q(opdict_id=6)),
            waga_odlewu=Max('parameter_value1', filter=Q(opdict_id=51) or Q(opdict_id=43)),
            obr_mech=Max('accordance', filter=Q(opdict_id=91)),
        )
        .order_by('-cast_id')[:5000]
    )

    return render(request, 'prod_reports/inserted_data.html', {'casts': casts})


def magazyn(request):
    return render(request, 'prod_reports/magazyn.html')


class MagazynViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.filter(cast_status=3)
    serializer_class = CastSerializer


def wagi_odlewow(request):
    return render(request, 'prod_reports/wagi_odlewow.html')


class WagiOdlewowViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict=51)
    serializer_class = OperationSerializer


def machining(request):
    return render(request, 'prod_reports/machining.html')


class MachiningViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict__in=[10, 21, 22, 24, 25, 26, 28, 56])
    serializer_class = OperationSerializer


def wybraki(request):
    return render(request, 'prod_reports/wybraki.html')


class WybrakiViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.filter(cast_status=5)
    serializer_class = CastSerializer


def uzyski(request):
    return render(request, 'prod_reports/uzyski.html')


class UzyskiViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.filter(pc_number=1)
    serializer_class = CastSerializer


def monitoring_all(request):
    objects = Cast.monitoring()
    return render(request, 'prod_reports/monitoring_in_work.html', {'objects': objects})


def monitoring_in_work(request):
    objects = list(Cast.monitoring().filter(cast_pcs__gt=F('wyslane') + F('anulowane') + F('odebrane')))

    for obj in objects:
        time = obj['termin_klienta'] - datetime.date.today()
        obj['time'] = time.days

    return render(request, 'prod_reports/monitoring_in_work.html', {'objects': objects})


def weight_per_client(request):

    objects = (
        Cast.objects
        .filter(cast_status__in=[1, 2, 3, 7])
        .values('customer')
        .annotate(
            nowe=Sum('cast_weight', filter=Q(cast_status=1)),
            planowanie=Sum('cast_weight', filter=Q(cast_status=7)),
            zalane=Sum('cast_weight', filter=Q(cast_status=2)),
            odebrane=Sum('cast_weight', filter=Q(cast_status=3)),
            razem=Sum('cast_weight')
        )
        .order_by('-razem')
    )

    sums = (
        Cast.objects
        .filter(cast_status__in=[1, 2, 3, 7])
        .aggregate(
            nowe=Sum('cast_weight', filter=Q(cast_status=1)),
            planowanie=Sum('cast_weight', filter=Q(cast_status=7)),
            zalane=Sum('cast_weight', filter=Q(cast_status=2)),
            odebrane=Sum('cast_weight', filter=Q(cast_status=3)),
            razem=Sum('cast_weight')
        )
    )

    context = {
        "objects": objects,
        "sums": sums,
    }

    return render(request, 'prod_reports/weight_per_client.html', context)


def weight_per_group(request):
    objects = (
        Cast.objects
        .filter(cast_status__in=[1, 2, 7])
        .values('mat_calc_group')
        .annotate(sum_cast_weight=Sum('cast_weight'))
        .order_by('mat_calc_group')
    )

    total_weight = Cast.objects.filter(cast_status__in=[1, 2, 7]).aggregate(razem=sum('cast_weight'))

    context = {
        "objects": objects,
        "total": total_weight
    }

    return render(request, 'prod_reports/weight_per_group.html', context)


def czas_wykonania(request):
    if request.method == 'POST':
        met_number = request.POST['met_number']
        company = request.POST['company']
        cast_name = request.POST['cast_name']
        picture_number = request.POST['picture_number']

        if met_number or company or cast_name or picture_number:
            casts = (
                Operation.objects
                .filter(
                    cast__porder__numer_met__icontains=met_number,
                    cast__customer__icontains=company,
                    cast__cast_name__icontains=cast_name,
                    cast__picture_number__icontains=picture_number
                )
                .values('cast')
                .annotate(
                    id=Max('cast__id'),
                    numer_met=Max('cast__porder__numer_met'),
                    customer=Max('cast__customer'),
                    cast_name=Max('cast__cast_name'),
                    picture_number=Max('cast__picture_number'),
                    pc_number=Max('parameter_value1', filter=Q(opdict_id=5)),
                    created_at=Max('cast__created_at'),
                    zaformowano=Max('completion_date1', filter=Q(opdict_id=5)),
                    zalane=Max('completion_date1', filter=Q(opdict_id=6)),
                    odbior=Max('completion_date1', filter=Q(opdict_id=38)),
                )
            )
            return render(request, 'prod_reports/czas_wykonania_results.html', {'objects': casts})

    return render(request, 'prod_reports/czas_wykonania_form.html', {'form': CzasWykonaniaForm()})
