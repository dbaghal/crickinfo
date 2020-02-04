from django.db import models
from random import randint
from collections import Counter
from django.core.exceptions import ValidationError
from django.urls import reverse,reverse_lazy
import datetime


class OrderManager(models.Manager):
  def get_random(self, items=1):
    if isinstance(items, int):
        return self.model.objects.order_by('?')[:items]
    return self.all()

class Team(models.Model):
    name = models.CharField(max_length=255,unique=True)
    logo  = models.ImageField(upload_to='image/',)
    club_state = models.CharField(max_length=255)
    objects = OrderManager()
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Team"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team_identity',kwargs={'pk':self.pk })

class PlayerStats(models.Model):
    player = models.OneToOneField('Player',on_delete=models.CASCADE)
    matches = models.IntegerField(default=0)
    runs = models.IntegerField(default=0)
    fifty = models.IntegerField(default=0)
    hundred = models.IntegerField(default=0)
    highest_score  = models.IntegerField(default=0)
    wicket = models.IntegerField(default=0)
    team = models.ForeignKey('Team',related_name='team_match',on_delete=models.CASCADE)
    match = models.ForeignKey('Matches',related_name='team_matches',on_delete=models.CASCADE)


    def __str__(self):
        return str(self.runs)

    class Meta:
        verbose_name = "PlayerStats"
        verbose_name_plural = "PlayerStats"

class Player(models.Model):
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    image = models.ImageField(upload_to='player/',)
    jersy_number = models.IntegerField()
    country = models.CharField(max_length=255)
    team = models.ForeignKey('Team',related_name='team_player',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team', 'jersy_number')
        verbose_name = "Player"
        verbose_name_plural = "Players"

    def __str__(self):
        return self.first_name

class Matches(models.Model):
    venue = models.CharField(max_length=255)
    date  = models.DateField()
    host_team  = models.ForeignKey('Team',related_name='host',on_delete=models.CASCADE)
    opponent_team = models.ForeignKey('Team',related_name='opponent',on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        return str(self.host_team) + " vs " + str(self.opponent_team)
    
    def validate_unique(self, *args, **kwargs):
        super(Matches, self).validate_unique(*args, **kwargs)

        if self.__class__.objects.filter(host_team=self.host_team,opponent_team=self.opponent_team, date=self.date).exists() or self.__class__.objects.filter(host_team=self.opponent_team,opponent_team=self.host_team, date=self.date).exists():
            raise ValidationError(
                message=f'Match with team ({self.host_team},{self.opponent_team}, for {self.date}) already exists.',
                code='unique_together',
            )

    def save(self, *args, **kwargs):
        random_teams = Team.objects.get_random(2)
        random_team = [i for i in random_teams]
        team_list = [i for i in Team.objects.all() if i not in random_team]
        if random_team[0] != random_team[1]:
            self.host_team = random_team[0]
            self.opponent_team = random_team[1]
        else:
            self.host_team = random_team[0]
            self.opponent_team = team_list[0]
            
        super(Matches, self).save(*args, **kwargs)

Winner = (
    (1,'Host Team'),
    (2,'Opponent Team')
)
class MatchResult(models.Model):
    match = models.OneToOneField('Matches', related_name='result', on_delete=models.CASCADE)
    winner = models.IntegerField(choices=Winner,default=1)
    def winner_name(self):
        if self.winner == 1:
            return str(self.match.host_team.name)
        else:
            return str(self.match.opponent_team.name)

    def __str__(self):
        return str(self.winner)

class PointsTable(models.Model):
    team_name = models.OneToOneField('Team',on_delete=models.CASCADE)
    matches  = models.IntegerField(default=0)
    win   = models.IntegerField(default=0)
    loss  = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return str(self.team_name)

    def save(self, *args, **kwargs):
        match_list = Matches.objects.all().values_list('host_team__name','opponent_team__name')
        team_played_list = [item for i in match_list for item in i ]
        match_played = Counter(team for team in team_played_list )
        result_list = MatchResult.objects.all().values_list('winner','match__host_team__name','match__opponent_team__name')
        match_result = []
        for j in result_list:
            if j[0] == 1:
                match_result.append(j[1])
            else:
                match_result.append(j[2])
        win_list = Counter(i for i in match_result)
        if self.team_name.name in team_played_list:
            self.matches = match_played[self.team_name.name]
            self.win     = win_list[self.team_name.name]
            self.loss    = self.matches - self.win
            self.points  = self.win * 2 
        super(PointsTable, self).save(*args, **kwargs)
