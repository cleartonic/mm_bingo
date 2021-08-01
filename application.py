from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, BooleanField, IntegerField
from htmlmin import minify
from bingo import generate_card

import datetime
import logging
import traceback
import os

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



class MainForm(FlaskForm):
    form_mm1 =  BooleanField(label='MM1:',default=True)
    form_mm2 =  BooleanField(label='MM2:',default=True)
    form_mm3 =  BooleanField(label='MM3:',default=True)
    form_mm4 =  BooleanField(label='MM4:',default=True)
    form_mm5 =  BooleanField(label='MM5:',default=True)
    form_mm6 =  BooleanField(label='MM6:',default=True) 
    form_seed = IntegerField(label='Seed number (integer):', validators = [validators.Optional(), validators.NumberRange(min=1,max=999999999, message="Must be integer")])


def get_settings_string(form):
    output_str = ''
    
    if form.form_mm1.data:
        output_str += "MM1, "
    if form.form_mm2.data:
        output_str += "MM2, "
    if form.form_mm3.data:
        output_str += "MM3, "
    if form.form_mm4.data:
        output_str += "MM4, "
    if form.form_mm5.data:
        output_str += "MM5, "
    if form.form_mm6.data:
        output_str += "MM6, "
    
    return output_str[:-2]

@application.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method=='POST':
        form = MainForm()
        form.validate_on_submit()
        
        if "form_seed" in form.errors.keys():
            print(form.errors)
            return minify(render_template('index.html', goals = None, settings = None, seed_number = None, form=form))
        
        ########### GENERATE CARD ###########
        
        if form.form_seed.data:
            seed = form.form_seed.data 
        else:
            seed = None
            
        settings = {'mm1' : form.form_mm1.data,
                    'mm2' : form.form_mm2.data,
                    'mm3' : form.form_mm3.data,
                    'mm4' : form.form_mm4.data,
                    'mm5' : form.form_mm5.data,
                    'mm6' : form.form_mm6.data}
            
        logging.error("SEED NUM: %s\nSETTINGS: %s" % (seed,settings))
        
        df, error_message, seed = generate_card(seed, settings)
        if df.empty:
            logging.info("No dataframe was returned")
            if error_message:
                logging.info(error_message)
        else:
            goals = list(df['goal'].unique())

            
            goalsd = df[['goal','notes', 'rank', 'games']].T.to_dict()
            goals = []
            for k, v in goalsd.items():
                notes = v['notes']
                if notes != notes:
                    notes = ''
                    
                goals.append([v['goal'],notes, v['rank'], v['games']])
            

        form.form_seed.data = seed

        settings_string = get_settings_string(form)

        return render_template('index.html', goals = goals,settings = settings_string,  seed_number = seed, form=form)
    else:
        return (render_template('index.html', goals = None, settings = None, seed_number = None,form=MainForm()))
if __name__ == '__main__':
    application.run()
    # application.run(debug=True)