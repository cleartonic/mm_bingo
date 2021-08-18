import bingo_df
import numpy as np
import random
import pandas as pd
import statistics
import logging
import os, datetime



pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('mode.chained_assignment', None)

STDEV_LIMIT = 1.5
SCORE_AVERAGE = 2 # this must be 2 for ranks 1 - 3, if this changes in the future in the questions, then this must also change
SCORE_MAX = 3
DF_ITER_LIMIT = 100
ITER_LIMIT = 500
USE_FIXED_LOCATIONS = True


logging.root.handlers = []
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO) # , filename='log.log')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


def apply_bool(x):
    if x == 'y' or x == 'Y':
        return True
    else:
        return False
        
        
def generate_card(SEED_NUM = random.randint(1,999999999),settings = None):
    
    if settings == None:
        settings = {'mm1' : True,
            'mm2' : False,
            'mm3' : False,
            'mm4' : False,
            'mm5' : True,
            'mm6' : False,
            'hard_mode' : False,
            'easy_mode' : False}
    
    if SEED_NUM == None:
        SEED_NUM = random.randint(1,999999999)
        
    error_message = ''
    # SEED_NUM = 1000
    random.seed(SEED_NUM)
    logging.info("SEED NUM %s" % SEED_NUM)
    
    # df = bingo_df.get_latest_bingo()
    
    # check if latest needs to be downloaded
    
    
    mtime = datetime.datetime.fromtimestamp(os.stat('latest_data.csv').st_mtime)
    
    logging.info("latest_data last modified time %s" % mtime)
    
    if (datetime.datetime.now() - mtime).seconds > 300:
        logging.info("Pulling latest data due to >5 minutes from last call")
        try:
            bingo_df.get_latest_bingo()
        except:
            logging.info("ERROR: could not parse google sheets")
            
    df = pd.read_csv('latest_data.csv')
    df.columns.name = ''
    # df = df.fillna('')
    
    def apply_int(x):
        try:
            return int(x)
        except:
            return 1
    
    df['rank'] = df['rank'].apply(apply_int)
    df['games'] = df['games'].astype(str)
    df['img'] = df['img'].apply(lambda x: x if type(x) == str else '')
    
    
    
    if False:
        df_copy = df.copy()
        df = df_copy.copy()
    
    
    ### filter out games not selected
    
    logging.info("Old df shape %s" % df.shape[0])    
    
    valid_games = ['any']
    for setting, boolean in settings.items():
        if boolean:
           valid_games.append(setting.replace("mm","")) 
            
           
            
    def apply_valid_games(x, y):
        # x = games
        # y = type
        
        real_games = [i for i in valid_games if i != 'any' and i != 'hard_mode' and i != 'easy_mode' and i != 'all']
        goal_games = x.split(',')
        
        if type(y) == float:
            y = ''
        
        # ALL case
        if y == 'all':
            for game in x.split(","):
                if game not in valid_games:
                    return False
            return True
        
        # if ANY# case (number)
        if 'any' in y and len(y) > 3:
            try:
                num = int(y.split("any")[1])
                
                if len(real_games) >= num and len([i for i in real_games if i in goal_games]) == len(real_games):
                    logging.info("TRUE")
                    return True
                else:
                    logging.info("FALSE")
                    return False
            except:
                logging.info("Failed parse on any#")
                return False
        
        
        # ANY default case
        if y == '' or y != y:
            for game in x.split(","):
                if game in valid_games:
                    return True
            return False

        logging.info("***** Neither case for valid games, returning True")        
        return True
        
        
    df['validator'] = np.vectorize(apply_valid_games)(df['games'],df['type'])
    df = df[df['validator']==True]
    df.drop('validator',axis=1,inplace=True)

    logging.info("New df shape %s" % df.shape[0])    
    
    
    
    df_iter_num = 0
    df_pass_flag = False
    df_dict = df.T.to_dict()
    
    ## tries 100 sets of questions, rearranging each set 1000 times until it meets criteria:
    
    # average of every row/col/diag is not out of bounds
    # making sure max rank is not present too often in row/col
    #   diag is specifically not checked here
    # stdev of every row is reasonable
    
    
    while df_iter_num < DF_ITER_LIMIT and not df_pass_flag:
        
        logging.info("Df iter attempt : %s " % df_iter_num)
        
        squares = 25
        # squares_3 = random.randint(5,5) # tried 4 -> 6, but 6 caused weirdness balancing
        # squares_2 = random.randint(6,10)
        squares_3 = 5
        squares_2 = 5
        squares_1 = squares - squares_3 - squares_2
        
        
        if settings['hard_mode']:
            df3 = df[df['rank']>3]
            df3t = df3.sample(squares_3, random_state=SEED_NUM)
            
            
            df2 = df[(df['rank']==3) & (~df.index.isin(df3t.index))]
            df1 = df[df['rank']==2]
            
            
            
            df2t = df2.sample(squares_2, random_state=SEED_NUM)
            df1t = df1.sample(squares_1, random_state=SEED_NUM)
            
            
        elif settings['easy_mode']:
            df3 = df[df['rank']==2]
            df3t = df3.sample(squares_3, random_state=SEED_NUM)

            df2 = df[df['rank']==1]
            df2t = df2.sample(squares_2, random_state=SEED_NUM)
            
            df1 = df[(df['rank']==1) & (~df.index.isin(df2t.index))]
            

            df1t = df1.sample(squares_1, random_state=SEED_NUM)
            
            
            
        else:
            df3 = df[df['rank']==3]
            df2 = df[df['rank']==2]
            df1 = df[df['rank']==1]

            df3t = df3.sample(squares_3, random_state=SEED_NUM)
            df2t = df2.sample(squares_2, random_state=SEED_NUM)
            df1t = df1.sample(squares_1, random_state=SEED_NUM)


        
        
        dft = df3t.append(df2t).append(df1t)

        
        ###############################
        ###### GROUP REPLACEMENT ######
        ###############################
        def check_groups(dft):
        
            df_count = dft[['group']]
            df_count['count'] = 1
            df_count = df_count[df_count['group']==df_count['group']]
            gdict = df_count.T.to_dict()
            gdict2 = {}
            for k, v in gdict.items():
                g = [i.strip() for i in gdict[k]['group'].split(",")]
                
                for i in g:
                    if i not in gdict2:
                        gdict2[i] = {}
                        gdict2[i]['count'] = 1
                        gdict2[i]['idx'] = [k]
                    else:
                        gdict2[i]['count'] = gdict2[i]['count'] + 1
                        gdict2[i]['idx'] = gdict2[i]['idx'] + [k]
                        
            
            current_idx = []
            for i in gdict2.keys():
                for i2 in gdict2[i]['idx']:
                    current_idx.append(i2)
            current_idx = sorted(list(set(current_idx)))
            
            
            groups_to_replace = [i for i in gdict2 if gdict2[i]['count'] > 1]            
            
            return df_count, gdict2, groups_to_replace



        def find_replacements(dft):

            

            existing_groups = []
            existing_groups2 = list(set(dft['group']))
            existing_groups2 = [i for i in existing_groups2 if type(i) == str]
            for i in existing_groups2:
                if type(i) == list:
                    for i2 in i:
                        existing_groups.append(i2)
                else:
                    existing_groups.append(i)
            existing_groups = sorted(list(set(existing_groups)))
    
    
            # now check if group type is unique and try to find replacements if not
            try: 
                
                indexes_to_add = []
                indexes_to_drop = []
                
                df_count, gdict2, groups_to_replace = check_groups(dft)
    
                
                df_piv = df_count.pivot_table(index=['group'],values='count',aggfunc=np.sum)
            
                if not df_piv.empty:            
                    
                    #### NEW METHOD, SPLIT GROUPS ####
                    
                    try:
    
                        
                        for g in groups_to_replace:
                            indexes = list(gdict2[g]['idx'])
                            index_to_keep = random.choice(indexes)
                            other_indexes = [i for i in indexes if i not in [index_to_keep]]
                            
                            for idx in other_indexes:
                                rank = dft.loc[idx]['rank']
                                matching_ranks = [i for i in df_dict if df_dict[i]['rank']==rank and df_dict[i]['group'] not in existing_groups and i not in dft.index and i not in indexes_to_add and i not in indexes_to_drop]
                                
                                if not matching_ranks:
                                    logging.info("Matching ranks & group types could not be found, ignoring")
                                else:
                                    chosen_idx = random.choice(matching_ranks)
                                    if type(df_dict[chosen_idx]['group']) == str:    
                                        existing_groups.append(df_dict[chosen_idx]['group'])
                                    indexes_to_add.append(chosen_idx)
                                    indexes_to_drop.append(idx)
                        
                    except Exception as e:
                        logging.info("Error on group allocation, retrying df %s" % e)
                        return pd.DataFrame()
                    
                    
                    #### OLD METHOD, BEFORE SPLIT GROUPS ####
                    
                    # try:
                    
                    #     breakpoint()
                    #     groups_to_replace = df_piv[df_piv['count']>1].to_dict()['count']
            
            
                    #     for group_type, count in groups_to_replace.items():
                            
                    #         # filter on matching group types
                    #         dft2 = dft[dft['group']==group_type]
                            
                    #         # sample 1, and then replace the remaining 
                    #         indexes = list(dft2.index)
                    #         index_to_keep = random.choice(indexes)
                    #         other_indexes = [i for i in indexes if i not in [index_to_keep]]
                            
                    #         for idx in other_indexes:
                    #             x = df_dict[idx]
                    #             rank = x['rank']
                    #             matching_ranks = [i for i in df_dict if df_dict[i]['rank']==rank and df_dict[i]['group'] not in existing_groups and i not in dft.index and i not in indexes_to_add and i not in indexes_to_drop]
                                
                    #             if not matching_ranks:
                    #                 logging.info("Matching ranks & group types could not be found, ignoring")
                    #             else:
                    #                 chosen_idx = random.choice(matching_ranks)
                    #                 if type(df_dict[chosen_idx]['group']) == str:    
                    #                     existing_groups.append(df_dict[chosen_idx]['group'])
                    #                 indexes_to_add.append(chosen_idx)
                    #                 indexes_to_drop.append(idx)
                    # except:
                    #     logging.info("Error on group allocation, retrying df")
                    #     continue
                                
                                
            except Exception as e:
                logging.info("Error on replacing group_types: %s" % e)
                
                
            logging.info("Adding indexes %s" % indexes_to_add)
            logging.info("Dropping indexes %s" % indexes_to_drop)
            
    
            
            dft = dft.drop(indexes_to_drop).append(df.loc[indexes_to_add])
            
            return dft
        
        
        
        dft = find_replacements(dft)
        
        if dft.empty:
            # failure case
            logging.info("Checking next df iteration")
            continue

        # now after adding new items, perform check again
        # if groups_to_replace is empty list, proceed
        # if not, repeat
        
        
        
        df_count, gdict2, groups_to_replace = check_groups(dft)
        
        if groups_to_replace:
            # repeat until success
            iternum = 0
            while not groups_to_replace or iternum  < 100:
                logging.info("Retrying group replacement %s" % iternum)
                df_count, gdict2, groups_to_replace = check_groups(dft)
                iternum  += 1
        

        
        if dft.shape[0] < 25:
            logging.info("Not enough rows to create bingo, retrying")
            continue 
        
        if len(dft.index.unique()) < 25:
            logging.info("Not enough unique squares to create bingo, retrying")
            continue 
        
        else:
            iter_num = 0
            if USE_FIXED_LOCATIONS:
                # fixed locations means use a preset bingo board for tier 2 and 3 slots
                # 
                
            

                # later, you could build out different sets of these 
                
                
                # square sets is a list that has 2 lists, first has rank 3, second has rank 2
                square_sets = [
                    [[1,5,12,19,23],[4,6,13,15,22]],  # a
                    [[3,9,12,15,21],[1,8,10,17,24]],  # a90
                    [[1,5,12,19,23],[2,9,11,18,20]],  # a180
                    [[3,9,12,15,21],[0,7,14,16,23]],  # a270
                    
                    [[3,5,12,19,21],[1,8,10,17,24]],  # b1
                    [[3,5,12,19,21],[2,9,11,18,20]],  # b2 90deg
                    [[3,5,12,19,21],[0,7,14,16,23]],  # b2 180deg
                    [[3,5,12,19,21],[4,6,13,15,22]],  # b2 270deg
                    
                    [[0,8,14,17,21],[2,9,11,18,20]],  # c1
                    [[4,5,11,18,22],[0,7,14,16,23]],  # c2 90
                    [[3,7,10,16,24],[4,6,13,15,22]],  # c3 180 
                    [[2,6,13,19,20],[1,8,10,17,24]],  # c4 270
                    
                                  
                              ] 
                
                chosen_set = random.choice(square_sets)
                # chosen_set = [square_sets[11]][0] # testing each one
                
                #
                tier_3_squares = chosen_set[0]
                tier_2_squares = chosen_set[1]
                
                tier_1_squares = [i for i in range(0,25)]
                tier_1_squares = [i for i in tier_1_squares if i not in tier_3_squares and i not in tier_2_squares]


                # build dataframes
            
            
                if settings['hard_mode']:
                    
                    try:
                        dft3 = dft[dft['rank']>3]
                        if dft3.shape[0] < 5:
                            dft3 = dft3.append(dft[dft['rank']==3].sample(5 - dft3.shape[0], random_state=SEED_NUM))
    
                        
                        dft3['squares'] = tier_3_squares
                        dft2 = dft[(dft['rank']==3) & (~dft.index.isin(dft3.index))]
                        dft2['squares'] = tier_2_squares
                        dft1 = dft[dft['rank']==2]
                        dft1['squares'] = tier_1_squares
                    except Exception as e:
                        logging.info("Error on building hardtype squares, retrying df generation: %s" % e)
                        continue
                    
                elif settings['easy_mode']:
                    dft3 = dft[dft['rank']==2]
                    dft3['squares'] = tier_3_squares
                    dft2 = dft[dft['rank']==1].iloc[0:5]
                    dft2['squares'] = tier_2_squares
                    dft1 = dft[(dft['rank']==1) & (~dft.index.isin(dft2.index))]
                    dft1['squares'] = tier_1_squares
                    
                    
                else:
   
                    dft3 = dft[dft['rank']==3]
                    dft3['squares'] = tier_3_squares
                    dft2 = dft[dft['rank']==2]
                    dft2['squares'] = tier_2_squares
                    dft1 = dft[dft['rank']==1]
                    dft1['squares'] = tier_1_squares
                    
                    
                        


                
                dft = dft3.append(dft2).append(dft1)
                dft = dft.sort_values(by='squares')
                
                if dft.shape[0] < 25:
                    logging.info("Not enough squares for bingo, retrying df generation")
                    
                    continue
                
                
                
                pass_flag = True
                df_pass_flag = True
            
            else:
                
                # if not using fixed rank 2/3, then this will try to automatically parse 
                
                #### iteration
                
                pass_flag = False
                while iter_num < ITER_LIMIT and not pass_flag:
                    # logging.info("Df iter %s, iter attempt: %s" % (df_iter_num, iter_num))
                    dft['random'] = df['goal'].apply(lambda x : random.randint(1,100000))
                    dft = dft.sort_values(by='random')
                    dft.reset_index(inplace=True,drop=True)
                    
                    
                    data = dft.to_dict()
                    ranks = list(data['rank'].values())[::-1]
                    
                    array = []
                    for r in range(5):
                        templ = []
                        for r2 in range(5):
                            templ.append(ranks.pop())
                        array.append(templ)
                    
                    
                    row_scores = []
                    for i in array:
                        row_scores.append(sum(i))
                        
                    col_scores = []
                    for i in range(5):
                        templ = []
                        for i2 in array:
                            templ.append(i2[i])
                        col_scores.append(sum(templ))
                    
                        
                    
                    # this is "dynamic" scaling that says if on the current set of questions
                    # it's starting to fail (e.g., too many filters applied)
                    # at least give it a shot to finish with some easier leniency near the end 
                    if iter_num > ITER_LIMIT * .95:
                        UPPER_AVG_LIMIT = 7.5
                        LOWER_AVG_LIMIT = 2.5
                    elif iter_num > ITER_LIMIT * .90:
                        UPPER_AVG_LIMIT = 7
                        LOWER_AVG_LIMIT = 3
                    else:
                        UPPER_AVG_LIMIT = 6.5
                        LOWER_AVG_LIMIT = 3.5
                        
                    
                    ## AVERAGE ## 
                    
                    row_avg_pass = True
                    for i in row_scores:
                        # if SCORE_AVERAGE * UPPER_AVG_LIMIT < i < SCORE_AVERAGE * LOWER_AVG_LIMIT: ## e.g. an average of 2, means row should be ~10, and force it not accept < 8
                        if i != 8:
                            row_avg_pass = False
                    col_avg_pass = True
                    for i in col_scores:
                        # if SCORE_AVERAGE * UPPER_AVG_LIMIT < i < SCORE_AVERAGE * LOWER_AVG_LIMIT: ## e.g. an average of 2, means row should be ~10, and force it not accept < 8
                        if i != 8:
                            col_avg_pass = False
                            
                            
                            
                    ## AVERAGE, DIAGONALS ##
                    tl_col_score = 0
                    for i in range(5):
                        tl_col_score += array[i][i]
                        
                    tr_col_score = 0
                    for i in range(5):
                        tr_col_score += array[i][4-i]
                        
                    # tl_pass = SCORE_AVERAGE * UPPER_AVG_LIMIT > tl_col_score > SCORE_AVERAGE * LOWER_AVG_LIMIT
                    # tr_pass = SCORE_AVERAGE * UPPER_AVG_LIMIT > tr_col_score > SCORE_AVERAGE * LOWER_AVG_LIMIT
                    
                    tl_pass = tl_col_score == 8
                    tr_pass = tr_col_score == 8
                    
                    # logging.info(tl_col_score, tr_col_score, tl_pass, tr_pass)
                    
                    ## STDEV ##
                    
                    row_stdev = round(statistics.stdev(row_scores),2)
                    col_stdev = round(statistics.stdev(col_scores),2)
                    
                    row_stdev_pass = row_stdev <= STDEV_LIMIT
                    col_stdev_pass = col_stdev <= STDEV_LIMIT
                    
                    
                    
                    #######################################
                    # this is temporarily disabled
                    # right now we have static 5 for rank 2 and 3
                    #######################################
                    
                    
                    # MAX OF HIGHEST RANK
                    # rows
                    
                    COUNT_LIMIT = 1
                    if squares_3 > 5:
                        COUNT_LIMIT = 2
                    
                    rows_max_rank = True
                    for i in array:
                        if i.count(SCORE_MAX) > COUNT_LIMIT:
                            rows_max_rank = False
                            break
            
                    # cols
                    cols_max_rank = True
                    for i in range(5):
                        temp_l = []
                        for i2 in array:
                            temp_l.append(i2[i])
                        if temp_l.count(SCORE_MAX) > COUNT_LIMIT:
                            cols_max_rank = False
                            break
                        
                        
                        
            
                    # MAX OF SECOND RANK
                    # rows
                    
                    COUNT_LIMIT = 1
                    if squares_2 > 5:
                        COUNT_LIMIT = 2
                    
                    SECOND_RANK = 2
                    rows_second_rank = True
                    for i in array:
                        if i.count(SECOND_RANK) > COUNT_LIMIT:
                            rows_second_rank = False
                            break
            
                    # cols
                    cols_second_rank = True
                    for i in range(5):
                        temp_l = []
                        for i2 in array:
                            temp_l.append(i2[i])
                        if temp_l.count(SECOND_RANK) > COUNT_LIMIT:
                            cols_second_rank = False
                            break
            
                    
                    
                    
                    logging.info("%s %s %s %s %s %s %s %s %s %s " % (row_stdev_pass , col_stdev_pass , row_avg_pass , col_avg_pass , tl_pass , tr_pass , rows_max_rank , cols_max_rank , rows_second_rank, cols_second_rank))
                    for i in array:
                        logging.info(i)
                    if row_stdev_pass and col_stdev_pass and row_avg_pass and col_avg_pass and tl_pass and tr_pass and rows_max_rank and cols_max_rank and rows_second_rank and cols_second_rank:
                    # if row_avg_pass and col_avg_pass:
                        pass_flag = True
                        df_pass_flag = True
                        
                    
                    
                    iter_num += 1
                    
                    
                
                    
                    
            df_iter_num += 1
                
            
    if df_iter_num == DF_ITER_LIMIT and iter_num == ITER_LIMIT:
        error_message = "No bingo set could be generated due to iteration limit."
        dft = pd.DataFrame()
    else:
        if not USE_FIXED_LOCATIONS:
            for i in array:
                logging.info(i)
            logging.info("%s %s" % (row_scores, col_scores))
            dft.drop('random',axis=1,inplace=True)
        logging.info(dft[['goal','rank','games','type','group','notes']])
        
        
        # logging.info(row_stdev, col_stdev)
        # logging.info(row_stdev_pass, col_stdev_pass)



    dft['pw'] = dft['pw'].apply(apply_bool)

    return dft, error_message, SEED_NUM


def generate_popout(settings):
    data = settings['data']
    data, settings_str = data.split(",Seed ")
    data = data.split(",")
    data_header = data[0]
    squares = [int(i) for i in data[1:]]
    
    df = pd.read_csv('latest_data.csv').loc[squares]
    df['pw'] = df['pw'].apply(apply_bool)
    df['img'] = df['img'].apply(lambda x: x if type(x) == str else '')
    

    goalsd = df[['goal','notes', 'rank', 'games','pw', 'img']].T.to_dict()
    goals = []
    for idx, (k, v) in enumerate(goalsd.items()):
        img = []
        notes = v['notes']
        if notes != notes:
            notes = ''
        if v['pw']:
            notes = '%s\n(password allowed)' % notes
             
        if v['img']:
            img = v['img'].replace(" ","").split(",")
            
        goals.append([v['goal'],notes, v['rank'], v['games'], v['pw'], k, img, idx])
    
    
    return data_header, goals, "Seed %s" % settings_str 





if __name__ == '__main__':
    if True:
        SEED_NUM = 530815525
        df, error_message, seed_num = generate_card(SEED_NUM)
        if df.empty:
            logging.info("No dataframe was returned")
            if error_message:
                logging.info(error_message)
        else:
            goals = list(df['goal'].unique())
            
