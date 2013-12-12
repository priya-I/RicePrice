import os
from flask import Flask, request, render_template, redirect, url_for, flash, Blueprint,make_response,session
import sqlite3
import traceback
from werkzeug import secure_filename
import csv 
import predict as p



ALLOWED_EXTENSIONS=set(['csv'])
current_dir=os.getcwd()
STATIC_FOLDER=current_dir+'/static/images/'
TEMPLATE_DIR=current_dir+'/templates/'
app=Flask(__name__)
app.config['static_folder']=STATIC_FOLDER
app.config['template_folder']=TEMPLATE_DIR
app.config.from_object(__name__)


@app.route('/')
def main():
    return render_template("prices.html")

@app.route('/plot',methods=["POST","GET"])
def plot():
    if request.method == "POST" and request.form is not None:
        types=[]
        options=request.form
        for k,v in options.items():
            if(k=='year'):
                year=v
            else:
                types.append(k)
        print types,year
        imgpath=p.create_plots(types,year)
        #im=Image.open(imgdata)
        #imgpath="."+imgpath
        print imgpath
    return render_template("prices.html",imgpath=imgpath)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS



if __name__=="__main__":
    app.debug=True
    app.run(port=8000)

