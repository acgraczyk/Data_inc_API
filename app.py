from flask import Flask, render_template, request, redirect
import json
import requests
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from bokeh.plotting import figure, output_file, show, save 
from bokeh.models.formatters import DatetimeTickFormatter
import math
from bokeh.models import HoverTool 
from bokeh.embed import json_item, components
from bokeh.resources import CDN
from jinja2 import Template



app = Flask(__name__)


page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-2.0.2.min.css" type="text/css" />
  <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-2.0.2.min.js"></script>
</head>

<body>
<p>The daily {{ dat }} price for {{ sym }} : </p>
  <div id="myplot"></div>
  <script>
  fetch('/test')
    .then(function(response) { return response.json(); })
    .then(function(item) { return Bokeh.embed.embed_item(item); })
  </script>
  
</body>
""")



app.vars={}

@app.route('/', methods=['GET','POST'])
def intro():
  if request.method=='GET':
    
    return render_template('intro_a.html',ans1='Open Value', ans2='Closing Value',ans3='Lowest Value',ans4='Highest Value')
    
  else:
   
   app.vars['sym']=request.form['symbol']
   app.vars['dat']=request.form['dat']
   
   
   fig = graph_test()

   script, div  = components(fig)

   return render_template('display.html', sym=app.vars['sym'], dat=app.vars['dat'], script=script, div=div)
  # return page.render(resources=CDN.render(), sym=app.vars['sym'], dat=app.vars['dat'])




@app.route('/test')
def graph_test():
    sym = app.vars['sym']
    sym.upper()
    dat = app.vars['dat']
    api_key = '2WO8P8MYSVYSE8LO'

    ts = TimeSeries(api_key, output_format='pandas')
    sym_data, sym_meta_data = ts.get_daily(symbol=sym)
    
    sym_data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    #output_file('tmp/moog.html', mode="inline")
    if dat == 'Closing':
      p = figure(tools="pan,box_zoom,reset,save", title="Stock Daily Closing Prices" , x_axis_label='Time', y_axis_label="Daily Closing Prices" )   
      p.line(x='date',y='Close', source=sym_data, legend_label=sym,line_width=2)
      hover = HoverTool(
    tooltips = [
        ("Date", "@date{%Y-%m-%d}"),
        ("Value", "@Close")
        ],
    formatters={
        '@date': 'datetime',
        '@Close' : 'printf',},)    

      p.add_tools(hover)        

    

    elif dat == 'Open':
      p = figure(tools="pan,box_zoom,reset,save", title="Stock Daily Open Prices" , x_axis_label='Time', y_axis_label="Daily Open Prices" )   
      p.line(x='date',y='Open', source=sym_data, legend_label=sym,line_width=2)

      hover = HoverTool(
    tooltips = [
        ("Date", "@date{%Y-%m-%d}"),
        ("Value", "@Open")
        ],
    formatters={
        '@date': 'datetime',
        '@Open' : 'printf',},)    

      p.add_tools(hover)   

    elif dat == 'Lowest':
      p = figure(tools="pan,box_zoom,reset,save", title="Stock Daily Low Prices" , x_axis_label='Time', y_axis_label="Daily Low Prices" )   
      p.line(x='date',y='Low', source=sym_data, legend_label=sym,line_width=2) 

      hover = HoverTool(
    tooltips = [
        ("Date", "@date{%Y-%m-%d}"),
        ("Value", "@Low")
        ],
    formatters={
        '@date': 'datetime',
        '@Low' : 'printf',},)    

      p.add_tools(hover)   

    else:
      p = figure(tools="pan,box_zoom,reset,save", title="Stock Daily High Prices" , x_axis_label='Time', y_axis_label="Daily High Prices" )   
      p.line(x='date',y='High', source=sym_data, legend_label=sym,line_width=2) 

      hover = HoverTool(
    tooltips = [
        ("Date", "@date{%Y-%m-%d}"),
        ("Value", "@High")
        ],
    formatters={
        '@date': 'datetime',
        '@High' : 'printf',},)    

      p.add_tools(hover)   


    p.xaxis.formatter=DatetimeTickFormatter(
    microseconds = ['%Y-%m-%d %H:%M:%S.%f'],
    milliseconds = ['%Y-%m-%d %H:%M:%S.%3N'],
    seconds = ["%Y-%m-%d %H:%M:%S"],
    minsec = ["%Y-%m-%d %H:%M:%S"],
    minutes = ["%Y-%m-%d %H:%M:%S"],
    hourmin = ["%Y-%m-%d %H:%M:%S"],
    hours=["%Y-%m-%d %H:%M:%S"],
    days=["%Y-%m-%d %H:%M:%S"],
    months=["%Y-%m-%d %H:%M:%S"],
    years=["%Y-%m-%d %H:%M:%S"],
    )


    
    p.xaxis.major_label_orientation = math.pi/2
    #save(p)
    return p
    #return json.dumps(json_item(p, "myplot"))


@app.errorhandler(500)
def error_500(error):
  return render_template('error_handle.html')

@app.errorhandler(404)
def error_400(error):
  return render_template('error_handle.html')

@app.errorhandler(400)
def error_404(error):
  return render_template('error_handle.html')
  

if __name__ == '__main__':
  app.run(port=33507)
