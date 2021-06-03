from django.contrib import admin
from cakes.models import (Cream,
                          Cake,
                          Biscuit,
                          Decoration,
                          Filling,
                          CakeDiameters,
                          Orders)


class CakeAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.save(commit=False)
        obj.weight = obj.total_weight()
        obj.save()


admin.site.register(Cream)
admin.site.register(Biscuit)
admin.site.register(Decoration)
admin.site.register(Filling)
admin.site.register(Cake, CakeAdmin)
admin.site.register(CakeDiameters)
admin.site.register(Orders)
