import socket

from .models import UsedViewsLogs


class UsedViewsMiddleware:
    monitored_paths = [
        '/reports/execution-time/',
        '/reports/finished/',
        '/reports/pouring/',
        '/reports/nonconformity/',
        '/reports/remarks/',
        '/reports/weight-per-client/',
        '/reports/weight-per-group/',
        '/reports/scraps/',
        '/reports/casting-weights/',
        '/reports/monitoring-in-work/',
        '/reports/monitoring-all/',
        '/reports/casts-in-stock/',
        '/reports/molding/',
        '/reports/non-destructive-testing/',
        '/reports/machining/',
        '/reports/yields/',
        '/reports/inserted-data/',
        '/reports/reports/',
        '/reports/castings-with-machining/',
        '/offers/details/',
        '/offers/details/searching/',
        '/offers/stats/',
        '/patterns/report/',
        '/patterns/create/',
        '/patterns/',
    ]

    old_paths = [
        '/modele/',
        '/kokila/raporty/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET':
            if request.path in self.monitored_paths or request.path in self.old_paths:
                user_ip = request.META.get('REMOTE_ADDR')

                # get hostname
                if user_ip == '127.0.0.1':
                    user_host = socket.gethostname()
                else:
                    try:
                        result_host = socket.gethostbyaddr(user_ip)
                        user_host = result_host[0]
                    except:
                        user_host = 'unknown'

                # set report_name
                if request.path in self.old_paths:
                    report_name = request.path + ' OLD PATH'
                else:
                    report_name = request.path

                UsedViewsLogs.objects.create(ip=user_ip, host=user_host, report=report_name)

        return self.get_response(request)

