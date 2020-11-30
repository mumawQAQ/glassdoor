from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from glassdoor import Glassdoor

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

print("""
   ____ _                   _                  
  / ___| | __ _ ___ ___  __| | ___   ___  _ __ 
 | |  _| |/ _` / __/ __|/ _` |/ _ \ / _ \| '__|
 | |_| | | (_| \__ \__ \ (_| | (_) | (_) | |   
  \____|_|\__,_|___/___/\__,_|\___/ \___/|_|   
                                               
""")
questions = [
    {
        'type': 'input',
        'name': 'search_name',
        'message': 'What job you want to search:',
    },
    {
        'type': 'input',
        'name': 'file_name',
        'message': 'Enter the output file name(*.csv):',
    },
    {
        'type': 'confirm',
        'name': 'Company',
        'message': 'Do you want the information about the company name?',
        'default': True
    },
    {
        'type': 'confirm',
        'name': 'Time',
        'message': 'Do you want the information about the post time?',
        'default': True
    },
    {
        'type': 'confirm',
        'name': 'Location',
        'message': 'Do you want the information about the job\'s location?',
        'default': True
    },
    {
        'type': 'confirm',
        'name': 'Job_Name',
        'message': 'Do you want the information about the job\'s name',
        'default': True
    },
    {
        'type': 'confirm',
        'name': 'Job_Type',
        'message': 'Do you want the information about the job\'s type',
        'default': True
    },
    {
        'type': 'input',
        'name': 'key_word',
        'message': 'Enter the key words you want to search in the context(split by comma):',
    }
]

answers = prompt(questions,style=style)
keyword = answers.get("key_word")
if keyword != "":
    keyword = keyword.split(",")
else:
    keyword =[]
glassdoor = Glassdoor(answers.get("search_name"))
glassdoor.run(file_name=answers.get("file_name"),Time=bool(answers.get("Time")),Company=bool(answers.get("Company")),Location=bool(answers.get("Location")),Job_Name=bool(answers.get("Job_Name")),Job_Type=bool(answers.get("Job_Type")),Key_Word=keyword)
glassdoor.my_headers