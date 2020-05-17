class ProdReportsRouter:
    def db_for_read(self, model, **hints):

        if model._meta.app_label == "prod_reports":
            return "kokila"
        return None
