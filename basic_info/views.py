from django.shortcuts import render,get_object_or_404 
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse,reverse_lazy
from .models import *
from .serializers import *
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from .forms import *
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator



class TeamListView(ListView):
    '''
    List of teams available
    '''
    model = Team
    template_name = 'user/dashboard.html'
    context_object_name = 'teams'
    paginate_by = 10
    queryset = Team.objects.all()

class TeamIdentityView(DetailView):
    '''
    Team Detail with all its player
    '''
    context_object_name = 'team'
    model = Team
    template_name='user/team-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player'] = Player.objects.filter(team__id=self.object.id)
        return context

class MatchCreateView(CreateView):
    model = Matches
    form_class = MatchForm
    template_name = 'user/add_team.html'

    def get_success_url(self):
        return reverse('team', kwargs={'pk': self.object.matches.id})

    def form_invalid(self, form):
        return HttpResponse(form.errors)




class MatchesListView(ListView):
    '''
    List of the Matches available
    '''
    model = Matches
    template_name= 'user/match_list.html'

class MatchesDetailView(DetailView):
    '''
    Result of each Matches
    '''
    context_object_name = 'match'
    model = Matches
    template_name = 'user/match_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['match_result'] = MatchResult.objects.filter(match_id=self.object.id).values_list('winner',flat=True)
        context['player'] = PlayerStats.objects.filter(match__id=self.object.id).order_by('-id')[:2]
        context['looser'] = PlayerStats.objects.filter(match__id=self.object.id).order_by('id')[:2]
        if context['match_result']== 1:
            context['winner'] = self.object.host_team
        else:
            context['winner'] = self.object.opponent_team
        return context

class PointsTableListView(ListView):
    '''
    Points Table
    '''
    model = PointsTable
    ordering = ['-points']
    template_name = 'user/pointstable.html'

class PlayerHistoryView(ListView):
    '''
    Player History
    '''
    model = PlayerStats
    template_name = 'user/player_history.html'

class PlayerCreateView(CreateView):
    '''
    Create a New Player within any team
    '''

    model = Player
    form_class = PlayerForm
    template_name='user/add_player.html'

    def get_success_url(self):
        return reverse('team_identity', kwargs={'pk': self.object.team.id})
        
    def form_valid(self, form):
        team = get_object_or_404(Team, id=self.kwargs['pk'])
        form.instance.team = team
        return super(PlayerCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return HttpResponse(form.errors)

class PlayerUpdateView(UpdateView):
    '''
    Update a player info within any team
    '''
    model = Player
    form_class = PlayerForm
    template_name='user/add_player.html'

    def get_success_url(self):
        return reverse('team_identity', kwargs={'pk': self.object.team.id})

class PlayerDeleteView(DeleteView):
    '''
    Delete any Player from any team
    '''
    model = Player
    success_url = reverse_lazy('team_list')
    template_name='user/remove_player.html'

'''
List of API"S
'''


class TeamView(generics.ListCreateAPIView):
    '''
    list of all teams and create API
    '''
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetailView(APIView):
    '''
    Retrieve a particular team data, update and delete it
    '''

    def get_object(self, pk):

        try:
            return Team.objects.get(id=pk)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request,pk,format=None):
        '''
        retreive a team data
        '''
        queryset = self.get_object(pk)

        serializer = TeamPlayerSerializer(queryset)

        return Response(serializer.data)
    
    def put(self, request,pk,format=None):
        '''
        update a existing team data
        '''
        queryset = self.get_object(pk)
        serializer = TeamSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        '''
        delete any existing data
        '''
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlayerListCreateView(generics.ListCreateAPIView):
    '''
    Create and List all the players
    '''
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrive, Update and Delete any player from the Database
    '''
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class MatchScheduleView(generics.ListCreateAPIView):
    '''
    Automatically generates Fixtures
    '''
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer

class MatchResultView(generics.ListCreateAPIView):
    '''
    Match Result table
    '''
    queryset = MatchResult.objects.all()
    serializer_class = MatchResultSerializer

class PointsTableView(generics.ListCreateAPIView):
    '''
    Results Table
    '''
    queryset = PointsTable.objects.all()
    serializer_class = PointsTableSerializer

class PlayerStatsView(generics.ListCreateAPIView):
    '''
    Although this section will be automatically but for now you can get and create it from here
    '''
    queryset = PlayerStats.objects.all()
    serializer_class = PlayerStatsSerializer

class PlayerStatsDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrive, Update and Delete any PlayerStats from the Database
    '''
    queryset = PlayerStats.objects.all()
    serializer_class = PlayerStatsSerializer


