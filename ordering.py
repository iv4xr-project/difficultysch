from main import play

MAPS = ["map_dif1.txt"]
RUNS = 1000
NOISE = 0.05
errors = ["continuous_random","timing"]
error = errors[0]



def main():
    gravity_factor = 0
    acceleration_factor = 0
    prob_success = []
    score_loss = []
    trial_to_learn = []
    maps_prob_dict = []
    maps_avg_dict = []
    for map in MAPS:
        possible = 1
        print(gravity_factor)
        prob_dict = {'name':map}
        avg_dict = {'name':map}
        while possible:
            success, total_score, best_sc, maxscore =  play(map, RUNS, NOISE, error, gravity_factor, acceleration_factor)
            if (success/RUNS *100 == 0):
                possible = 0
                continue
            avg_score_sing = maxscore - round(total_score/success,2)

            prob_dict[1+gravity_factor] = round(success/RUNS *100,1)
            avg_dict[1+gravity_factor] = round((1 - avg_score_sing/best_sc)*100,2)

            gravity_factor = round(gravity_factor + 0.2,1)

        maps_prob_dict.append(prob_dict.copy())
        maps_avg_dict.append(avg_dict.copy())
    
    
    #evaluate probability of success metric

    for map_dict in maps_prob_dict:
        map_name = map_dict['name']
        print("Ranking for probability of success for different gravity in "+ map_name +" :\n")
        map_dict_copy = map_dict.copy()
        del map_dict_copy['name']
        prob_succ_map_sort = {k: v for k, v in sorted(map_dict_copy.items(), key=lambda item: item[1])}
        keys_list = list(prob_succ_map_sort)
    
        for i in range(1,len(prob_succ_map_sort)+1):
            print(i,"º  -  " ,keys_list[-i] ,"gravity with ", prob_succ_map_sort[keys_list[-i]],"%" )
            
    map_dicts = {}
    for map_dict in maps_prob_dict:
        map_dicts[map_dict['name']] = map_dict[1]
    print(map_dicts)

    prob_succ_maps_sort = {k: v for k, v in sorted(map_dicts.items(), key=lambda item: item[1])}
    keys_list = list(prob_succ_maps_sort)
    print("Ranking for probability of success for different maps with 1.0 gravity   :\n")
    for i in range(1,len(prob_succ_maps_sort)+1):
        print(i,"º  -  " , keys_list[-i]," with ", prob_succ_maps_sort[keys_list[-i]],"%" )

    
    #evaluate average score loss metric

    for map_dict in maps_avg_dict:
        map_name = map_dict['name']
        print("Ranking for average score loss for different gravity in "+ map_name +" :\n")
        map_dict_copy = map_dict.copy()
        del map_dict_copy['name']
        prob_avg_map_sort = {k: v for k, v in sorted(map_dict_copy.items(), key=lambda item: item[1])}
        keys_list = list(prob_avg_map_sort)
    
        for i in range(len(prob_avg_map_sort)):
            print(i+1,"º  -  " ,keys_list[i] ,"gravity with ", prob_avg_map_sort[keys_list[i]],"%" )
            
    map_dicts = {}
    for map_dict in maps_avg_dict:
        map_dicts[map_dict['name']] = map_dict[1]

    prob_avg_maps_sort = {k: v for k, v in sorted(map_dicts.items(), key=lambda item: item[1])}
    keys_list = list(prob_avg_maps_sort)
    print("Ranking for average score loss for different maps with 1.0 gravity   :\n")
    for i in range(1,len(prob_avg_maps_sort)+1):
        print(i,"º  -  " , keys_list[-i]," with ", prob_avg_maps_sort[keys_list[-i]],"%" )


    #evaluate Difficulty of learning metric
    for map in MAPS:
        with open("maps/"+map[:-4]+"/report_"+map) as f:
            first_line = f.readline()
            trial = [int(s) for s in first_line.split() if s.isdigit()][0]
            trial_to_learn.append(trial)

    trial_to_learn_sort = sorted(range(len(trial_to_learn)), key=lambda k: trial_to_learn[k])
    print("\nRanking for difficulty of learning:\n")
    last_rank = 0
    for i in range(len(MAPS)):
        if i>0 and (trial_to_learn[trial_to_learn_sort[i]] == trial_to_learn[trial_to_learn_sort[i-1]]):
            rank = last_rank
        else:
            rank = last_rank+1
        print(rank,"º  -  " , MAPS[trial_to_learn_sort[i]],"with ", trial_to_learn[trial_to_learn_sort[i]]," trials" )
        last_rank = rank



if __name__ == "__main__":
    main()