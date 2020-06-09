from flask import Flask, render_template, request
import requests
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from bokeh.plotting import figure, output_file, show 
from bokeh.models.formatters import DatetimeTickFormatter
import math
from bokeh.models import HoverTool 



app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def intro():
  if request.method=='GET':
    
    return render_template('intro_a.html',ans1='Open Value', ans2='Closing Value',ans3='Lowest Value',ans4='Highest Value')
    
  else:
   
   sym=request.form['symbol']
   dat=request.form['dat']
   
   graph_test(sym,dat)
   

   return render_template('display_a.html',symbol=sym, dat_type=dat)




@app.route('/test')
def graph_test(sym,dat):
    api_key = '2WO8P8MYSVYSE8LO'
    ts = TimeSeries(api_key, output_format='pandas')
    sym_data, sym_meta_data = ts.get_daily(symbol=sym)
    
    sym_data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']


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
    
    return show(p)




if __name__ == '__main__':
  app.run(port=33507)
