from django.contrib import admin

from .models import BulkPromoCreate, History, Product, PromoCode

# action section


@admin.action(description='Активировать выбранные коды')
def bulk_activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Деактивировать выбранные коды')
def bulk_disactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description='Экспортировать выбранные в csv')
def export_as_csv(modeladmin, request, queryset):
    import csv

    from django.http import HttpResponse
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response


# inlines section


class ProductsInLine(admin.TabularInline):
    model = PromoCode.products.through
    fields = ('product', 'promo_code')
    extra = 1


class HistoryInLine(admin.TabularInline):
    model = History
    can_delete = False
    extra = 0


class ProductsBulkInLine(admin.TabularInline):
    model = BulkPromoCreate.products.through
    fields = ('product', 'bulk')
    extra = 1


# register section

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    inlines = (ProductsInLine,)
    list_display = ('code', 'title', 'description', 'created', 'user_id', 'display_products', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('title', 'created_by', 'is_active', 'start_at', 'expired')
    search_fields = ('title', 'description', 'code')
    actions = (bulk_activate, bulk_disactivate)
    readonly_fields = ('created', 'modified')
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'code', 'is_active', 'discount_type', 'discount_amount', 'created', 'modified')
        }),
        ('Ограничения', {
            'fields': ('start_at', 'expired', 'activates_possible', 'activates_left', 'minimal_amount')
        }),
        ('Привязки', {
            'fields': ('user_id',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('products')

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='Привязан к продуктам')
    def display_products(self, obj):
        return ', '.join(product.name for product in obj.products.all())


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('get_code', 'created', 'promocode', 'applied_user_id', 'discount_amount')
    list_filter = ('created', 'promocode', 'applied_user_id', 'promocode__products')
    search_fields = ('promocode__code',)
    actions = (export_as_csv,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('promocode').prefetch_related('promocode__products')

    @admin.display(description='Код')
    def get_code(self, obj):
        return obj.promocode.code


@admin.register(BulkPromoCreate)
class BulkCreationAdmin(admin.ModelAdmin):
    list_display = ('created', 'creation_done', 'url_download', 'created_by')
    list_filter = ('created', 'created_by', 'creation_done')
    save_as = True
    save_as_continue = False
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'quantity', 'discount_type', 'discount_amount')
        }),
        ('Ограничения', {
            'fields': ('start_at', 'expired', 'minimal_amount')
        }),
    )
    inlines = (ProductsBulkInLine,)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
