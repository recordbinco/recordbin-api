# Generated by Django 2.1.3 on 2018-11-16 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0002_auto_20160226_1747'),
        ('recordbin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='token',
            field=models.ForeignKey(default='51620f580086dd9f8f30efed30b248f597f771f9', on_delete=django.db.models.deletion.CASCADE, related_name='records', to='authtoken.Token'),
            preserve_default=False,
        ),
    ]
