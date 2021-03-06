# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:33:19 2021

@author: Grant
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import os
import pickle
from src import Writer
writer = Writer()

imported_df = pd.read_csv('keep_me_df.csv')
temp = []
for index, row in imported_df.iterrows():
    try: 
        if row['Role'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
            temp.append([int(row['ID']), int(row['Role'])])
    except:
        continue

# print("temp length", len(temp))   2320
# print(temp)

'''
Just looking at the preplant A scenario, where do the T's different players play 
  1) when they win
  2) when they lose 

 def write_data():
     writer.main()
'''

""" 
TO-DO:
get a single player in a single round x10
check unqiue att_id/vic_id (sanity)
Follow att_id for 1 side on a single round, should disappear on round end or death
 """
 
print("Loading Data")
#make empty df   
data = pd.DataFrame()

#gets copy of original data  Every single NORMAL round on mirage 
data = writer.get_data()
writer.main()

#reading
with open('file_to_rounds.txt', 'rb') as handle: #All files on Mirage map with only Normal rounds
    _input = handle.read()

#dictionary
file_to_rounds = pickle.loads(_input)


# #Arrays to store outcomes
T_Wins_Preplant = []
T_Loses_Preplant = []

print("Filtering Data")
for k,v in file_to_rounds.items(): #taking a single round at a time and splitting by pre and post plant
    for rnd in v:
        T_Wins_Preplant.append(data[(data['bomb_site'] != 'A') & (data['bomb_site'] != 'B') & (data['round'] == rnd) & (data['file'] == k) & (data['att_side'] == 'Terrorist') & (data['winner_side'] == 'Terrorist')].values.tolist())
        T_Loses_Preplant.append(data[(data['bomb_site'] != 'A') & (data['bomb_site'] != 'B') & (data['round'] == rnd) & (data['file'] == k) & (data['att_side'] == 'Terrorist') & (data['winner_side'] == 'CounterTerrorist')].values.tolist())
        
#remove empty lists
t_remove_empties = [ele for ele in T_Wins_Preplant if ele != []]
t2_remove_empties = [ele for ele in T_Loses_Preplant if ele != []]    

#check if lists are the same
t_remove_empties.sort() 
t2_remove_empties.sort()
  
#convert 3D array to 2D array
t_flat_list = [arr for sub_arrs in t_remove_empties for arr in sub_arrs]
t2_flat_list = [arr for sub_arrs in t2_remove_empties for arr in sub_arrs]


#make new dataframe from list (T_Wins_PrePlant)
T_Wins_Preplant_A_df = pd.DataFrame(t_flat_list, columns =['Unnamed: 0','file','map','date','round','tick','seconds','att_team','vic_team','att_side','vic_side','hp_dmg','arm_dmg','is_bomb_planted',
                                                                'bomb_site','hitbox','wp','wp_type','award','winner_team','winner_side','att_id','att_rank','vic_id','vic_rank','att_pos_x','att_pos_y','vic_pos_x',
                                                                'vic_pos_y','round_type','ct_eq_val','t_eq_val','avg_match_rank', 'attacker_mapX', 'attacker_mapY', 'victim_mapX','victim_mapY'])

T_Loses_Preplant_A_df = pd.DataFrame(t2_flat_list, columns =['Unnamed: 0','file','map','date','round','tick','seconds','att_team','vic_team','att_side','vic_side','hp_dmg','arm_dmg','is_bomb_planted',
                                                                'bomb_site','hitbox','wp','wp_type','award','winner_team','winner_side','att_id','att_rank','vic_id','vic_rank','att_pos_x','att_pos_y','vic_pos_x',
                                                                'vic_pos_y','round_type','ct_eq_val','t_eq_val','avg_match_rank', 'attacker_mapX', 'attacker_mapY', 'victim_mapX','victim_mapY'])

print (T_Wins_Preplant_A_df)


#Upload to csv
# T_Wins_Preplant_A_df.to_csv('T_Wins_Preplant_A_df.csv', index = False, encoding='utf-8')
# T_Loses_Preplant_A_df.to_csv('T_Loses_Preplant_A_df.csv', index = False, encoding='utf-8')
# print("Done")


#Now I have 2 data frames of Every single NORMAL round where the T's attack in gunfights (on mirage) where the T's win preplant and the T's lose preplant
# for index, row in T_Wins_Preplant_A_df.iterrows():
#     print(row['att_id'])

im = plt.imread('./input/de_mirage.png')
t_wins = plt.imshow(im)
t_loses = plt.imshow(im)
iterations = 0
T_Wins_Preplant_A_df.insert(0, 'player_color', 'NaN')


for index, row in T_Wins_Preplant_A_df.iterrows():
    for pair in temp:
        iterations= iterations + 1
        print("Loading comparison ", iterations)
        if pair[0] == row['att_id']:
            print("True")
            break
        else:
            print("False ", pair[0], " ", row['att_id'])
        
        
        # and pair[1] == 0:
        #     T_Wins_Preplant_A_df.at[index, 'player_color'] = 'green'
        #     print(" Green")
        # elif pair[0] == row['att_id'] and pair[1] == 1:
        #     T_Wins_Preplant_A_df.at[index, 'player_color'] = 'red'
        #     print(" Red")
        # elif row['att_id'] == pair[0] and pair[1] == 2:
        #     T_Wins_Preplant_A_df.at[index, 'player_color'] = 'yellow'
        #     print(" Yellow")
        # elif row['att_id'] == pair[0] and pair[1] == 3:
        #     T_Wins_Preplant_A_df.at[index, 'player_color'] = 'blue'
        #     print(" Blue")
        # elif row['att_id'] == pair[0] and pair[1] == 4:
        #     T_Wins_Preplant_A_df.at[index, 'player_color'] = 'orange'
        #     print(" Orange")
        # else:
        #     print(" No_match")
        
#   # # Heat map
# print("Plotting Heat Map")
# im = plt.imread('./input/de_mirage.png')
# plt.figure(figsize=(20,20))

# for index, row in T_Wins_Preplant_A_df.iterrows():
#     data = np.array([[row['attacker_mapX'], row['attacker_mapY']]]) #array == [[att x/y]]
#     x,y = data.T #turn array of just numbers into x/y pairs
#     new_plt = plt.imshow(im)
#     new_plt = plt.scatter(x, y, alpha=1, c = row['player_color'])
        
  
        

 
        
            # temp.append([int(row['id']), int(row['Role'])])
            # t_wins = plt.scatter(T_Wins_Preplant_A_df['attacker_mapX'], T_Wins_Preplant_A_df['attacker_mapY'],alpha=0.04,c='orange')
            # t_loses = plt.scatter(T_Loses_Preplant_A_df['attacker_mapX'], T_Loses_Preplant_A_df['attacker_mapY'],alpha=0.04,c='orange')
 
# def pointx_to_resolutionx(xinput,startX=-3217,endX=1912,resX=1024):
#         sizeX=endX-startX
#         if startX < 0:
#             xinput += startX *(-1.0)
#         else:
#             xinput += startX
#         xoutput = float((xinput / abs(sizeX)) * resX);
#         return xoutput
    
# def pointy_to_resolutiony(yinput,startY=-3401,endY=1682,resY=1024):
#     sizeY=endY-startY
#     if startY < 0:
#         yinput += startY *(-1.0)
#     else:
#         yinput += startY
#     youtput = float((yinput / abs(sizeY)) * resY);
#     return resY-youtput

#returns two arrays of victims and attackers in one game from one round
#find a round where A is attacked
#find a file that contains the most lines of captured data 
#Return: List of att ids & List of vic ids
# def find_player_ids_in_round(file, rnd):
#     sim_round_one = (data[(data['round'] == rnd) & (data['file'] == file)].values.tolist())

#     #make sure there are <= 10 att_id's
#     #attid = 21, vic_id = 23
#     att_id_list = []
#     vic_id_list = []

#     for aids in sim_round_one:
#         att_id_list.append(aids[21])
#         vic_id_list.append(aids[23])
    
#     filtered_att_id_list = list(set(att_id_list))
#     filtered_vic_id_list = list(set(vic_id_list))
    
#     return filtered_att_id_list,filtered_vic_id_list

# #Get data for a single player in a single round in a game (attacking/defending)
# #Return: DataFrame of round
# def find_player_in_round(player_id, file, rnd, attacking):
#     if attacking == True:
#         single_round = data[(data['round'] == rnd) & (data['file'] == file) & (data['att_id'] == player_id)]
        
#     else:
#         single_round = data[(data['round'] == rnd) & (data['file'] == file) & (data['vic_id'] == player_id)]
    
#     return single_round

# #get all player ids in a file
# #Return: list of t and ct ids (10)
# def find_team_ids(file):
# #['Unnamed: 0','file','map','date','round','tick','seconds','att_team','vic_team','att_side','vic_side','hp_dmg','arm_dmg','is_bomb_planted',
# #                                                                 'bomb_site','hitbox','wp','wp_type','award','winner_team','winner_side','att_id',
# #                                                                 'att_rank','vic_id','vic_rank','att_pos_x','att_pos_y','vic_pos_x',
# #                                                                 'vic_pos_y','round_type','ct_eq_val','t_eq_val','avg_match_rank']
#     list_of_ct_ids = []
#     list_of_t_ids = []

#     game_data = data[(data['file'] == file) & (data['round'] < 16) & (data['att_id'] != 0)]
#     for index, row in game_data.iterrows():
#         if row['att_side'] == "CounterTerrorist":
#             if row['att_id'] not in list_of_ct_ids:
#                 list_of_ct_ids.append(row['att_id'])
            
#         else:
#             if row['att_id'] not in list_of_t_ids:
#                 list_of_t_ids.append(row['att_id'])
                
#     return list_of_ct_ids, list_of_t_ids

# #Track one side
# #needs lists of ids for both teams, id1 and id2
# def produce_maps_for_each_team(df, t_list, file, rnd):
#     df_copy = df.copy()

#     #assign each player a shade of color (green)
#     t_color = ['green', 'red', 'yellow', 'blue', 'orange']
#     roles = [0, 1, 2, 3, 4]
    
#     single_round_df = df_copy[(df_copy['round'] == rnd) & (df_copy['file'] == file)]
#     single_round_df.insert(0, 'ct_color', 'NaN')
    
#     #adding colors to DF
#     for index, row in single_round_df.iterrows():
#         for _id in t_list:
#             #check if att or vic (has to be one or other)
#             if row['att_id'] == _id:
#                 single_round_df.at[index, 't_color'] = ct_color[ct_list.index(_id)]
                    
#             if row['vic_id'] == _id:
#                   single_round_df.at[index, 'ct_color'] = 'white'
    
#     #print maps with new colors
#     produce_maps_from_list_single(single_round_df, ct_list)

# #given a dataframe of a round return maps on one side
# def produce_maps_from_list_single(single_round_df, ct_list):
#     print("here")
#     single_round_copy = single_round_df.copy()
        
#     single_round_copy['attacker_mapX'] = single_round_copy['att_pos_x'].apply(pointx_to_resolutionx)
#     single_round_copy['attacker_mapY'] = single_round_copy['att_pos_y'].apply(pointy_to_resolutiony)
#     single_round_copy['victim_mapX'] = single_round_copy['vic_pos_x'].apply(pointx_to_resolutionx)
#     single_round_copy['victim_mapY'] = single_round_copy['vic_pos_y'].apply(pointy_to_resolutiony)
    
#     # # Heat map
#     im = plt.imread('./input/de_mirage.png')
    
#     for index, row in single_round_copy.iterrows():
#         if row['att_id'] in ct_list:
#             plt.figure(figsize=(20,20))
        
#             new_plt = plt.imshow(im)           
#             new_plt = plt.scatter(row['attacker_mapX'], row['attacker_mapY'],alpha=1, c = row['ct_color'])
            
#         else:
#             plt.figure(figsize=(20,20))       
#             new_plt = plt.imshow(im)           
#             new_plt = plt.scatter(row['victim_mapX'], row['victim_mapY'],alpha=1,c='white')
            
# #given a dataframe of a round return maps on one side
# def produce_maps_from_lists(single_round_df, ct_list, t_list):
#     single_round_copy = single_round_df.copy()
        
#     single_round_copy['attacker_mapX'] = single_round_copy['att_pos_x'].apply(pointx_to_resolutionx)
#     single_round_copy['attacker_mapY'] = single_round_copy['att_pos_y'].apply(pointy_to_resolutiony)
#     single_round_copy['victim_mapX'] = single_round_copy['vic_pos_x'].apply(pointx_to_resolutionx)
#     single_round_copy['victim_mapY'] = single_round_copy['vic_pos_y'].apply(pointy_to_resolutiony)
    
#     # # Heat map
#     im = plt.imread('./input/de_mirage.png')
#     counter = 1
#     for index, row in single_round_copy.iterrows():
#         data = np.array([[row['attacker_mapX'], row['attacker_mapY']], [row['victim_mapX'], row['victim_mapY']]]) #array == [[att x/y],[vic x/y]]
#         ct_att_color = [row['ct_color'], 'white']
#         t_att_color = [row['t_color'], 'white']
        
#         x,y = data.T #turn array of just numbers into x/y pairs
       
#         if row['att_id'] in ct_list:
#             plt.figure(figsize=(20,20))
#             new_plt = plt.imshow(im)
#             new_plt = plt.scatter(x, y, alpha=1, c = ct_att_color)
#             print("Attacker", x[0], y[0])
            
#             for box in list_of_boxes:
#                 if (box[0] < x[0] < box[2]) and (box[3] < y[0] < box[1]):
#                     print("Attacker", row['vic_id'], "in", box[4],"box")

            
#         else:
#             plt.figure(figsize=(20,20))
#             new_plt = plt.imshow(im)
#             new_plt = plt.scatter(x, y, alpha=1, c = t_att_color)
#             print("Victim", x[0], y[0])
            
#             for box in list_of_boxes:
#                 if (box[0] < x[0] < box[2]) and (box[3] < y[0] < box[1]):
#                     print("Victim", row['vic_id'], "in", box[4],"box")
            
        
#         counter = counter + 1
        
    
# def produce_pairs(df, ct_list, t_list, file, rnd):
#     df_copy = df.copy()
    
#     #assign each player a shade of color (green)
#     ct_color = ['deepskyblue','cyan', 'springgreen', 'blue', 'blueviolet']
#     t_color = ['orange', 'yellow', 'red', 'peru', 'pink']
    
#     single_round_df = df_copy[(df_copy['round'] == rnd) & (df_copy['file'] == file)]
#     single_round_df.insert(0, 'ct_color', 'NaN')
#     single_round_df.insert(0, 't_color', 'NaN')
    
#     #adding colors to DF
#     for index, row in single_round_df.iterrows():
#         for _id in ct_list:
#             #check if att or vic (has to be one or other)
#             if row['att_id'] == _id:
#                 single_round_df.at[index, 'ct_color'] = ct_color[ct_list.index(_id)]
#                 single_round_df.at[index, 't_color'] = 'white'
                    
#             if row['vic_id'] == _id:
#                 single_round_df.at[index, 't_color'] = t_color[t_list.index(row['att_id'])]
#                 single_round_df.at[index, 'ct_color'] = 'white'
                 
#     #print maps with new colors
#     produce_maps_from_lists(single_round_df, ct_list, t_list)
    

            
















#get attacker and victim lists for a round
#att_list, vic_list = find_player_ids_in_round("003218553373129179487_1555113029.dem", 4)
#get single round df from playerID, game, round, attacking == True
#single_round_df = find_player_in_round(76561198152153688, "003218553373129179487_1555113029.dem", 4, True)

#Return ids for a game
# ct_ids, t_ids = find_team_ids("003218553373129179487_1555113029.dem")

#produce_maps_for_each_team(data, ct_ids,"003218553373129179487_1555113029.dem", 4)
#produce_maps_for_each_team(data, t_ids,"003218553373129179487_1555113029.dem", 4)




''' Use These '''
#produce_pairs(data, ct_ids, t_ids,"003218553373129179487_1555113029.dem", 4)

#draw_boxes_tester()
#draw_boxes(A_boxes, './input/de_mirage.png')




###############################################################################


# #t_wins = plt.scatter(T_Wins_Preplant_A_df['attacker_mapX'], T_Wins_Preplant_A_df['attacker_mapY'],alpha=0.04,c='orange')
# t_loses = plt.scatter(T_Loses_Preplant_A_df['attacker_mapX'], T_Loses_Preplant_A_df['attacker_mapY'],alpha=0.04,c='orange')













