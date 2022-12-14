# Generated by Django 4.1.3 on 2022-12-08 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=20, verbose_name='название')),
                ('favorites', models.BooleanField(default=False, verbose_name='избранное')),
                ('super_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_shop.category', verbose_name='родительская категория')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='название')),
                ('count', models.PositiveIntegerField(blank=True, default=1, verbose_name='количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='цена')),
                ('description', models.TextField(max_length=5000, verbose_name='описание')),
                ('status', models.SlugField(choices=[('limited', 'Ограниченный тираж'), ('top', 'Топ продаж'), ('sale', 'Распродажа'), ('default', 'Стандарт')], default='default', max_length=10)),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='дата поступления')),
                ('image', models.ImageField(blank=True, upload_to='products/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='app_shop.category')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'product',
            },
        ),
    ]
