from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, BooleanField, IntegerField
from htmlmin import minify
from bingo import generate_card, generate_popout, generate_df_for_custom


import datetime, traceback
import logging
import traceback
import os
import pandas as pd

application = app = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
application.config.from_object(__name__)

SECRET_KEY = os.urandom(32)
application.config['SECRET_KEY'] = SECRET_KEY


logging.basicConfig(filename='log.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

passed_settings = None

class MainForm(FlaskForm):

    form_mm1 =  BooleanField(label='MM1',default=True)
    form_mm2 =  BooleanField(label='MM2',default=True)
    form_mm3 =  BooleanField(label='MM3',default=True)
    form_mm4 =  BooleanField(label='MM4',default=True)
    form_mm5 =  BooleanField(label='MM5',default=True)
    form_mm6 =  BooleanField(label='MM6',default=True) 
    form_hard_mode =  BooleanField(label='Hard Mode',default=False) 
    form_easy_mode =  BooleanField(label='Easy Mode',default=False) 
    form_balanced_games =  BooleanField(label='Balanced games',default=True) 
    form_multi_goals =  BooleanField(label='Multi-game goals',default=True) 
    form_seed = IntegerField(label='Seed number (integer):', validators = [validators.Optional(), validators.NumberRange(min=1,max=999999999, message="Must be integer")])


class CustomForm(FlaskForm):

    goals = generate_df_for_custom()
    form_choice1 = SelectField('', choices=goals)
    form_choice2 = SelectField('', choices=goals)
    form_choice3 = SelectField('', choices=goals)
    form_choice4 = SelectField('', choices=goals)
    form_choice5 = SelectField('', choices=goals)
    form_choice6 = SelectField('', choices=goals)
    form_choice7 = SelectField('', choices=goals)
    form_choice8 = SelectField('', choices=goals)
    form_choice9 = SelectField('', choices=goals)
    form_choice10 = SelectField('', choices=goals)
    form_choice11 = SelectField('', choices=goals)
    form_choice12 = SelectField('', choices=goals)
    form_choice13 = SelectField('', choices=goals)
    form_choice14 = SelectField('', choices=goals)
    form_choice15 = SelectField('', choices=goals)
    form_choice16 = SelectField('', choices=goals)
    form_choice17 = SelectField('', choices=goals)
    form_choice18 = SelectField('', choices=goals)
    form_choice19 = SelectField('', choices=goals)
    form_choice20 = SelectField('', choices=goals)
    form_choice21 = SelectField('', choices=goals)
    form_choice22 = SelectField('', choices=goals)
    form_choice23 = SelectField('', choices=goals)
    form_choice24 = SelectField('', choices=goals)
    form_choice25 = SelectField('', choices=goals)

 
    # form_choice1 = SelectField('', choices=goals, default=goals[0][0])
    # form_choice2 = SelectField('', choices=goals, default=goals[1][0])
    # form_choice3 = SelectField('', choices=goals, default=goals[2][0])
    # form_choice4 = SelectField('', choices=goals, default=goals[3][0])
    # form_choice5 = SelectField('', choices=goals, default=goals[4][0])
    # form_choice6 = SelectField('', choices=goals, default=goals[5][0])
    # form_choice7 = SelectField('', choices=goals, default=goals[6][0])
    # form_choice8 = SelectField('', choices=goals, default=goals[7][0])
    # form_choice9 = SelectField('', choices=goals, default=goals[8][0])
    # form_choice10 = SelectField('', choices=goals, default=goals[9][0])
    # form_choice11 = SelectField('', choices=goals, default=goals[10][0])
    # form_choice12 = SelectField('', choices=goals, default=goals[11][0])
    # form_choice13 = SelectField('', choices=goals, default=goals[12][0])
    # form_choice14 = SelectField('', choices=goals, default=goals[13][0])
    # form_choice15 = SelectField('', choices=goals, default=goals[14][0])
    # form_choice16 = SelectField('', choices=goals, default=goals[15][0])
    # form_choice17 = SelectField('', choices=goals, default=goals[16][0])
    # form_choice18 = SelectField('', choices=goals, default=goals[17][0])
    # form_choice19 = SelectField('', choices=goals, default=goals[18][0])
    # form_choice20 = SelectField('', choices=goals, default=goals[19][0])
    # form_choice21 = SelectField('', choices=goals, default=goals[20][0])
    # form_choice22 = SelectField('', choices=goals, default=goals[21][0])
    # form_choice23 = SelectField('', choices=goals, default=goals[22][0])
    # form_choice24 = SelectField('', choices=goals, default=goals[23][0])
    # form_choice25 = SelectField('', choices=goals, default=goals[24][0])

def get_settings_string(form):
    output_str = 'MM'
    
    if form.form_mm1.data:
        output_str += "1, "
    if form.form_mm2.data:
        output_str += "2, "
    if form.form_mm3.data:
        output_str += "3, "
    if form.form_mm4.data:
        output_str += "4, "
    if form.form_mm5.data:
        output_str += "5, "
    if form.form_mm6.data:
        output_str += "6, "
    if form.form_hard_mode.data:
        output_str += "Hard, "
    if form.form_easy_mode.data:
        output_str += "Easy, "
    if form.form_balanced_games.data:
        output_str += "Balanced, "
    if not form.form_multi_goals.data:
        output_str += "No Multi, "
    
    return output_str[:-2]

def get_url(settings, seed): 
    url = '?'
    
    t1 = 'settings='
    for k2, v2 in settings['games'].items():
        t1 += '%s,' % k2.split("mm")[1]
    for k, v in settings.items():
        if 'hard_mode' in k and v:
            t1 += '%s,' % "H"
        if 'easy_mode' in k and v:
            t1 += '%s,' % "E"
        if 'balanced_games' in k and v:
            t1 += '%s,' % "B"
        if 'multi_goals' in k and v:
            t1 += '%s,' % "M"
            
    t1 = t1[0:-1]
    url += "%s&seed=%s" % (t1, seed)
    
    return url


@application.route("/custom",  methods=['GET', 'POST'])
def custom():
    if request.method=='POST':
        form = CustomForm()
        
        indices = []
        for i in form._fields:
            i2 = str(form._fields[i].data)
            if i2 == '':
                i2 = '0'
            indices.append(i2)



        
        settings_str = 'BOARD,%s,Seed Number: Null, Settings: Null' % ','.join(indices)
        custom_settings = {'data' : settings_str}
        
        #
        # {'data': 'BOARD,605,315,404,812,130,382,64,519,161,32,66,511,627,354,778,61,785,757,65,622,297,562,571,515,756,
        # Seed Number: 782762547 | Settings: MM1, 2, 3, 4, 5, 6, Balanced'} 
        #
        
        data_header, goals, settings_str = generate_popout(custom_settings)
         
        return render_template('bingo_popout.html', data_header = data_header, goals = goals, settings_str = settings_str)

    

    ## GET
    else: 
        
        passed_settings = dict(request.args)
        
        form = CustomForm()
        
        if passed_settings:
            if "data" not in passed_settings.keys() or len(passed_settings.keys()) > 1:
                return None
        
            
            if "data" in passed_settings.keys():
                passed_settings = passed_settings['data']
            else:
                passed_settings = None
            
            goals = generate_df_for_custom(passed_settings)
    
    
            # breakpoint()
            
            for idx, i in enumerate(goals):
                
                form._fields['form_choice%s' % str(int(idx) + 1)].default = i[0]
                form.process()
                # form._fields['form_choice%s' % str(int(idx) + 1)].data = newd
                    
                            
            

        return render_template('custom.html', form = form)




@application.route("/faq", methods=['GET'])
def faq():

    logging.info("FAQ")
    
    df = pd.read_csv('latest_faq.csv')
    rules = list(df['goal'])    
    

    
    return render_template('faq.html', rules = rules)
    

@application.route("/password", methods=['GET'])
def password():

    logging.info("Password")
    
    df = pd.read_csv('latest_data.csv')
    images = sorted([i for i in df['img'].unique() if '-pw' in str(i) and "," not in str(i) or "3+4" in str(i)])
    
    

    
    return render_template('password.html', images= images)
    

@application.route("/bingo-popout", methods=['GET'])
def popout():

    logging.info("Popout")
    
    passed_settings = dict(request.args)
    

    
    if "data" not in passed_settings.keys() or len(passed_settings.keys()) > 1:
        return None
    

    data_header, goals, settings_str = generate_popout(passed_settings)
    
    logging.info("\n\n")
    for i in goals:
        logging.info(i)
    logging.info("\n\n")
    
    return render_template('bingo_popout.html', data_header = data_header, goals = goals, settings_str = settings_str)
    


@application.route("/", methods=['GET', 'POST'])
def index():
    
    try:
        
        settings = {}
        error_message = None
        # try to parse any arguments
        try:
            # logging.info("\n\n%s" % request.args) 
            passed_settings = dict(request.args)
            
            if 'settings' in passed_settings.keys() and 'seed' in passed_settings.keys():
                # attempt to parse both
                x = passed_settings['settings'].split(",")
                
                settings = { 'games' :{'mm1' : False,
                            'mm2' : False,
                            'mm3' : False,
                            'mm4' : False,
                            'mm5' : False,
                            'mm6' : False
                            },
                            'hard_mode' : False,
                            'easy_mode' : False,
                            'balanced_games':True,
                            'multi_goals':True}
                
                if "H" in x and "E" in x:
                    passed_settings_flag = False
                else:
                    for i in x:
                        if i == 'H':
                            settings['hard_mode'] = True
                        elif i == 'E':
                            settings['easy_mode'] = True
                        elif i == 'B':
                            settings['balanced_games'] = True
                        elif i == 'M':
                            settings['multi_goals'] = True
                        else:
                            new = 'mm%s' % i
                            settings['games'][new] = True
                        

                passed_settings_flag = True
            else:
                passed_settings_flag = False
        except:
            logging.info("Could not parse any request.args")
            passed_settings = {}
            passed_settings_flag = False
        
        
        logging.info(passed_settings)
        
            

        if request.method=='POST' or passed_settings_flag:
            form = MainForm()
            
            settings_check = [i for i in list(passed_settings.keys()) if i not in ['settings','seed']]
            if settings_check:
                error_message = 'Error on generation. Do not pass in foreign arguments'
                return None
            
            if passed_settings:
                for k, v in settings['games'].items():
                    form._fields['form_%s' % k].data = v

                for k, v in settings.items():
                    if "hard_mode" in k:
                        form._fields['form_hard_mode'].data = v
                    if "easy_mode" in k:
                        form._fields['form_easy_mode'].data = v
                    if "balanced_games" in k:
                        form._fields['form_balanced_games'].data = v
                    if "multi_goals" in k:
                        form._fields['form_multi_goals'].data = v
            
            form.validate_on_submit()
            
            
            if "form_seed" in form.errors.keys():
                print(form.errors)
                ### RETURN NULL
                
                error_message = 'Error on generation. Try choosing a different combination of settings'
                return minify(render_template('index.html', goals = None, settings = None, seed_number = None, form=form, url = None, error_message = error_message))
            
            ########### GENERATE CARD ###########
            
            if 'seed' in passed_settings.keys():
                seed = int(passed_settings['seed'])
                
            
            elif form.form_seed.data:
                seed = form.form_seed.data 
            else:
                seed = None
            if not settings:
                settings = { 'games' : {'mm1' : form.form_mm1.data,
                                'mm2' : form.form_mm2.data,
                                'mm3' : form.form_mm3.data,
                                'mm4' : form.form_mm4.data,
                                'mm5' : form.form_mm5.data,
                                'mm6' : form.form_mm6.data
                            },
                            'hard_mode' : form.form_hard_mode.data,
                            'easy_mode' : form.form_easy_mode.data,
                            'balanced_games' : form.form_balanced_games.data,
                            'multi_goals' : form.form_multi_goals.data}
                
                
                if form.form_hard_mode.data and form.form_easy_mode.data:
                    
                    ### RETURN NULL
                    error_message = 'Cannot select both Easy and Hard mode'
                    return (render_template('index.html', goals = None, settings = None, seed_number = None,form=MainForm(), url = None, error_message = error_message))
                    
            logging.error("SEED NUM: %s\nSETTINGS: %s" % (seed,settings))
            
            df, error_message, seed = generate_card(seed, settings)
            if df.empty:
                logging.info("No dataframe was returned")
                if error_message:
                    logging.info(error_message)
            else:
                goals = list(df['goal'].unique())
    
                
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
                
                

                logging.info("\n\n")
                for i in goals:
                    logging.info(i)
                logging.info("\n\n")

    
            form.form_seed.data = seed
    
            settings_string = get_settings_string(form)

            url = get_url(settings, seed)
            
    
            return render_template('index.html', goals = goals,settings = settings_string,  seed_number = seed, form=form, url=url)
        else:
            ### RETURN NULL
            return (render_template('index.html', goals = None, settings = None, seed_number = None,form=MainForm(), url = None, error_message = error_message))
    except:
        traceback.print_exc()
        error_message = 'Error on generation. Try choosing a different combination of settings'
        return (render_template('index.html', goals = None, settings = None, seed_number = None,form=MainForm(), url = None, error_message = error_message))
if __name__ == '__main__':
    
    
    df = pd.read_csv("latest_data.csv")
    img = [i for i in df['img'].unique() if i == i]
    
    for i in img:
        if not os.path.exists(os.path.join('static','img',i)) and "\n" not in i and "," not in i:
            print("Missing %s" % i)
    # application.run()
    # application.run(debug=True)