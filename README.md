# NHS Scotland Waiting List Tool
#### Video Demo:  <https://www.youtube.com/watch?v=TbFROoQztAg>
#### Description:
Hello, my name is Alex Doyle, thank you for taking a look at my project. Here I will be attempting to take you through the design choices that I made and challenge that I faced when developing the site. For this project I used many different resources and languages. Primarily, Python, HTML, and SQL. As well as some additional resources such as Flask and Bootstrap.
For my project I have created a website which allows people to access and navigate the NHS Scotland waiting list databases in an efficient and understandable way. Although these databases are made public by the NHS, they do not make them easy to find or easy to interpret the information within them. The databases come as a .csv file which aren’t ordered and do not use plain English for things such as hospital names or specialties; instead, opting for codes to represent them. This makes the databases almost unusable for any member of the public without previous experience in hospitals or the NHS. This is where my website comes in, using my experience working with the NHS and newfound coding abilities, I have created a site where anyone can easily access and understand information about NHS Scotland waiting times.
Firstly, I found it quite difficult to come up with an idea on what to create, I wanted a project which combines my previous area of work (medical) with what I hope to move into (computer science). But when presented with an open objective such as this final project I find it difficult to decide on what to make when there are essentially endless options. In the end I felt this was my best idea, so I began work creating it.
I found getting stated somewhat difficult as this was the first entirely unguided coding project I had undertaken. I did not know what the first steps to take should be, so I began by searching for the NHS databases on waiting lists. These were not easy to find as I had to look in many different places to finally find where they are published.
Once I had found the databases, I now needed to think about how I was going to access and use the data within them. I decided I wanted to use SQL for database management as I had some experience with it from the course. However, the NHS databases came as .csv files so I realised I need to convert them into a .db. To do this I initially used the inbuilt command in SQLITE3.
However, this created a number of problems, for example when conducting SQL queries, it does not like it if the column titles begin with a number and unfortunately the NHS databases had many titles which began with numbers. So, to save time having to manually change all the .csv files to better format them for sql, I created python program called dbinsert.py.
dbinsert.py : This is a small python program that I created to format the .csv files more easily and automatically insert them into a table in a .db database.

Next, I decided to begin working on the website itself. I decided I wanted to use flask as it added many important features to the website such as template inheritance and the ability to pass variables from python to HTML. I initially struggles with getting flask to work for me as I was not aware of how to properly set up flask for the first time on a project. To remedy this, I found the flask documentation and specifically the user guide and worked trough the tutorials which they provide to get a better understanding of flask and how to use it.
After flask was working properly for me, I began to create the website. I started by creating the layouts.html file as a starting point for all the other pages to use through template inheritance. Layouts.html contains the navbar at the top of the page the footer and a number of style templates that are used throughout the site.
I chose to use bootstrap as an additional library for html as it added a huge range of convenient and attractive features that I wanted to implement on my website. I feel that my use of bootstrap greatly improved the aesthetics of my website.
All of my HTML files can be found within the templates folder of my project, index.html is the homepage of my website and it what first greets users from there users are directed to select.html where they choose which of the databases they want to search into. From there they are taken to a specific html depending on the database chosen where the user is able to select the parameters that they wish to search for and at the press of a button a table appears which will display the requested information. Allowing the user to compare waiting times across Scotland by medical board or specialty.
The back end of my website can be found within the file app.py, here I used python and sql to process the users’ requests and give back the requested information. As can be seen there are a number of different routes within app.py at least one for each database. This is because each of the databases used was formatted in different ways and contained different information types. Therefore, a one size fits all solution was not possible. However, to explain what is going on broadly let’s look into the /search/ route.

/search/ : So, search begins with a number of sql  queries. These queries are done to populate the fields of the form on the webpage so that the user can chose which parameters they wish to search for. As you can see search accepts both GET and POST methods. GET is used to load the webpage as new and POST is used when the user has submitted the form on the webpage. So if request.method is POST we first gather what the user had input into the form.
Next a SQL query is written as an fstring. This is done because when using db.execute it does not accept variables as operators directly.
So now I use the users input in the form to access my database and return the information that the user requested. As I mentioned previously the NHS databases don’t actually use place or specialty names, they instead use codes. So, to make this more understandable for users I created a few additional tables in my database to act as references so that the users are able to read the hospital names in plain English. These tables are called hbref, hscspref, specialtyref, and locationref. You can see in the query here I have joined them to the main table to access their data.
After the query is done and the data has been gathered a different webpage is then rendered depending on weather the user requested simple or complex data, the data gathered is passed to it and a table appears below the form displaying the data which the user requested.
All of the different route’s work on broadly the same principle as /search/ however all are slightly different to account for the uniqueness of each database and how they are formatted. /diag/ is probably the most different as for some reason this csv. was formatted in such a way that data which I wanted to present on a single row was instead found on 8 different rows with the same headings. So as can be seen in /diag/ I have written a small amount of code to ensure all the information is presented neatly on a single row.

Thank you once again for having a look at and reading about my project. I am very proud of what I have created here. However, this was not an easy task; I spent a lot of time on this project learning new things and reading about solutions to problems which I was facing for the first time. I have learned greatly from this experience and although the roadblocks were frustrating and difficult at the time, through what I’ve learned, I am now more prepared in dealing if they arise again in the future. I am excited to see where my coding skills take me going forward.
