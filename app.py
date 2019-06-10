from flask import Flask, render_template, request, session, redirect, url_for, session
from flask_wtf import FlaskForm
import requests
import json
import io
from io import BytesIO
from flask import send_file
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import recommender
#from StringIO import StringIO
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired


app = Flask(__name__)

# Configure a secret SECRET_KEY
app.config['SECRET_KEY'] = 'mysecretkey'


class InfoForm(FlaskForm):
    #User defined sticker and date
    eyecolor = RadioField('Please choose your eye color', choices=[('0','green'),('1','blue'),('2','hazel'),('2','brown'),('4','N/A')])
    haircolor = RadioField('Please choose your hair color', choices=[('0','red'),('1','brunette'),('2','blonde'),('4','black'),\
                            ('5','auburn'),('6','gray'),('3','N/A')])
    skintone = RadioField('Please choose your skintone', choices=[('0','fair'),('1','light'),('2','olive'),('3','meduim'),('4','tan'),\
                            ('5','porcelain'),('6','deep'),('7','dark'),('8','ebony'),('9','N/A')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = InfoForm()

    # If the form is valid on submission
    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        session['eyecolor'] = form.eyecolor.data
        session['haircolor'] = form.haircolor.data
        session['skintone'] = form.skintone.data

        #Month adjust
        demo_code = session['eyecolor']+session['haircolor']+session['skintone']
        recom_output = recommender.get_recommender(demo_code)
        brand_names = recom_output.brand_names.values.tolist()
        product_names = recom_output.product_names.values.tolist()
        links2 = recom_output.links2.values.tolist()
        avg_scores = recom_output.avg_score.values.tolist()
        imgs = recom_output.img.values.tolist()
        hot_shades = recom_output.hot_shade.values.tolist()

        #recom_output['product_names'] = recom_output['product_names'].apply(lambda x: '<a href="https://www.sephora.com/product/mattemoiselle-10-10-P19117864?icid2=products%20grid:p19117864:product">link</a>'.format(x))
        #raw_html = recom_output.to_html(classes='data',index=False)
        #raw_html.replace('<tr>', '<tr align="center">')
        #return render_template('about.html',  tables=[raw_html], titles=recom_output.columns.values)
        return render_template('grid_info.html',  brand_names=brand_names,product_names=product_names,avg_scores=avg_scores,\
                                links2=links2,imgs=imgs,hot_shades=hot_shades)

    return render_template('index.html', form=form)

#def html_table():

if __name__ == '__main__':
    app.run(debug=True)
