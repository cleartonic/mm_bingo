import bingo_df
import random
import pandas as pd
import statistics
import logging

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

STDEV_LIMIT = 1.5
SCORE_AVERAGE = 2 # this must be 2 for ranks 1 - 3, if this changes in the future in the questions, then this must also change
SCORE_MAX = 3
DF_ITER_LIMIT = 100
ITER_LIMIT = 500


logging.basicConfig(filename='log.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)



def generate_card(SEED_NUM = random.randint(1,999999999),settings = None):
    
    if settings == None:
        settings = {'mm1' : True,
            'mm2' : False,
            'mm3' : False,
            'mm4' : False,
            'mm5' : False,
            'mm6' : True}
    
    if SEED_NUM == None:
        SEED_NUM = random.randint(1,999999999)
    error_message = ''
    # SEED_NUM = 1000
    random.seed(SEED_NUM)
    
    # df = bingo_df.get_latest_bingo()
    
    df = pd.read_csv('testing.csv')
    df.columns.name = ''
    
    df['rank'] = df['rank'].astype(int)
    
    
    if False:
        df_copy = df.copy()
        df = df_copy.copy()
    
    
    ### filter out games not selected
    
    logging.error("Old df shape %s" % df.shape[0])    
    
    valid_games = ['all']
    for setting, boolean in settings.items():
        if boolean:
           valid_games.append(setting.replace("mm","")) 
            
           
            
    def apply_valid_games(x):
        if x == 'all':
            return True
        
        else:
            categories = x.split(",")
            for c in categories:
                if c not in valid_games:
                    return False
            # passes test
            return True
    df['validator'] = df['category'].apply(apply_valid_games)
    df = df[df['validator']==True]
    df.drop('validator',axis=1,inplace=True)

    logging.error("New df shape %s" % df.shape[0])    
    
    
    
    df_iter_num = 0
    df_pass_flag = False
    
    
    ## tries 100 sets of questions, rearranging each set 1000 times until it meets criteria:
    
    # average of every row/col/diag is not out of bounds
    # making sure max rank is not present too often in row/col
    #   diag is specifically not checked here
    # stdev of every row is reasonable
    
    
    while df_iter_num < DF_ITER_LIMIT and not df_pass_flag:
        
        logging.info("Df iter attempt : %s " % df_iter_num)
        
        squares = 25
        squares_3 = random.randint(5,5) # tried 4 -> 6, but 6 caused weirdness balancing
        squares_2 = random.randint(6,10)
        squares_1 = squares - squares_3 - squares_2
        
        df3 = df[df['rank']==3].sample(squares_3, random_state=SEED_NUM)
        df2 = df[df['rank']==2].sample(squares_2, random_state=SEED_NUM)
        df1 = df[df['rank']==1].sample(squares_1, random_state=SEED_NUM)
        
        
        # iterate here too 
        
        
        dft = df3.append(df2).append(df1)
        
        if dft.shape[0] < 25:
            logging.info("Not enough rows to create bingo, retrying")
            continue 
        
        else:
            
            
            #### iteration
            iter_num = 0
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
                    UPPER_AVG_LIMIT = 7
                    LOWER_AVG_LIMIT = 3
                elif iter_num > ITER_LIMIT * .90:
                    UPPER_AVG_LIMIT = 6.5
                    LOWER_AVG_LIMIT = 3.5
                else:
                    UPPER_AVG_LIMIT = 6
                    LOWER_AVG_LIMIT = 4
                    
                
                ## AVERAGE ## 
                
                row_avg_pass = True
                for i in row_scores:
                    if SCORE_AVERAGE * UPPER_AVG_LIMIT < i < SCORE_AVERAGE * LOWER_AVG_LIMIT: ## e.g. an average of 2, means row should be ~10, and force it not accept < 8
                        row_avg_pass = False
                col_avg_pass = True
                for i in col_scores:
                    if SCORE_AVERAGE * UPPER_AVG_LIMIT < i < SCORE_AVERAGE * LOWER_AVG_LIMIT: ## e.g. an average of 2, means row should be ~10, and force it not accept < 8
                        col_avg_pass = False
                        
                        
                        
                ## AVERAGE, COLUMNS ##
                tl_col_score = 0
                for i in range(5):
                    tl_col_score += array[i][i]
                    
                tr_col_score = 0
                for i in range(5):
                    tr_col_score += array[i][4-i]
                    
                tl_pass = SCORE_AVERAGE * UPPER_AVG_LIMIT > tl_col_score > SCORE_AVERAGE * LOWER_AVG_LIMIT
                tr_pass = SCORE_AVERAGE * UPPER_AVG_LIMIT > tr_col_score > SCORE_AVERAGE * LOWER_AVG_LIMIT
                # logging.info(tl_col_score, tr_col_score, tl_pass, tr_pass)
                
                ## STDEV ##
                
                row_stdev = round(statistics.stdev(row_scores),2)
                col_stdev = round(statistics.stdev(col_scores),2)
                
                row_stdev_pass = row_stdev <= STDEV_LIMIT
                col_stdev_pass = col_stdev <= STDEV_LIMIT
                
                
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
        
                
                
                
                
                if row_stdev_pass and col_stdev_pass and row_avg_pass and col_avg_pass and tl_pass and tr_pass and rows_max_rank and cols_max_rank:
                # if row_avg_pass and col_avg_pass:
                    pass_flag = True
                    df_pass_flag = True
                    
                
                
                iter_num += 1
            df_iter_num += 1
                
            
    if df_iter_num == DF_ITER_LIMIT and iter_num == ITER_LIMIT:
        error_message = "No bingo set could be generated due to iteration limit."
        dft = pd.DataFrame()
    else:
        for i in array:
            logging.info(i)
        logging.info("%s %s" % (row_scores, col_scores))
        dft.drop('random',axis=1,inplace=True)
        logging.info(dft)
        
        
        # logging.info(row_stdev, col_stdev)
        # logging.info(row_stdev_pass, col_stdev_pass)

    return dft, error_message, SEED_NUM

if __name__ == '__main__':
    df, error_message, seed_num = generate_card()
    if df.empty:
        logging.info("No dataframe was returned")
        if error_message:
            logging.info(error_message)
    else:
        goals = list(df['goal'].unique())
        
