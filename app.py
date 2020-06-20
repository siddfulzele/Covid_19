import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import time

from flask import *

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


#Load Data
def ld():
	print("\n")
	#National Level :Time series, State-wise stats and Test counts
	res_NL = requests.get("https://api.covid19india.org/data.json")
	call_NL = res_NL.json()
	ld.nl_ts = pd.DataFrame(call_NL['cases_time_series'])
	ld.nl_tc = pd.DataFrame(call_NL['tested'])
	ld.nl_sw = pd.DataFrame(call_NL['statewise'])

	#State Level : Daily changes
	res_SD = requests.get("https://api.covid19india.org/states_daily.json")
	call_SD = res_SD.json()
	ld.sd_data = pd.DataFrame(call_SD['states_daily'])

	#LOADING RAW DATA
	'''
	Raw data 1 Data till EoD Apr 19th
	Raw data 2 Data till EoD Apr 26th
	Raw data 3 Data till EoD May 9th
	Raw data 4 Data Live
	'''
	ld.raw_data = pd.DataFrame()
	for i in range(1,7):
	    res_data = requests.get("https://api.covid19india.org/raw_data"+str(i)+".json")
	    call_data = res_data.json()
	    nl_data = pd.DataFrame(call_data['raw_data'])    
	    ld.raw_data = ld.raw_data.append(nl_data)


	print("Data Load Successfully")

def plot():
	ld()
	## Daily Cases ##
	plot.dc_fig = go.Figure()
	plot.dc_fig.add_trace(
	    go.Bar(x = ld.nl_ts.date , y = ld.nl_ts.dailyconfirmed , name = 'Confirmed')
	)
	plot.dc_fig.add_trace(
	    go.Bar(x = ld.nl_ts.date , y = ld.nl_ts.dailydeceased , name = 'Deceased')
	)
	plot.dc_fig.add_trace(
	    go.Bar(x = ld.nl_ts.date , y = ld.nl_ts.dailyrecovered , name = 'Recovered')
	)
	plot.dc_fig.update_layout(
	    xaxis_title="Date",
	    yaxis_title="Count",
	    paper_bgcolor='rgba(0,0,0,0)',
	    plot_bgcolor='rgba(0,0,0,0)',
	    margin=dict(l=20, r=20, t=20, b=20),
	    font=dict(
	        family="Times New Roman",
	        size=18,
	    )
	)
	plot.dc_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e6e6e6')
	plot.dc_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e6e6e6')


	## Total Cases ##
	plot.tc_fig = go.Figure()
	plot.tc_fig.add_trace(
	    go.Scatter(x = ld.nl_ts.date , y = ld.nl_ts.totalconfirmed , name = 'Confirmed')
	)
	plot.tc_fig.add_trace(
	    go.Scatter(x = ld.nl_ts.date , y = ld.nl_ts.totaldeceased , name = 'Deceased')
	)
	plot.tc_fig.add_trace(
	    go.Scatter(x = ld.nl_ts.date , y = ld.nl_ts.totalrecovered , name = 'Recovered')
	)
	plot.tc_fig.update_layout(
	    xaxis_title="Date",
	    yaxis_title="Count",
	    paper_bgcolor='rgba(0,0,0,0)',
	    plot_bgcolor='rgba(0,0,0,0)',
	    margin=dict(l=20, r=20, t=20, b=20),
	    font=dict(
	        family="Times New Roman",
	        size=18,
	    )
	)
	plot.tc_fig.add_shape(
	    dict(
	        type="line",
	        x0='22 March ',
	        y0=0,
	        x1='22 March ',
	        y1=250000,        
	        line=dict(
	            color="black",
	            width=2
	        )
	))
	plot.tc_fig.add_annotation(
	            x='22 March ',
	            y=250000,
	            text="Phase 1")
	plot.tc_fig.add_shape(
	    dict(
	        type="line",
	        x0='15 April ',
	        y0=0,
	        x1='15 April ',
	        y1=250000,        
	        line=dict(
	            color="black",
	            width=2
	        )
	))
	plot.tc_fig.add_annotation(
	            x='15 April ',
	            y=250000,
	            text="Phase 2")
	plot.tc_fig.add_shape(
	    dict(
	        type="line",
	        x0='04 May ',
	        y0=0,
	        x1='04 May ',
	        y1=250000,        
	        line=dict(
	            color="black",
	            width=2
	        )
	))
	plot.tc_fig.add_annotation(
	            x='04 May ',
	            y=250000,
	            text="Phase 3")
	plot.tc_fig.add_shape(
	    dict(
	        type="line",
	        x0='18 May ',
	        y0=0,
	        x1='18 May ',
	        y1=250000,        
	        line=dict(
	            color="black",
	            width=2
	        )
	))
	plot.tc_fig.add_annotation(
	            x='18 May ',
	            y=250000,
	            text="Phase 4")
	plot.tc_fig.add_shape(
	    dict(
	        type="line",
	        x0='01 June ',
	        y0=0,
	        x1='01 June ',
	        y1=250000,        
	        line=dict(
	            color="black",
	            width=2
	        )
	))
	plot.tc_fig.add_annotation(
	            x='01 June ',
	            y=250000,
	            text="Phase 5")
	plot.tc_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e6e6e6')
	plot.tc_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e6e6e6')

	#MORTALITY RATE
	plot.count = ld.nl_ts.tail(1).iloc[0]		
	ta = int(plot.count['totalconfirmed']) - (int(plot.count['totaldeceased']) + int(plot.count["totalrecovered"]))
	plot.count = plot.count.append(pd.Series({"totalActive" : ta}))

	plot.mc_fig = go.Figure(go.Pie(
	    values = [plot.count.totalrecovered,plot.count.totaldeceased,plot.count.totalActive],
	    labels = ['Recovered','Death','Active'],
	    textposition = "inside",
	    pull=[0, 0.2, 0])
	)

	plot.mc_fig.update_traces(
	    marker=dict(colors=['LightGreen','FireBrick','DeepSkyBlue'])
	)

	plot.mc_fig.update_layout(
		paper_bgcolor='rgba(0,0,0,0)',
	    height = 500,
	    margin=dict(l=20, r=20, t=20, b=20),
	    font=dict(
	        family="Courier New, monospace",
	        size=22,
	    )
	)

	## State Wise Comparison
	ld.nl_sw = ld.nl_sw.drop([0])

	plot.sw_fig = go.Figure()
	plot.sw_fig.add_trace(
	    go.Bar(x = ld.nl_sw.statecode , y = ld.nl_sw.confirmed , name = 'Confirmed')
	)
	plot.sw_fig.add_trace(
	    go.Bar(x = ld.nl_sw.statecode , y = ld.nl_sw.deaths , name = 'Deceased')
	)
	plot.sw_fig.add_trace(
	    go.Bar(x = ld.nl_sw.statecode , y = ld.nl_sw.recovered , name = 'Recovered')
	)
	plot.sw_fig.update_layout(
	    xaxis_title="State Code",
	    margin=dict(l=20, r=20, t=20, b=20),
	    paper_bgcolor='rgba(0,0,0,0)',
	    plot_bgcolor='rgba(0,0,0,0)',
	    yaxis_title="Count",
	    font=dict(
	        family="Courier New, monospace",
	        size=22,
	    )
	)
	plot.sw_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e6e6e6')
	plot.sw_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e6e6e6')


	## State wise Daily Count

	sd_data_c = ld.sd_data[ld.sd_data.status == "Confirmed"]
	sd_data_c = sd_data_c.drop(['status','tt'],axis=1)
	y = sd_data_c.iloc[:,7].tolist()
	sd_data_c = sd_data_c.drop('date',axis=1)
	x = list(sd_data_c)
	z = sd_data_c.values

	plot.swdc_fig = go.Figure(go.Surface(
	    contours = {
	        "x": {"show": True, "start": 1.5, "end": 2, "size": 0.04, "color":"white"},
	        "z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.05}
	    },
	    x = x,
	    y = y,
	    z = z))
	plot.swdc_fig.update_layout(
			paper_bgcolor='rgba(0,0,0,0)',
			height = 600,
	        scene = {
	            "xaxis": {"nticks": 20},
	            "zaxis": {"nticks": 4},
	            'camera_eye': {"x": 0, "y": -1, "z": 0.5},
	            "aspectratio": {"x": 1, "y": 1, "z": 0.2}
	        },
	        margin=dict(l=20, r=20, t=20, b=20),
	        font=dict(
	            family="Courier New, monospace",
	            size=14,
	        )
	)

	##Age Comparison
	age =  ld.raw_data.agebracket[ld.raw_data.agebracket != ""]
	age = age[age != '28-35'] #UNWANTED DATA
	age = age[age != '0'] #UNWANTED DATA
	age = age[age != '6 Months'] #UNWANTED DATA
	age = age[age != '6 MONTHS'] #UNWANTED DATA
	age = age[age != '8 Months'] #UNWANTED DATA
	age = age[age != '3 months'] #UNWANTED DATA
	age = age.astype(float) #COVERT VALUES TO FLOAT
	age_data = pd.DataFrame()
	age_data['Age'] = age
	bins = [x for x in range(0,101,10)]
	g_labels = ['0-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91-100']
	age_data['group'] = pd.cut(age,bins,labels=g_labels)
	age_data = age_data[age_data.Age != 0]
	plt_age = age_data.Age.groupby(age_data.group).count()
	plot.age_smp_size = age_data.Age.count()

	plot.age_fig = go.Figure()
	plot.age_fig.add_trace(
	    go.Bar(x=plt_age.index, y = plt_age, name = 'Age')
	)
	plot.age_fig.update_layout(	    		
	    paper_bgcolor='rgba(0,0,0,0)',
	    plot_bgcolor='rgba(0,0,0,0)',
	    margin=dict(l=20, r=20, t=20, b=20),
	    xaxis_title="Age",
	    yaxis_title="Cases",
	    font=dict(
	        family="Courier New, monospace",
	        size=14,
	    )
	)
	

	#Gender
	gen = ld.raw_data[['gender']]
	gen = gen[gen != '']
	gen = gen[gen != 'NA']
	gen = gen.groupby(['gender']).size().reset_index(name='counts')
	plot.gen_smp_size = str(gen.counts.sum())
	plot.gen_fig = go.Figure(go.Pie(
	    values = gen.counts,
	    labels = ['Females','Males'],
	    texttemplate = "%{label}: %{value} <br>(%{percent})",
	    textposition = "inside",
	    pull=[0, 0])
	)

	plot.gen_fig.update_traces(
	    marker=dict(colors=['LightGreen','FireBrick','DeepSkyBlue'])
	)

	plot.gen_fig.update_layout(	
	    paper_bgcolor='rgba(0,0,0,0)',
	    plot_bgcolor='rgba(0,0,0,0)',
	    margin=dict(l=20, r=20, t=20, b=20),
	    height = 400,        
	    font=dict(
	        family="Courier New, monospace",
	        size=18,
	    )
	)

	#Death Rate
	ld.nl_sw['death_rate'] = ld.nl_sw['deaths'].astype(int) / ld.nl_sw['confirmed'].astype(int)
	ld.nl_sw['death_rate'] = ld.nl_sw['death_rate'] * 100
	ld.nl_sw = ld.nl_sw.sort_values('death_rate', ascending=False)
	plot.dr_fig = go.Figure()
	plot.dr_fig.add_trace(
	    go.Bar(x=ld.nl_sw.statecode, y = ld.nl_sw.death_rate, name = 'Death Rate')
	)
	plot.dr_fig.update_layout(
	    xaxis_title="State",
	    yaxis_title="Death Rate",
	    paper_bgcolor='rgba(0,0,0,0)',
	    plot_bgcolor='rgba(0,0,0,0)',
	    margin=dict(l=20, r=20, t=20, b=20),
	    font=dict(
	        family="Courier New, monospace",
	        size=14,
	    )
	)

	#Recovery Rate
	ld.nl_sw['recovery_rate'] = ld.nl_sw['recovered'].astype(int) / ld.nl_sw['confirmed'].astype(int)
	plot.rr_fig = px.bar(ld.nl_sw.sort_values('recovery_rate', ascending=False), x="statecode", y="recovery_rate")
	plot.rr_fig.update_layout(
	    xaxis_title="State",
	    yaxis_title="Recovery Rate",
	    paper_bgcolor='rgba(0,0,0,0)',
	    plot_bgcolor='rgba(0,0,0,0)',
	    margin=dict(l=20, r=20, t=20, b=20),
	    font=dict(
	        family="Courier New, monospace",
	        size=14,
	    )
	)

	print("All Graphs ploted Successfully")

plot()





######### DASH CODE ##########

server = Flask(__name__)

@server.route('/')
def Home():	
	return render_template("index.html")

@server.route('/index')
def index():	
	return render_template("index.html")

@server.route('/report')
def report():	
	return render_template("report.html")


@server.route('/covid_India',methods=['GET'])
def dashbord():
	return redirect("/covid_India")

app = dash.Dash(__name__,server = server,routes_pathname_prefix='/covid_India/' ,external_stylesheets =[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
	

	html.Div([
			html.H1(children ="Coronavirus disease (COVID-19) Pandemic ",style = {'color':'black','padding':'0px', 'margin':'0px','font-size':'35px'}),
			html.H1(children ="India",style = {'color':'#ffffff','padding':'0px', 'margin':'0px','font-size':'50px','font-weight': 'bold'})
	],className = "jumbotron text-center", style={'padding':'50px','background':'#99ccff','margin':'0px'}),

	
	dbc.Navbar([		
		html.A([
			dbc.Button("Home",color="primary",className="ml-12")
			],href="/index",style={"margin":"0 0 0 40%"}),
		html.A([
			dbc.Button("Dashbord",color="primary",className="ml-12")
			],href="/covid_India/",style={"margin":"0px 10px"}),
		html.A([
			dbc.Button("Report",color="primary",className="ml-12")
			],href="/report")				
	],color="dark",dark=True,sticky="top"),

	html.Div([
		html.H5(children="Last Updated : "+plot.count.date,style={'color':'#666666','font-weight': 'bold','margin':'10px'},className="text-center col-md-12"),
				html.Div([
			## Count
			html.Div([
					html.H1(children="Counts",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					html.Div([
						html.Div([
							html.H4(children="Deceased",style={'font-weight':'bold'}),
							html.H2(children=plot.count.totaldeceased,style={'font-weight':'bold'})
						],className='col-md-4 text-center',style={'background':'#FFE0E6','color':'#E23028','border':'3px solid #f1f2ff','border-radius':'15px','padding':'15px'}),
						html.Div([
							html.H4(children="Active",style={'font-weight':'bold'}),
							html.H2(children=plot.count.totalActive,style={'font-weight':'bold'})
						],className='col-md-4 text-center',style={'background':'#b3d9ff','color':'#007BFF','border':'3px solid #f1f2ff','border-radius':'15px','padding':'15px'}),
						html.Div([
							html.H4(children="Recovered",style={'font-weight':'bold'}),
							html.H2(children=plot.count.totalrecovered,style={'font-weight':'bold'})
						],className='col-md-4 text-center',style={'background':'#E4F4E8','color':'#28A745','border':'3px solid #f1f2ff','border-radius':'15px','padding':'15px'})
					],className='row',style={'margin':'80px 0px 40px 0px'}),
					html.Div([
						html.Div(className='col-md-3'),
						html.Div([
								html.H4(children="Confirmed",style={'font-weight':'bold'}),
								html.H2(children=plot.count.totalconfirmed,style={'font-weight':'bold'})
						],className='col-md-6 text-center',style={'background':'#B22222','color':'#f2f2f2','border':'3px solid #f1f2ff','border-radius':'15px','padding':'15px 25px'}),
						html.Div(className='col-md-3')
					],className='row')
			],className="col-md-6",style={'margin':'0px'}),
			## Mortality
			html.Div([
				html.H1(children="Percentage Rate ",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					dcc.Graph(id='MC', figure=plot.mc_fig),
					dcc.Loading( type="default")
			],className="col-md-6",style={'margin':'0px'})
		],className="row",style={'margin':'50px 0px'}),

		html.Div([
			## total Cases
			html.Div([
					html.H1(children="Total Cases",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					dcc.Graph(id='TC', figure=plot.tc_fig)
			],className="col-md-12",style={'margin':'0px'})
		],className="row"),

		html.Div([
			## daily Cases
			html.Div([
				html.H1(children="Daily Cases",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					dcc.Graph(id='DC', figure=plot.dc_fig)
			],className="col-md-12",style={'margin':'0px'})
		],className="row"),

		html.Div([
			## Age Comparison
			html.Div([
					html.H1(children="Age Comparison",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					html.H4(children="Sample Size : "+str(plot.age_smp_size),style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					dcc.Graph(id='Age', figure=plot.age_fig)
			],className="col-md-6",style={'margin':'0px'}),
			## patient Gender Cases
			html.Div([
				html.H1(children="Patient Gender",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
				html.H4(children="Sample Size : "+str(plot.gen_smp_size),style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					dcc.Graph(id='Gen', figure=plot.gen_fig)
			],className="col-md-6",style={'margin':'0px'})
		],className="row",style={'margin':'50px 0px'}),

		html.Div([
			html.Div([
				html.H1(children="State Comparison - Cumulative",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					dcc.Graph(id='SW', figure=plot.sw_fig)
			],className="",style={'margin':'80px 50px'})
		]),

		html.Div([
			## Death Rate
			html.Div([
					html.H1(children="Death Rate",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),					
					dcc.Graph(id='Dr', figure=plot.dr_fig)
			],className="col-md-6",style={'margin':'0px'}),

			#Recovery Rate
			html.Div([
					html.H1(children="Recovery Rate",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),					
					dcc.Graph(id='rr', figure=plot.rr_fig)
			],className="col-md-6",style={'margin':'0px'})
		],className="row",style={'margin':'50px 0px'}),

		html.Div([
			html.Div([
				html.H1(children="State wise Daily Count",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					dcc.Graph(id='SWDC', figure=plot.swdc_fig)
			],className="",style={'margin':'80px 50px'})
		]),

		dbc.Row([
			## GDP INDIA
			dbc.Col([
					html.H1(children="GDP India",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),
					html.H4(children="Year - 2019",style={'color':'#666666','font-weight': 'bold','margin':'0px 0px 10px 0px'},className="text-center"),
					html.Img(src="https://raw.githubusercontent.com/siddfulzele/Covid_19/master/GDP.png", className="img-responsive img-thumbnail")
			],className="col-md-4 col-xs-6",style={'margin':'0px','padding':'1px'}),

			## Confirm INDIA
			dbc.Col([
					html.H1(children="Confirm Cases",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),					
					html.H4(children="Till 5th June 2020",style={'color':'#666666','font-weight': 'bold','margin':'0px 0px 10px 0px'},className="text-center"),
					html.Img(src="https://raw.githubusercontent.com/siddfulzele/Covid_19/master/covid_confirmed.png", className="img-responsive img-thumbnail")
			],className="col-md-4 col-xs-6",style={'margin':'0px','padding':'1px'}),

			#urban Population
			dbc.Col([
					html.H2(children="Urban Population",style={'color':'#666666','font-weight': 'bold','margin':'0px'},className="text-center"),					
					html.H4(children="Data from Census 2011",style={'color':'#666666','font-weight': 'bold','margin':'0px 0px 8px 0px'},className="text-center"),
					html.Img(src="https://raw.githubusercontent.com/siddfulzele/Covid_19/master/urban_population.png", className="img-responsive img-thumbnail")
			],className="col-md-4 col-xs-6",style={'margin':'0px','padding':'1px'})
		],className="row",style={'margin':'50px 0px'})

	],style={'width':'98%','margin':'1%'}),

	html.Div([
		html.Div([
			html.Div([
				html.H5(children='Source : https://www.covid19india.org',style={'margin':'30px 0 0 0'}),
				html.H5(children='https://www.wikipedia.org/',style={'margin':'0px 0 0 75px'}),
				html.H5(children='https://twitter.com/',style={'margin':'0px 0 0 75px'})
			],className='col-md-4'),

			html.Div([
			],className='col-md-4'),

			html.Div([
				html.H5(children='Analysis Team : '),
				html.H5(children='Siddhant Fulzele',style={'margin':'0 0 0 50px'}),
				html.H5(children='Shubham Rajput',style={'margin':'0 0 0 50px'}),
				html.H5(children='Akash Kundu',style={'margin':'0 0 0 50px'}),
				html.H5(children='Tejas Akadkar',style={'margin':'0 0 0 50px'}),
				html.H5(children='Akshay Kale',style={'margin':'0 0 0 50px'})
			],className='col-md-4'),
		],className='row',style={'margin':'0px'})
	],className='jumbotron',style={'background':'#99ccff','bottom':'0','margin':'0px','padding':'10px'})

	

],style={'margin':'0px','background':'#f1f1f1'})

if __name__ == "__main__":
	app.run_server(debug=True)
