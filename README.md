RicePrice
=========

This repository contains the code for the visualization application RicePrice which visualizes how the rice prices have changed over the years and highlights the inequality of different varieties of rice amongst the different states in India.

- Data Source: http://data.gov.in

- Directory Structure:
+ RicePrice/
	code/
		rice.db
		__init__.py
		app.py
		predict.py
		static/
			images/
				graph.png
		templates/
			prices.html
	Screenshots/
	data/
		argmarkrice2001.csv to ...2012.csv
	README.md

- Requirements:
Python
sqlite3
Python packages:
sqlite3
matplotlib
Flask


- 1. On the command prompt, go to the code directory:
run sqlite3 rice.db

Then, run the following:

+ CREATE TABLE "prices" (ID integer primary key autoincrement,
                                      State varchar(50),
                                      District varchar(50),
                                      Market varchar(50),
                                      Commodity varchar(50),
                                      Variety varchar(150),
                                      pdate DateTime,
                                      MINPrice INT,
                                      MAXPrice INT,
                                      MODALPrice INT,
                                      PDay varchar(2),
                                      PMonth varchar(2),
                                      PYear varchar(4),
                                      Category varchar(50));

- 2. Get out of sqlite3. Within the code directory itself, run > python app.py
- 3. On the browser, go to http://localhost:8000
