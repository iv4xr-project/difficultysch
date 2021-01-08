from main import play
MAPS = ["map_dif10.txt","map_dif1.txt","map_dif2.txt"]
prob_success = []
avg_score = []
best_score = []
score_loss = []
RUNS = 2
NOISE = 0.00
for map in MAPS:
   success, total_score, best_sc, maxscore =  play(map, RUNS, NOISE)
   prob_success.append(success/RUNS *100)
   avg_score_sing = maxscore - round(total_score/success,2)
   avg_score.append(avg_score_sing)
   best_score.append(maxscore - best_sc)
   score_loss.append((1 - avg_score_sing/best_sc)*100)
   
#evaluate probability of success metric

prob_succ_sort = sorted(range(len(prob_success)), key=lambda k: prob_success[k])
print("Ranking for probability of success:\n\n")
last_rank = 0
for i in range(len(MAPS)):
    if i>0 and (prob_success[prob_succ_sort[i]] == prob_success[prob_succ_sort[i-1]]):
        rank = last_rank
    else:
        rank = last_rank+1
    print(rank,"º  -  " , MAPS[prob_succ_sort[i]],"with ", prob_success[prob_succ_sort[i]],"%" )
    last_rank = rank

#evaluate average score metric

score_loss_sort = sorted(range(len(score_loss)), key=lambda k: score_loss[k])
print("\nRanking for average score:\n\n")
last_rank = 0
for i in range(len(MAPS)):
    if i>0 and (score_loss[score_loss_sort[i]] == score_loss[score_loss_sort[i-1]]):
        rank = last_rank
    else:
        rank = last_rank+1
    print(rank,"º  -  " , MAPS[score_loss_sort[i]],"with ", score_loss[score_loss_sort[i]],"%" )
    last_rank = rank