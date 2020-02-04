# Generated by Django 2.2.7 on 2020-02-04 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue', models.CharField(max_length=255)),
                ('date', models.DateField()),
            ],
            options={
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='player/')),
                ('jersy_number', models.IntegerField()),
                ('country', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Player',
                'verbose_name_plural': 'Players',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('logo', models.ImageField(upload_to='image/')),
                ('club_state', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Team',
            },
        ),
        migrations.CreateModel(
            name='PointsTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matches', models.IntegerField(default=0)),
                ('win', models.IntegerField(default=0)),
                ('loss', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('team_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='basic_info.Team')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matches', models.IntegerField(default=0)),
                ('runs', models.IntegerField(default=0)),
                ('fifty', models.IntegerField(default=0)),
                ('hundred', models.IntegerField(default=0)),
                ('highest_score', models.IntegerField(default=0)),
                ('wicket', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_matches', to='basic_info.Matches')),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='basic_info.Player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_match', to='basic_info.Team')),
            ],
            options={
                'verbose_name': 'PlayerStats',
                'verbose_name_plural': 'PlayerStats',
            },
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_player', to='basic_info.Team'),
        ),
        migrations.CreateModel(
            name='MatchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.IntegerField(choices=[(1, 'Host Team'), (2, 'Opponent Team')], default=1)),
                ('match', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='basic_info.Matches')),
            ],
        ),
        migrations.AddField(
            model_name='matches',
            name='host_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host', to='basic_info.Team'),
        ),
        migrations.AddField(
            model_name='matches',
            name='opponent_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='basic_info.Team'),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together={('team', 'jersy_number')},
        ),
    ]