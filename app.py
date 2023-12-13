
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import numpy as np




######### DATA #####################################################################################################################################
####################################################################

#--DIM_TABLES------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# ARENAS------------------------------------------------------------------------------------------
#df_dim_arena_info = pd.read_excel('data/dim_arena_info.xlsx')
#df_dim_arena_info = df_dim_arena_info.drop(columns=['shortName','teamName','abbreviation','franchiseId'])

# DATES------------------------------------------------------------------------------------------
#df_dim_dates = pd.read_csv('data/dim_dates.csv')
#df_dim_dates = df_dim_dates.drop(columns=['Record_timestamp'])
#df_dim_dates["Date"] = pd.to_datetime(df_dim_dates["Date"])
#df_dim_dates["DateKey"] = df_dim_dates["Date"].astype(str)
#df_dim_dates["DateKey"] = df_dim_dates["DateKey"].str.replace('-','')

# GAMES------------------------------------------------------------------------------------------
#df_dim_game = pd.read_csv('data/dim_game.csv')
#df_dim_game["Date"] = pd.to_datetime(df_dim_game["date_time_GMT"]).dt.date
#df_dim_game["DateKey"] = df_dim_game["Date"].astype(str)
#df_dim_game["DateKey"] = df_dim_game["DateKey"].str.replace('-','')
#df_dim_game = df_dim_game.drop(columns=['venue_link','venue_time_zone_id','venue_time_zone_offset','venue_time_zone_tz',
#                                        'date_time_GMT','venue','home_rink_side_start'])

# PLAYERS------------------------------------------------------------------------------------------
#df_dim_player_info = pd.read_csv('data/dim_player_info.csv')
#df_dim_player_info["birthDate"] = pd.to_datetime(df_dim_player_info["birthDate"]).dt.date
#df_dim_player_info = df_dim_player_info.drop(columns=['height_cm'])

# SEASON YEAR------------------------------------------------------------------------------------------
df_dim_seasonyear_ref = pd.read_csv('data/dim_seasonyear_ref.csv')

# TEAM COLORS------------------------------------------------------------------------------------------
df_dim_team_colors = pd.read_csv('data/dim_team_colors.csv')
df_dim_team_colors = df_dim_team_colors.drop(columns=['shortName','teamName','abbreviation','LogoUrl','WordMarkURL'])

# TEAM INFO------------------------------------------------------------------------------------------
df_dim_team_info = pd.read_excel('data/dim_team_info.xlsx')
df_dim_team_info = df_dim_team_info.drop(columns=['link'])
df_dim_team_info = df_dim_team_info.loc[(df_dim_team_info['team_id']!=11)&
                (df_dim_team_info['team_id']!=27)]




#--FACT_TABLES------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#--GAME_STATS---------------------- ----------------------------------------------------------------
# GAME GOALIE------------------------------------------------------------------------------------------
#df_fact_game_goalie_stats = pd.read_csv('data/fact_game_goalie_stats.csv')

# GAME GOALS------------------------------------------------------------------------------------------
#df_fact_game_goals = pd.read_csv('data/fact_game_goals.csv')
#df_fact_game_goals["gameWinningGoal"].fillna("False", inplace = True)
#df_fact_game_goals["emptyNet"].fillna("False", inplace = True)

# GAME PENALTY------------------------------------------------------------------------------------------
#df_fact_game_penalties = pd.read_csv('data/fact_game_penalties.csv')

# GAME PLAYER PLAYS------------------------------------------------------------------------------------------
#df_fact_game_plays_players = pd.read_csv('data/fact_game_plays_players.csv')

# GAME PLAYS------------------------------------------------------------------------------------------
#df_fact_game_plays = pd.read_csv('data/fact_game_plays.csv')
#df_fact_game_plays = df_fact_game_plays.dropna(subset=['team_id_for'])
#df_fact_game_plays = df_fact_game_plays.drop(columns=['dateTime'])

# GAME SCRATCHES------------------------------------------------------------------------------------------
#df_fact_game_scratches = pd.read_csv('data/fact_game_scratches.csv')

# GAME SHIFTS------------------------------------------------------------------------------------------
#df_fact_game_shifts = pd.read_csv('data/fact_game_shifts.csv')

# GAME SKATER STATS------------------------------------------------------------------------------------------
#df_fact_game_skater_stats = pd.read_csv('data/fact_game_skater_stats.csv')

# GAME TEAM STATS------------------------------------------------------------------------------------------
#df_fact_game_teams_stats = pd.read_csv('data/fact_game_teams_stats.csv')


#--SEASON_STATS--------------------------------------------------------------------------------------
# ATTENDENCE------------------------------------------------------------------------------------------
#df_fact_attendance = pd.read_csv('data/fact_attendance.csv')
#df_fact_attendance = df_fact_attendance.drop(columns=['shortName','teamName','abbreviation','Address','City','State','Country','Zip'])

# SEASON STANDINGS------------------------------------------------------------------------------------------
df_fact_season_standings = pd.read_csv('data/fact_season_standings.csv')

# SEASON TEAM STATS------------------------------------------------------------------------------------------
df_fact_season_teams_stats = pd.read_csv('data/fact_season_teams_stats.csv')
df_fact_season_teams_stats_all = pd.read_csv('data/fact_season_teams_stats.csv')
df_fact_season_teams_stats = df_fact_season_teams_stats[df_fact_season_teams_stats['situation']=='all']

# SEASON GOALIE STATS------------------------------------------------------------------------------------------
#df_fact_season_goalie_stats = pd.read_csv('data/fact_season_goalie_stats.csv')

# SEASON SKATER STATS------------------------------------------------------------------------------------------
#df_fact_season_skaters_stats = pd.read_csv('data/fact_season_skaters_stats.csv')

# SEASON LINE STATS------------------------------------------------------------------------------------------
#df_fact_season_lines_stats = pd.read_csv('data/fact_season_lines_stats.csv')

# CUP WINNERS STATS------------------------------------------------------------------------------------------
df_fact_cup_winners = pd.read_csv('data/fact_cup_winners.csv')





# MERGED DATA------------------------------------------------------------------------------------------

# merge team colors with team info
df_team_colors_merged = pd.merge(df_dim_team_colors, df_dim_team_info[['shortName','teamName','team_id','fullName']], on=['team_id'])

# merge seaon standings with team info
fact_season_standings_merged =  pd.merge(df_fact_season_standings, df_dim_team_info[['shortName','teamName','team_id','fullName']], on=['team_id'])
fact_season_standings_merged =  pd.merge(fact_season_standings_merged, df_dim_seasonyear_ref[['season_year','season']], on=['season'])

# merge season stats with standings
fact_team_stats_merged = pd.merge(df_fact_season_teams_stats, fact_season_standings_merged[['GP','W','L','OTL','RW','GF','GA','Playoff Seed','PlayoffRound','Playoff Seed_Cat','PlayoffRound_Cat','season_year','team_id','Playoffs','RoundCategory']], on = ['team_id', 'season_year'])
fact_team_stats_merged =  pd.merge(fact_team_stats_merged, df_dim_team_info[['shortName','teamName','team_id','fullName','Conference','Division']], on=['team_id'])

# create calculated columns in team stats
fact_team_stats_merged["WinPercentage"] = (fact_team_stats_merged["W"]*2 + fact_team_stats_merged["OTL"]) / (fact_team_stats_merged["GP"]*2)*100
fact_team_stats_merged["GoalDifferential"] = (fact_team_stats_merged['GF']-fact_team_stats_merged['GA'])/fact_team_stats_merged['season_year']
fact_team_stats_merged["Points"] = (fact_team_stats_merged["W"]*2 + fact_team_stats_merged["OTL"])


#fact_team_stats_merged_all = pd.merge(df_fact_season_teams_stats_all, fact_season_standings_merged[['GP','W','L','OTL','RW','GF','GA','Playoff Seed','PlayoffRound','Playoff Seed_Cat','PlayoffRound_Cat','season_year','team_id','Playoffs','RoundCategory']], on = ['team_id', 'season_year'])
#fact_team_stats_merged_all =  pd.merge(fact_team_stats_merged_all, df_dim_team_info[['shortName','teamName','team_id','fullName','Conference','Division']], on=['team_id'])

#fact_team_stats_merged_all["WinPercentage"] = (fact_team_stats_merged_all["W"]*2 + fact_team_stats_merged_all["OTL"]) / (fact_team_stats_merged_all["GP"]*2)*100
#fact_team_stats_merged_all["GoalDifferential"] = (fact_team_stats_merged_all['GF']-fact_team_stats_merged_all['GA'])/fact_team_stats_merged_all['season_year']
#fact_team_stats_merged_all["Points"] = (fact_team_stats_merged_all["W"]*2 + fact_team_stats_merged_all["OTL"])





######### FUNCTIONS #####################################################################################################################################
####################################################################

# function to calculate columns frequently used
def calc_standings_column(data):
    data["WinPercentage"] = (data["W"] * 2 + data["OTL"]) / (data["GP"] * 2) * 100
    data["Points"] = (data["W"] * 2 + data["OTL"])
    data["GoalDifferential"] = (data['GF'] - data['GA'])
    return data


# function to group data frequently used. Passed a data frame and the column to group by
def group_season_data(data, column):
    grouped_df = data.groupby([column], as_index=False).agg(
        {'Pos': 'mean', 'GP': 'sum', 'W': 'sum', 'L': 'sum', 'OTL': 'sum', 'RW': 'sum', 'GF': 'sum', 'GA': 'sum',
         'season_year': 'count'})
    grouped_df["WinPercentage"] = (grouped_df["W"] * 2 + grouped_df["OTL"]) / (grouped_df["GP"] * 2) * 100
    grouped_df["GoalDifferential"] = (grouped_df['GF'] - grouped_df['GA']) / grouped_df['season_year']
    grouped_df["Avg Points"] = (grouped_df["W"] * 2 + grouped_df["OTL"]) / grouped_df['season_year']
    grouped_df = grouped_df.round(decimals=0)
    grouped_df = grouped_df.sort_values(by='WinPercentage', ascending=False)
    return grouped_df


# function to calculate the average playoff points
def avg_playoff_points(data):
    playoffs_filtered_df = data[data['Playoffs'] == 'Y']  # filter for only playoff teams
    playoffs_group_df = playoffs_filtered_df.groupby(['season_year'], as_index=False).agg(
        {'GP': 'sum', 'W': 'sum', 'OTL': 'sum', 'team_id': 'count'})
    playoff_team_gp = playoffs_group_df['GP'].sum()
    playoff_teams_total = playoffs_group_df['team_id'].sum()
    playoff_team_w = playoffs_group_df['W'].sum()
    playoff_team_otl = playoffs_group_df['OTL'].sum()
    AvgPlayoffWinPercentage = ((playoff_team_w * 2) + playoff_team_otl) / (playoff_team_gp * 2) * 100
    AvgPlayoffWinPercentage = AvgPlayoffWinPercentage.round(decimals=0)
    AvgPlayoffPoints = ((playoff_team_w * 2) + playoff_team_otl) / playoff_teams_total
    AvgPlayoffPoints = AvgPlayoffPoints.round(decimals=0)
    return AvgPlayoffWinPercentage, AvgPlayoffPoints


# function to retrieve the logo, url, and team colors
def get_colors_logo(data):
    # get logo and workmark urls
    logo = data['LogoURLDark'].values[0]
    wordmark = data['NHLWordMarkURL'].values[0]
    logo_light = data['LogoURLLight'].values[0]
    # get custom colors
    bg_color = data['BackgroundColor'].values[0]
    sec_color = data['AccentColor'].values[0]
    th_color = data['Color3'].values[0]
    # get team url
    url = data['URL'].values[0]
    return logo, wordmark, logo_light, bg_color, sec_color, th_color, url


# function to create scatter plot. Passed a dataframe, metric to use on y axis, and color sequence
def create_scatter(data, metric, color_seq):
    data = data.rename(columns={"fullName": "Team", "season_year": "Season", 'PlayoffRound_Cat': "Playoff Round",
                                'Playoff Seed_Cat': 'Playoffs Seed'})
    fig_scatter = px.scatter(data, x='WinPercentage', y=metric, color='Points', color_continuous_scale=color_seq,
                             size='RoundCategory', hover_data=['Team', 'Season', 'Playoff Round', 'Playoffs Seed'])
    # fig_scatter.add_vline(x=AvgPlayoffWinPercentage, annotation_text='Average Playoff Team Winning % = 68%')
    return fig_scatter


# function to create main bar chart. Passed data, axis variables, and colors
def create_main_bar(data, xaxis, yaxis, sel_color, color_seq):
    fig_bar = px.bar(data, x=xaxis, y=yaxis, color=sel_color, color_continuous_scale=color_seq
                     # ,hover_data=[hover]
                     )
    # fig_bar.add_hline(y=AvgPlayoffWinPercentage, annotation_text='Average Playoff Team Winning % = 62%')
    return fig_bar


# function to create the data frame used in cup winner visuals
def create_cup_winners_df(data):
    df_fact_cup_winners_grouped_win = data.groupby(['Winning Team', 'WinningTeamId'], as_index=False).agg(
        {'season_year': 'count'})  # create df for only winning teams
    df_fact_cup_winners_grouped_loss = data.groupby(['Losing Team', 'LosingTeamId'], as_index=False).agg(
        {'season_year': 'count'})  # create df for only losing teams
    df_fact_cup_winners_grouped = pd.merge(df_dim_team_info, df_fact_cup_winners_grouped_win, how='left',
                                           left_on='team_id', right_on='WinningTeamId')  # merge team info
    df_fact_cup_winners_grouped = pd.merge(df_fact_cup_winners_grouped, df_fact_cup_winners_grouped_loss, how='left',
                                           left_on='team_id', right_on='LosingTeamId')  # merge team info
    df_fact_cup_winners_grouped = df_fact_cup_winners_grouped.rename(columns={"season_year_x": "Cup Wins",
                                                                              "season_year_y": 'Cup Losses'})  # merge win and loss df to count
    df_fact_cup_winners_grouped = df_fact_cup_winners_grouped.drop(
        columns=['Losing Team', 'franchiseId', 'Arena', 'Address', 'City', 'State', 'Zip', 'ArenaID', 'Winning Team',
                 'WinningTeamId', 'Losing Team', 'LosingTeamId'])
    df_fact_cup_winners_grouped['Cup Wins'] = df_fact_cup_winners_grouped['Cup Wins'].fillna(0)
    df_fact_cup_winners_grouped['Cup Losses'] = df_fact_cup_winners_grouped['Cup Losses'].fillna(0)
    df_fact_cup_winners_grouped['Appearances'] = df_fact_cup_winners_grouped['Cup Wins'] + df_fact_cup_winners_grouped[
        'Cup Losses']
    df_fact_cup_winners_grouped['Win Percentage'] = df_fact_cup_winners_grouped['Cup Wins'] / \
                                                    df_fact_cup_winners_grouped['Appearances']
    df_fact_cup_winners_grouped['Win Percentage'] = df_fact_cup_winners_grouped['Win Percentage'].fillna(0)
    df_fact_cup_winners_grouped = df_fact_cup_winners_grouped.round(decimals=1)
    df_fact_cup_winners_grouped = df_fact_cup_winners_grouped.sort_values(by='Appearances', ascending=False)
    return df_fact_cup_winners_grouped


# function to create cup winners bar chart. Passed data, xaxis and colors
def create_cup_winners_bar(data, xaxis, dis_color_seq):
    data = data.groupby([xaxis], as_index=False).agg({'Cup Wins': 'sum', 'Cup Losses': 'sum', 'Appearances': 'sum'})
    data = data[data['Appearances'] > 0]
    data = data.sort_values(by='Appearances', ascending=False)
    fig_bar = px.bar(data, x=xaxis, y=['Cup Wins', 'Cup Losses'], color_discrete_map=dis_color_seq)
    return fig_bar


# function to create cup winner pie chart. Passed data, colors, and the filtered team from drop down
def create_cup_winners_pie(data, dis_color_seq, team):
    filtered_df_cup_win = data.iloc[0:100, 0:4]  # pull winners columns into df
    filtered_df_cup_win['Outcome'] = 'Cup Win'  # create static column
    filtered_df_cup_loss = data.iloc[0:100, 0:4]  # pull loser columns into df
    filtered_df_cup_loss['Outcome'] = 'Cup Loss'  # create static column
    filtered_df_cup_win = filtered_df_cup_win.rename(columns={"Winning Team": "Team", "Losing Team": "Opponent"})
    filtered_df_cup_loss = filtered_df_cup_loss.rename(columns={"Winning Team": "Opponent", "Losing Team": "Team"})
    filtered_df_cup_loss = filtered_df_cup_loss[['season_year', 'Team', 'Games', 'Opponent', 'Outcome']]
    filtered_df_cup_all = pd.concat([filtered_df_cup_loss, filtered_df_cup_win])  # join winner and loser df
    filtered_df_cup_all = filtered_df_cup_all[filtered_df_cup_all['Team'] == team]  # filter for selected team
    filtered_df_cup_all = filtered_df_cup_all.groupby(['Team', 'Outcome'], as_index=False).agg({'season_year': 'count'})
    fig_pie = px.pie(filtered_df_cup_all, values='season_year', names='Outcome', hole=0.5,
                     color_discrete_sequence=dis_color_seq)
    return fig_pie


# function to create cup appearance table
def create_cup_winners_table(data, team):
    filtered_df_cup_win = data.iloc[0:100, 0:4]  # pull winners columns into df
    filtered_df_cup_win['Outcome'] = 'Cup Win'  # create static column
    filtered_df_cup_loss = data.iloc[0:100, 0:4]  # pull loser columns into df
    filtered_df_cup_loss['Outcome'] = 'Cup Loss'  # create static colum
    filtered_df_cup_win = filtered_df_cup_win.rename(columns={"Winning Team": "Team", "Losing Team": "Opponent"})
    filtered_df_cup_loss = filtered_df_cup_loss.rename(columns={"Winning Team": "Opponent", "Losing Team": "Team"})
    filtered_df_cup_loss = filtered_df_cup_loss[['season_year', 'Team', 'Games', 'Opponent', 'Outcome']]
    filtered_df_cup_all = pd.concat([filtered_df_cup_loss, filtered_df_cup_win])  # join winner and loser df
    filtered_df_cup_all = filtered_df_cup_all[filtered_df_cup_all['Team'] == team]  # filter for selected team
    filtered_df_cup_all = filtered_df_cup_all.sort_values('season_year', ascending=False)
    filtered_df_cup_all = filtered_df_cup_all.rename(columns={"season_year": "Season"})
    table = dash_table.DataTable(filtered_df_cup_all.to_dict('records'),
                                 [{"name": i, "id": i} for i in filtered_df_cup_all.columns],
                                 style_cell={'height': 'auto', 'width': 100, 'textAlign': 'left'},
                                 style_table={'height': '300px', 'width': 'auto', 'overflowY': 'auto',
                                              'overflowX': 'auto'},
                                 # fixed_columns={'headers': True, 'data': 3},
                                 # fixed_rows={'headers': True},
                                 style_data_conditional=[{
                                     'if': {
                                         'filter_query': '{Outcome} != "Cup Loss"'

                                     },
                                     'backgroundColor': '#8394A1',
                                     'color': 'white',
                                 }
                                 ],
                                 style_cell_conditional=[
                                     {
                                         'textAlign': 'left'
                                     }
                                 ]
                                 )
    return table


# function to create standings table
def create_standings_table(data):
    df = data.drop(
        columns=['team_id', 'season', 'Playoffs', 'RoundCategory', 'shortName', 'teamName', 'fullName', 'Conference',
                 'Division', 'PlayoffRound'])
    df["Win %"] = (df["W"] * 2 + df["OTL"]) / (df["GP"] * 2) * 100
    df = df[['season_year', 'Pos', 'Team', 'GP', 'W', 'L', 'OTL', 'PCT', 'Win %', 'RW', 'GF', 'GA', 'GD',
             'Playoff Seed_Cat', 'PlayoffRound_Cat']]
    df = df.rename(columns={"PlayoffRound_Cat": "Playoff Round", "PCT": "Points", 'season_year': 'Season',
                            'Playoff Seed_Cat': 'Playoff Seed'})
    df = df.round(decimals=0)
    df = df.sort_values(['Season', 'Pos'], ascending=[False, True])
    table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                                 style_cell={'height': 'auto', 'width': 100, 'textAlign': 'left'},
                                 style_table={'height': '300px', 'width': 'auto', 'overflowY': 'auto',
                                              'overflowX': 'auto'},
                                 # fixed_columns={'headers': True, 'data': 3},
                                 fixed_rows={'headers': True},
                                 style_data_conditional=[{
                                     'if': {
                                         'filter_query': '{Playoff Seed} != NONE'

                                     },
                                     'backgroundColor': '#8394A1',
                                     'color': 'white',
                                 }
                                 ],
                                 style_cell_conditional=[
                                     {
                                         'textAlign': 'left'
                                     }
                                 ]
                                 )
    return table


# function to create heatmap. Passed data, colors, and x axis value
def create_heatmap(data, color_seq, xval):
    data = data.rename(columns={"PlayoffRound_Cat": "Playoff Round"})
    data = data.groupby(['Team', 'Playoff Round', 'Playoff Seed_Cat', 'season_year', 'PlayoffSeedIndex'],
                        as_index=False).agg({'season': 'count'})
    # data = data.rename(columns={"Playoff Seed_Cat": "Playoff Seed"})
    if xval == 'Playoff Seed_Cat':
        data = data.sort_values('PlayoffSeedIndex', ascending=True)
    fig_hm = px.density_heatmap(data, x=xval, y="Playoff Round", z="season", histfunc="count",
                                color_continuous_scale=color_seq,
                                hover_data=['season_year', 'Playoff Round', 'Playoff Seed_Cat'])
    fig_hm.update_yaxes(categoryorder='array',
                        categoryarray=['NONE', 'Qualifying Round Loser', 'Round 1 Loser', 'Round 2 Loser',
                                       'Conference Final Loser', 'Stanley Cup Loser',
                                       'Stanley Cup Winner'])  # order values
    # fig_hm.update_xaxes(categoryorder='array', categoryarray= ['NONE','Qualifying Round','Conference 8 Seed','Conference 7 Seed','Conference 6 Seed',
    # 'Conference 5 Seed','Conference 4 Seed','Conference 3 Seed','Conference 2 Seed','Conference 1 Seed',
    # 'Division 3 Seed','Division 2 Seed','Division 1 Seed','Wild Card 1','Wild Card 2',''])
    return fig_hm


# function to create correlation matrix
def create_corr_matrix(data):
    drop_cols = ['team', 'season_year', 'name', 'team.1', 'team_id', 'position', 'situation',
                 'xOnGoalFor', 'xReboundsFor', 'xFreezeFor', 'xPlayStoppedFor',
                 'xPlayContinuedInZoneFor', 'xPlayContinuedOutsideZoneFor', 'flurryAdjustedxGoalsFor',
                 'scoreVenueAdjustedxGoalsFor', 'flurryScoreVenueAdjustedxGoalsFor',
                 'reboundsFor', 'reboundGoalsFor', 'freezeFor', 'playStoppedFor', 'scoreAdjustedShotsAttemptsFor',
                 'scoreAdjustedUnblockedShotAttemptsFor', 'xGoalsFromxReboundsOfShotsFor',
                 'xGoalsFromActualReboundsOfShotsFor', 'totalShotCreditFor', 'scoreAdjustedTotalShotCreditFor',
                 'scoreFlurryAdjustedTotalShotCreditFor',
                 'xReboundsAgainst', 'xFreezeAgainst', 'xPlayStoppedAgainst', 'flurryAdjustedxGoalsAgainst',
                 'scoreVenueAdjustedxGoalsAgainst', 'flurryScoreVenueAdjustedxGoalsAgainst',
                 'reboundsAgainst', 'reboundGoalsAgainst', 'freezeAgainst', 'playStoppedAgainst',
                 'scoreAdjustedShotsAttemptsAgainst', 'scoreAdjustedUnblockedShotAttemptsAgainst',
                 'xGoalsFromxReboundsOfShotsAgainst', 'xGoalsFromActualReboundsOfShotsAgainst', 'reboundxGoalsAgainst',
                 'scoreAdjustedTotalShotCreditAgainst', 'scoreFlurryAdjustedTotalShotCreditAgainst',
                 'W', 'L', 'OTL', 'RW', 'GF', 'GA', 'Playoff Seed', 'PlayoffRound', 'Playoff Seed_Cat',
                 'PlayoffRound_Cat', 'Playoffs', 'RoundCategory', 'shortName', 'teamName', 'fullName', 'Conference',
                 'Division', 'games_played', 'iceTime', 'blockedShotAttemptsFor', 'shotAttemptsFor', 'penaltiesFor',
                 'reboundxGoalsFor', 'missedShotsAgainst', 'blockedShotAttemptsAgainst',
                 'shotAttemptsAgainst', 'savedShotsOnGoalAgainst', 'penaltiesAgainst', 'unblockedShotAttemptsAgainst',
                 'dZoneGiveawaysAgainst',
                 'totalShotCreditAgainst', 'GP', 'GoalDifferential', 'Points'
                 ]

    df = data.drop(columns=drop_cols)  # drop columns that are not needed
    df_num = df._get_numeric_data()  # drop all non-numeric columns
    df_cor = df_num.corr()  # generate correlation matrix

    # drop all columns but win percentage
    df_cor_small = df_cor.drop(columns=['xGoalsPercentage',
                                        'corsiPercentage',
                                        'fenwickPercentage',
                                        'xGoalsFor',
                                        'shotsOnGoalFor',
                                        'missedShotsFor',
                                        'goalsFor',
                                        'playContinuedInZoneFor',
                                        'playContinuedOutsideZoneFor',
                                        'savedShotsOnGoalFor',
                                        'savedUnblockedShotAttemptsFor',
                                        'penalityMinutesFor',
                                        'faceOffsWonFor',
                                        'hitsFor',
                                        'takeawaysFor',
                                        'giveawaysFor',
                                        'lowDangerShotsFor',
                                        'mediumDangerShotsFor',
                                        'highDangerShotsFor',
                                        'lowDangerxGoalsFor',
                                        'mediumDangerxGoalsFor',
                                        'highDangerxGoalsFor',
                                        'lowDangerGoalsFor',
                                        'mediumDangerGoalsFor',
                                        'highDangerGoalsFor',
                                        'unblockedShotAttemptsFor',
                                        'dZoneGiveawaysFor',
                                        'xOnGoalAgainst',
                                        'xGoalsAgainst',
                                        'xPlayContinuedInZoneAgainst',
                                        'xPlayContinuedOutsideZoneAgainst',
                                        'shotsOnGoalAgainst',
                                        'goalsAgainst',
                                        'playContinuedInZoneAgainst',
                                        'playContinuedOutsideZoneAgainst',
                                        'savedUnblockedShotAttemptsAgainst',
                                        'penalityMinutesAgainst',
                                        'faceOffsWonAgainst',
                                        'hitsAgainst',
                                        'takeawaysAgainst',
                                        'giveawaysAgainst',
                                        'lowDangerShotsAgainst',
                                        'mediumDangerShotsAgainst',
                                        'highDangerShotsAgainst',
                                        'lowDangerxGoalsAgainst',
                                        'mediumDangerxGoalsAgainst',
                                        'highDangerxGoalsAgainst',
                                        'lowDangerGoalsAgainst',
                                        'mediumDangerGoalsAgainst',
                                        'highDangerGoalsAgainst'])

    df_cor_small['Correlation'] = np.where(df_cor_small['WinPercentage'] >= 0, 'Pos',
                                           'Neg')  # assign pos or neg value to correlation
    df_cor_small['CorrleationCoefAbs'] = df_cor_small['WinPercentage'].abs()  # find absolute value of correlation
    df_cor_small = df_cor_small.sort_values(['CorrleationCoefAbs'], ascending=False)
    df_cor_small = df_cor_small.drop(columns=['WinPercentage'])
    df_cor_small = df_cor_small.reset_index()
    df_cor_small = df_cor_small.rename(columns={"index": "Variable"})
    df_cor_small = df_cor_small[df_cor_small['CorrleationCoefAbs'] < 1]  # remove winpercentage row
    df_cor_small = df_cor_small.rename(
        columns={"Variable": "Metric", 'CorrleationCoefAbs': "Absolute Correlation Coef."})
    df_cor_small = df_cor_small.round(decimals=2)
    table = dash_table.DataTable(df_cor_small.to_dict('records'), [{"name": i, "id": i} for i in df_cor_small.columns],
                                 style_cell={'height': 'auto', 'width': 100, 'textAlign': 'left'},
                                 style_table={'height': '500px', 'width': 'auto', 'overflowY': 'auto',
                                              'overflowX': 'auto'},
                                 # fixed_columns={'headers': True, 'data': 3},
                                 # fixed_rows={'headers': True},
                                 style_cell_conditional=[
                                     {
                                         'textAlign': 'left'
                                     }
                                 ]
                                 )
    columns = df_cor_small['Metric'].unique()  # to pull dropdown values
    return columns, table


######### INIT APP #####################################################################################################################################
########################################################################################################################################################
my_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
server = my_app.server

######### CREATE HTML ELEMENTS #########################################################################################################################
########################################################################################################################################################

# ---- FILTER ROW --------------------------------------------------------------------------------------------------------------------------------
filter_row = dbc.Card(
    dbc.CardBody([
        html.Div([
            dbc.Row([
                # select year range slider
                dbc.Col(
                    html.Div([
                        html.H4("Select Year"),
                        dcc.RangeSlider(
                            id='year-slider',
                            min=2013,
                            max=df_dim_seasonyear_ref['season_year'].max(),
                            value=[2013, 2019],
                            marks={str(year): str(year) for year in df_dim_seasonyear_ref['season_year'].unique()},
                            step=1)])),

                # select conference dropdown
                dbc.Col(html.Div([
                    html.H4("Select Conference"),
                    dcc.RadioItems(id='conference_dropdown',
                                   options=[{'label': 'All', 'value': 'all_values'}] + [{'label': i, 'value': i} for i
                                                                                        in df_dim_team_info[
                                                                                            'Conference'].unique()],
                                   # add an 'all values'
                                   value='all_values')]),
                    width=3),

                # select team dropdown
                dbc.Col(html.Div([
                    html.H4("Select Team"),
                    dcc.Dropdown(id='team_dropdown',
                                 options=[],  # empty list for chained call back
                                 value='all_values')]),
                    width=3)
            ])
        ])
    ])
)

# ---- INFO & MAIN--------------------------------------------------------------------------------------------------------------------------------
# create main description and bar graph
info_main_bar = dbc.CardGroup([

    # descrition
    dbc.Card(
        dbc.CardBody([
            html.H5("Description", className="card-title"),
            html.P([
                "There are many factors that play into how an NHL team performs over time, the most obvious being playoff success and championships. This Dashboard explores how teams become championship contenders.",
                html.Br(), html.Br(),
                html.I([
                           "It is important to note that there is one teams that has incomplete data based on when they entered the league, the Vegas Golden Knights entered in 2017.",
                           html.Br(), html.Br(),
                           "It is also important to note that the 2019 season was cut short due to Covid."]), html.Br(),
                html.Br(),
                html.A("Data Source", href='https://www.kaggle.com/datasets/martinellis/nhl-game-data', target="_blank")
            ],
                className="card-text")
        ]), style={'max-width': '30rem'}),

    # main bar chart
    dbc.Card(
        dbc.CardBody([
            html.H5("Season Points & Win Percentage", className="card-title"),
            dcc.Graph(id='bar_graph_output'),
            html.P(
                "This graph shows either the teams winning percentage (if conference is selected) or season points (if a team is selected) over the time frame selected.",
                className="card-text")
        ]), style={'width': 9})
])

# ---- CUP WINNERS --------------------------------------------------------------------------------------------------------------------------------
# create cup winners div
cup_winners = html.Div([
    dbc.Row([
        html.Div(id='cup_winners_output')
    ]),

])

# ---- PLAYOFF HM --------------------------------------------------------------------------------------------------------------------------------
# create playoff heatmap card
playoff_hm = dbc.Card(
    dbc.CardBody([
        html.H5("Playoff Round Heatmap", className="card-title"),
        dcc.Graph(id='playoff_hm_output'),
        html.P([
            "This heatmap shows the number of times a team has advanced to a given playoff round", html.Br(),
            html.Br()],
            className="card-text")
    ])
)

# ---- STANDINGS --------------------------------------------------------------------------------------------------------------------------------
# create standings div
standings = html.Div([
    dbc.Row([
        html.Div(id='standings_output')
    ]),

])

# ---- SCATTER & COEF --------------------------------------------------------------------------------------------------------------------------------
# create scatter plot and coefficitnet matrix

columns_metric, x = create_corr_matrix(
    fact_team_stats_merged)  # used to pull unique values from the variables to create dropdown values

scatter_coef = dbc.CardGroup([

    # create card for correlation table
    dbc.Card(
        dbc.CardBody([
            html.Div(id='corr_output'),
        ]), style={'width': 4}),

    # create card for dropdown and scatter plot
    dbc.Card(
        dbc.CardBody([

            # create metric dropdown
            html.Div([
                html.H5("Select Metric"),
                dcc.Dropdown(id='metric_dropdown',
                             options=columns_metric,
                             value='xGoalsPercentage')]),

            html.Br(),

            # create scatter plot
            html.Div(id='scatter_output'),
        ]), style={'width': 8}),
])

######### CREATE APP #########################################################################################################################
##############################################################################################################################################
my_app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([

            # headers
            html.Div([
                dbc.Row([
                    html.Div(id='header_output')  # header
                ]),

                # filters
                dbc.Row([
                    html.Div([filter_row])
                ])], style={'position': 'sticky', 'top': '0', 'zIndex': '1', 'color': '#fbfbfb'}),
            # floating filters pin to top of page

            html.Br(),  # line break

            # row 1: main bar and desc.
            dbc.Row([
                dbc.Col([
                    info_main_bar
                ], width=12),

            ], align='center'),

            html.Br(),  # line break

            # row 2: scatter and coefficient table
            dbc.Row([
                scatter_coef]),

            html.Br(),  # line break

            # row 3: playoff heatmap and cup winners
            dbc.Row([
                dbc.Col([
                    playoff_hm
                ], width=6),
                dbc.Col([
                    cup_winners
                ], width=6),
            ], align='center'),

            html.Br(),  # line break

            # row 4: standings
            dbc.Row([
                standings]),

            html.Br(),  # line break

            # footer
            dbc.Row([
                html.Div(id='footer_output')]),

        ]), color='#fbfbfb'  # set overall background color
    )
])


######### CREATE CALLBACKS #########################################################################################################################
####################################################################################################################################################

# ---- HEADER --------------------------------------------------------------------------------------------------------------------------------
@my_app.callback(Output('header_output', 'children'),
              Input('team_dropdown', 'value'))
def display_header(selected_team):
    # IF TEAM IS SELECTED
    if selected_team != 'all_values':
        # FILTER COLOR DATAFRAME TO SELECTED TEAM
        df_team_colors_filtered = df_team_colors_merged[df_team_colors_merged['fullName'] == selected_team]

        logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(df_team_colors_filtered)

        # USE CARD FOR STYLING
        header_output = dbc.Card(
            dbc.CardBody([
                html.Div([
                    dbc.Row(
                        [
                            dbc.Col(html.Div(html.Img(src=logo, height='auto')), width=1,
                                    style={'align': 'center', 'padding': '10px'}),  # LEFT SIDE LOGO
                            dbc.Col(html.Div(html.Img(src=wordmark, height='auto'), style={'margin-top': 10}), width=4,
                                    style={'align': 'center', 'padding': '20px'}),  # LEFT-CENTER WORDMARK
                            dbc.Col(html.Span(html.H1('Yearly Performances',
                                                      style={'color': 'white', 'fontSize': '72px',
                                                             'textAlign': 'start'})), width=7,
                                    style={'padding': '10px'})  # TEXT
                        ]),
                ])
            ]), color=bg_color
        )


    # IF NO TEAM IS SELECTED
    else:

        # SET LOGO AND COLORS TO NHL DEFAULTS
        df_team_colors_filtered = df_dim_team_colors[df_dim_team_colors['team_id'] == 100]

        logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(df_team_colors_filtered)

        # USE CARD FOR STYLING
        header_output = dbc.Card(
            dbc.CardBody([
                html.Div([
                    dbc.Row(
                        [
                            dbc.Col(html.Div(html.Img(src=logo, height=80)), width=5,
                                    style={'align': 'center', 'padding': '10px'}),  # LEFT SIDE LOGO
                            dbc.Col(html.Span(html.H1('NHL Yearly Performances',
                                                      style={'color': 'white', 'fontSize': '72px',
                                                             'textAlign': 'start'})), width=7,
                                    style={'padding': '10px'})  # TEXT
                        ]),
                ])
            ]), color=bg_color
        )

    return header_output


# ---- FOOTER --------------------------------------------------------------------------------------------------------------------------------
@my_app.callback(Output('footer_output', 'children'),
              Input('team_dropdown', 'value'))
def display_header(selected_team):
    # IF TEAM IS SELECTED
    if selected_team != 'all_values':

        # FILTER COLOR DATAFRAME TO SELECTED TEAM
        df_team_colors_filtered = df_team_colors_merged[df_team_colors_merged['fullName'] == selected_team]
        logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(df_team_colors_filtered)

        # USE CARD FOR STYLING
        header_output = dbc.Card(
            dbc.CardBody([
                html.Div([
                    dbc.Row(
                        [
                            dbc.Col(html.Span(html.P('Ronnie Pinnell | MIS667 Final',
                                                     style={'color': 'white', 'fontSize': '22px',
                                                            'textAlign': 'start'})), width=7, style={'padding': '10px'})
                            # TEXT
                        ]),
                ])
            ]), color=sec_color
        )


    # IF NO TEAM IS SELECTED
    else:

        # SET LOGO AND COLORS TO NHL DEFAULTS
        df_team_colors_filtered = df_dim_team_colors[df_dim_team_colors['team_id'] == 100]

        logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(df_team_colors_filtered)

        # USE CARD FOR STYLING
        header_output = dbc.Card(
            dbc.CardBody([
                html.Div([
                    dbc.Row(
                        [
                            dbc.Col(html.Span(html.P('Ronnie Pinnell | MIS667 Final',
                                                     style={'color': 'white', 'fontSize': '22px',
                                                            'textAlign': 'start'})), width=7, style={'padding': '10px'})
                            # TEXT
                        ]),
                ])
            ]), color=sec_color
        )

    return header_output


# ---- MAIN CALLBACK --------------------------------------------------------------------------------------------------------------------------------
@my_app.callback(Output('bar_graph_output', 'figure'),
              Output('cup_winners_output', 'children'),
              Output('playoff_hm_output', 'figure'),
              Input('team_dropdown', 'value'),
              Input('year-slider', 'value'),
              Input('conference_dropdown', 'value'))
def display_main_graph(selected_team, selected_year, selected_conference):
    # FILTER FOR SPECIFIC SEASONS
    filtered_df_bar = fact_season_standings_merged[
        fact_season_standings_merged['season_year'].between(selected_year[0], selected_year[1], inclusive='both')]

    filtered_df_cup = df_fact_cup_winners[df_fact_cup_winners['season_year'].between(1927, 2019, inclusive='both')]
    filtered_df_hm = fact_season_standings_merged[
        fact_season_standings_merged['season_year'].between(selected_year[0], selected_year[1], inclusive='both')]

    AvgPlayoffWinPercentage, AvgPlayoffPoints = avg_playoff_points(
        filtered_df_bar)  # call function to pull avg. playoff points

    # GROUP DATA FOR IF NO TEAM OR CONFERENCE SELECTED
    grouped_df = group_season_data(filtered_df_bar, 'fullName')

    # FILTER COLORS TO CREATE CUSTOM COLORING
    filtered_df_color = df_dim_team_colors[df_dim_team_colors['team_id'] == 100]  # default color value
    logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(filtered_df_color)
    color_seq = [(0, sec_color), (0.5, th_color), (1, bg_color)]
    dis_color_seq = {"Cup Wins": bg_color, "Cup Losses": sec_color}
    color_seq_hm = [(0, 'white'), (1, bg_color)]

    # IF NO TEAM OR CONFERENCE SELECTED ---------------------------------------------------------------------------------------
    if selected_conference == 'all_values' and selected_team == 'all_values':
        # CREATE PLOTS
        fig_bar = create_main_bar(grouped_df, 'fullName', 'WinPercentage', 'Avg Points', color_seq)
        fig_bar.add_hline(y=AvgPlayoffWinPercentage,
                          annotation_text=f'Average Playoff Team Winning % = {AvgPlayoffWinPercentage}%')
        fig_bar.update_layout(xaxis_title="Team")

        filtered_df_cup = create_cup_winners_df(filtered_df_cup)
        fig_cup = create_cup_winners_bar(filtered_df_cup, 'fullName', dis_color_seq)
        fig_cup.update_layout(xaxis_title="Team", yaxis_title='Stanley Cup Appearances', legend_title=None)

        fig_hm = create_heatmap(filtered_df_hm, color_seq_hm, 'Team')

        cup_winners = dbc.CardGroup([
            dbc.Card(
                dbc.CardBody([
                    html.H5("Stanley Cup Champions", className="card-title"),
                    dcc.Graph(figure=fig_cup),
                    html.P([
                        "This graph shows the number of Stanley Cup wins and losses by team dating back to 1927.",
                        html.Br(),
                        html.A("More information", href='https://en.wikipedia.org/wiki/Stanley_Cup', target="_blank")],
                        className="card-text")
                ])
            )])

    # IF A CONFERENCE IS SELECTED ---------------------------------------------------------------------------------------
    if selected_conference != 'all_values':
        filtered_df_bar = filtered_df_bar[filtered_df_bar['Conference'] == selected_conference]

        filtered_df_cup2 = create_cup_winners_df(filtered_df_cup)
        filtered_df_cup2 = filtered_df_cup2[filtered_df_cup2['Conference'] == selected_conference]

        filtered_df_hm = filtered_df_hm[filtered_df_hm['Conference'] == selected_conference]

        # GROUP BY TEAM ADD CALC COLUMNS
        grouped_df2 = group_season_data(filtered_df_bar, 'fullName')

        # CREATE PLOTS
        fig_bar = create_main_bar(grouped_df2, 'fullName', 'WinPercentage', 'GoalDifferential', color_seq)
        fig_bar.add_hline(y=AvgPlayoffWinPercentage,
                          annotation_text=f'Average Playoff Team Winning % = {AvgPlayoffWinPercentage}%')
        fig_bar.update_layout(xaxis_title="Team")

        fig_cup = create_cup_winners_bar(filtered_df_cup2, 'fullName', dis_color_seq)
        fig_cup.update_layout(xaxis_title="Team", yaxis_title='Stanley Cup Appearances', legend_title=None)

        fig_hm = create_heatmap(filtered_df_hm, color_seq_hm, 'Team')

        cup_winners = dbc.CardGroup([
            dbc.Card(
                dbc.CardBody([
                    html.H5("Stanley Cup Champions", className="card-title"),
                    dcc.Graph(figure=fig_cup),
                    html.P([
                        "This graph shows the number of Stanley Cup wins and losses by team dating back to 1927.",
                        html.Br(),
                        html.A("More information", href='https://en.wikipedia.org/wiki/Stanley_Cup', target="_blank")],
                        className="card-text")
                ])
            )])

    # IF A TEAM IS SELECTED ---------------------------------------------------------------------------------------
    if selected_team != 'all_values':
        filtered_df_bar = filtered_df_bar[filtered_df_bar['fullName'] == selected_team]

        filtered_df_hm = filtered_df_hm[filtered_df_hm['fullName'] == selected_team]

        # ADD CALC COLUMNS
        filtered_df_bar_2 = calc_standings_column(filtered_df_bar)

        # FILTER COLORS TO CREATE CUSTOM COLORING
        df_team_colors_filtered = df_team_colors_merged[df_team_colors_merged['fullName'] == selected_team]
        logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(df_team_colors_filtered)
        color_seq = [(0, sec_color), (0.5, 'white'), (1, bg_color)]
        dis_color_seq = {"Cup Wins": bg_color, "Cup Losses": sec_color}
        color_seq_hm = [(0, 'white'), (1, bg_color)]
        dis_color_seq_pie = [bg_color, sec_color]

        # CREATE PLOTS
        fig_bar = px.bar(filtered_df_bar_2, x='season_year', y='Points', color='WinPercentage',
                         color_continuous_scale=color_seq,
                         hover_data=['Playoffs', 'PlayoffRound', 'Playoff Seed'])
        fig_bar.add_hline(y=AvgPlayoffPoints, annotation_text=f'Average Playoff Points = {AvgPlayoffPoints}%')
        fig_bar = fig_bar.update_layout(
            xaxis=dict(
                tickmode='linear',
                dtick=1))
        fig_bar.update_layout(xaxis_title="Season")

        fig_cup = create_cup_winners_pie(df_fact_cup_winners, dis_color_seq_pie, selected_team)
        table_cup = create_cup_winners_table(df_fact_cup_winners, selected_team)

        fig_hm = create_heatmap(filtered_df_hm, color_seq_hm, 'Playoff Seed_Cat')
        fig_hm.update_layout(xaxis_title="Playoff Seed")

        cup_winners = dbc.CardGroup([
            dbc.Card(
                dbc.CardBody([
                    html.H5(f"{selected_team} Championships", className="card-title"),
                    dcc.Graph(figure=fig_cup),
                    html.P([
                        "Stanley Cup wins and losses dating back to 1927.", html.Br()],
                        className="card-text")
                ]), style={'width': 3}),
            dbc.Card(
                dbc.CardBody([
                    dbc.Container(table_cup),
                ]), style={'width': 3}),
        ])

    return fig_bar, cup_winners, fig_hm


# ---- SCATTER CALLBACK --------------------------------------------------------------------------------------------------------------------------------
@my_app.callback(Output('scatter_output', 'children'),
              Output('corr_output', 'children'),
              Input('team_dropdown', 'value'),
              Input('year-slider', 'value'),
              Input('conference_dropdown', 'value'),
              Input('metric_dropdown', 'value'), )
def display_scatter(selected_team, selected_year, selected_conference, selected_metric):
    # FILTER FOR SPECIFIC SEASONS
    filtered_df_scatter = fact_team_stats_merged[
        fact_team_stats_merged['season_year'].between(selected_year[0], selected_year[1], inclusive='both')]

    AvgPlayoffWinPercentage, AvgPlayoffPoints = avg_playoff_points(filtered_df_scatter)

    # FILTER COLORS TO CREATE CUSTOM COLORING
    filtered_df_color = df_dim_team_colors[df_dim_team_colors['team_id'] == 100]
    logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(filtered_df_color)
    color_seq = [(0, sec_color), (0.5, th_color), (1, bg_color)]

    # IF NO TEAM OR CONFERENCE SELECTED ---------------------------------------------------------------------------------------
    if selected_conference == 'all_values' and selected_team == 'all_values':
        # CREATE PLOTS
        x, fig_cor_table = create_corr_matrix(filtered_df_scatter)

        table = html.Div([
            html.H5("Correlation to WinPercentage", className="card-title"),
            html.Br(),
            dbc.Container(fig_cor_table),
            html.Br(),
            html.P([
                "This sectiom shows the relationship between a team's winning percentage and a selection of advanced stats.",
                html.Br(),
                html.A("Advanced Stats Glossary", href='https://moneypuck.com/glossary.htm', target="_blank")],
                className="card-text")
        ])

        fig_scatter = create_scatter(filtered_df_scatter, selected_metric, color_seq)
        fig_scatter.add_vline(x=AvgPlayoffWinPercentage,
                              annotation_text=f'Average Playoff Team Winning % = {AvgPlayoffWinPercentage}%')

        scatter = html.Div([
            html.H5(f"Relationship Between {selected_metric} and Win Percentage", className="card-title"),
            dcc.Graph(figure=fig_scatter),

        ])

    # IF A CONFERENCE IS SELECTED ---------------------------------------------------------------------------------------
    if selected_conference != 'all_values':
        filtered_df_scatter = filtered_df_scatter[filtered_df_scatter['Conference'] == selected_conference]

        # CREATE PLOTS
        fig_scatter = create_scatter(filtered_df_scatter, selected_metric, color_seq)
        fig_scatter.add_vline(x=AvgPlayoffWinPercentage,
                              annotation_text=f'Average Playoff Team Winning % = {AvgPlayoffWinPercentage}%')

        scatter = html.Div([
            html.H5(f"Relationship Between {selected_metric} and Win Percentage", className="card-title"),
            dcc.Graph(figure=fig_scatter),

        ])

        x, fig_cor_table = create_corr_matrix(filtered_df_scatter)

        table = html.Div([
            html.H5("Correlation to WinPercentage", className="card-title"),
            html.Br(),
            dbc.Container(fig_cor_table),
            html.Br(),
            html.P([
                "This sectiom shows the relationship between a team's winning percentage and a selection of advanced stats.",
                html.Br(),
                html.A("Advanced Stats Glossary", href='https://moneypuck.com/glossary.htm', target="_blank")],
                className="card-text")
        ])

    # IF A TEAM IS SELECTED ---------------------------------------------------------------------------------------
    if selected_team != 'all_values':
        filtered_df_scatter = filtered_df_scatter[filtered_df_scatter['fullName'] == selected_team]

        # ADD CALC COLUMNS
        filtered_df_scatter_2 = calc_standings_column(filtered_df_scatter)

        # FILTER COLORS TO CREATE CUSTOM COLORING
        df_team_colors_filtered = df_team_colors_merged[df_team_colors_merged['fullName'] == selected_team]
        logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(df_team_colors_filtered)
        color_seq = [(0, sec_color), (0.5, 'white'), (1, bg_color)]

        # CREATE PLOTS

        fig_scatter = create_scatter(filtered_df_scatter_2, selected_metric, color_seq)
        fig_scatter.add_vline(x=AvgPlayoffWinPercentage,
                              annotation_text=f'Average Playoff Team Winning % = {AvgPlayoffWinPercentage}%')

        scatter = html.Div([
            html.H5(f"Relationship Between {selected_metric} and Win Percentage", className="card-title"),
            dcc.Graph(figure=fig_scatter),

        ])

        x, fig_cor_table = create_corr_matrix(filtered_df_scatter)

        table = html.Div([
            html.H5("Correlation to WinPercentage", className="card-title"),
            html.Br(),
            dbc.Container(fig_cor_table),
            html.Br(),
            html.P([
                "This sectiom shows the relationship between a team's winning percentage and a selection of advanced stats.",
                html.Br(),
                html.A("Advanced Stats Glossary", href='https://moneypuck.com/glossary.htm', target="_blank")],
                className="card-text")
        ])

    return scatter, table


# ---- STANDINGS --------------------------------------------------------------------------------------------------------------------------------
@my_app.callback(Output('standings_output', 'children'),
              Input('year-slider', 'value'),
              Input('team_dropdown', 'value'),
              Input('conference_dropdown', 'value'))
def display_standings(selected_year, selected_team, selected_conference):
    df = fact_season_standings_merged[
        fact_season_standings_merged['season_year'].between(selected_year[0], selected_year[1], inclusive='both')]
    num_years = selected_year[1] - selected_year[0] + 1

    # IF NO CONFERENCE OR TEAM IS SELECTED ---------------------------------------------------------------------------------------
    if selected_conference == 'all_values' and selected_team == 'all_values':
        # create a table for each division
        df_ea = df[df['Division'] == 'Atlantic']
        table_ea = create_standings_table(df_ea)

        df_em = df[df['Division'] == 'Metropolitan']
        table_em = create_standings_table(df_em)

        df_wc = df[df['Division'] == 'Central']
        table_wc = create_standings_table(df_wc)

        df_wp = df[df['Division'] == 'Central']
        table_wp = create_standings_table(df_wp)

        standings = dbc.CardGroup([
            dbc.Card(
                dbc.CardBody([
                    html.H5("East: Atlantic Standings", className="card-title"),
                    dbc.Container(table_ea),
                ]), style={'width': 3}),
            dbc.Card(
                dbc.CardBody([
                    html.H5("East: Metropolitan Standings", className="card-title"),
                    dbc.Container(table_em),
                ]), style={'width': 3}),
            dbc.Card(
                dbc.CardBody([
                    html.H5("West: Central Standings", className="card-title"),
                    dbc.Container(table_wc),
                ]), style={'width': 3}),
            dbc.Card(
                dbc.CardBody([
                    html.H5("West: Pacific Standings", className="card-title"),
                    dbc.Container(table_wp),
                ]), style={'width': 3})
        ])

    # IF A CONFERENCE IS SELECTED ---------------------------------------------------------------------------------------
    if selected_conference != 'all_values':
        df = df[df['Conference'] == selected_conference]

        divisions = df['Division'].unique()  # create unique list of divisions in conference

        d1 = divisions[0]  # pull first division
        d2 = divisions[1]  # pull second division

        # create table for each of the divisions pulled
        df_1 = df[df['Division'] == d1]
        table_1 = create_standings_table(df_1)

        df_2 = df[df['Division'] == d2]
        table_2 = create_standings_table(df_2)

        # pull colors
        filtered_df_color = df_dim_team_colors[df_dim_team_colors['team_id'] == 100]
        logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(filtered_df_color)
        color_seq = [(0, sec_color), (0.5, th_color), (1, bg_color)]

        # create dataframe for only playoff teams
        df2 = df[df['Playoffs'] == 'Y']
        df2 = df2.groupby('Team', as_index=False).agg(
            {'GP': 'sum', 'W': 'sum', 'L': 'sum', 'OTL': 'sum', 'RW': 'sum', 'GF': 'sum', 'GA': 'sum',
             'season_year': 'count'})
        df2['PlayoffPercentage'] = (df2['season_year'] / num_years) * 100
        df2 = df2.sort_values(by='season_year', ascending=False)
        df2 = df2.round(decimals=0)

        # create plots
        fig_bar = create_main_bar(df2, 'Team', 'season_year', 'PlayoffPercentage', color_seq)

        standings = dbc.CardGroup([
            dbc.Card(
                dbc.CardBody([
                    html.H5(f"{selected_conference}: {d1} Standings", className="card-title"),
                    dbc.Container(table_1),
                ]), style={'width': 3}),
            dbc.Card(
                dbc.CardBody([
                    html.H5(f"{selected_conference}: {d2} Standings", className="card-title"),
                    dbc.Container(table_2),
                ]), style={'width': 3}),
            dbc.Card(
                dbc.CardBody([
                    html.H5(f"{selected_conference}: Count of Playoff Appearances", className="card-title"),
                    dcc.Graph(figure=fig_bar),
                ]), style={'width': 6}),

        ])

    # IF A TEAM IS SELECTED ---------------------------------------------------------------------------------------
    if selected_team != 'all_values':
        df = df[df['Team'] == selected_team]

        # pull colors
        filtered_df_color = df_team_colors_merged[df_team_colors_merged['fullName'] == selected_team]
        logo, wordmark, logo_light, bg_color, sec_color, th_color, url = get_colors_logo(filtered_df_color)
        color_seq = [(0, sec_color), (0.5, 'white'), (1, bg_color)]

        # create plots
        table = create_standings_table(df)

        df_sun = df.groupby(['Playoffs', 'Playoff Seed_Cat', 'PlayoffRound_Cat'], as_index=False).agg(
            {'Pos': 'sum', 'GP': 'sum', 'W': 'sum', 'L': 'sum', 'OTL': 'sum', 'RW': 'sum', 'GF': 'sum', 'GA': 'sum',
             'season_year': 'count'})
        df_sun["WinPercentage"] = (df_sun["W"] * 2 + df_sun["OTL"]) / (df_sun["GP"] * 2) * 100
        # df_sun = df_sun.sort_values(by='season', ascending = False)
        df_sun = df_sun.round(decimals=0)

        fig = px.sunburst(df_sun, path=['Playoffs', 'Playoff Seed_Cat', 'PlayoffRound_Cat'], values='season_year',
                          color='WinPercentage', color_continuous_scale=color_seq)

        standings = dbc.CardGroup([
            dbc.Card(
                dbc.CardBody([
                    html.H5(f"{selected_team}: Standings by Year", className="card-title"),
                    dbc.Container(table),
                ]), style={'width': 6}),
            dbc.Card(
                dbc.CardBody([
                    html.H5(f"{selected_team}: Playoff Appearances and Performance", className="card-title"),
                    dcc.Graph(figure=fig),
                ]), style={'width': 6}),

        ])

    return standings


# ---- DROP DOWN CHAINED --------------------------------------------------------------------------------------------------------------------------------
@my_app.callback(Output('team_dropdown', 'options'),
              Input('conference_dropdown', 'value'))
def conf_div_team_options(chosen_conf):
    if chosen_conf == 'all_values':
        teams = [{'label': 'All', 'value': 'all_values'}] + [{'label': i, 'value': i} for i in
                                                             df_dim_team_info['fullName'].unique()]

    else:
        filtered_df = df_dim_team_info[df_dim_team_info['Conference'] == chosen_conf]  # filter on radio selected cat
        teams = [{'label': 'All', 'value': 'all_values'}] + [{'label': i, 'value': i} for i in
                                                             filtered_df['fullName'].unique()]

    return teams


######### RUN APP #########################################################################################################################
###########################################################################################################################################
if __name__ == "__main__":
    my_app.run_server(debug=False, port=8069)



