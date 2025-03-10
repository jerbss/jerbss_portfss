from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_projectdraft'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='collaboration',
            field=models.CharField(
                choices=[('solo', 'Solo'), ('duo', 'Dupla'), ('trio', 'Trio'), ('group', 'Grupo (4+)')],
                default='solo',
                max_length=20,
                verbose_name='Colaboração'
            ),
        ),
        migrations.AddField(
            model_name='projectdraft',
            name='collaboration',
            field=models.CharField(
                choices=[('solo', 'Solo'), ('duo', 'Dupla'), ('trio', 'Trio'), ('group', 'Grupo (4+)')],
                default='solo',
                max_length=20,
                verbose_name='Colaboração'
            ),
        ),
    ]
