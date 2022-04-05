# Restaurant web app
#### Video Demo:  https://youtu.be/MKM3WEfAZyU
#### Description: Lets people view the restaurant's menu, create their account, and place psuedo orders when they sign in.


#### Final Project:

A restaurant website featuring a menu with 107 items that uses Flask to process requests and SQLite to store data such as users' credentials, menu items, categories, and orders. 

##### Outline
- Home: Welcome screen with an image carousel
- Menu: Displays items within each category, users can place orders if they're logged in (Add to Cart link is made available once they log in)
To create the webpage I pulled in the items from clayovenindy.com via scrapy (web scraping python module), stored them in a json format and then wrote a script to populate the database using the json object as per the relationships in the database.
- Gift Cards
- Cart: Execute order via this page
- Profile: Welcomes the user and displays username and past orders 
- Sign In/Up/Out: Create Account/Clears up session 

