import pandas as pd 
import numpy as np
from math import pi
import matplotlib.pyplot as plt 
import seaborn as sns
from datetime import datetime
from fpdf import FPDF 
import sys

def create_DonutChart(df):

    #Data Selection
    selected = pd.DataFrame(df.groupby(['category'])['category'].count())
    selected = selected.rename({'category': 'Count'}, axis=1) 
    selected['Count'] = (selected['Count']/len(df))*100 # Convert to percentage 
    selected = selected.sort_values(by='Count',ascending=False)
    categories = selected.index.tolist()

    colors = ["#0a5e66","#54112f","#88ccd9"]

    fig, ax = plt.subplots(figsize=(5,5))
    # Create a pieplot
    plt.pie(selected['Count'], labels = categories, colors=colors, autopct='%.0f%%',pctdistance=0.7,textprops={"color":'#fbf7f5'})

    # add a circle at the center to transform it in a donut chart
    my_circle=plt.Circle( (0,0), 0.45, color='white')
    p=plt.gcf()
    p.gca().add_artist(my_circle)

    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0)

    fig.savefig("pie_chart.png",transparent=False,  
            facecolor='white', 
            bbox_inches="tight")


def create_BarChart(df):
    fig, ax = plt.subplots(figsize=(12, 8))

    # Define plot background colors
    sns.set(rc={'axes.facecolor':'#fbf7f5'})

    x_vals = list(df['productType'].value_counts(sort='ascending'))[:10]
    y_vals = list(df['productType'].value_counts(sort='ascending').keys())[:10]

    for i in range(len(y_vals)):
        # Replace 'Other' with 'Accessory'
        if y_vals[i] == 'Other':
            y_vals[i] = 'Accessory'

    #create horizontal bar chart 
    ax = sns.barplot(x=x_vals, y=y_vals, color='#88ccd9', orient='h')

    # add axis labels
    plt.xlabel('Count', fontsize=14, loc='center')

    plt.ylabel('Product Type', fontsize=14)
    ax.yaxis.set_label_coords(-.08, .88)

    sns.despine()

    # Add annotations
    total = len(x_vals)
    for p in ax.patches:
            value = '{:.0f}'.format(p.get_width())
            x = p.get_x() + p.get_width() - 8
            y = p.get_y() + p.get_height()/2
            ax.annotate(value, (x, y), ha='center', color='#fbf7f5')

    fig.savefig("bar_chart.png",transparent=False,  
            facecolor='white', 
            bbox_inches="tight") 


def create_BoxPlot(df):
    selectedProducts = ['Shorts','T-shirt','Tank',
                   'Tights','Stringer','Legging',
                   'Jogger','Bra','Hoodie']

    df_selected = df[df['productType'].isin(selectedProducts)]

    fig, ax = plt.subplots(figsize=(16, 8))

    # Define plot background colors
    sns.set(rc={'axes.facecolor':'#fbf7f5'})

    flierprops = dict(marker='o', markersize=5, markeredgecolor='black', markerfacecolor='#6f2b77', alpha=0.5)

    ax = sns.boxplot(
        data=df_selected, x="productType", y="price",
        flierprops=flierprops,
        boxprops={"facecolor": '#88ccd9'},
        medianprops={"color": "#0a5e66"},
    )

    # Labels 
    plt.xlabel('Product Type', fontsize=14)
    ax.xaxis.set_label_coords(0.05, -.08)

    plt.ylabel('Price ($)', fontsize=14)
    ax.yaxis.set_label_coords(-.05, .85)

    plt.tick_params(axis='both', which='major', labelsize=14)

    fig.savefig("boxplot_chart.png",transparent=False,  
            facecolor='white', 
            bbox_inches="tight") 


def create_ViolinPlot(df):

    mens = df.loc[df['category'] == 'Men']
    womens = df.loc[df['category'] == 'Women']
    df_violin = pd.concat([mens,womens])

    fig, ax = plt.subplots(figsize=(12, 8))

    # Define plot background colors
    sns.set(rc={'axes.facecolor':'#fbf7f5'})
    color_palette = {"Men": "#0a5e66", "Women": "#6f2b77"}

    sns.violinplot(data=df_violin, y="price", x="category", palette = color_palette)


    # Labels 
    plt.xlabel('Gender', fontsize=14, loc='center')

    plt.ylabel('Price ($)', fontsize=14)
    ax.yaxis.set_label_coords(-.05, .85)

    plt.tick_params(axis='both', which='major', labelsize=14)

    fig.savefig("violinplot_chart.png",transparent=False,  
            facecolor='white', 
            bbox_inches="tight")

def generate_report(df,fileName):
    # Margin
    m = 10 
    # Page width: Width of A4 is 210mm
    pw = 210 - 2*m 

    # Cell height
    height_logo = 25
    height_header = 10
    height_cell_1 = 70
    height_cell_2 = 80
    height_cell_3 = 50
    height_cell_chartTitle = 10

    pdf = FPDF()
    pdf.add_page()

    # Add new font
    pdf.add_font('BebasNeue','','BebasNeue-Regular.ttf', uni=True)


    # Logo
    pdf.set_xy(x=10, y= 5) # or use pdf.ln(50)
    pdf.set_font('BebasNeue','',60)
    pdf.cell(w=(pw/4.5), h=height_logo, txt="GYM", border=0, ln=1, align = 'C')

    pdf.set_xy(x=10, y= 17) # or use pdf.ln(50)
    pdf.set_font('BebasNeue','',37)
    pdf.cell(w=(pw/4.5), h=height_logo, txt="SHARK", border=0, ln=1, align = 'C')

    # Title
    pdf.set_xy(x=58, y= 10)
    currentTime = datetime.today().strftime('%B %d %Y [ %H:%M:%S ]')
    pdf.set_font('BebasNeue','',21)
    pdf.cell(w=(pw/1.3), h=height_header, txt=f'Report Generated: {currentTime}', border=0, ln=1, align = 'C')

    # Subtitle
    pdf.set_xy(x=58, y= 22) 
    pdf.set_font('BebasNeue','',25)
    pdf.cell(w=(pw/1.3), h=height_header, txt="Online Store Breakdown", border=0, ln=1, align = 'C')

    # Pie Chart Title
    pdf.set_xy(x=15, y= 41) 
    pdf.set_font('BebasNeue','',16)
    pdf.cell(w=(pw/3), h=height_cell_chartTitle, txt="Product Demographic", border=0, ln=1, align = '')

    # Pie Chart
    pdf.set_xy(x=10, y= 45) 
    # pdf.cell(w=(pw/2.2), h=height_cell_1, txt="Cell 1A", border=0, ln=1, align = 'C')
    pdf.image('./pie_chart.png', x = 18, y = 50, w = 70, h = 0, type = 'PNG', link = '')

    # Bar Chart Title
    pdf.set_xy(x=99, y= 40) 
    pdf.set_font('BebasNeue','',16)
    pdf.cell(w=(pw/3), h=height_cell_chartTitle, txt="Product Inventory", border=0, ln=1, align = 'C')

    # Bar Chart
    pdf.set_xy(x=99, y= 45) 
    pdf.image('./bar_chart.png', x = 102, y = 47, w = 100, h = 0, type = 'PNG', link = '')

    # Box Plot Title
    pdf.set_xy(x=92, y= 108) 
    pdf.set_font('BebasNeue','',16)
    pdf.cell(w=(pw/3), h=height_cell_chartTitle, txt="Price Distribution", border=0, ln=1, align = '')

    # Box Plot
    pdf.set_xy(x=15, y= 127) 
    pdf.image('./boxplot_chart.png', x = 15, y = 115, w = 180, h = 0, type = 'PNG', link = '')

    # Violin Plot Title
    pdf.set_xy(x=114, y= 208) 
    pdf.set_font('BebasNeue','',16)
    pdf.cell(w=(pw/3), h=height_cell_chartTitle, txt="Price Distribution by Gender", border=0, ln=1, align = '')

    # Violin Plot
    pdf.set_xy(x=140, y= 219) 
    pdf.image('./violinplot_chart.png', x = 107, y = 215, w = 100, h = 0, type = 'PNG', link = '')

    # Table Header
    pdf.set_xy(x=9, y= 197) 
    pdf.set_font('BebasNeue', '', 16)
    pdf.cell(w=(pw/3), h=height_cell_3, txt="Items with the Most Discount", border=0, ln=1, align = '')

    pdf.set_xy(x=10, y= 225) 
    table_ch = 8
    pdf.set_font('BebasNeue', '', 11)
    pdf.cell(59, table_ch, 'Item', 1, 0, 'C')
    pdf.cell(35, table_ch, 'Color', 1, 1, 'C')

    # Get Table Info
    mostDiscount = df.sort_values(by='discountPercentage', ascending=False)[:5]
    mostDiscount = mostDiscount[['name','color','preSalePrice','discountPercentage']]

    # Table contents
    pdf.set_font('Arial', '', 10)
    for i in range(0, len(mostDiscount)):
        pdf.cell(59, table_ch, mostDiscount['name'].iloc[i], 1, 0, 'C')   
        pdf.cell(35, table_ch, mostDiscount['color'].iloc[i], 1, 1, 'C')

    pdf.output(f'./{fileName}.pdf', 'F')

def main():

    df = pd.read_csv('gymshark_cleaned.csv')

    # File Name of Report
    file_name = sys.argv[1]

    # Creating Charts
    create_DonutChart(df)
    create_BarChart(df)
    create_BoxPlot(df)
    create_ViolinPlot(df)

    # Creating Report
    generate_report(df, file_name)

main()