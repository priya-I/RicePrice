import os
from flask import Flask, request, render_template, redirect, url_for, flash, Blueprint,make_response,session
import sqlite3
import traceback
import csv 
import predict as p

current_dir=os.getcwd()
STATIC_FOLDER=current_dir+'/static/images/'
TEMPLATE_DIR=current_dir+'/templates/'
app=Flask(__name__)
app.config['static_folder']=STATIC_FOLDER
app.config['template_folder']=TEMPLATE_DIR
app.config.from_object(__name__)

@app.route('/')
def main():
    '''
    Method called to render the landing page
    '''
    return render_template("prices.html")

@app.route('/plot',methods=["POST","GET"])
def plot():
    '''
    Main method that plots the charts based on the input parameters
    '''
    if request.method == "POST" and request.form is not None:
        types=[]
        #Get the parameters passed on from the request form
        options=request.form
        for k,v in options.items():
            #Extract the year parameter from the page
            if(k=='year'):
                year=v
            else:
                #Extract the categories from the input checkboxes
                types.append(k)
        #Calling the method that creates charts based on types of rice and year
        imgpath=p.create_plots(types,year)
    return render_template("prices.html",imgpath=imgpath)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__=="__main__":
    app.debug=True
    app.run(port=8000)

