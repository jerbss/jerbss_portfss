# Generated by Django 5.1.6 on 2025-03-04 12:40

from django.db import migrations, models
from tinymce.models import HTMLField


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_at'], 'verbose_name': 'Projeto', 'verbose_name_plural': 'Projetos'},
        ),
        migrations.RemoveField(
            model_name='project',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='projects',
        ),
        migrations.AddField(
            model_name='project',
            name='content',
            field=HTMLField(default='', verbose_name='Conteúdo Completo'),
        ),
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Conclusão'),
        ),
        migrations.AddField(
            model_name='project',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Projeto Destacado'),
        ),
        migrations.AddField(
            model_name='project',
            name='github_url',
            field=models.URLField(blank=True, null=True, verbose_name='Link do GitHub'),
        ),
        migrations.AddField(
            model_name='project',
            name='short_description',
            field=models.TextField(default='', max_length=500, verbose_name='Breve Descrição'),
        ),
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateField(default='2024-01-01', verbose_name='Data de Início'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('in_progress', 'Em andamento'), ('completed', 'Concluído')], default='in_progress', max_length=20, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='projects', to='main.tag'),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Última Atualização'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de Publicação'),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(upload_to='projects/', verbose_name='Capa do Projeto'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.CharField(choices=[('web', 'Web Development'), ('mobile', 'Mobile Development'), ('design', 'Design'), ('other', 'Outro')], default='web', max_length=20, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='project',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Link do Projeto'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
