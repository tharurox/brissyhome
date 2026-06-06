# brissyhome

This is the Assignment Made for IFN 582 Web Development Module. 

How to run the website: 

1) Run SQL file in MySQL workbench to Create the databas tables. 
2) edit the init.py with the password of your localhost for MySQL.
3) Run "pip install -r requirements.txt"
4) Run "python run.py" to start the web application.
5) the application will run in port 8888. 


User can register as a buyer or a seller. 
User can login with the registered credetials.
There may be no homes available when the database is created as it's empty.  So I have adde few SQL queries to populate the db when it's getting created by taking a dump from the mysql workbench of the existing db. 

Dummy Users: 

    * Login as Agent: agent1 / Password : qwerty@123
    * Login as User: user1 / Password: qwerty@123

If the account is a buyer account :  

    *The buyer can view the listed properties, bookmark them to view them later.

    *The buyer can search the properties matching thier price, solar availability, bedrooms. 

    *Buyer can apply for a scheduled booking. 


If the account is a seller account :

    *The seller can post a listing in the website by uploading picture, adding the details of the property. 

    *The seller can manage the listed properties like edit the details, edit the photo and remove the listing from the website.
    
    * The seller can't bookmark the properties. 


Completed Items: 
    * Bookmarks
    * CRUD Tasks on property 
    * Authentication

Pending Items: 
    * Enquiries (Halfway done)
    * Offers  


    Developed by : 
    TharakaRavishan Ranathunga
    N11849622 
    QUT - IFN 582 - Assignment 3 


