import sqlite3
import json

# with sqlite3.connect('restaurant.db') as db:
    
file = open('menu_cleaned.json', 'r')
menu = json.load(file)
   
catgID = 0 
with sqlite3.connect('restaurant.db') as conn:
    db = conn.cursor()
    for i in menu:
        # category: print(i)
        #db.execute('INSERT INTO category (type) VALUES (?)', [str(i)])
        
        # cycling through items under a category
        for j in menu[i]:    
            #print(f'{i}:, {j} \n{menu[i][j]["price"]}\n {menu[i][j]["desc"]}')
            catgID = db.execute('SELECT id FROM category WHERE type = ?', [i]).fetchall()[0][0]
            #print(catgID)
            #db.execute('INSERT INTO items (item, desc, price, categoryID) VALUES (?, ?, ?, ?)', (str(j), str(menu[i][j]["desc"]), float(menu[i][j]["price"]), int(catgID)))
            #db.execute('UPDATE items SET categoryID = ? WHERE item = ?', (catgID, j))
            
            # fixing T. Shrimp appetizer's catg id
            db.execute('UPDATE items SET categoryID = ? WHERE id = ?', (1, 5))