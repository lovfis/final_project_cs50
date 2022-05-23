# Norwegian government revenue history

### Video demo: https://youtu.be/3Jo2HfKUZnI 

### Introduction

I started this project with a desire to learn more about where the state of Norway get it's revenue from and if there are certain developments over the years that are interesting and deserves a closer look. F.ex. did the tax revenues quadruple (300% increase) in 30 years, while the average salary increased with 200% and the CPI (Consumer price index) increased with 87%. It would be interesting to look into why the tax revenues increased that much. My guess is that the work force in procentage is bigger now than then (more women are working), and that the government is earning more on taxes because of increase in production of oil and gas. But there must be more to it than that. I was optimistic about what I was going to achieve on the analytical side of this project, but the technical bits took up so much of my time, that I have had to settle with what I have achieved so far.

Before starting this project, I knew nothing about virtual environments, connecting to a database from my own computer through a program or an app, matplotlib or mpld3 (which is a package one can use to make matplotlib figures a bit interactive). The learning curve has been steep, but it is part of what makes it fun and interesting.

My web app contains three graphs showing how Norwegian government revenues has developed over the past 30 years, with respect to main entries. In the second page of the app one can display the revenues in table view. It is interactive, one can chose to display data with respect to year or main_entry. The app looks fine on different devices. It provides simple information that is already accessible online, but if I find it worth prioritizing, maybe I'll develop the app further later. The main point for me now is that I have learned a lot in fields that interest me, and I'm proud of that.

### My web app

I made my web app in a virtual environment using pipenv, on my computer. I have the VSCode editor and am using the bash terminal. I used Flask to make my app. The data I use is downloaded as a csv-file from [SSB (Statistics Norway)](https://www.ssb.no/en/statbank/table/10486/)

### My folders:
- final_project_cs50 (main folder)
    * database_handling
    * static
    * stored_charts
    * templates

### Files in the main folder final_project_cs50
#### .env
.env is a file containg key value pairs of the environment variables I'm using in my application. I stored the username and password for my postgres database there. Os.environ and psycopg2 enables accessing the values of the variables. .env is included with the project locally, but not saved to source control, so that the information I want to keep protected, is not accesible to anyone.

#### app.py
This is my central configuration object for the entire app. Here I import what I need from my installed packages, connect to the database, and use Python code to select the data I need and generate different visual appearances of them. The web app consists of two pages: main page  with charts and a page for table view of the data.

The Python code and also some Javascript generated from an mpld3 package I use pass on informaton to the html-files about what to render.

#### .gitignore
Telling git which files ato ignore.

#### Pipfile and Pipfile.lock
Two files generated when creating a virtual environment using pipenv. They contain information about required packages for the app and what version of Python I'm using. There's a few packages there that I did'nt use, like Pandas and Gunicorn (I'll use that if I deploy the wep app in Heroku or Google Cloud Platform).

#### requirements.txt
This file is not necessary when I'm using pipenv and have a Pipfile, but I keep it there in case I need it later. It contains the name of all the packages I downloaded in my virtual environment, and can be used when I need to to installations in other environments.

### Files in templates
#### index.html
This is my main page. It contains three graphs showing how norwegian government revenue has developed over the past 30 years, with respect to main entries. Most of the code from this page is generated when I use the mpld3 package to convert my matplotlib figures to interactive figures.

#### table.html
In this page one can display the revenues in table view. It is interactive, one can chose to display data with respect to one year or a main_entry. I query the database, use python and some jinja looping to get this done.

#### layout.html
This file contains html and bootstrap. It creates a layout for both my other pages, and links so that I can navigate between them. I've used a lot of the layout from the assignment finance from week 9 in the CS50 course.

### Files in database_handling
#### norwegian_state_incomes.txt
In this folder is a csv-file that contains data downloaded from SSB (Statistics Norway, ). I chose to transfer this data to a postgres database, because I wanted to get experience with connecting to a Postgres database from my computer and also because I find the data is much simpler to access from a db then from a csv-file, once I have it stored.

#### init_db.py
in the file init_db.py I made some code that:
 * connected to the postgres database nor_state_stats using psycopg2
 * read the csv-file and cleaned it up to better fit the postgres table nor_incomes
 * inserted the data to the nor_incomes table

### Files in static
Styles.css contains a few CSS styles. I reused some from the finance assignment done earlier.

### Files in stored_charts
This folder contains the charts aggregated from my app.py code. I'm not rendering them in the web app. Instead I use the mpld3 generated charts.

### Some of the many challenges I experienced
- connecting to the postgres database through bash
    * f.ex. I didn't know that if you are using Windows you have to copy your postgres path into the computers environment variables, to make a proper connection to the database. It took some time googling before I managed to solve this problem.
    * there were some minor issues with accessing the environment variables in the .env file. It took some time to figure out.
- transferring data from the csv file to the postgres database
    * After establishing a proper connection to the database, my program init_db.py in the database_handling folder worked just fine, *except*: one line from the csv file (line nr 215, "Total transfers";"2018";1184699) switched place and was not in line in the table in the database. When I used the postgres query "SELECT * FROM nor_incomes; (select all the data from the table nor_incomes), the line was some random place in between all the other data. 
    
    I tried to understand why this happened. I studied the csv file, but couldn't find anything wrong with it (might be some invisible stuff I have not noticed, though). I tried to transfer the data from the csv file in other ways, among other by going into the SQL Shell (psql) and executing this:
    \copy nor_incomes(main_entry, year, amount_in_mill) FROM 'C:\path\into\the\final_project_cs50\database_handling/norwegian_state_incomes.txt' DELIMITER ';' csv header; 
    This execution do not get rid of some of the spaces and characters I wanted to get rid of, but otherwise copies the csv data to the database table. BUT: the same thing happened to line nr 215 from the csv-file. I ended up some random place in the database table. 
    
    My guess is that there is something wrong in the csv-file, I don't know what, but anyway there is a solution to this in my program, and that is not to execute "SELECT * FROM nor_incomes;", but to execute (in a loop over all the main entries): "SELECT * FROM nor_incomes WHERE main_entry=%s ORDER BY year;" Then I get the data ordered in line, like in the csv file.

    * executing a select query like this: 
    select_query = """SELECT * FROM nor_incomes WHERE main_entry=%s ORDER BY year;"""
    *cur.execute(select_query, (entry,))*
    At first I didn't know that the variable entry had to be in the form of a tuple (you don't have to do that in sqlite). I wrote: cur.execute(select_query, entry). This gave me an error, that didn't in an easy way suggest the solution, but after some googling I found a post in stackoverflow that helped me.


### Subjects I want to work on later / improvements
- choosing field in dropdown menu without having to press a submit button afterwards
- make some more functions in other files to keep my app.py code easier to read
- displaying tables and charts over norwegian government expenses as well, make some comparisons ad lightweight analysis

### Credits
I owe a lot of credit to Corey Schafer. I have learned a lot from his youtube videos about Python, virtual environments (pipenv), Flask and Matplotlib, especially this one about [matplotlib subplots](https://www.youtube.com/watch?v=XFZRVnP-MTU&list=PL-osiE80TeTvipOqomVEeZ1HRrcEvtZB_&index=10) and this one about [pipenv](https://www.youtube.com/watch?v=zDYL22QNiWk)

I've also learned a lot from studying matplotlib.org. One specific example helped me a lot. I have actually used a lot of the code from it and adjusted it to my project. The example came from here: [graph of multiple time series](https://matplotlib.org/2.1.2/gallery/showcase/bachelors_degrees_by_gender.html#sphx-glr-gallery-showcase-bachelors-degrees-by-gender-py)

