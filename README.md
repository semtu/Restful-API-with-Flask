# Restful API using Flask micro-framework

There are four files:
1. data_processing.py : This makes GET requests asynchronously to specified url and scrapes the website for information then dumps this processed data in a Json file
2. api.py : This is the Flask Api. It has two routes, /ping and /posts which uses GET methods to ping the website and grab resource data respectively.
3. api_test.py : Used unit test to perform some basic Api validation tests
