# Generated by Django 3.0 on 2020-04-25 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('currency_code', models.CharField(choices=[('USD', 'US dollar'), ('CAD', 'CA dollar')], default='CAD', max_length=3)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('application_date', models.DateField(blank=True, null=True)),
                ('deadline_minimum_spending', models.DateField(blank=True, null=True)),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('cancellation_date', models.DateField(blank=True, null=True)),
                ('mininum_spending', models.IntegerField(blank=True, null=True)),
                ('signup_bonus', models.IntegerField(blank=True, null=True)),
                ('first_year_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('annual_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cycle_day', models.IntegerField(blank=True, null=True)),
                ('earning_rates', models.CharField(blank=True, max_length=200, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.Account')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_added', models.DateField()),
                ('payment_method_type', models.CharField(choices=[('CC', 'Credit card'), ('CA', 'Cash'), ('ET', 'E-transfer'), ('TR', 'Direct transfer'), ('CK', 'Check')], default='CC', max_length=2)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.Account')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expense.Category')),
                ('credit_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expense.CreditCard')),
            ],
        ),
    ]
