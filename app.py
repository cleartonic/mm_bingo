from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, BooleanField, IntegerField
from htmlmin import minify
from bingo import generate_card, generate_popout


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

    form_mm1 =  BooleanField(label='MM1:',default=True)
    form_mm2 =  BooleanField(label='MM2:',default=True)
    form_mm3 =  BooleanField(label='MM3:',default=True)
    form_mm4 =  BooleanField(label='MM4:',default=True)
    form_mm5 =  BooleanField(label='MM5:',default=True)
    form_mm6 =  BooleanField(label='MM6:',default=True) 
    form_hard_mode =  BooleanField(label='Hard Mode:',default=False) 
    form_easy_mode =  BooleanField(label='Easy Mode:',default=False) 
    # else:
    #     form_mm1 =  BooleanField(label='MM1:',default=passed_settings['mm1'])
    #     form_mm2 =  BooleanField(label='MM2:',default=passed_settings['mm2'])
    #     form_mm3 =  BooleanField(label='MM3:',default=passed_settings['mm3'])
    #     form_mm4 =  BooleanField(label='MM4:',default=passed_settings['mm4'])
    #     form_mm5 =  BooleanField(label='MM5:',default=passed_settings['mm5'])
    #     form_mm6 =  BooleanField(label='MM6:',default=passed_settings['mm6'])     
    form_seed = IntegerField(label='Seed number (integer):', validators = [validators.Optional(), validators.NumberRange(min=1,max=999999999, message="Must be integer")])


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
    
    return output_str[:-2]

def get_url(settings, seed): 
    url = '?'
    
    t1 = 'settings='
    for k, v in settings.items():
        if 'mm' in k and v:
            t1 += '%s,' % k.split("mm")[1]
        if 'hard_mode' in k and v:
            t1 += '%s,' % "H"
        if 'easy_mode' in k and v:
            t1 += '%s,' % "E"
            
    t1 = t1[0:-1]
    url += "%s&seed=%s" % (t1, seed)
    
    return url

@application.route("/faq", methods=['GET'])
def faq():

    logging.info("FAQ")
    
    df = pd.read_csv('latest_faq.csv')
    rules = list(df['goal'])    

    
    return render_template('faq.html', rules = rules)
    

@application.route("/bingo-popout", methods=['GET'])
def popout():

    logging.info("Popout")
    
    passed_settings = dict(request.args)
    

    
    if "data" not in passed_settings.keys() or len(passed_settings.keys()) > 1:
        return None
    
    data_header, goals, settings_str = generate_popout(passed_settings)
    
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
                
                settings = {'mm1' : False,
                            'mm2' : False,
                            'mm3' : False,
                            'mm4' : False,
                            'mm5' : False,
                            'mm6' : False,
                            'hard_mode' : False,
                            'easy_mode' : False}
                
                if "H" in x and "E" in x:
                    passed_settings_flag = False
                else:
                    
                    for i in x:
                        if i == 'H':
                            settings['hard_mode'] = True
                        elif i == 'E':
                            settings['easy_mode'] = True
                        else:
                            new = 'mm%s' % i
                            settings[new] = True
                        

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
                for k, v in settings.items():
                    if "mm" in k:
                        form._fields['form_%s' % k].data = v
                    if "hard_mode" in k:
                        form._fields['form_hard_mode'].data = v
                    if "easy_mode" in k:
                        form._fields['form_easy_mode'].data = v
            
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
                settings = {'mm1' : form.form_mm1.data,
                            'mm2' : form.form_mm2.data,
                            'mm3' : form.form_mm3.data,
                            'mm4' : form.form_mm4.data,
                            'mm5' : form.form_mm5.data,
                            'mm6' : form.form_mm6.data,
                            'hard_mode' : form.form_hard_mode.data,
                            'easy_mode' : form.form_easy_mode.data}
                
                
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
    
                
                goalsd = df[['goal','notes', 'rank', 'games','pw']].T.to_dict()
                goals = []
                for k, v in goalsd.items():
                    notes = v['notes']
                    if notes != notes:
                        notes = ''
                    if v['pw']:
                        notes = '%s\n(password allowed)' % notes
                        
                    goals.append([v['goal'],notes, v['rank'], v['games'], v['pw'], k])
                
    
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
    application.run()
    # application.run(debug=True)