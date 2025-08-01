# Generated by Django 3.2.5 on 2024-03-25 03:48

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bloginfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('b_content', models.TextField()),
                ('user_id', models.TextField(blank=True, null=True)),
                ('hot_index', models.TextField(blank=True, null=True)),
                ('admin_cheak', models.TextField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('img1', models.TextField(blank=True, null=True)),
                ('intr', models.TextField(blank=True, null=True)),
                ('hit_num', models.TextField(blank=True, null=True)),
                ('blog_name', models.TextField(blank=True, null=True)),
                ('user_blog', tinymce.models.HTMLField()),
            ],
            options={
                'db_table': 'bloginfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comminfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('usr_id', models.IntegerField()),
                ('jd_id', models.IntegerField()),
                ('commentinfo', models.TextField(blank=True, null=True)),
                ('datetime', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'comminfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Foodinfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('foodname', models.CharField(blank=True, max_length=100, null=True)),
                ('introudec', models.CharField(blank=True, max_length=300, null=True)),
                ('img', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'foodinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Historyinfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('userid', models.IntegerField(blank=True, null=True)),
                ('jdintr', models.TextField(blank=True, null=True)),
                ('foodintr', models.TextField(blank=True, null=True)),
                ('datetime', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'historyinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Hotleinfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hotlename', models.CharField(blank=True, max_length=100, null=True)),
                ('introudec', models.CharField(blank=True, max_length=300, null=True)),
                ('img', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'hotleinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Jdinfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('jiname', models.CharField(blank=True, max_length=100, null=True)),
                ('jdtype', models.CharField(blank=True, max_length=30, null=True)),
                ('jdwhere', models.CharField(blank=True, max_length=100, null=True)),
                ('times', models.CharField(blank=True, max_length=30, null=True)),
                ('lon', models.CharField(blank=True, max_length=50, null=True)),
                ('lat', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('grade', models.CharField(blank=True, max_length=20, null=True)),
                ('sum_sc', models.CharField(blank=True, max_length=10, null=True)),
                ('jd_sc', models.CharField(blank=True, max_length=10, null=True)),
                ('yq_sc', models.CharField(blank=True, max_length=10, null=True)),
                ('xj_sc', models.CharField(blank=True, max_length=10, null=True)),
                ('img1', models.CharField(blank=True, max_length=100, null=True)),
                ('img2', models.CharField(blank=True, max_length=100, null=True)),
                ('img3', models.CharField(blank=True, max_length=100, null=True)),
                ('introudec', models.CharField(blank=True, max_length=300, null=True)),
                ('jdtype1', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'jdinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trficinfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('trname', models.CharField(blank=True, max_length=30, null=True)),
                ('trtype', models.CharField(blank=True, max_length=30, null=True)),
                ('trprice', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'trficinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('tel', models.TextField(blank=True, null=True)),
                ('password', models.TextField(blank=True, null=True)),
                ('img', models.TextField(blank=True, null=True)),
                ('user_like', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'userinfo',
                'managed': False,
            },
        ),
    ]
