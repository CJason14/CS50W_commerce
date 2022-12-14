# Generated by Django 4.1 on 2022-10-01 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listings_currentbid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('key', models.CharField(max_length=200)),
                ('bidder', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='listings',
            name='currentbid',
        ),
        migrations.RemoveField(
            model_name='listings',
            name='currentprice',
        ),
    ]
