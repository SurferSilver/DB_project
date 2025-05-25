import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='avatarbajsA_1!',
    database='PROJECT'
)
cursor = conn.cursor()

# ------------------------------
# Utility to call SQL function
def call_function(func_name, *args):
    cursor.execute(f"SELECT {func_name}({', '.join(['%s']*len(args))})", args)
    result = cursor.fetchone()
    return result[0] if result else None

# ------------------------------
# Call stored procedure
def call_procedure(proc_name, *args):
    cursor.callproc(proc_name, args)
    conn.commit()

# ------------------------------
# Insert mock data (optional setup)
def insert_test_data():
    cursor.execute("DELETE FROM Shopping_Lists")
    cursor.execute("DELETE FROM Meal_Ingredients")
    cursor.execute("DELETE FROM Meals")
    cursor.execute("DELETE FROM Ingredients")
    cursor.execute("DELETE FROM Users")
    
    cursor.execute("INSERT INTO Users (user_id, name, email, allergies) VALUES (1, 'Alice', 'alice@example.com', 'nuts')")
    
    cursor.execute("""
    INSERT INTO Ingredients (ingredient_id, name, is_vegetarian, price, calories, protein, allergy_tags)
    VALUES 
    (1, 'Falukorv', FALSE, 3.0, 36, 12.0, NULL),
    (2, 'Gul lök', TRUE, 0.5, 13, 1.1, NULL),
    (3, 'Tomatpuré', TRUE, 1.0, 26, 1.5, NULL),
    (4, 'Dijonsenap', TRUE, 1.2, 27, 0.5, NULL),
    (5, 'Grädde', TRUE, 1.5, 30, 2.0, 'dairy'),
    (6, 'Halloumi', TRUE, 4.0, 29, 20.0, 'dairy'),
    (7, 'Vitlök', TRUE, 0.3, 10, 0.5, NULL),
    (8, 'Krossade tomater', TRUE, 1.0, 15, 1.0, NULL),
    (9, 'Grönsaksbuljongtärning', TRUE, 0.5, 15, 0.5, NULL),
    (10, 'Morötter', TRUE, 0.7, 12, 0.9, NULL),
    (11, 'Balsamvinäger', TRUE, 1.0, 35, 0.0, NULL),
    (12, 'Torkad timjan', TRUE, 0.5, 5, 0.0, NULL),
    (13, 'Rapsolja', TRUE, 1.0, 68, 0.0, NULL),
    (14, 'Ris', TRUE, 1.5, 30, 2.5, NULL),
    (15, 'Kycklingfilé', FALSE, 4.0, 70, 31.0, NULL),
    (16, 'Jordnötter', TRUE, 1.5, 60, 25.8, 'nuts'),
    (17, 'Sojasås', TRUE, 0.8, 50, 8.0, 'soy'),
    (18, 'Paprika', TRUE, 0.7, 20, 0.9, NULL),
    (19, 'Vitlök', TRUE, 0.3, 10, 0.5, NULL),
    (20, 'Sesamolja', TRUE, 1.2, 120, 0.0, 'sesame')
    """)

    cursor.execute("""
    INSERT INTO Meals (meal_id, name, recipe_url, total_cost, total_calories, total_protein, is_vegetarian)
    VALUES
    (1, 'Korv Stroganoff', 'https://www.koket.se/sara_begner/soppor_och_grytor/korv_och_chark/korv_stroganoff', 7.2, 585, 16.6, FALSE),
    (2, 'Halloumi Stroganoff med ris', 'https://www.koket.se/halloumi-stroganoff-med-ris', 10.5, 700, 25.0, TRUE),
    (3, 'Peanut Chicken Stir-Fry', 'https://www.koket.se/peanut-chicken-stir-fry', 8.5, 750, 40.0, FALSE)
    """)

    cursor.execute("""
    INSERT INTO Meal_Ingredients (meal_id, ingredient_id, quantity)
    VALUES 
    (1, 1, '500g'),
    (1, 2, '1 st'),
    (1, 3, '3 msk'),
    (1, 4, '2 tsk'),
    (1, 5, '2 dl'),
    (2, 6, '400g'),
    (2, 2, '2 st'),
    (2, 7, '2 klyftor'),
    (2, 3, '3 msk'),
    (2, 8, '400g'),
    (2, 9, '1 tärning'),
    (2, 10, '2 st'),
    (2, 4, '1 msk'),
    (2, 11, '1 msk'),
    (2, 12, '2 tsk'),
    (2, 13, '0.5 msk'),
    (2, 14, '2 dl'),
    (3, 15, '200g'),
    (3, 16, '50g'),
    (3, 17, '2 msk'),
    (3, 18, '1 st'),
    (1, 19, '2 klyftor'),
    (3, 20, '1 msk')
    """)



    conn.commit()

# ------------------------------
insert_test_data()
print(' ')
print("Safe meals for user 1:", call_function("GetSafeMeals", 1))
call_procedure("AddMealToShoppingList", 1, 1)
print(' ')
print("Shopping ingredients for user 1:", call_function("GetUserShoppingIngredients", 1))
print(' ')
print("Vegetarian meals under SEK60:", call_function("GetVegMealsUnderBudget", 60.00))
print(' ')
print("Meals sorted by protein:", call_function("GetMealsByProtein"))

cursor.close()
conn.close()
