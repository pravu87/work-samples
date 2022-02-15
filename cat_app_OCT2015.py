"""
This file demonstrates a bokeh applet, which can either be viewed
directly on a bokeh-server, or embedded into a flask application.
See the README.md file in this directory for instructions on running.
"""

import logging

logging.basicConfig(level=logging.DEBUG)

from os import listdir
from os.path import dirname, join, splitext

import numpy as np
import pandas as pd

from bokeh.models import CustomJS,ColumnDataSource, Plot
from bokeh.plotting import figure, curdoc
from bokeh.properties import String, Instance, Int,List
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, VBox, VBoxForm, PreText, Select
from bokeh.models.widgets import CheckboxGroup,RadioGroup,CheckboxButtonGroup
from bokeh.models.glyphs import Circle,Line,ImageURL,Image


#==================================================================
from bokeh.models import Callback,Slider
from bokeh.models.widgets import Slider, VBox, Tabs, Panel
from bokeh.models.glyphs import Rect

from bokeh.models import (
    GMapPlot, Range1d, ColumnDataSource, LinearAxis,
    PanTool, WheelZoomTool, BoxSelectTool,
    BoxSelectionOverlay, GMapOptions,
    NumeralTickFormatter, PrintfTickFormatter)


from bokeh.models import (
    GMapPlot, Range1d, ColumnDataSource, LinearAxis,
    PanTool, WheelZoomTool, BoxSelectTool,HoverTool,ResetTool,
    BoxSelectionOverlay, GMapOptions,ResizeTool,
    BoxZoomTool,NumeralTickFormatter, PrintfTickFormatter)
#==================================================================
from bokeh.charts import Bar, output_file, show,Scatter
#from bokeh._legacy_charts import Bar, output_file, show,Scatter
from bokeh.models.renderers import GlyphRenderer
from bokeh.models.widgets import CheckboxGroup,RadioGroup

from bokeh.simpleapp import simpleapp
import time
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib._png import read_png
import bokeh.plotting as bp
from bokeh.plotting import figure, curdoc,vplot, hplot, cursession, output_server, show
from chart_constants import PLOT_FORMATS
from bokeh.models import Text, Triangle, Rect
from chart_constants import FONT_PROPS_SM, FONT_PROPS_MD, FONT_PROPS_LG, ORANGE, ORANGE_SHADOW


#from chart_constants import PLOT_FORMATS


# build up list of stock data in the daily folder
data_dir = join(dirname(__file__), "daily")
try:
    tickers = listdir(data_dir)
except OSError as e:
    print(' data not available, see README for download instructions.')
    raise e
tickers = [splitext(x)[0].split("table_")[-1] for x in tickers]

# cache stock data as dict of pandas DataFrames
#pd_cache = {}


def get_ticker_data(ticker):
    fname = join(data_dir, "table_%s.csv" % ticker.lower())
    data = pd.read_csv(
        fname,
        names=['date', 'foo', 'o', 'h', 'l', 'c', 'v'],
        header=False,
        parse_dates=['date']
    )
    data = data.set_index('date')
    data = pd.DataFrame({ticker: data.c, ticker + "_returns": data.c.diff()})
    return data



def get_data(ticker1, ticker2):
    if pd_cache.get((ticker1, ticker2)) is not None:
        return pd_cache.get((ticker1, ticker2))

    # only append columns if it is the same ticker
    if ticker1 != ticker2:
        print (" @get data: if not")
        data1 = get_ticker_data(ticker1)
        data2 = get_ticker_data(ticker2)
        data = pd.concat([data1, data2], axis=1)
    else:

        print (" @get data: else")
        data = get_ticker_data(ticker1)

    data = data.dropna()
    pd_cache[(ticker1, ticker2)] = data
    return data







data_dir_machine = join(dirname(__file__), "machine_daily")

try:
    tickers = listdir(data_dir_machine)
except OSError as e:
    print('machine data not available, see README for download instructions.')
    raise e





tickers = [splitext(x)[0] for x in tickers]




# cache data as dict of pandas DataFrames
pd_cache = {}
pd_cache1 = {}

def get_ticker_data1(ticker,ticker_slider_day):
    day=int(ticker_slider_day)
    ticker_file=ticker+"_"+"%s" % day
    file_d=r"C:\\Users\\tumulp\\Desktop\\Tai_Bokeh_Sample\\machine_daily"
    data_dir=file_d
    fname = join(data_dir, "%s.csv" % ticker_file) #.lower()
    data = pd.read_csv(
        fname,
        header=False,
        parse_dates=['Timestamp']
    )

    data = data.set_index('Timestamp')
    data = pd.DataFrame({ticker: data["Actual Engine RPM"], ticker + "_mile": data["cumsum_mile"],
                     ticker + "_latitude": data["GPGGA Latitude"], ticker + "_longitude": data["GPGGA Longitude"]})#,
    return data



def get_data1(ticker1, ticker2,ticker_slider_day):
    print ("==get_data1==")
    if pd_cache.get((ticker1, ticker2,ticker_slider_day)) is not None:
        return pd_cache.get((ticker1, ticker2,ticker_slider_day))

    # only append columns if it is the same ticker
    if ticker1 != ticker2:
        data1 = get_ticker_data1(ticker1,ticker_slider_day)
        data2 = get_ticker_data1(ticker2,ticker_slider_day)
        data = data1.join(data2, how='outer')
    else:

        data = get_ticker_data(ticker1,ticker_slider_day)

    data = data.dropna()
    pd_cache[(ticker1, ticker2,ticker_slider_day)] = data
    return data





def get_data_summary(ticker_slider_day):
    day=int(ticker_slider_day)
    ticker_file="AT_"+"%s" % day + "_summary_all"
    file_d=r"C:\\Users\\tumulp\\Desktop\\Tai_Bokeh_Sample\\machine_daily\\"
    data_dir=file_d
    fname = join(data_dir, "%s.csv" % ticker_file) #.lower()
    data = pd.read_csv(
        fname,
        header=0
    )
    pd_cache1[(ticker_slider_day)] = data


    return data

def get_data_summary_cum(ticker_slider_day):
    if pd_cache1.get((ticker_slider_day)) is not None:
        return pd_cache1.get((ticker_slider_day))
    day=int(ticker_slider_day)
    ticker_file="AT_"+"%s" % day + "_summary_all"
    file_d=r"C:\\Users\\tumulp\\Desktop\\Tai_Bokeh_Sample\\machine_daily"
    data_dir=file_d
    fname = join(data_dir, "%s.csv" % ticker_file) #.lower()
    data = pd.read_csv(
        fname,
        header=False
    )
    pd_cache1[(ticker_slider_day)] = data
    return data


def get_ticker_dumping_data(ticker,ticker_slider_day,active_at=None):
    day=int(ticker_slider_day)
    ticker_file=ticker+"_"+"%s" % day   #AT6_8
    file_d=r"C:\\Users\\tumulp\\Desktop\\Tai_Bokeh_Sample\\machine_daily"
    data_dir=file_d
    fname = join(data_dir, "%s.csv" % ticker_file) #.lower()
    try:
        data = pd.read_csv(
            fname,
            header=0,
            #parse_dates=['Timestamp']
        )
        data_up=data.loc[data['bodyup']==1].copy()
        data_up_only=data_up[["BodyUpCat","GPGGA Latitude_1","GPGGA Longitude_1","mile_cycle","Delta"]].copy()
        data_up_only=data_up_only.dropna()
        data_up_only_travel=data_up_only[data_up_only["BodyUpCat"].str.contains("BodyUpTravel")]
    except:
        data=None
        data_up_only_travel=None
        pass
    return data_up_only_travel


def get_ticker_loading_data(ticker,ticker_slider_day,active_at=None):
    day=int(ticker_slider_day)
    ticker_file=ticker+"_"+"%s" % day   #AT6_8
    file_d=r"C:\\Users\\tumulp\\Desktop\\Tai_Bokeh_Sample\\machine_daily"
    data_dir=file_d
    fname = join(data_dir, "%s.csv" % ticker_file) #.lower()
    data = pd.read_csv(
        fname,
        header=False,
        #parse_dates=['Timestamp']
    )
    data_dwn=data.loc[data['Loading']==1].copy()
    data_dwn_only=data_dwn[["GPGGA Latitude","GPGGA Longitude","Delta_cumsumMile","Delta_loading","BodyDwnLoadCat"]].copy()
    data_dwn_only=data_dwn_only.dropna(subset=['BodyDwnLoadCat'], how='all')
    data_dwn_only_travel=data_dwn_only[data_dwn_only["BodyDwnLoadCat"].str.contains("BodyDwnLoadTravel")]
    return data_dwn_only_travel



class CatApp(VBox):
    extra_generated_classes = [["CatApp", "CatApp", "VBox"]]
    jsmodel = "VBox"
    pretext = Instance(PreText)

    # plots
    plot = Instance(GMapPlot)# GMap
    image_plot = Instance(Plot)
    image_plot_adv = Instance(Plot)
    hist1 = Instance(Plot)
    hist2 = Instance(Plot)

    # data source
    source  = Instance(ColumnDataSource)
    source1 = List(Instance(ColumnDataSource)) #Instance(ColumnDataSource)
    source2 = List(Instance(ColumnDataSource)) #Instance(ColumnDataSource)

    # layout boxes
    mainrow = Instance(HBox)
    image_row = Instance(HBox)
    #image_row_adv = Instance(HBox)
    histrow = Instance(HBox)
    histrow1 = Instance(HBox)
    #statsbox = Instance(VBox)

    # inputs
    ticker1 = String(default="AT1")
    ticker2 = String(default="AT2")
    ticker_slider_day = Int(default=1)

    ticker_job_site= String(default="Houston SH99")

    ticker1_select  = Instance(Select)
    ticker2_select  = Instance(Select)
    ticker3_select  = Instance(CheckboxGroup)
    ticker4_select  = Instance(CheckboxButtonGroup)

    slider_1        = Instance(Slider)
    select_job_site = Instance(Select)

    input_box = Instance(VBoxForm)

    def __init__(self, *args, **kwargs):
        super(CatApp, self).__init__(*args, **kwargs)
        self._dfs = {}

    @classmethod
    def create(cls):
        """
        This function is called once, and is responsible for
        creating all objects (plots, datasources, etc)
        """
        # create layout widgets
        obj = cls()
        obj.mainrow = HBox()
        obj.histrow = HBox()
        obj.histrow1 = HBox()
        obj.image_row = HBox()
        #obj.image_row_adv =HBox()
        obj.input_box = VBoxForm()

        # create input widgets
        obj.make_inputs()

        # outputs
        obj.pretext = PreText(text=" Daily Information ", width=900,height=70)
        obj.make_source()
        obj.make_source1()
        obj.make_source2()
        obj.construct_text_box()
        #obj.make_plots()
        obj.create_map()
        obj.create_image_plot()
        #obj.create_image_plot_adv()
        obj.hist_plots()
        obj.hist_plots1()
        obj.make_stats()

        # layout
        obj.set_children()
        return obj

    def make_inputs(self):

        self.select_job_site = Select(
        name='ticker_job_site',
         value='Houston SH99', options=['Houston SH99', 'Gallatin TN', 'Peoria PG, IL'])

        self.ticker1_select = Select(
            name='ticker1',
            value='AT1',
            options=['AT1', 'AT2', 'AT3','AT4','AT5','AT6','AT7']
        )
        self.ticker2_select = Select(
            name='ticker2',
            value='AT2',
            options=['AT1', 'AT2', 'AT3','AT4','AT5','AT6','AT7']
        )


        self.ticker3_select = CheckboxGroup(
            name='ticker3',
            labels=['AT1', 'AT2', 'AT3','AT4','AT5','AT6','AT7','ALL'],
            active=[0,1,2,3,4,5,6]
        )

        self.slider_1 = Slider(
            name='ticker_slider_day',
            start=1, end=8, value=1, step=1, title="\n Day")

        self.ticker4_select = CheckboxButtonGroup(
            name='ticker4',
            labels=['Load', 'Dump', 'Path'],
            active=[1]
        )



    @property
    def selected_df(self):
        pandas_df = self.df1
        selected = self.source.selected['1d']['indices']
        if selected:
            pandas_df = pandas_df.iloc[selected, :]
        print pandas_df.head(2)
        return pandas_df

    def make_source(self):
        trucks = ['AT1', 'AT2', 'AT3','AT4','AT5','AT6','AT7'] #self.df1.AT.values.tolist()
        cycles = [20, 20, 20,20,20,20,20] #self.df1['number_of_cycles'].astype(float).values
        self.source = ColumnDataSource(
                data=dict(
                    x=trucks,
                    y=cycles,

                )
            )

    def make_source1(self):
        self.source1 = self.df

    def make_source2(self):
        self.source2 = self.df  #self.df_loading

    def create_image_plot(self):
        ticker_slider_day=self.ticker_slider_day
        ticker_job_site=self.ticker_job_site
        active_at=self.ticker3_select.active
        ticker_job_site= "Houston SH99"
        #==========Dummy JobSite Longitude and Latitude================#
        if ticker_job_site == "Houston SH99":
            Job_Site_1_lat=30.052343
            Job_Site_1_lng=-95.642177
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]
        if ticker_job_site == "JobSite2":
            Job_Site_1_lat=30.2861
            Job_Site_1_lng=-97.7394
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]
        if ticker_job_site == "JobSite3":
            Job_Site_1_lat=40.74118
            Job_Site_1_lng=-89.484877
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]


        x_range=Range1d()
        y_range=Range1d()


        #========Dummy Loading and Dumping Zones=====================#
        source_map = ColumnDataSource(
            data=dict(
                lat=[30.055, 30.064, 30.042], #lat_list,  #
                lon=[-95.675, -95.640, -95.610], #longt_list,  #
                #bodyup=BodyUp_list,

                fill=['orange', 'blue', 'green']
            )
        )

        #=============================================================

        #arr_hand = read_png("C://ESDC SVN//trunk//spatial_visualization//houston_jobsite.png")
        #imagebox = OffsetImage(arr_hand, zoom=1)
        map_options = GMapOptions(lat=Job_Site_loc[0], lng=Job_Site_loc[1], map_type="satellite", zoom=14)
        plot = GMapPlot(
            x_range=x_range, y_range=y_range,
            map_options=map_options,
            title ="HOUSTON SH99",  # ticker_job_site,  #"HOUSTON SS99",
            plot_width=1200,
            plot_height=400,
           # **PLOT_FORMATS
        )
        colormap=["#a6cee3","#1f78b4","#fdbf6f","#b2df8a","#33a02c","#bbbb88","#baa2a6","#e08e79"]*10
        for x in range(0,len(active_at)-1): #active_at:
            print ("x is:", x)
            circle = Circle(x="lon", y="lat", size=10, fill_color=colormap[x],line_color=colormap[x]) #fill_color="fill",
            plot.add_glyph( self.source1[x], circle)

        hover = HoverTool()
        #hover = plot.select(dict(type=HoverTool))
        hover.tooltips = [("Order ", " $index"),("Truck ", " @model"),("Brand ", " @cat")]
        hover.mode = 'mouse'

        pan = PanTool()
        wheel_zoom = WheelZoomTool()
        box_zoom = BoxZoomTool()
        #hover = HoverTool()
        resize = ResizeTool()
        reset = ResetTool()

        plot.add_tools(pan,wheel_zoom, box_zoom,hover,resize,reset)
        #plot.add_tools(hover)
        self.image_plot=plot
        return plot


    def create_image_plot_def(self):
        url ="https://www.rcfl.gov/images/houston-map-zoom.png"  #"C://ESDC SVN//trunk//spatial_visualization//houston_jobsite.png" ##"http://alternative-schools.org/ElliotHallmark/wp-content/uploads/2014/05/austin_zoning.html"   #r ####"https://www.rcfl.gov/images/houston-map-zoom.png"# ###### "http://bokeh.pydata.org/en/latest/_static/bokeh-transparent.png" #["C://ESDC SVN//trunk//spatial_visualization//houston_jobsite.png"]
        N = 1
        print (url)
        source_map2 = ColumnDataSource(dict(
            url = [url],
            x1  = np.linspace(  0, 150, N),
            y1  = np.linspace(  0, 150, N),
            w1  = np.linspace( 10,  50, N),
            h1  = np.linspace( 10,  50, N),
            x2  = np.linspace(-50, 150, N),
            y2  = np.linspace(  0, 200, N),
        ))

        xdr = Range1d(start=-600, end=600)
        ydr = Range1d(start=-50, end=50)

        plot2 = Plot(
            title=None, x_range=xdr, y_range=ydr, plot_width=1100, plot_height=400,
            h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location=None)

        image3 = ImageURL(url="url", x=0, y=0, anchor="center")
        plot2.add_glyph(source_map2, image3)


        pan = PanTool()
        wheel_zoom = WheelZoomTool()
        box_zoom = BoxZoomTool()
        #hover = HoverTool()
        resize = ResizeTool()
        reset = ResetTool()
        plot2.add_tools(pan,wheel_zoom, box_zoom,resize,reset)
        self.image_plot=plot2
        return plot2
    def create_map(self):

        ticker1 = self.ticker1
        ticker2 = self.ticker2
        ticker_slider_day=self.ticker_slider_day
        ticker_job_site=self.ticker_job_site
        active_at=self.ticker3_select.active
        #==========Dummy JobSite Longitude and Latitude================#
        if ticker_job_site == "Houston SH99":
            print "job site"
            Job_Site_1_lat=30.052343
            Job_Site_1_lng=-95.642177
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]
            map_options = GMapOptions(lat=Job_Site_loc[0], lng=Job_Site_loc[1], map_type="satellite", zoom=14)
        if ticker_job_site == "JobSite2":
            Job_Site_1_lat=30.2861
            Job_Site_1_lng=-97.7394
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]
            map_options = GMapOptions(lat=Job_Site_loc[0], lng=Job_Site_loc[1], map_type="satellite", zoom=14)
        if ticker_job_site == "JobSite3":
            Job_Site_1_lat=40.74118
            Job_Site_1_lng=-89.484877
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]
            map_options = GMapOptions(lat=Job_Site_loc[0], lng=Job_Site_loc[1], map_type="satellite", zoom=14)

        x_range=Range1d()
        y_range=Range1d()

        #plot=None
        plot = GMapPlot(
            x_range=x_range, y_range=y_range,
            map_options=map_options,
            title = ticker_job_site,  #"HOUSTON SS99",
            plot_width=1200,
            plot_height=400,
           # **PLOT_FORMATS
        )
        #plot.map_options.map_type="satellite"
        hover = HoverTool()
        #hover = plot.select(dict(type=HoverTool))
        hover.tooltips = [("Cycle# ", " $index"),("Truck ", " @model")] #        #hover = HoverTool()
        hover.mode = 'mouse'

        pan = PanTool()
        wheel_zoom = WheelZoomTool()
        box_zoom = BoxZoomTool()
        #hover = HoverTool()
        resize = ResizeTool()
        reset = ResetTool()
        #box_select = BoxSelectTool()

        plot.add_tools(pan,wheel_zoom, box_zoom,hover,resize,reset)

        xaxis = LinearAxis(axis_label="lat", major_tick_in=0, formatter=NumeralTickFormatter(format="0.000"))
        plot.add_layout(xaxis, 'below')

        yaxis = LinearAxis(axis_label="lon", major_tick_in=0, formatter=PrintfTickFormatter(format="%.3f"))
        plot.add_layout(yaxis, 'left')

        self.plot = plot
        return plot


    def create_map_def(self):

        ticker1 = self.ticker1
        ticker2 = self.ticker2
        ticker_slider_day=self.ticker_slider_day
        ticker_job_site=self.ticker_job_site
        active_at=self.ticker3_select.active
        try:
            df = get_ticker_dumping_data(ticker1,ticker_slider_day)
            ticker_day=ticker1+"_"+str(ticker_slider_day)
            source_at_day = ColumnDataSource(
            data=dict(lat=df['GPGGA Latitude_1'],
            lon=df['GPGGA Longitude_1'],
            order=range(1,df.shape[0]+1),
            model=[ticker1]*(df.shape[0]+1),
            cat=['CAT']*(df.shape[0]+1),
             )
            )

        except:
            pass
        #==========Dummy JobSite Longitude and Latitude================#
        if ticker_job_site == "Houston SH99":
            Job_Site_1_lat=30.052343
            Job_Site_1_lng=-95.642177
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]
        if ticker_job_site == "JobSite2":
            Job_Site_1_lat=30.2861
            Job_Site_1_lng=-97.7394
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]
        if ticker_job_site == "JobSite3":
            Job_Site_1_lat=40.74118
            Job_Site_1_lng=-89.484877
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]


        map_options = GMapOptions(lat=Job_Site_loc[0], lng=Job_Site_loc[1], map_type="satellite", zoom=14)

        #map_options = GMapOptions(lat=Job_Site_loc[0], lng=Job_Site_loc[1], map_type="roadmap", zoom=14) #,, zoom=14

        #x_range=None
        #y_range=None
        x_range=Range1d()
        y_range=Range1d()

        #plot=None
        plot = GMapPlot(
            x_range=x_range, y_range=y_range,
            map_options=map_options,
            title = ticker_job_site,  #"HOUSTON SS99",
            plot_width=900,
            plot_height=400,

        )
        plot.map_options.map_type="satellite"
        #time.sleep(3)
        try:
            for x in active_at:
                circle = Circle(x="lon", y="lat", size=4, line_color="green") #fill_color="fill",
                plot.add_glyph( source_at_day, circle)
        except:
            pass
        self.plot = plot
        hover = HoverTool()
        #hover = plot.select(dict(type=HoverTool))
        hover.tooltips = [("Cycle# ", " $index"),("Truck ", " @model")] #        #hover = HoverTool()
        hover.mode = 'mouse'

        pan = PanTool()
        wheel_zoom = WheelZoomTool()
        box_zoom = BoxZoomTool()
        #hover = HoverTool()
        resize = ResizeTool()
        reset = ResetTool()
        #box_select = BoxSelectTool()

        plot.add_tools(pan,wheel_zoom, box_zoom,hover,resize,reset)
        #plot.tools.append(hover)

        #self.hist_plots()
        self.plot = plot
        xaxis = LinearAxis(axis_label="lat", major_tick_in=0, formatter=NumeralTickFormatter(format="0.000"))
        plot.add_layout(xaxis, 'below')

        yaxis = LinearAxis(axis_label="lon", major_tick_in=0, formatter=PrintfTickFormatter(format="%.3f"))
        plot.add_layout(yaxis, 'left')

        self.plot = plot
        self.plot = plot
        print ("@ create_map=======assign new plot")
        print
        #self.hist_plots()
        return plot

    def create_map_def2(self):

        ticker1 = self.ticker1
        ticker2 = self.ticker2
        ticker_slider_day=self.ticker_slider_day
        ticker_job_site=self.ticker_job_site
        active_at=self.ticker3_select.active
        print ("*****************")
        print ("@ create_map")
        print ("*****************")
        print (ticker1)
        print (ticker2)
        print (ticker_slider_day)
        print (ticker_job_site)
        print (" active_at checked is: ",active_at)
        colormap_class = {
            "alkali metal"         : "#a6cee3",
            "alkaline earth metal" : "#1f78b4",
            "halogen"              : "#fdbf6f",
            "metal"                : "#b2df8a",
            "metalloid"            : "#33a02c",
            "noble gas"            : "#bbbb88",
            "nonmetal"             : "#baa2a6",
            "transition metal"     : "#e08e79",
        }

        colormap=["#a6cee3","#1f78b4","#fdbf6f","#b2df8a","#33a02c","#bbbb88","#baa2a6","#e08e79"]
        sources_all = [] #ColumnDataSource(data=dict(lat=[], lon=[],order=[], model=[], cat=[]))
        for x in active_at:
                ticker1_new="AT"+str(x+1)
                try:
                    df = get_ticker_dumping_data(ticker1_new,ticker_slider_day)
                    ticker_day=ticker1_new+"_"+str(ticker_slider_day)
                    source_at_day = ColumnDataSource(
                    data=dict(lat=df['GPGGA Latitude_1'],
                    lon=df['GPGGA Longitude_1'],
                    order=range(1,df.shape[0]+1),
                    model=[ticker1_new]*(df.shape[0]+1),
                    cat=['CAT']*(df.shape[0]+1),
                     )
                    )
                except:
                    pass
                sources_all.append(source_at_day)
            #except:
               # pass
        time.sleep(1)
        #==========Dummy JobSite Longitude and Latitude================#
        if ticker_job_site == "Houston SH99":
            Job_Site_1_lat=30.052343
            Job_Site_1_lng=-95.642177
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]
        if ticker_job_site == "JobSite2":
            Job_Site_1_lat=30.2861
            Job_Site_1_lng=-97.7394
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]
        if ticker_job_site == "JobSite3":
            Job_Site_1_lat=40.74118
            Job_Site_1_lng=-89.484877
            Job_Site_loc=[Job_Site_1_lat,Job_Site_1_lng]


        map_options = GMapOptions(lat=Job_Site_loc[0], lng=Job_Site_loc[1], map_type="satellite", zoom=14)
        x_range=Range1d()
        y_range=Range1d()

        #plot=None
        plot = GMapPlot(
            x_range=x_range, y_range=y_range,
            map_options=map_options,
            title = ticker_job_site,  #"HOUSTON SS99",
            plot_width=900,
            plot_height=400,

        )
        plot.map_options.map_type="satellite"

        for x in active_at:
            circle = Circle(x="lon", y="lat", size=4, line_color=colormap[x]) #fill_color="fill",
            plot.add_glyph( sources_all[x], circle)

        self.plot = plot
        hover = HoverTool()
        #hover = plot.select(dict(type=HoverTool))
        hover.tooltips = [("Cycle# ", " $index"),("Truck ", " @model")] #        #hover = HoverTool()
        hover.mode = 'mouse'

        pan = PanTool()
        wheel_zoom = WheelZoomTool()
        box_zoom = BoxZoomTool()
        #hover = HoverTool()
        resize = ResizeTool()
        reset = ResetTool()
        #box_select = BoxSelectTool()

        plot.add_tools(pan,wheel_zoom, box_zoom,hover,resize,reset)
        #plot.tools.append(hover)

        #self.hist_plots()
        self.plot = plot
        xaxis = LinearAxis(axis_label="lat", major_tick_in=0, formatter=NumeralTickFormatter(format="0.000"))
        plot.add_layout(xaxis, 'below')

        yaxis = LinearAxis(axis_label="lon", major_tick_in=0, formatter=PrintfTickFormatter(format="%.3f"))
        plot.add_layout(yaxis, 'left')
        self.plot = plot
        self.plot = plot
        #overlay = BoxSelectionOverlay(tool=box_select)
        #plot.add_layout(overlay)

        self.plot = plot
        self.plot = plot
        return plot



    def hist_plots(self):
        ticker1 = self.ticker1
        ticker2 = self.ticker2
        ticker_slider_day=self.ticker_slider_day
        self.hist1 = self.bar_plot(ticker_slider_day)
        #self.hist2 = self.hist_plot(ticker2)

    def hist_plots1(self):
        ticker1 = self.ticker1
        ticker2 = self.ticker2
        ticker_slider_day=self.ticker_slider_day
        self.hist2 = self.bar_plot2(ticker_slider_day)


    def construct_text_box(self):
        xdr = Range1d(0, 220)
        ydr = Range1d(0, 120)

        ticker_slider_day=self.ticker_slider_day
        df_summary1 = get_data_summary(ticker_slider_day)
        data1 = df_summary1.sort("AT", ascending=True)

        TOOLS="pan,wheel_zoom,box_zoom,reset,hover"
        trucks = data1.AT.values.tolist()
        cycles = np.array(data1['number_of_cycles'].astype(float).values).tolist()
        count=0
        for x in range(0, len(cycles)):
            if cycles[x]==0.0 :
                count+=1
        percent_val=float(((len(cycles)-count)/float(len(cycles))*100))
        percent_val1=np.round(percent_val,1)

        plot = Plot(
            x_range=xdr,
            y_range=ydr,
            title="",
            plot_width=900,
            plot_height=120,
            min_border=1,
            **PLOT_FORMATS
        )
        # Add the writing
        ticker_slider_day=self.ticker_slider_day #at_day=['20150623','20150624','20150625','20150626','20150707','20150708','20150709','20150710']
        date=["June 23, Tue","June 24, Wed","June 25, Thur","June 26, Fri","July 7, Mon","July 8, Tue","July 9, Wed","July 10, Thur"]

        str_date_temp=date[ticker_slider_day-1]
        str_date=str_date_temp + ", "+ "2015"
        value_string="value color"
        color_string="color color"

        #for a in range(0, len(0,len(self.daily_cycles)))

        country = Text(x=5, y=50, text='name', **FONT_PROPS_MD)
        percent = Text(x=60, y=13, text=[str(percent_val1)],  **FONT_PROPS_LG)  # nopep8
        percent_sign = Text(x=75, y=13, text=['%'],  **FONT_PROPS_LG)  # nopep8
        line_one = Text(x=85, y=28, text=['of Articulated Trucks'], **FONT_PROPS_MD)
        line_two_p1 = Text(x=90, y=14, text=['were in operation'], **FONT_PROPS_MD)
        #line_two_p2 = Text(x=136, y=14, text=['2010'], **FONT_PROPS_SM)
        #plot.add_glyph(source, Text(), selection_glyph=country)
        plot.add_glyph(percent)
        plot.add_glyph(percent_sign)
        plot.add_glyph(line_one)
        plot.add_glyph(line_two_p1)

        # Add the orange box with year
        shadow = Triangle(x=150, y=109, size=35, fill_color=ORANGE_SHADOW, line_color=None)  # nopep8
        plot.add_glyph(shadow)
        # Add the blue bar
        rect = Rect(x=75, y=99, width=150, height=5, fill_color="#a6cee3", line_color=None)  # nopep8
        plot.add_glyph(rect)
        box = Rect(x=200, y=100, width=100, height=40, fill_color=ORANGE, line_color=None)  # nopep8
        plot.add_glyph(box)
        year = Text(x=160, y=85, text=[str_date], text_font_size='18pt', text_color="black", text_font_style="bold")  # nopep8
        #plot.add_glyph(source, Text(), selection_glyph=year)
        plot.add_glyph(year)
        return plot


    def set_children(self):

        water_text = self.construct_text_box()


        tabs = Tabs(
            tabs=[
                Panel(
                    title="Daily",
                    child=hplot(vplot(vplot(water_text),self.hist1))
                ),
                Panel(
                    title="Weekly",
                    child=hplot(vplot(self.hist2))
                )
            ]
        )



        #self.pretext.color="red"
        self.children = [self.mainrow, self.histrow,self.image_row] #,self.image_row_adv
        #self.mainrow.children = [self.input_box, self.hist1]
        self.mainrow.children = [self.input_box, tabs]
        #self.mainrow.children = [self.input_box]
        self.input_box.children = [self.ticker2_select, self.ticker1_select, self.ticker3_select,self.slider_1,self.select_job_site, self.ticker4_select]
        self.image_row.children = [self.image_plot]
        #self.image_row_adv.children = [self.image_plot_adv]
        self.histrow.children = [self.plot]
        #self.statsbox.children = [self.pretext]


    def bar_plot(self,ticker_slider_day):
        df_summary1 = get_data_summary(ticker_slider_day)
        data1 = df_summary1.sort("AT", ascending=True)

        TOOLS="pan,wheel_zoom,box_zoom,reset,hover"
        trucks = data1.AT.values.tolist()
        cycles = data1['number_of_cycles'].astype(float).values
        #bar = Bar(cycles, trucks,  title="Total Cycles per AT ",stacked=True, width=900, height=300,tools=TOOLS)
        bar = Bar(data1, label="AT", values="number_of_cycles", title="Total Cycles per AT ")
        glyph_renderers = bar.select(dict(type=GlyphRenderer))
        bar_source = glyph_renderers[0].data_source
        bar._yaxis.minor_tick_out
        hover = bar.select(dict(type=HoverTool))
        hover.tooltips = [
            # ("position ", " $index"),
            ("Truck ", "  @cat"),
             ('Total Cycles ', '  @zero'),
        ]

        return bar

    def bar_plot2(self,ticker_slider_day):

        df_summary1 = get_data_summary(ticker_slider_day)
        data1 = df_summary1.sort("AT", ascending=True)

        TOOLS="pan,wheel_zoom,box_zoom,reset,hover"
        trucks = data1.AT.values.tolist()
        cycles = data1['number_of_cycles'].astype(float).values
        #print ("here")
        #bar = Bar(cycles, trucks,  title="Total Cycles per AT ",stacked=True, width=900, height=400,tools=TOOLS)
        bar = Bar(data1, label="AT", values="number_of_cycles", title="Total Cycles per AT ")        
        glyph_renderers = bar.select(dict(type=GlyphRenderer))
        bar_source = glyph_renderers[0].data_source

        hover = bar.select(dict(type=HoverTool))
        #print ("here 2")
        hover.tooltips = [
             #("position ", " $index"),
            ("Truck ", "  @cat"),
             ('Total Cycles ', '  @zero'),
        ]

        return bar


    def checkbox_group_handler(self,active):
        self.make_source()
        self.make_source1()
        self.make_source2()
        self.create_image_plot()
        self.set_children()
        curdoc().add(self)


    def input_change(self, obj, attrname, old, new):
        if obj == self.ticker2_select:
            self.ticker2 = new
        if obj == self.ticker1_select:
            self.ticker1 = new
        if obj == self.select_job_site:
            print ("job site")
            print (new)
        if obj == self.slider_1:
            self.ticker_slider_day = new
        if obj == self.ticker3_select:
            print (" num check ", new)
            #self.ticker1 = new


        self.make_source()
        self.make_source1()
        self.make_source2()
        self.create_image_plot()
        #self.create_image_plot_adv()
        self.hist_plots()
        self.hist_plots1()
        #self.image_plot=self.create_image_plot()
        #self.plot=self.create_map()

        #self.set_children()
        #self.plot=self.create_map()
        self.set_children()
        curdoc().add(self)

    def setup_events(self):
        print ("setup_event")
        super(CatApp, self).setup_events()
        if self.source:
            print ("@@ setup source change")
            self.source.on_change('selected', self, 'selection_change')
        if self.select_job_site:
            self.select_job_site.on_change('value', self, 'input_change')
        if self.ticker1_select:
            self.ticker1_select.on_change('value', self, 'input_change')
        if self.ticker2_select:
            self.ticker2_select.on_change('value', self, 'input_change')
        if self.slider_1:
            self.slider_1.on_change('value', self, 'input_change')
        if self.ticker3_select:
            #print ("checkbox selected")
            self.ticker3_select.on_click(self.checkbox_group_handler)

    def make_stats(self):
        #stats = self.selected_df.describe()
        stats=" Day1: June 23, 2015, Tue "
        self.pretext.text = str(stats)

    def selection_change(self, obj, attrname, old, new):
        #self.make_stats()
        self.make_source()
        self.make_source1()
        self.make_source2()
        self.set_children()
        curdoc().add(self)

    @property
    def df(self):
        ticker1 = self.ticker1
        ticker2 = self.ticker2
        ticker_slider_day=self.ticker_slider_day
        ticker_job_site=self.ticker_job_site
        active_at=self.ticker3_select.active # [0,1,2,3,4,5,6]
        sources_all=[]

        for x in range(0,len(active_at)):
                ticker1_new="AT"+str(active_at[x]+1)
                try:
                    df = get_ticker_dumping_data(ticker1_new,ticker_slider_day,active_at)
                    ticker_day=ticker1_new+"_"+str(ticker_slider_day)
                    source_at_day = ColumnDataSource(
                    data=dict(lat=df['GPGGA Latitude_1'],
                    lon=df['GPGGA Longitude_1'],
                    order=range(1,df.shape[0]+1),
                    model=[ticker1_new]*(df.shape[0]),
                    cat=['CAT']*(df.shape[0]),
                     )
                    )
                        #sources_all.append(source_at_day)
                except:
                    pass
                try:
                    sources_all.append(source_at_day)
                except:pass
        return sources_all


    def df1(self):
        print
        return get_data_summary(1)#get_data(self.ticker1, self.ticker2)


    def df_loading(self):
        ticker1 = self.ticker1
        ticker2 = self.ticker2
        ticker_slider_day=self.ticker_slider_day

        ticker_job_site=self.ticker_job_site
        active_at=self.ticker3_select.active
        sources_loading=[]

        for x in range(0,len(active_at)):
                ticker1_new="AT"+str(active_at[x]+1)
                try:
                    df2 = get_ticker_loading_data(ticker1_new,ticker_slider_day,active_at)
                    ticker_day=ticker1_new+"_"+str(ticker_slider_day)
                    source_at_day1 = ColumnDataSource(
                    data=dict(lat=df2['GPGGA Latitude'],
                    lon=df2['GPGGA Longitude'],
                    order=range(1,df2.shape[0]+1),
                    model=[ticker1_new]*(df2.shape[0]),
                    cat=['CAT']*(df2.shape[0]),
                     )
                    )
                    #sources_loading.append(source_at_day1)
                except:
                    pass
                try:
                    sources_loading.append(source_at_day1)
                except:pass
        return sources_loading


#If you don't want serve this applet from a Bokeh
# server (for instance if you are embedding in a separate Flask application),
# then just remove this block of code.
@bokeh_app.route("/bokeh/em_cat_site/")
@object_page("em_cat_site")
def make_apps():
    app = CatApp.create()
    return app