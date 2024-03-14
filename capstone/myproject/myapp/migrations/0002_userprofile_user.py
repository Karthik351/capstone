from django.db import migrations, models
from django.utils import timezone

def create_default_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    user = User.objects.create()
    UserProfile = apps.get_model('myapp', 'UserProfile')
    UserProfile.objects.update(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(
                on_delete=models.CASCADE,
                to='auth.User',
                null=True,  # Add this line to make the field nullable
            ),
        ),
        migrations.RunPython(create_default_user),
    ]
