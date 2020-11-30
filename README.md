# Glassdoor 

### Introduction

1. This is web crawler for Glassdoor. This program can help you find the useful information about the jobs you are interested in from the Glassdoor. This program can also output a CSV file if you need.
2. I also wrote a user friendly console app, if you don't have too much experience with programming in python

## Version

**11/29/2020 Update** v1 released!

### Run

1. **Console app**

   ~~~cmd
   python program.py
   ~~~

2. **Python code**

   init program

   ~~~python
   from glassdoor import Glassdoor
   glassdoor = Glassdoor(job name)
   ~~~

   run program

   ```python
   glassdoor.run(file_name=FileName,Time=True/False,Company=True/False,Location=True/False,Job_Name=True/False,Job_Type=True/False,Key_Word=[list])
   ```

   **Note**:

   ​	default for time,company....job_Type is *True*

   ​	default for key_word is *empty list*

3. Change Proxy and UA

   ~~~python
   # proxy
   glassdoor.proxy_list = {"http":'ip:port'}
   # UA
   glassdoor.my_headers = ["ua","ua"]
   ~~~

### Contact

If you have any question fell free to contact GuangruiWang [GUW18@pitt.edu]

