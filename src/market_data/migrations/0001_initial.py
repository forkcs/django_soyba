# Generated by Django 4.2 on 2023-04-10 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=255)),
                ('market_data_source', models.CharField(choices=[('binance', 'Binance')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OHLC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.DecimalField(decimal_places=16, max_digits=32)),
                ('close', models.DecimalField(decimal_places=16, max_digits=32)),
                ('low', models.DecimalField(decimal_places=16, max_digits=32)),
                ('high', models.DecimalField(decimal_places=16, max_digits=32)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                (
                    'instrument',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='ohlc_list',
                        to='market_data.instrument',
                    ),
                ),
            ],
        ),
    ]