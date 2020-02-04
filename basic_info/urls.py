from django.urls import path
from .views import *

urlpatterns = [
    path('',TeamListView.as_view(),name='team_list'),
    # path('team_list/',TeamListView.as_view(),name='team_list'),
    path('team_identity/<int:pk>',TeamIdentityView.as_view(),name='team_identity'),
    path('matches_list/',MatchesListView.as_view(),name='matches_list'),
    path('points_table/',PointsTableListView.as_view(),name='points_table'),
    path('player_history/',PlayerHistoryView.as_view(),name='player_history'),
    path('player/add/<int:pk>', PlayerCreateView.as_view(), name='player-add'),
    path('player/<int:pk>/', PlayerUpdateView.as_view(), name='player-update'),
    path('player/<int:pk>/delete', PlayerDeleteView.as_view(), name='player-delete'),
    path('match_detail/<int:pk>',MatchesDetailView.as_view(),name='match_detail'),
    path('team/',TeamView.as_view(),name='team'),
    path('team-create/',MatchCreateView.as_view(),name='createteam'),
    path('team_detail/<int:pk>',TeamDetailView.as_view(),name='team_detail'),
    path('player/',PlayerListCreateView.as_view(),name='player'),
    path('player_stats/',PlayerStatsView.as_view(),name='player_stats'),   
    path('player_history_detail/<int:pk>',PlayerStatsDetailView.as_view(),name='player_history_detail'),
    path('player_detail/<int:pk>',PlayerDetailView.as_view(),name='player_detail'),
    path('match/',MatchScheduleView.as_view(),name='match'),
    path('match_result/',MatchResultView.as_view(),name='match_result'),
    path('points/',PointsTableView.as_view(),name='points'),    
]
