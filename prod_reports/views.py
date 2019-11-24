import datetime

from django.db.models import F, Max, Q, Sum, Subquery
from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.views.generic.base import TemplateView
from rest_framework import viewsets

from .forms import ExecutionTimeForm
from .models import Cast, Operation
from .serializers import CastSerializer, OperationSerializer


class PouringViewSet(viewsets.ModelViewSet):
    """ All confirmed pouring operations."""
    queryset = Operation.objects.filter(opdict=6, completion_date1__isnull=False)
    serializer_class = OperationSerializer


class MoldingViewSet(viewsets.ModelViewSet):
    """ All confirmed moulding form operations."""
    queryset = Operation.objects.filter(opdict=5, completion_date1__isnull=False)
    serializer_class = OperationSerializer


class FinishedViewSet(viewsets.ModelViewSet):
    """ All confirmed final control operations. """
    queryset = Operation.objects.filter(opdict=38, completion_date1__isnull=False)
    serializer_class = OperationSerializer


class RemarksViewSet(viewsets.ModelViewSet):
    """ All remarks written for any operation. """
    queryset = Operation.objects.filter(notes__regex=r'\w+')
    serializer_class = OperationSerializer


class NonDestructiveTestingViewSet(viewsets.ModelViewSet):
    """ All confirmed NDT operations. """
    queryset = Operation.objects.filter(opdict__in=[10, 21, 22, 24, 25, 26, 28, 56], completion_date1__isnull=False)
    serializer_class = OperationSerializer


class NonconformityViewSet(viewsets.ModelViewSet):
    """ All nonconformity confirmed for operations."""
    queryset = Operation.objects.filter(accordance=3)
    serializer_class = OperationSerializer


class InsertedDataList(ListView):
    """ List of selected data from productions process written during the operation confirmation."""
    context_object_name = 'casts'
    template_name = 'prod_reports/inserted_data.html'
    queryset = (
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


class CastsInStockViewSet(viewsets.ModelViewSet):
    """ All casting on the stock (after final control but not sent)."""
    queryset = Cast.objects.filter(cast_status=3)
    serializer_class = CastSerializer


class CastingWeightsViewSet(viewsets.ModelViewSet):
    """ All confirmed weighting operations."""
    queryset = Operation.objects.filter(opdict=51, completion_date1__isnull=False)
    serializer_class = OperationSerializer


class MachiningViewSet(viewsets.ModelViewSet):
    """ All confirmed machining operations."""
    queryset = Operation.objects.filter(opdict__in=[19, 20, 64, 65, 82, 91], completion_date1__isnull=False)
    serializer_class = OperationSerializer


class ScrapsViewSet(viewsets.ModelViewSet):
    """ Scrapped castings. """
    queryset = Cast.objects.filter(cast_status=5)
    serializer_class = CastSerializer


class YieldsViewSet(viewsets.ModelViewSet):
    """ Technological yield on every casting."""
    queryset = Cast.objects.filter(pc_number=1)
    serializer_class = CastSerializer


class MonitoringAllList(ListView):
    """Shows amount of castings on with the particular production status for all orders."""
    queryset = Cast.monitoring()
    context_object_name = 'objects'
    template_name = 'prod_reports/monitoring_all.html'


class MonitoringInWorkList(ListView):
    """Shows amount of castings on with the particular production status for not finished orders."""
    template_name = 'prod_reports/monitoring_in_work.html'
    context_object_name = 'objects'

    def get_queryset(self):
        objects = list(Cast.monitoring().filter(cast_pcs__gt=F('sent') + F('cancelled') + F('finished')))

        # calculate amount of days till delivery date required by customer
        for obj in objects:
            time = obj['customer_date'] - datetime.date.today()
            obj['time'] = time.days

        return objects


class WeightPerClientView(TemplateView):
    """ Total weight of castings with open order in the particular production status. """
    template_name = 'prod_reports/weight_per_client.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = (
            Cast.objects
            .filter(cast_status__in=[1, 2, 3, 7])
            .values('customer')
            .annotate(
                new=Sum('cast_weight', filter=Q(cast_status=1)),
                planned=Sum('cast_weight', filter=Q(cast_status=7)),
                poured=Sum('cast_weight', filter=Q(cast_status=2)),
                on_stock=Sum('cast_weight', filter=Q(cast_status=3)),
                in_production=Sum('cast_weight', filter=Q(cast_status__in=[1, 7, 2]))
            )
            .order_by('-in_production')
        )

        context['sums'] = (
            Cast.objects
            .filter(cast_status__in=[1, 2, 3, 7])
            .aggregate(
                new=Sum('cast_weight', filter=Q(cast_status=1)),
                planned=Sum('cast_weight', filter=Q(cast_status=7)),
                poured=Sum('cast_weight', filter=Q(cast_status=2)),
                on_stock=Sum('cast_weight', filter=Q(cast_status=3)),
                in_production=Sum('cast_weight', filter=Q(cast_status__in=[1, 7, 2]))
            )
        )

        return context


class WeightPerGroupView(TemplateView):
    """ Total weight of castings in the particular material group. """
    template_name = 'prod_reports/weight_per_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['objects'] = (
            Cast.objects
            .filter(cast_status__in=[1, 2, 7])
            .values('mat_calc_group')
            .annotate(sum_cast_weight=Sum('cast_weight'))
            .order_by('mat_calc_group')
        )

        context['total_weight'] = (
            Cast.objects
            .filter(cast_status__in=[1, 2, 7])
            .aggregate(weight_sum=Sum('cast_weight'))
        )

        return context


class ExecutionTimeView(FormView):
    """ Confirmation date for specified operations and specified data written during confirmation. """
    form_class = ExecutionTimeForm
    template_name = 'prod_reports/execution_time_form.html'

    def post(self, request, *args, **kwargs):
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
                    created_at=Max('cast__created_at'),
                    moulding_date=Max('completion_date1', filter=Q(opdict_id=5)),
                    pc_number=Max('parameter_value1', filter=Q(opdict_id=5)),
                    pouring_date=Max('completion_date1', filter=Q(opdict_id=6)),
                    melt_no=Max('parameter_value1', filter=Q(opdict_id=6)),
                    pouring_temp=Max('parameter_value2', filter=Q(opdict_id=6)),
                    knock_out=Max('completion_date1', filter=Q(opdict_id=61)),
                    casting_weight=Max('parameter_value1', filter=Q(opdict_id__in=[43, 51])),
                    machining_flatness=Max('completion_date1', filter=Q(opdict_id=91)),
                    finishing_date=Max('completion_date1', filter=Q(opdict_id=38)),
                )
            )
            return render(request, 'prod_reports/execution_time_results.html', {'objects': casts})


class CastsWithMachiningViewSet(viewsets.ModelViewSet):
    """ All castings required machining (raw or final)."""
    subquery = Operation.objects.filter(opdict__in=[19, 20])
    queryset = Cast.objects.filter(porder__status__in=[1, 2],
                                   cast_status__in=[1, 2, 7],
                                   id__in=Subquery(subquery.values('cast').distinct())
                                   )
    serializer_class = CastSerializer
