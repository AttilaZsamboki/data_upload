from django.db import models
from sqlalchemy import true


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DatauploadBevtelek(models.Model):
    # Field name made lowercase.
    azonosito = models.TextField(db_column='Azonosito', primary_key=True)
    # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)
    # Field name made lowercase.
    teljesites_datuma = models.TextField(
        db_column='Teljesites_datuma', blank=True, null=True)
    # Field name made lowercase.
    ar = models.FloatField(db_column='Ar', blank=True, null=True)
    # Field name made lowercase.
    penznem = models.TextField(db_column='Penznem', blank=True, null=True)
    # Field name made lowercase.
    atvaltasi_rata = models.BigIntegerField(
        db_column='Atvaltasi_rata', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    afa_field = models.BigIntegerField(db_column='AFA_', blank=True, null=True)
    # Field name made lowercase.
    osszesen_huf = models.FloatField(
        db_column='Osszesen_HUF', blank=True, null=True)
    # Field name made lowercase.
    netto_ossz = models.FloatField(
        db_column='Netto_ossz', blank=True, null=True)
    # Field name made lowercase.
    afa_ertek = models.BigIntegerField(
        db_column='AFA_ertek', blank=True, null=True)
    # Field name made lowercase.
    tipus = models.TextField(db_column='Tipus', blank=True, null=True)
    # Field name made lowercase.
    penztarca = models.TextField(db_column='Penztarca', blank=True, null=True)
    # Field name made lowercase.
    kategoria = models.TextField(db_column='Kategoria', blank=True, null=True)
    # Field name made lowercase.
    eredmeny_kategoria = models.TextField(
        db_column='Eredmeny_kategoria', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_uzenet = models.TextField(
        db_column='Tranzakcio_uzenet', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_partner_fiok = models.TextField(
        db_column='Tranzakcio_partner_fiok', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_beszallito_neve = models.TextField(
        db_column='Tranzakcio_beszallito_neve', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_tipusa = models.TextField(
        db_column='Tranzakcio_tipusa', blank=True, null=True)
    id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dataupload_bevételek'


class DatauploadDatabaseconnections(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=40)
    host = models.CharField(max_length=150)
    database = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    created_by_id = models.IntegerField()
    port = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'dataupload_databaseconnections'


class DatauploadImporttemplates(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    table = models.CharField(max_length=30)
    special_query = models.CharField(max_length=1000)
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dataupload_importtemplates'


class DatauploadTabletemplates(models.Model):
    id = models.BigAutoField(primary_key=True)
    table = models.CharField(max_length=30)
    pkey_col = models.CharField(max_length=30)
    skiprows = models.CharField(max_length=10)
    created_by_id = models.IntegerField()
    append = models.CharField(max_length=40)
    extension_format = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'dataupload_tabletemplates'


class DatauploadUploadmodel(models.Model):
    table = models.CharField(max_length=50)
    file = models.FileField(upload_to='upload_files/', max_length=200)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dataupload_uploadmodel'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FolBevtelek(models.Model):
    # Field name made lowercase.
    azonosito = models.TextField(db_column='Azonosito', blank=True, null=True)
    # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)
    # Field name made lowercase.
    teljesites_datuma = models.DateField(
        db_column='Teljesites_datuma', blank=True, null=True)
    # Field name made lowercase.
    ar = models.FloatField(db_column='Ar', blank=True, null=True)
    # Field name made lowercase.
    penznem = models.TextField(db_column='Penznem', blank=True, null=True)
    # Field name made lowercase.
    atvaltasi_rata = models.BigIntegerField(
        db_column='Atvaltasi_rata', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    afa_field = models.BigIntegerField(db_column='AFA_', blank=True, null=True)
    # Field name made lowercase.
    osszesen_huf = models.FloatField(
        db_column='Osszesen_HUF', blank=True, null=True)
    # Field name made lowercase.
    netto_ossz = models.FloatField(
        db_column='Netto_ossz', blank=True, null=True)
    # Field name made lowercase.
    afa_ertek = models.BigIntegerField(
        db_column='AFA_ertek', blank=True, null=True)
    # Field name made lowercase.
    tipus = models.TextField(db_column='Tipus', blank=True, null=True)
    # Field name made lowercase.
    penztarca = models.TextField(db_column='Penztarca', blank=True, null=True)
    # Field name made lowercase.
    kategoria = models.TextField(db_column='Kategoria', blank=True, null=True)
    # Field name made lowercase.
    eredmeny_kategoria = models.TextField(
        db_column='Eredmeny_kategoria', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_uzenet = models.TextField(
        db_column='Tranzakcio_uzenet', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_partner_fiok = models.TextField(
        db_column='Tranzakcio_partner_fiok', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_beszallito_neve = models.TextField(
        db_column='Tranzakcio_beszallito_neve', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_tipusa = models.TextField(
        db_column='Tranzakcio_tipusa', blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'fol_bevételek'


class FolGlsElszmols(models.Model):
    # Field name made lowercase.
    csomagszam = models.BigIntegerField(
        db_column='Csomagszam', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    ugyfel_hivatkozas_field = models.TextField(
        db_column='Ugyfel_hivatkozas_', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    utanvet_hivatkozas_field = models.TextField(
        db_column='Utanvet_hivatkozas_', blank=True, null=True)
    # Field name made lowercase.
    utanvet_osszege = models.FloatField(
        db_column='Utanvet_osszege', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    felvetel_datuma_field = models.DateTimeField(
        db_column='Felvetel_datuma_', blank=True, null=True)
    # Field name made lowercase.
    kiszallitas_napja = models.DateTimeField(
        db_column='Kiszallitas_napja', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    celorszag_field = models.TextField(
        db_column='Celorszag_', blank=True, null=True)
    # Field name made lowercase.
    suly = models.FloatField(db_column='Suly', blank=True, null=True)
    # Field name made lowercase.
    kapcsolt_szolgaltatasok = models.TextField(
        db_column='Kapcsolt_szolgaltatasok', blank=True, null=True)
    # Field name made lowercase.
    futar_koltseg = models.FloatField(
        db_column='Futar_koltseg', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    cimzett_neve_field = models.TextField(
        db_column='Cimzett_neve_', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    kiszallitasi_cim_field = models.TextField(
        db_column='Kiszallitasi_cim_', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    atvevo_neve_field = models.TextField(
        db_column='Atvevo_neve_', blank=True, null=True)
    logisztika = models.FloatField(blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'fol_gls_elszámolás'


class FolKltsgek(models.Model):
    azonosito = models.TextField()
    honap = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    partner = models.TextField(blank=True, null=True)
    koltsegelem = models.TextField(blank=True, null=True)
    ar = models.FloatField(blank=True, null=True)
    penznem = models.TextField(blank=True, null=True)
    atvaltasi_rata = models.BigIntegerField(blank=True, null=True)
    # Field renamed because it ended with '_'.
    afa_field = models.BigIntegerField(db_column='afa_', blank=True, null=True)
    osszesen_huf = models.FloatField(blank=True, null=True)
    netto_ossz = models.FloatField(blank=True, null=True)
    afa_ertek = models.FloatField(blank=True, null=True)
    tipus = models.TextField(blank=True, null=True)
    penztarca = models.TextField(blank=True, null=True)
    koltseg_osztaly = models.TextField(blank=True, null=True)
    iktatasi_allapot = models.TextField(blank=True, null=True)
    szamla_sorszama = models.FloatField(blank=True, null=True)
    tranzakcio_uzenet = models.TextField(blank=True, null=True)
    tranzakcio_partner_fiok = models.TextField(blank=True, null=True)
    tranzakcio_beszallito_neve = models.TextField(blank=True, null=True)
    tranzakcio_tipusa = models.TextField(blank=True, null=True)
    teljesites_datuma = models.DateField(blank=True, null=True)
    megjegyzesek = models.TextField(blank=True, null=True)
    tranzakcio_belso_azonosito = models.TextField(blank=True, null=True)
    tranzakcio_kulso_azonosito = models.TextField(blank=True, null=True)
    megjegyzesek2 = models.TextField(blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'fol_költségek'


class FolOrders(models.Model):
    # Field name made lowercase.
    row_type = models.TextField(db_column='Row_Type', blank=True, null=True)
    # Field name made lowercase.
    order_id = models.TextField(db_column='Order_Id', blank=True, null=True)
    # Field name made lowercase.
    sku = models.TextField(db_column='Sku', blank=True, null=True)
    # Field name made lowercase.
    product_name = models.TextField(
        db_column='Product_Name', blank=True, null=True)
    # Field name made lowercase.
    default_supplier_unit_price = models.TextField(
        db_column='Default_Supplier_Unit_Price', blank=True, null=True)
    # Field name made lowercase.
    default_supplier_currency = models.TextField(
        db_column='Default_Supplier_Currency', blank=True, null=True)
    # Field name made lowercase.
    quantity = models.FloatField(db_column='Quantity', blank=True, null=True)
    # Field name made lowercase.
    unit_price = models.FloatField(
        db_column='Unit_Price', blank=True, null=True)
    # Field name made lowercase.
    discount = models.FloatField(db_column='Discount', blank=True, null=True)
    # Field name made lowercase.
    tax = models.FloatField(db_column='Tax', blank=True, null=True)
    # Field name made lowercase.
    subtotal = models.FloatField(db_column='Subtotal', blank=True, null=True)
    # Field name made lowercase.
    cogs = models.FloatField(db_column='Cogs', blank=True, null=True)
    # Field name made lowercase.
    margin = models.FloatField(db_column='Margin', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    margin_field = models.FloatField(
        db_column='Margin_', blank=True, null=True)
    # Field name made lowercase.
    item_note = models.TextField(db_column='Item_Note', blank=True, null=True)
    # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)
    # Field name made lowercase.
    webshop_id = models.TextField(
        db_column='Webshop_Id', blank=True, null=True)
    # Field name made lowercase.
    order_total = models.FloatField(
        db_column='Order_Total', blank=True, null=True)
    # Field name made lowercase.
    currency = models.TextField(db_column='Currency', blank=True, null=True)
    # Field name made lowercase.
    source = models.TextField(db_column='Source', blank=True, null=True)
    # Field name made lowercase.
    source_name = models.TextField(
        db_column='Source_Name', blank=True, null=True)
    # Field name made lowercase.
    order_status = models.TextField(
        db_column='Order_Status', blank=True, null=True)
    # Field name made lowercase.
    order_date = models.DateField(
        db_column='Order_Date', blank=True, null=True)
    # Field name made lowercase.
    memo = models.TextField(db_column='Memo', blank=True, null=True)
    # Field name made lowercase.
    billing_email = models.TextField(
        db_column='Billing_Email', blank=True, null=True)
    # Field name made lowercase.
    billing_address_1 = models.TextField(
        db_column='Billing_Address_1', blank=True, null=True)
    # Field name made lowercase.
    billing_address_2 = models.TextField(
        db_column='Billing_Address_2', blank=True, null=True)
    # Field name made lowercase.
    billing_country = models.TextField(
        db_column='Billing_Country', blank=True, null=True)
    # Field name made lowercase.
    billing_city = models.TextField(
        db_column='Billing_City', blank=True, null=True)
    # Field name made lowercase.
    billing_zip_code = models.TextField(
        db_column='Billing_Zip_Code', blank=True, null=True)
    # Field name made lowercase.
    billing_last_name = models.TextField(
        db_column='Billing_Last_Name', blank=True, null=True)
    # Field name made lowercase.
    billing_first_name = models.TextField(
        db_column='Billing_First_Name', blank=True, null=True)
    # Field name made lowercase.
    billing_tax_number = models.TextField(
        db_column='Billing_Tax_Number', blank=True, null=True)
    # Field name made lowercase.
    billing_company = models.TextField(
        db_column='Billing_Company', blank=True, null=True)
    # Field name made lowercase.
    manual_invoicing = models.BooleanField(
        db_column='Manual_Invoicing', blank=True, null=True)
    # Field name made lowercase.
    manual_proforma = models.BooleanField(
        db_column='Manual_Proforma', blank=True, null=True)
    # Field name made lowercase.
    shipping_email = models.TextField(
        db_column='Shipping_Email', blank=True, null=True)
    # Field name made lowercase.
    shipping_address_1 = models.TextField(
        db_column='Shipping_Address_1', blank=True, null=True)
    # Field name made lowercase.
    shipping_address_2 = models.TextField(
        db_column='Shipping_Address_2', blank=True, null=True)
    # Field name made lowercase.
    shipping_country = models.TextField(
        db_column='Shipping_Country', blank=True, null=True)
    # Field name made lowercase.
    shipping_city = models.TextField(
        db_column='Shipping_City', blank=True, null=True)
    # Field name made lowercase.
    shipping_zip_code = models.TextField(
        db_column='Shipping_Zip_Code', blank=True, null=True)
    # Field name made lowercase.
    shipping_last_name = models.TextField(
        db_column='Shipping_Last_Name', blank=True, null=True)
    # Field name made lowercase.
    shipping_first_name = models.TextField(
        db_column='Shipping_First_Name', blank=True, null=True)
    # Field name made lowercase.
    shipping_company = models.TextField(
        db_column='Shipping_Company', blank=True, null=True)
    # Field name made lowercase.
    delivery_note = models.TextField(
        db_column='Delivery_Note', blank=True, null=True)
    # Field name made lowercase.
    shipping_method = models.TextField(
        db_column='Shipping_Method', blank=True, null=True)
    # Field name made lowercase.
    payment_method = models.TextField(
        db_column='Payment_Method', blank=True, null=True)
    # Field name made lowercase.
    discount_value = models.FloatField(
        db_column='Discount_Value', blank=True, null=True)
    # Field name made lowercase.
    exchange_rate = models.BigIntegerField(
        db_column='Exchange_Rate', blank=True, null=True)
    # Field name made lowercase.
    payment_status = models.TextField(
        db_column='Payment_Status', blank=True, null=True)
    # Field name made lowercase.
    warehouse = models.TextField(db_column='Warehouse', blank=True, null=True)
    # Field name made lowercase.
    delivery_date = models.DateField(
        db_column='Delivery_Date', blank=True, null=True)
    # Field name made lowercase.
    proforma_invoice_id = models.TextField(
        db_column='Proforma_Invoice_Id', blank=True, null=True)
    # Field name made lowercase.
    proforma_invoice_id_2 = models.TextField(
        db_column='Proforma_Invoice_Id_2', blank=True, null=True)
    # Field name made lowercase.
    invoice_id = models.TextField(
        db_column='Invoice_Id', blank=True, null=True)
    # Field name made lowercase.
    reverse_invoice_id = models.TextField(
        db_column='Reverse_Invoice_Id', blank=True, null=True)
    prepayment_reverse_invoice_id = models.TextField(
        db_column='Prepayment_Reverse_Invoice_Id', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    prepayment_invoice_id_2 = models.TextField(
        db_column='Prepayment_Invoice_Id_2', blank=True, null=True)
    # Field name made lowercase.
    tags = models.TextField(db_column='Tags', blank=True, null=True)
    # Field name made lowercase.
    customer_classes = models.TextField(
        db_column='Customer_classes', blank=True, null=True)
    # Field name made lowercase.
    created_by = models.TextField(
        db_column='Created_by', blank=True, null=True)
    # Field name made lowercase.
    assigned_user = models.TextField(
        db_column='Assigned_User', blank=True, null=True)
    # Field name made lowercase.
    default_customer_class = models.TextField(
        db_column='Default_Customer_Class', blank=True, null=True)
    # Field name made lowercase.
    completed_date = models.DateField(
        db_column='Completed_Date', blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'fol_orders'


class FolProductSuppliers(models.Model):
    # Field name made lowercase.
    product_name = models.TextField(
        db_column='Product_Name', blank=True, null=True)
    # Field name made lowercase.
    sku = models.TextField(db_column='SKU', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_name = models.TextField(
        db_column='Supplier___1___Name', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_net_price = models.FloatField(
        db_column='Supplier___1___Net_Price', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_vat = models.TextField(
        db_column='Supplier___1___VAT', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row. Field renamed because it ended with '_'.
    supplier_1_vat_field = models.FloatField(
        db_column='Supplier___1___VAT_', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_currency = models.TextField(
        db_column='Supplier___1___Currency', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_barcode = models.FloatField(
        db_column='Supplier___1___Barcode', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_reference = models.TextField(
        db_column='Supplier___1___Reference', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_product_name = models.TextField(
        db_column='Supplier___1___Product_Name', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_minimum_order_quantity = models.FloatField(
        db_column='Supplier___1___Minimum_Order_Quantity', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_unit_of_measurement = models.FloatField(
        db_column='Supplier___1___Unit_of_Measurement', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_package_size = models.FloatField(
        db_column='Supplier___1___Package_Size', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_lead_time = models.FloatField(
        db_column='Supplier___1___Lead_Time', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_days_of_stock = models.FloatField(
        db_column='Supplier___1___Days_of_Stock', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_safety_stock = models.FloatField(
        db_column='Supplier___1___Safety_Stock', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_default = models.FloatField(
        db_column='Supplier___1___Default', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_note = models.FloatField(
        db_column='Supplier___1___Note', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_name = models.TextField(
        db_column='Supplier___2___Name', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_net_price = models.FloatField(
        db_column='Supplier___2___Net_Price', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_vat = models.TextField(
        db_column='Supplier___2___VAT', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row. Field renamed because it ended with '_'.
    supplier_2_vat_field = models.FloatField(
        db_column='Supplier___2___VAT_', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_currency = models.TextField(
        db_column='Supplier___2___Currency', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_barcode = models.FloatField(
        db_column='Supplier___2___Barcode', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_reference = models.TextField(
        db_column='Supplier___2___Reference', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_product_name = models.TextField(
        db_column='Supplier___2___Product_Name', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_minimum_order_quantity = models.FloatField(
        db_column='Supplier___2___Minimum_Order_Quantity', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_unit_of_measurement = models.FloatField(
        db_column='Supplier___2___Unit_of_Measurement', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_package_size = models.FloatField(
        db_column='Supplier___2___Package_Size', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_lead_time = models.FloatField(
        db_column='Supplier___2___Lead_Time', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_days_of_stock = models.FloatField(
        db_column='Supplier___2___Days_of_Stock', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_safety_stock = models.FloatField(
        db_column='Supplier___2___Safety_Stock', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_default = models.FloatField(
        db_column='Supplier___2___Default', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_note = models.FloatField(
        db_column='Supplier___2___Note', blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'fol_product_suppliers'


class FolStockReport(models.Model):
    id = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    sku = models.TextField(blank=True, null=True)
    on_stock = models.BigIntegerField(blank=True, null=True)
    layers_warehouse = models.TextField(blank=True, null=True)
    on_stock_layer = models.FloatField(blank=True, null=True)
    net_price = models.FloatField(blank=True, null=True)
    landed_cost_layer = models.FloatField(blank=True, null=True)
    inventory_value_layer = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    sales = models.BigIntegerField(blank=True, null=True)
    index = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'fol_stock_report'


class FolSzmlk(models.Model):
    # Field name made lowercase.
    szamla_belso_azonosito = models.TextField(
        db_column='Szamla_belso_azonosito')
    # Field name made lowercase.
    szamla_azonosito = models.TextField(
        db_column='Szamla_azonosito', blank=True, null=True)
    # Field name made lowercase.
    date = models.TextField(db_column='Date', blank=True, null=True)
    # Field name made lowercase.
    hatarido = models.TextField(db_column='Hatarido', blank=True, null=True)
    # Field name made lowercase.
    fizetes_datuma = models.TextField(
        db_column='Fizetes_datuma', blank=True, null=True)
    # Field name made lowercase.
    teljesites_datuma = models.TextField(
        db_column='Teljesites_datuma', blank=True, null=True)
    # Field name made lowercase.
    tipus = models.TextField(db_column='Tipus', blank=True, null=True)
    # Field name made lowercase.
    fizetesi_allapot = models.TextField(
        db_column='Fizetesi_allapot', blank=True, null=True)
    # Field name made lowercase.
    iktatasi_allapot = models.TextField(
        db_column='Iktatasi_Allapot', blank=True, null=True)
    # Field name made lowercase.
    expired = models.BooleanField(db_column='Expired', blank=True, null=True)
    # Field name made lowercase.
    partner = models.TextField(db_column='Partner', blank=True, null=True)
    # Field name made lowercase.
    szallitmanyok = models.TextField(
        db_column='Szallitmanyok', blank=True, null=True)
    # Field name made lowercase.
    koltseg = models.FloatField(db_column='Koltseg', blank=True, null=True)
    # Field name made lowercase.
    penznem = models.TextField(db_column='Penznem', blank=True, null=True)
    # Field name made lowercase.
    atvaltasi_rata = models.FloatField(
        db_column='Atvaltasi_rata', blank=True, null=True)
    # Field name made lowercase.
    osszesen_huf = models.FloatField(
        db_column='Osszesen_HUF', blank=True, null=True)
    # Field name made lowercase.
    pdf = models.TextField(db_column='PDF', blank=True, null=True)
    # Field name made lowercase.
    fizetesi_mod = models.TextField(
        db_column='Fizetesi_mod', blank=True, null=True)
    # Field name made lowercase.
    megjegyzes = models.TextField(
        db_column='Megjegyzes', blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'fol_számlák'


class FolUnas(models.Model):
    cikkszam = models.TextField(blank=True, primary_key=True)
    termek_nev = models.TextField(blank=True, null=True)
    netto_ar = models.FloatField(blank=True, null=True)
    brutto_ar = models.FloatField(blank=True, null=True)
    # Field name made lowercase.
    parameter_minosegtext = models.TextField(
        db_column='Parameter_Minosegtext', blank=True, null=True)
    # Field name made lowercase.
    parameter_kiszerelesenum = models.TextField(
        db_column='Parameter_Kiszerelesenum', blank=True, null=True)
    # Field name made lowercase.
    parameter_szintext = models.TextField(
        db_column='Parameter_Szintext', blank=True, null=True)
    parameter_1_m2_feluletheztext = models.TextField(
        db_column='Parameter_1_m2_feluletheztext', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    parameter_csaladtext = models.TextField(
        db_column='Parameter_Csaladtext', blank=True, null=True)
    # Field name made lowercase.
    parameter_kategoriatext = models.TextField(
        db_column='Parameter_Kategoriatext', blank=True, null=True)
    parameter_teli_hangulat_mintatext = models.TextField(
        db_column='Parameter_Teli_hangulat_mintatext', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    parameter_szelessegtext = models.TextField(
        db_column='Parameter_Szelessegtext', blank=True, null=True)
    # Field name made lowercase.
    parameter_hossztext = models.TextField(
        db_column='Parameter_Hossztext', blank=True, null=True)
    # Field name made lowercase.
    parameter_merettext = models.TextField(
        db_column='Parameter_Merettext', blank=True, null=True)
    parameter_ablakfolia_tipustext = models.TextField(
        db_column='Parameter_Ablakfolia_tipustext', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    parameter_belathatosagtext = models.TextField(
        db_column='Parameter_Belathatosagtext', blank=True, null=True)
    # Field name made lowercase.
    parameter_felhelyezestext = models.TextField(
        db_column='Parameter_Felhelyezestext', blank=True, null=True)
    # Field name made lowercase.
    parameter_felulettext = models.TextField(
        db_column='Parameter_Felulettext', blank=True, null=True)
    # Field name made lowercase.
    parameter_hovisszaverestext = models.TextField(
        db_column='Parameter_Hovisszaverestext', blank=True, null=True)
    # Field name made lowercase.
    parameter_koporetegtext = models.TextField(
        db_column='Parameter_Koporetegtext', blank=True, null=True)
    parameter_ontapados_padlopadlotext = models.TextField(
        db_column='Parameter_Ontapados_padloPadlotext', blank=True, null=True)  # Field name made lowercase.
    parameter_padlo_tipusapadlotext = models.TextField(
        db_column='Parameter_Padlo_tipusaPadlotext', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    parameter_uv_vedelemtext = models.TextField(
        db_column='Parameter_UV_vedelemtext', blank=True, null=True)
    # Field name made lowercase.
    parameter_vastagsagtext = models.TextField(
        db_column='Parameter_Vastagsagtext', blank=True, null=True)
    parameter_csomag_kiszerelesenum = models.TextField(
        db_column='Parameter_Csomag_kiszerelesenum', blank=True, null=True)  # Field name made lowercase.
    parameter_video_segitsegvideokhtml = models.TextField(
        db_column='Parameter_Video_segitsegVideokhtml', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    parameter_vip_artext = models.FloatField(
        db_column='Parameter_VIP_artext', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    parameter_m2_doboztext = models.TextField(
        db_column='Parameter_m2/doboztext', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    parameter_m2_tekercstext = models.TextField(
        db_column='Parameter_m2/tekercstext', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    parameter_m2_csomagtext = models.TextField(
        db_column='Parameter_m2/csomagtext', blank=True, null=True)
    parameter_felhelyezes_nehezsegetext = models.FloatField(
        db_column='Parameter_Felhelyezes_nehezsegetext', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    parameter_eltavolithatotext = models.TextField(
        db_column='Parameter_Eltavolithatotext', blank=True, null=True)
    # Field name made lowercase.
    parameter_illesztestext = models.TextField(
        db_column='Parameter_Illesztestext', blank=True, null=True)
    # Field name made lowercase.
    parameter_tisztitasatext = models.TextField(
        db_column='Parameter_Tisztitasatext', blank=True, null=True)
    # Field name made lowercase.
    parameter_elofizetestext = models.TextField(
        db_column='Parameter_ELOFIZETEStext', blank=True, null=True)
    # Field name made lowercase.
    parameter_konzultacioenum = models.TextField(
        db_column='Parameter_Konzultacioenum', blank=True, null=True)
    # Field name made lowercase.
    parameter_brandtext = models.TextField(
        db_column='Parameter_brandtext', blank=True, null=True)
    # Field name made lowercase.
    parameter_eantext = models.TextField(
        db_column='Parameter_eantext', blank=True, null=True)
    # Field name made lowercase.
    parameter_mpntext = models.TextField(
        db_column='Parameter_mpntext', blank=True, null=True)
    # Field name made lowercase.
    parameter_lepesmelysegtext = models.TextField(
        db_column='Parameter_Lepesmelysegtext', blank=True, null=True)
    # Field name made lowercase.
    parameter_lehajlo_peremtext = models.TextField(
        db_column='Parameter_Lehajlo_peremtext', blank=True, null=True)
    # Field name made lowercase.
    parameter_aremelestext = models.TextField(
        db_column='Parameter_Aremelestext', blank=True, null=True)
    # Field renamed because it wasn't a valid Python identifier.
    number_1_alkategoria = models.TextField(
        db_column='1_alkategoria', blank=True, null=True)
    # Field renamed because it wasn't a valid Python identifier.
    number_2_alkategoria = models.TextField(
        db_column='2_alkategoria', blank=True, null=True)
    # Field renamed because it wasn't a valid Python identifier.
    number_3_alkategoria = models.TextField(
        db_column='3_alkategoria', blank=True, null=True)
    # Field renamed because it wasn't a valid Python identifier.
    number_4_alkategoria = models.TextField(
        db_column='4_alkategoria', blank=True, null=True)
    # Field renamed because it wasn't a valid Python identifier.
    number_5_alkategoria = models.TextField(
        db_column='5_alkategoria', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fol_unas'


class ProBevtelek(models.Model):
    # Field name made lowercase.
    azonosito = models.TextField(
        db_column='Azonosito', blank=True, primary_key=True)
    # Field name made lowercase.
    date = models.TextField(db_column='Date', blank=True, null=True)
    # Field name made lowercase.
    teljesites_datuma = models.TextField(
        db_column='Teljesites_datuma', blank=True, null=True)
    # Field name made lowercase.
    ar = models.FloatField(db_column='Ar', blank=True, null=True)
    # Field name made lowercase.
    penznem = models.TextField(db_column='Penznem', blank=True, null=True)
    # Field name made lowercase.
    atvaltasi_rata = models.FloatField(
        db_column='Atvaltasi_rata', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    afa_field = models.BigIntegerField(db_column='AFA_', blank=True, null=True)
    # Field name made lowercase.
    osszesen_huf = models.FloatField(
        db_column='Osszesen_HUF', blank=True, null=True)
    # Field name made lowercase.
    netto_ossz = models.FloatField(
        db_column='Netto_ossz', blank=True, null=True)
    # Field name made lowercase.
    afa_ertek = models.BigIntegerField(
        db_column='AFA_ertek', blank=True, null=True)
    # Field name made lowercase.
    tipus = models.TextField(db_column='Tipus', blank=True, null=True)
    # Field name made lowercase.
    penztarca = models.TextField(db_column='Penztarca', blank=True, null=True)
    # Field name made lowercase.
    kategoria = models.TextField(db_column='Kategoria', blank=True, null=True)
    # Field name made lowercase.
    eredmeny_kategoria = models.TextField(
        db_column='Eredmeny_kategoria', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_uzenet = models.TextField(
        db_column='Tranzakcio_uzenet', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_partner_fiok = models.TextField(
        db_column='Tranzakcio_partner_fiok', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_beszallito_neve = models.TextField(
        db_column='Tranzakcio_beszallito_neve', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_tipusa = models.TextField(
        db_column='Tranzakcio_tipusa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pro_bevételek'


class ProKltsgek(models.Model):
    # Field name made lowercase.
    azonosito = models.TextField(db_column='Azonosito', blank=True, null=True)
    # Field name made lowercase.
    honap = models.TextField(db_column='Honap', blank=True, null=True)
    # Field name made lowercase.
    date = models.TextField(db_column='Date', blank=True, null=True)
    # Field name made lowercase.
    partner = models.TextField(db_column='Partner', blank=True, null=True)
    # Field name made lowercase.
    koltsegelem = models.TextField(
        db_column='Koltsegelem', blank=True, null=True)
    # Field name made lowercase.
    ar = models.FloatField(db_column='Ar', blank=True, null=True)
    # Field name made lowercase.
    penznem = models.TextField(db_column='Penznem', blank=True, null=True)
    # Field name made lowercase.
    atvaltasi_rata = models.FloatField(
        db_column='Atvaltasi_rata', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    afa_field = models.BigIntegerField(db_column='AFA_', blank=True, null=True)
    # Field name made lowercase.
    osszesen_huf = models.FloatField(
        db_column='Osszesen_HUF', blank=True, null=True)
    # Field name made lowercase.
    netto_ossz = models.FloatField(
        db_column='Netto_ossz', blank=True, null=True)
    # Field name made lowercase.
    afa_ertek = models.BigIntegerField(
        db_column='AFA_ertek', blank=True, null=True)
    # Field name made lowercase.
    tipus = models.TextField(db_column='Tipus', blank=True, null=True)
    # Field name made lowercase.
    penztarca = models.TextField(db_column='Penztarca', blank=True, null=True)
    # Field name made lowercase.
    koltseg_osztaly = models.TextField(
        db_column='Koltseg_osztaly', blank=True, null=True)
    # Field name made lowercase.
    iktatasi_allapot = models.TextField(
        db_column='Iktatasi_allapot', blank=True, null=True)
    # Field name made lowercase.
    szamla_sorszama = models.FloatField(
        db_column='Szamla_sorszama', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_uzenet = models.TextField(
        db_column='Tranzakcio_uzenet', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_partner_fiok = models.TextField(
        db_column='Tranzakcio_partner_fiok', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_beszallito_neve = models.TextField(
        db_column='Tranzakcio_beszallito_neve', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_tipusa = models.TextField(
        db_column='Tranzakcio_tipusa', blank=True, null=True)
    # Field name made lowercase.
    teljesites_datuma = models.TextField(
        db_column='Teljesites_datuma', blank=True, null=True)
    # Field name made lowercase.
    megjegyzesek = models.TextField(
        db_column='Megjegyzesek', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_belso_azonosito = models.TextField(
        db_column='Tranzakcio_belso_azonosito', blank=True, null=True)
    # Field name made lowercase.
    tranzakcio_kulso_azonosito = models.TextField(
        db_column='Tranzakcio_kulso_azonosito', blank=True, null=True)
    # Field name made lowercase.
    megjegyzesek1 = models.FloatField(
        db_column='Megjegyzesek1', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pro_költségek'


class ProOrders(models.Model):
    # Field name made lowercase.
    row_type = models.TextField(db_column='Row_Type', blank=True, null=True)
    # Field name made lowercase.
    order_id = models.TextField(db_column='Order_Id', blank=True, null=True)
    # Field name made lowercase.
    sku = models.TextField(db_column='Sku', blank=True, null=True)
    # Field name made lowercase.
    product_name = models.TextField(
        db_column='Product_Name', blank=True, null=True)
    # Field name made lowercase.
    default_supplier_unit_price = models.TextField(
        db_column='Default_Supplier_Unit_Price', blank=True, null=True)
    # Field name made lowercase.
    default_supplier_currency = models.TextField(
        db_column='Default_Supplier_Currency', blank=True, null=True)
    # Field name made lowercase.
    quantity = models.FloatField(db_column='Quantity', blank=True, null=True)
    # Field name made lowercase.
    unit_price = models.TextField(
        db_column='Unit_Price', blank=True, null=True)
    # Field name made lowercase.
    discount = models.FloatField(db_column='Discount', blank=True, null=True)
    # Field name made lowercase.
    tax = models.FloatField(db_column='Tax', blank=True, null=True)
    # Field name made lowercase.
    subtotal = models.TextField(db_column='Subtotal', blank=True, null=True)
    # Field name made lowercase.
    cogs = models.FloatField(db_column='Cogs', blank=True, null=True)
    # Field name made lowercase.
    margin = models.FloatField(db_column='Margin', blank=True, null=True)
    # Field name made lowercase. Field renamed because it ended with '_'.
    margin_field = models.FloatField(
        db_column='Margin_', blank=True, null=True)
    # Field name made lowercase.
    item_note = models.FloatField(db_column='Item_Note', blank=True, null=True)
    # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)
    # Field name made lowercase.
    webshop_id = models.TextField(
        db_column='Webshop_Id', blank=True, null=True)
    # Field name made lowercase.
    order_total = models.TextField(
        db_column='Order_Total', blank=True, null=True)
    # Field name made lowercase.
    currency = models.TextField(db_column='Currency', blank=True, null=True)
    # Field name made lowercase.
    source = models.TextField(db_column='Source', blank=True, null=True)
    # Field name made lowercase.
    source_name = models.TextField(
        db_column='Source_Name', blank=True, null=True)
    # Field name made lowercase.
    order_status = models.TextField(
        db_column='Order_Status', blank=True, null=True)
    # Field name made lowercase.
    order_date = models.TextField(
        db_column='Order_Date', blank=True, null=True)
    # Field name made lowercase.
    memo = models.TextField(db_column='Memo', blank=True, null=True)
    # Field name made lowercase.
    billing_email = models.TextField(
        db_column='Billing_Email', blank=True, null=True)
    # Field name made lowercase.
    billing_address_1 = models.TextField(
        db_column='Billing_Address_1', blank=True, null=True)
    # Field name made lowercase.
    billing_address_2 = models.TextField(
        db_column='Billing_Address_2', blank=True, null=True)
    # Field name made lowercase.
    billing_country = models.TextField(
        db_column='Billing_Country', blank=True, null=True)
    # Field name made lowercase.
    billing_city = models.TextField(
        db_column='Billing_City', blank=True, null=True)
    # Field name made lowercase.
    billing_zip_code = models.BigIntegerField(
        db_column='Billing_Zip_Code', blank=True, null=True)
    # Field name made lowercase.
    billing_last_name = models.TextField(
        db_column='Billing_Last_Name', blank=True, null=True)
    # Field name made lowercase.
    billing_first_name = models.TextField(
        db_column='Billing_First_Name', blank=True, null=True)
    # Field name made lowercase.
    billing_tax_number = models.TextField(
        db_column='Billing_Tax_Number', blank=True, null=True)
    # Field name made lowercase.
    billing_company = models.TextField(
        db_column='Billing_Company', blank=True, null=True)
    # Field name made lowercase.
    manual_invoicing = models.BooleanField(
        db_column='Manual_Invoicing', blank=True, null=True)
    # Field name made lowercase.
    manual_proforma = models.BooleanField(
        db_column='Manual_Proforma', blank=True, null=True)
    # Field name made lowercase.
    shipping_email = models.TextField(
        db_column='Shipping_Email', blank=True, null=True)
    # Field name made lowercase.
    shipping_address_1 = models.TextField(
        db_column='Shipping_Address_1', blank=True, null=True)
    # Field name made lowercase.
    shipping_address_2 = models.TextField(
        db_column='Shipping_Address_2', blank=True, null=True)
    # Field name made lowercase.
    shipping_country = models.TextField(
        db_column='Shipping_Country', blank=True, null=True)
    # Field name made lowercase.
    shipping_city = models.TextField(
        db_column='Shipping_City', blank=True, null=True)
    # Field name made lowercase.
    shipping_zip_code = models.BigIntegerField(
        db_column='Shipping_Zip_Code', blank=True, null=True)
    # Field name made lowercase.
    shipping_last_name = models.TextField(
        db_column='Shipping_Last_Name', blank=True, null=True)
    # Field name made lowercase.
    shipping_first_name = models.TextField(
        db_column='Shipping_First_Name', blank=True, null=True)
    # Field name made lowercase.
    shipping_company = models.TextField(
        db_column='Shipping_Company', blank=True, null=True)
    # Field name made lowercase.
    delivery_note = models.TextField(
        db_column='Delivery_Note', blank=True, null=True)
    # Field name made lowercase.
    shipping_method = models.TextField(
        db_column='Shipping_Method', blank=True, null=True)
    # Field name made lowercase.
    payment_method = models.TextField(
        db_column='Payment_Method', blank=True, null=True)
    # Field name made lowercase.
    discount_value = models.FloatField(
        db_column='Discount_Value', blank=True, null=True)
    # Field name made lowercase.
    exchange_rate = models.BigIntegerField(
        db_column='Exchange_Rate', blank=True, null=True)
    # Field name made lowercase.
    payment_status = models.TextField(
        db_column='Payment_Status', blank=True, null=True)
    # Field name made lowercase.
    warehouse = models.TextField(db_column='Warehouse', blank=True, null=True)
    # Field name made lowercase.
    delivery_date = models.FloatField(
        db_column='Delivery_Date', blank=True, null=True)
    # Field name made lowercase.
    proforma_invoice_id = models.TextField(
        db_column='Proforma_Invoice_Id', blank=True, null=True)
    # Field name made lowercase.
    proforma_invoice_id_2 = models.FloatField(
        db_column='Proforma_Invoice_Id_2', blank=True, null=True)
    # Field name made lowercase.
    invoice_id = models.TextField(
        db_column='Invoice_Id', blank=True, null=True)
    # Field name made lowercase.
    reverse_invoice_id = models.FloatField(
        db_column='Reverse_Invoice_Id', blank=True, null=True)
    prepayment_reverse_invoice_id = models.FloatField(
        db_column='Prepayment_Reverse_Invoice_Id', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    prepayment_invoice_id_2 = models.FloatField(
        db_column='Prepayment_Invoice_Id_2', blank=True, null=True)
    # Field name made lowercase.
    tags = models.TextField(db_column='Tags', blank=True, null=True)
    # Field name made lowercase.
    customer_classes = models.TextField(
        db_column='Customer_classes', blank=True, null=True)
    # Field name made lowercase.
    created_by = models.TextField(
        db_column='Created_by', blank=True, null=True)
    # Field name made lowercase.
    assigned_user = models.TextField(
        db_column='Assigned_User', blank=True, null=True)
    # Field name made lowercase.
    default_customer_class = models.TextField(
        db_column='Default_Customer_Class', blank=True, null=True)
    # Field name made lowercase.
    completed_date = models.TextField(
        db_column='Completed_Date', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pro_orders'


class ProProductSuppliers(models.Model):
    # Field name made lowercase.
    product_name = models.TextField(
        db_column='Product_Name', blank=True, null=True)
    # Field name made lowercase.
    sku = models.TextField(db_column='SKU', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_name = models.TextField(
        db_column='Supplier___1___Name', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_net_price = models.FloatField(
        db_column='Supplier___1___Net_Price', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_vat = models.TextField(
        db_column='Supplier___1___VAT', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row. Field renamed because it ended with '_'.
    supplier_1_vat_field = models.FloatField(
        db_column='Supplier___1___VAT_', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_currency = models.TextField(
        db_column='Supplier___1___Currency', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_barcode = models.FloatField(
        db_column='Supplier___1___Barcode', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_reference = models.TextField(
        db_column='Supplier___1___Reference', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_product_name = models.TextField(
        db_column='Supplier___1___Product_Name', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_minimum_order_quantity = models.FloatField(
        db_column='Supplier___1___Minimum_Order_Quantity', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_unit_of_measurement = models.FloatField(
        db_column='Supplier___1___Unit_of_Measurement', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_package_size = models.FloatField(
        db_column='Supplier___1___Package_Size', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_lead_time = models.FloatField(
        db_column='Supplier___1___Lead_Time', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_days_of_stock = models.FloatField(
        db_column='Supplier___1___Days_of_Stock', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_safety_stock = models.FloatField(
        db_column='Supplier___1___Safety_Stock', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_default = models.FloatField(
        db_column='Supplier___1___Default', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_1_note = models.FloatField(
        db_column='Supplier___1___Note', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_name = models.TextField(
        db_column='Supplier___2___Name', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_net_price = models.FloatField(
        db_column='Supplier___2___Net_Price', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_vat = models.TextField(
        db_column='Supplier___2___VAT', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row. Field renamed because it ended with '_'.
    supplier_2_vat_field = models.FloatField(
        db_column='Supplier___2___VAT_', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_currency = models.TextField(
        db_column='Supplier___2___Currency', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_barcode = models.FloatField(
        db_column='Supplier___2___Barcode', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_reference = models.TextField(
        db_column='Supplier___2___Reference', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_product_name = models.TextField(
        db_column='Supplier___2___Product_Name', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_minimum_order_quantity = models.FloatField(
        db_column='Supplier___2___Minimum_Order_Quantity', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_unit_of_measurement = models.FloatField(
        db_column='Supplier___2___Unit_of_Measurement', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_package_size = models.FloatField(
        db_column='Supplier___2___Package_Size', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_lead_time = models.FloatField(
        db_column='Supplier___2___Lead_Time', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_days_of_stock = models.FloatField(
        db_column='Supplier___2___Days_of_Stock', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_safety_stock = models.FloatField(
        db_column='Supplier___2___Safety_Stock', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_default = models.FloatField(
        db_column='Supplier___2___Default', blank=True, null=True)
    # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    supplier_2_note = models.FloatField(
        db_column='Supplier___2___Note', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pro_product_suppliers'


class ProStockReport(models.Model):
    # Field name made lowercase.
    id = models.BigIntegerField(db_column='ID', blank=True, primary_key=True)
    # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)
    # Field name made lowercase.
    sku = models.TextField(db_column='SKU', blank=True, null=True)
    # Field name made lowercase.
    on_stock = models.BigIntegerField(
        db_column='On_Stock', blank=True, null=True)
    # Field name made lowercase.
    layers_warehouse = models.TextField(
        db_column='Layers_Warehouse', blank=True, null=True)
    # Field name made lowercase.
    on_stock_layer = models.FloatField(
        db_column='On_Stock_Layer', blank=True, null=True)
    # Field name made lowercase.
    net_price = models.FloatField(db_column='Net_Price', blank=True, null=True)
    # Field name made lowercase.
    landed_cost_layer = models.FloatField(
        db_column='Landed_Cost_Layer', blank=True, null=True)
    # Field name made lowercase.
    inventory_value_layer = models.FloatField(
        db_column='Inventory_Value_Layer', blank=True, null=True)
    # Field name made lowercase.
    date = models.TextField(db_column='Date', blank=True, null=True)
    # Field name made lowercase.
    sales = models.BigIntegerField(db_column='Sales', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pro_stock_report'


class ProSzmlk(models.Model):
    # Field name made lowercase.
    szamla_belso_azonosito = models.TextField(
        db_column='Szamla_belso_azonosito', blank=True, null=True)
    # Field name made lowercase.
    szamla_azonosito = models.TextField(
        db_column='Szamla_azonosito', blank=True, null=True)
    # Field name made lowercase.
    date = models.TextField(db_column='Date', blank=True, null=True)
    # Field name made lowercase.
    hatarido = models.TextField(db_column='Hatarido', blank=True, null=True)
    # Field name made lowercase.
    fizetes_datuma = models.TextField(
        db_column='Fizetes_datuma', blank=True, null=True)
    # Field name made lowercase.
    teljesites_datuma = models.TextField(
        db_column='Teljesites_datuma', blank=True, null=True)
    # Field name made lowercase.
    tipus = models.TextField(db_column='Tipus', blank=True, null=True)
    # Field name made lowercase.
    fizetesi_allapot = models.TextField(
        db_column='Fizetesi_allapot', blank=True, null=True)
    # Field name made lowercase.
    iktatasi_allapot = models.TextField(
        db_column='Iktatasi_Allapot', blank=True, null=True)
    # Field name made lowercase.
    expired = models.BooleanField(db_column='Expired', blank=True, null=True)
    # Field name made lowercase.
    partner = models.TextField(db_column='Partner', blank=True, null=True)
    # Field name made lowercase.
    szallitmanyok = models.TextField(
        db_column='Szallitmanyok', blank=True, null=True)
    # Field name made lowercase.
    koltseg = models.FloatField(db_column='Koltseg', blank=True, null=True)
    # Field name made lowercase.
    penznem = models.TextField(db_column='Penznem', blank=True, null=True)
    # Field name made lowercase.
    atvaltasi_rata = models.FloatField(
        db_column='Atvaltasi_rata', blank=True, null=True)
    # Field name made lowercase.
    osszesen_huf = models.FloatField(
        db_column='Osszesen_HUF', blank=True, null=True)
    # Field name made lowercase.
    pdf = models.TextField(db_column='PDF', blank=True, null=True)
    # Field name made lowercase.
    fizetesi_mod = models.TextField(
        db_column='Fizetesi_mod', blank=True, null=True)
    # Field name made lowercase.
    megjegyzes = models.TextField(
        db_column='Megjegyzes', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pro_számlák'


class StartingClosingCf(models.Model):
    months = models.TextField(blank=True, null=True)
    starting_values = models.BigIntegerField(blank=True, null=True)
    closing_values = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'starting_closing_cf'