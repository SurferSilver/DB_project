USE PROJECT;

-- 1. Users table
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    allergies TEXT -- comma-separated list or JSON if needed
);

-- 2. Ingredients table
CREATE TABLE Ingredients (
    ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    is_vegetarian BOOLEAN,
    price DECIMAL(6,2),
    calories INT,
    protein DECIMAL(5,2),
    allergy_tags TEXT -- comma-separated tags (e.g., 'nuts,gluten')
);

-- 3. Meals (Recipes) table
CREATE TABLE Meals (
    meal_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    recipe_url TEXT NOT NULL,
    total_cost DECIMAL(6,2),
    total_calories INT,
    total_protein DECIMAL(5,2),
    is_vegetarian BOOLEAN
);

-- 4. Meal_Ingredients junction table (many-to-many)
CREATE TABLE Meal_Ingredients (
    meal_id INT,
    ingredient_id INT,
    quantity VARCHAR(100),
    PRIMARY KEY (meal_id, ingredient_id),
    FOREIGN KEY (meal_id) REFERENCES Meals(meal_id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id) ON DELETE CASCADE
);

-- 5. Shopping_Lists table
CREATE TABLE Shopping_Lists (
    list_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    meal_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (meal_id) REFERENCES Meals(meal_id) ON DELETE CASCADE
);


-- 1. Function to get meals excluding user allergies
DELIMITER //
CREATE FUNCTION GetSafeMeals(userId INT)
RETURNS TEXT
DETERMINISTIC
BEGIN
    RETURN (
        SELECT GROUP_CONCAT(DISTINCT CONCAT(m.name, ' (', m.recipe_url, ')') SEPARATOR ', ')
        FROM Meals m
        WHERE NOT EXISTS (
            SELECT 1
            FROM Meal_Ingredients mi
            JOIN Ingredients i ON mi.ingredient_id = i.ingredient_id
            JOIN Users u ON u.user_id = userId
            WHERE mi.meal_id = m.meal_id
              AND i.allergy_tags IS NOT NULL
              AND (
                  u.allergies LIKE CONCAT('%', i.allergy_tags, '%')
              )
        )
    );
END;
//
DELIMITER ;

-- 2. Procedure to add a meal to shopping list
DELIMITER //
CREATE PROCEDURE AddMealToShoppingList(IN uid INT, IN mid INT)
BEGIN
    INSERT INTO Shopping_Lists (user_id, meal_id)
    VALUES (uid, mid);
END;//
DELIMITER ;

-- 3. Function to list all ingredients in a user’s shopping list
DELIMITER //
CREATE FUNCTION GetUserShoppingIngredients(uid INT)
RETURNS TEXT
DETERMINISTIC
BEGIN
    RETURN (
        SELECT GROUP_CONCAT(DISTINCT i.name SEPARATOR ', ')
        FROM Shopping_Lists sl
        JOIN Meal_Ingredients mi ON sl.meal_id = mi.meal_id
        JOIN Ingredients i ON mi.ingredient_id = i.ingredient_id
        WHERE sl.user_id = uid
    );
END;//
DELIMITER ;

-- 4. Function to get vegetarian meals under budget
DELIMITER //
CREATE FUNCTION GetVegMealsUnderBudget(budget DECIMAL(6,2))
RETURNS TEXT
DETERMINISTIC
BEGIN
    RETURN (
        SELECT GROUP_CONCAT(CONCAT(name, ' (', recipe_url, ')') SEPARATOR ', ')
        FROM Meals
        WHERE is_vegetarian = TRUE AND total_cost < budget
    );
END;
//
DELIMITER ;

-- 5. Function to get meals sorted by protein content
DELIMITER //
CREATE FUNCTION GetMealsByProtein()
RETURNS TEXT
DETERMINISTIC
BEGIN
    RETURN (
        SELECT GROUP_CONCAT(CONCAT(name, ' (', recipe_url, ')') ORDER BY total_protein DESC SEPARATOR ', ')
        FROM Meals
    );
END;
//
DELIMITER ;
