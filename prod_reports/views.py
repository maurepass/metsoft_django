import datetime

from django.db.models import F, Max, Q, Sum
from django.shortcuts import render
from rest_framework import viewsets

from .forms import ExecutionTimeForm
from .models import Cast, Operation
from .serializers import CastSerializer, OperationSerializer


def pouring(request):
    return render(request, 'prod_reports/pouring.html')


class PouringViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict=6)
    serializer_class = OperationSerializer


def molding(request):
    return render(request, 'prod_reports/molding.html')


class MoldingViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict=5)
    serializer_class = OperationSerializer


def finished(request):
    return render(request, 'prod_reports/finished.html')


class FinishedViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict=38)
    serializer_class = OperationSerializer


def remarks(request):
    return render(request, 'prod_reports/remarks.html')


class RemarksViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(notes__regex=r'\w+')
    serializer_class = OperationSerializer


def non_destructive_testing(request):
    return render(request, 'prod_reports/non_destructive_testing.html')


class NonDestructiveTestingViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict__in=[10, 21, 22, 24, 25, 26, 28, 56])
    serializer_class = OperationSerializer


def nonconformity(request):
    return render(request, 'prod_reports/nonconformity.html')


class NonconformityViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(accordance=3)
    serializer_class = OperationSerializer


def inserted_data(request):
    casts = (
        Operation.objects
        .values('cast')
        .annotate(
            id=Max('cast_id'),
            met_no=Max('cast__porder__met_no'),
            customer=Max('cast__customer'),
            cast_name=Max('cast__cast_name'),
            picture_number=Max('cast__picture_number'),
            cast_no=Max('parameter_value1', filter=Q(opdict_id=5)),
            metling_no=Max('parameter_value1', filter=Q(opdict_id=6)),
            pouring_temp=Max('parameter_value2', filter=Q(opdict_id=6)),
            cast_weight=Max('parameter_value1', filter=Q(opdict_id=51) or Q(opdict_id=43)),
            machining=Max('accordance', filter=Q(opdict_id=91)),
        )
        .order_by('-cast_id')[:5000]
    )

    return render(request, 'prod_reports/inserted_data.html', {'casts': casts})


def casts_in_stock(request):
    return render(request, 'prod_reports/casts_in_stock.html')


class CastsInStockViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.filter(cast_status=3)
    serializer_class = CastSerializer


def casting_weights(request):
    return render(request, 'prod_reports/casting_weights.html')


class CastingWeightsViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict=51)
    serializer_class = OperationSerializer


def machining(request):
    return render(request, 'prod_reports/machining.html')


class MachiningViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.filter(opdict__in=[10, 21, 22, 24, 25, 26, 28, 56])
    serializer_class = OperationSerializer


def scraps(request):
    return render(request, 'prod_reports/scraps.html')


class ScrapsViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.filter(cast_status=5)
    serializer_class = CastSerializer


def yields(request):
    return render(request, 'prod_reports/yields.html')


class YieldsViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.filter(pc_number=1)
    serializer_class = CastSerializer


def monitoring_all(request):
    objects = Cast.monitoring()
    return render(request, 'prod_reports/monitoring_all.html', {'objects': objects})


def monitoring_in_work(request):
    objects = list(Cast.monitoring().filter(cast_pcs__gt=F('sent') + F('cancelled') + F('finished')))

    for obj in objects:
        time = obj['customer_date'] - datetime.date.today()
        obj['time'] = time.days

    return render(request, 'prod_reports/monitoring_in_work.html', {'objects': objects})


def weight_per_client(request):

    objects = (
        Cast.objects
        .filter(cast_status__in=[1, 2, 3, 7])
        .values('customer')
        .annotate(
            new=Sum('cast_weight', filter=Q(cast_status=1)),
            planned=Sum('cast_weight', filter=Q(cast_status=7)),
            poured=Sum('cast_weight', filter=Q(cast_status=2)),
            finished=Sum('cast_weight', filter=Q(cast_status=3)),
            all=Sum('cast_weight')
        )
        .order_by('-all')
    )

    sums = (
        Cast.objects
        .filter(cast_status__in=[1, 2, 3, 7])
        .aggregate(
            new=Sum('cast_weight', filter=Q(cast_status=1)),
            planned=Sum('cast_weight', filter=Q(cast_status=7)),
            poured=Sum('cast_weight', filter=Q(cast_status=2)),
            finished=Sum('cast_weight', filter=Q(cast_status=3)),
            all=Sum('cast_weight')
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

    total_weight = Cast.objects.filter(cast_status__in=[1, 2, 7]).aggregate(weight_sum=Sum('cast_weight'))

    context = {
        "objects": objects,
        "total": total_weight['weight_sum']
    }

    return render(request, 'prod_reports/weight_per_group.html', context)


def execution_time(request):
    if request.method == 'POST':
        met_number = request.POST['met_number']
        company = request.POST['company']
        cast_name = request.POST['cast_name']
        picture_number = request.POST['picture_number']

        if met_number or company or cast_name or picture_number:
            casts = (
                Operation.objects
                .filter(
                    cast__porder__met_no__icontains=met_number,
                    cast__customer__icontains=company,
                    cast__cast_name__icontains=cast_name,
                    cast__picture_number__icontains=picture_number
                )
                .values('cast')
                .annotate(
                    id=Max('cast__id'),
                    met_no=Max('cast__porder__met_no'),
                    customer=Max('cast__customer'),
                    cast_name=Max('cast__cast_name'),
                    picture_number=Max('cast__picture_number'),
                    pc_number=Max('parameter_value1', filter=Q(opdict_id=5)),
                    created_at=Max('cast__created_at'),
                    moulding_date=Max('completion_date1', filter=Q(opdict_id=5)),
                    pouring_date=Max('completion_date1', filter=Q(opdict_id=6)),
                    finishing_date=Max('completion_date1', filter=Q(opdict_id=38)),
                )
            )
            return render(request, 'prod_reports/execution_time_results.html', {'objects': casts})

    return render(request, 'prod_reports/execution_time_form.html', {'form': ExecutionTimeForm()})
