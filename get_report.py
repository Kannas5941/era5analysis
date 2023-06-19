from fpdf import FPDF
import datetime
from era5analysis import get_stats
import os


def get_report(data, analysis, frequency, lat=None, lon=None):
    """This function creates a report of the performed analysis, showing
    the plots arrangd in a .pdf file.

    Args:
        data (object): This can be a dataset for spatial analysis or a 
                        dataframe for time series analysis.
        analysis (str): this is the type of analysis to be perfomed and
                        it defines the type of the data used.
        frequency (str): This define the frequency of the data used.
        lat (float, optional): This is the latitud for performing time series analysis
                        in the spatial data. Defaults to None.
        lat (float, optional): This is the longitude for performing time series analysis
                        in the spatial data. Defaults to None.
    """
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    
    print('REMAINDER: The generation of the report might take \
        up to 10 minutes.')

    today = datetime.datetime.today()
    pdf = FPDF('P', 'mm', 'Letter')

    def header(pdf):
        pdf.add_page()
        pdf.image('../docs/dtu_logo.png', x=180, y=3, w=20, h=30)

    def cover_page(pdf):
        pdf.add_page()
        pdf.image('../docs/cover1.png', x=0, y=0, w=150, h=80)
        pdf.image('../docs/dtu_logo.png', x=160, y=10, w=40, h=50)
        pdf.image('../docs/cover2.png', x=70, y=200, w=150, h=80)
        pdf.set_font('Arial', 'B', 30)
        pdf.set_xy(10, 100)
        pdf.cell(150, 10, "ERA5 Analysis Report", 0, 1, 'L')
        pdf.set_font('Arial', size=23)
        pdf.set_xy(10, 110)
        pdf.cell(150, 10, 'Global winds from the ERA5 dataset', 0, 1, 'L')
        pdf.set_font('Arial', size=26)
        pdf.set_xy(10, 150)
        pdf.cell(100, 10, "Analysis:  {}".format(
            analysis.replace('_', ' ').title()), 0, 1, 'L')
        pdf.set_xy(10, 165)
        pdf.set_font('Arial', size=22)
        pdf.cell(100, 10, "Frequency: {}".format(frequency.title()), 0, 2, 'L')
        pdf.set_xy(12, 195)
        pdf.set_font('Arial', size=18)
        pdf.cell(100, 10, "Date: {:%d, %b %Y}".format(today), 0, 1, 'L')
        pdf.set_xy(12, 210)
        pdf.set_font('Arial', 'I', size=18)
        pdf.cell(100, 10, " DTU Wind Energy", 0, 1, 'L')
        pdf.set_xy(35, 249)
        pdf.set_font('Arial', size=15)
        pdf.cell(0, 10, '- '+str(pdf.page_no())+' -', 0, 0, 'L')

    cover_page(pdf)
    header(pdf)

    if analysis == 'time_series':
        df = data
        # Calling plotting functions
        get_stats.plot_timeseries(df)
        get_stats.plot_windrose(df, analysis, lat=None, lon=None)
        get_stats.plot_pdf_ts(df)
        #
        pdf.image('../docs/time_series.png', x=5, y=50, w=200, h=60)
        pdf.image('../docs/windrose_10m.png', x=5, y=125, w=80, h=80)
        pdf.image('../docs/windrose_100m.png', x=120, y=125, w=80, h=80)
        pdf.image('../docs/pdf_10.png', x=5, y=200, w=80, h=80)
        pdf.image('../docs/pdf_100.png', x=120, y=200, w=80, h=80)
        pdf.set_xy(10, 35)
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(100, 10, "Time Series Analysis", 0, 2, 'L')
        pdf.set_xy(10, 45)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(100, 10, 'Wind speed time series at 10 and 100 meters:', 0, 1, 'L')
        pdf.set_xy(10, 115)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(100, 10, 'Wind rose and wind speed frequency:', 0, 1, 'L')
    elif analysis == 'spatial':
        ds = data
        # Calling plotting functions
        get_stats.plot_spatial_map(ds)
        get_stats.plot_spatial_timeseries(ds, lat, lon)
        get_stats.plot_windrose(ds, analysis, lat, lon)
        #
        pdf.image('../docs/spatial_time_series.png', x=5, y=50, w=200, h=60)
        pdf.image('../docs/windrose_10m.png', x=5, y=125, w=80, h=80)
        pdf.image('../docs/windrose_100m.png', x=120, y=125, w=80, h=80)
        pdf.image('../docs/spatial_map.png', x=5, y=200, w=190, h=70)
        pdf.set_xy(10, 35)
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(100, 10, "Spatial Analysis", 0, 2, 'L')
        pdf.set_xy(10, 45)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(100, 10, 'Wind speed time series of 10 and 100 meters, at location lat={}, lon={}:'.format(
            lat, lon), 0, 1, 'L')
        pdf.set_xy(10, 115)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(100, 10, 'Wind rose and wind maps of the study area:', 0, 1, 'L')

    pdf.set_xy(15, 249)
    pdf.set_font('Arial', size=15)
    pdf.cell(0, 10, '- '+str(pdf.page_no())+' -', 0, 0, 'C')

    pdf.output('../report_{}.pdf'.format(analysis), 'F')
    pdf.close()
