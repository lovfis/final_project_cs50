import os
import psycopg2

from flask import Flask, render_template, request
from matplotlib import pyplot as plt
# a tool to turn static matplotlib charts to interactive html data
import mpld3

# Import functions from functions
from functions import axes_settings

app = Flask(__name__)

# Setting debug mode to true or false 
ENV = 'dev'

if ENV  == 'dev':
    app.debug = True
else:
    app.debug = False

# Ensure templates are auto-reloaded, THINK I NEED IT...
app.config["TEMPLATES_AUTO_RELOAD"] = True

def get_db_connection():
    conn = psycopg2.connect(
            host="localhost",
            database="nor_state_stats",
            # db = SQL(os.environ['DATABASE_URL'])
            user=os.environ.get('DB_USERNAME'),
            password=os.environ.get('DB_PASSWORD'),
            port="5432"
            )
    
    return conn

# A global variable (within the environment), that contains all the relevant years
# from the table nor_incomes in the database (1991-2021)
YEARS = list(range(1991, 2022))

ENTRIES = ["TOTAL REVENUE", "Sales revenue", "Operating surplus extraction of petroleum",\
    "Depreciation etc. extraction of petroleum", \
    "Depreciation etc. other central government enterprises", \
    "Other revenue from fixed capital formation", "Total transfers", "Tax revenue", \
    "Members' contributions National Insurance Scheme", \
    "Employers' contributions National Insurance Scheme", "Interest and dividends", \
    "Transfers from other state accounts", "Transfers from municipalities and county authorities",\
    "Transfers from the central bank", "Other transfers"]


# Main page
@app.route('/')
def index():

    # Connect to the database nor_state_states via function up above
    conn = get_db_connection()
    cur = conn.cursor()

    # Query for all the data from the database, sorted by year in list of lists for each main entry
    # In addition I'm going to use these data in several loops, so it's nice to have them ready for use
    incomes_sorted = [] 
    for entry in ENTRIES:
        select_query = """SELECT * FROM nor_incomes WHERE main_entry=%s ORDER BY year;"""
        # for some reason, the variable must be put in a tuple (therefore the comma...)
        cur.execute(select_query, (entry,))
        incomes = cur.fetchall()
        for income in incomes:
            post = income[1]
            year = income[2]
            amount = income[3]
            incomes_sorted.append([post, year, amount])

    # Append to incomes_sorted a list in the end, to make sure that the plot loop further down 
    # also plots in the last main entry with corresponding values
    incomes_sorted.append(['main_entry', 'year', 'amount'])

    # Close connection to database, all the data you need are now stored in the incomes_sorted list
    conn.close()

    #----------------------------------------------------------------------------------------   
    # These are the colors that will be used in the plot
    color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f']

    # Use matplotlib to display data as several graphs in one diagram 
    # First: Create 3 figures with axes   
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    fig2, ax2 = plt.subplots(figsize=(12, 4))
    fig3, ax3 = plt.subplots(figsize=(12, 6))

    axes = [ax1, ax2, ax3]

    # Make settings for all of the axes using function from functions.py
    axes = axes_settings(axes)

    # Limit the range of the plot to only where the data is.
    # Avoid unnecessary whitespace.
    ax1.set_xlim(1991, 2039.5)
    ax1.set_ylim(0, 1650000)
    ax2.set_xlim(1991, 2039.5)
    ax2.set_ylim(0, 220000.1)
    ax3.set_xlim(1991, 2039.5)
    ax3.set_ylim(0, 43000.1)

    # Make sure your axis ticks are large enough to be easily read.
    for ax in axes:
        ax.set_xticks(range(1991, 2022, 2), fontsize=14)
        ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
        ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
    
    ax1.set_yticks(range(0, 1700000, 100000), fontsize=14)   
    ax2.set_yticks(range(0, 230000, 20000), fontsize=14)    
    ax3.set_yticks(range(0, 42000, 5000), fontsize=14)

    entries_without_label_ax1 = ["Sales revenue", "Depreciation etc. other central government enterprises", \
    "Other revenue from fixed capital formation",\
    "Transfers from other state accounts", "Transfers from municipalities and county authorities",\
    "Other transfers", "Transfers from the central bank", \
    "Depreciation etc. extraction of petroleum"]

    y_offsets = {"Sales revenue": 0, \
    "Depreciation etc. other central government enterprises": 3300, "Other revenue from fixed capital formation": 1700,\
    "Transfers from other state accounts": -1000, "Transfers from municipalities and county authorities": 500,\
    "Other transfers": 0}

    y_offsets2 = {"Employers' contributions National Insurance Scheme": 30000, "Operating surplus extraction of petroleum": 0, \
    "Members' contributions National Insurance Scheme": -35000}

    # Set some values before looping over the data and plotting into the diagrams/figures
    years_x = YEARS
    graph_label = ""
    # The count value will help keep track of colors from the color list up above, so that the loop picks the 
    # right color for each graph
    count = 0
    # amount list to keep track of amounts and corresponding entries and years
    amount_y = []

    # Plot loop, plotting graphs into the four different figures. Getting data from the incomes_sorted list
    # (which has data from the table nor_incomes in database nor_state_stats)
    for income in incomes_sorted:
        # Variables for main entry and amount
        entry = income[0]
        amount = income[2]
        
        # Checks to see if the loop is at a new entry
        if graph_label != entry:
            # checks if the list amount_y has content
            if len(amount_y):  
                # Plotting in all the data from list amount_y and years_x list into fig1 (ax1)
                # This figure will contain all the axes
                ax1.plot(years_x, amount_y, lw=2.5, color=color_sequence[count])
                # Add a text label to the right end of every line, except the last 
                if graph_label in y_offsets2:
                    # Set a y coordinate to use when plotting in text, so that the labels are separated
                    # from one another (some of them were on top of eachother to begin with)
                    y_pos = amount_y[-1] - 0.5
                    if graph_label in y_offsets2:
                        y_pos += y_offsets2[graph_label] 
                    ax1.text(2021.5, y_pos, graph_label, fontsize=14, color=color_sequence[count])
                elif graph_label not in entries_without_label_ax1:
                    ax1.text(2021.5, amount_y[-1], graph_label, fontsize=14, color=color_sequence[count])
                elif graph_label == "Other transfers":
                    ax1.text(2021.5, amount_y[-1], "Other (see graphs below)", fontsize=14, color=color_sequence[count])
                
                # Plot into the second graph (ax2) half of the main entries with revenue under 220000 mill nok
                if graph_label not in y_offsets and graph_label not in ['TOTAL REVENUE', 'Total transfers', 'Tax revenue']:
                    ax2.plot(years_x, amount_y, lw=2.5, color=color_sequence[count])
                    # Add a text label to the right end of every line
                    ax2.text(2021.5, amount_y[-1], graph_label, fontsize=14, color=color_sequence[count])

                # Plot into the last graph (ax3) the rest of the main entries
                else:
                    # Set a y coordinate to use when plotting in text, so that the labels are separated
                    # from one another (some of them were on top of eachother to begin with)
                    y_pos = amount_y[-1] - 0.5
                    if graph_label in y_offsets:
                        y_pos += y_offsets[graph_label]
                    # Plot 
                    ax3.plot(years_x, amount_y, lw=2.5, color=color_sequence[count])
                    # Add a text label to the right end of every line
                    ax3.text(2021.5, y_pos, graph_label, fontsize=14, color=color_sequence[count])
                
                # Increment count, reset amount_y list and append the current graph_label (which
                # is a new accurance) to it. Set the graph_label to be equal to the current entry,
                # so that the loop runs correctly
                count += 1
                amount_y = []
                amount_y.append(amount)
                graph_label = entry
            else:
                graph_label = entry
                amount_y.append(amount)
        else:
            amount_y.append(amount)

    
    # Set title, I find it necessary onlu over the first diagram
    ax1.set_title("Government Revenues in Norway, 1991-2021\n", fontsize=20, ha='center')

    #--------------------------------------------------------------------------------------

    # Save the figures for later (although I don't need them right now, because of the use of mpld3)
    """ fig1.savefig('stored_charts/fig1.png', bbox_inches='tight')
    fig2.savefig('stored_charts/fig2.png', bbox_inches='tight')
    fig3.savefig('stored_charts/fig3.png', bbox_inches='tight') """

    # Can also save using mpld3:
    # mpld3.save_html(fig, fileobj, **kwargs)

    # Use mpld3 to make the figures a bit interactive
    # Write the interactive figures with html from layout.html etc to index.html
    html_str1 = mpld3.fig_to_html(fig1)
    html_str2 = mpld3.fig_to_html(fig2)
    html_str3 = mpld3.fig_to_html(fig3)
    Html_file= open("templates/index.html","w")
    Html_file.write("{% extends 'layout.html' %}\n\n{% block title %}\n\tNorwegian government revenue history\n \
{% endblock %}\n\n{% block main %}\n")
    Html_file.write(html_str1)
    Html_file.write(html_str2)
    Html_file.write(html_str3)
    Html_file.write("\n{% endblock %}")
    Html_file.close()
    
    plt.close(fig1)
    plt.close(fig2)
    plt.close(fig3)

    #--------------------------------------------------------------------------------------

    return render_template('index.html')
    

@app.route('/table', methods=["GET", "POST"])
def table():
        
    if request.method=='POST':  
        # The user chooses a year or a main_entry from a dropdown table in table.html  
        year_chosen = request.form.get("year")
        entry_chosen = request.form.get("main_entry")

        # Connect to the database nor_state_states via function up above
        conn = get_db_connection()
        cur = conn.cursor()

        if year_chosen:
            # cur is the holder of the data, in the form of a list, when executing the line below        
            # Query the database for information and present a table with data from that year
            query = """SELECT * FROM nor_incomes WHERE year = %s;"""
            # for some reason, the variable must be put in a tuple (therefore the comma...)
            cur.execute(query, (year_chosen,))  
            show_total = True
        
        elif entry_chosen:
            query = """SELECT * FROM nor_incomes WHERE main_entry = %s;"""
            # for some reason, the variable must be put in a tuple (therefore the comma...)
            cur.execute(query, (entry_chosen,))
            show_total = False

        incomes = cur.fetchall()

        # Close database after getting all the data you need (stored in incomes list)
        conn.close()    
        
        # Calculate total income if year is the chosen variable
        total = 0
        if show_total:
            for income in incomes:
                total += income[3]

        return render_template('table.html', years=YEARS, entries=ENTRIES, \
            incomes=incomes, total=total, show_total=show_total)
    
    else:
        return render_template('table.html', years=YEARS, entries=ENTRIES)


if __name__ == '__main__':
    app.run()
