# Unit 10 Assignment - SQL
# By: Arvinder Singh
### Create these queries to develop greater fluency in SQL, an important database language.

USE SAKILA; -- set to use sakila_db

## 1a. You need a list of all the actors who have Display the first and last names of all actors from the table `actor`. 
SELECT 
    first_name, last_name
FROM
    actor;

#1b. Display the first and last name of each actor in a single column in upper case letters. Name the column `Actor Name`. 
SELECT 
    *, UPPER(CONCAT(first_name, ' ', last_name)) AS Actor_Name
FROM
    actor;

# 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
SELECT 
    actor_id, first_name, last_name
FROM
    actor
WHERE
    first_name = 'Joe';
 
# 2b. Find all actors whose last name contain the letters `GEN`:
SELECT 
    actor_id, first_name, last_name
FROM
    actor
WHERE
    UPPER(last_name) LIKE  '%GEN%';

  	
# 2c. Find all actors whose last names contain the letters `LI`. This time, order the rows by last name and first name, in that order:
SELECT 
    actor_id, first_name, last_name
FROM
    actor
WHERE
    UPPER(last_name) LIKE  '%LI%'
ORDER BY last_name, first_name;

# 2d. Using `IN`, display the `country_id` and `country` columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT 
    country_id, country
FROM
    country
WHERE
    country IN ('Afghanistan' , 'Bangladesh', 'China');

# 3a. Add a `middle_name` column to the table `actor`. Position it between `first_name` and `last_name`. Hint: you will need to specify the data type.
ALTER TABLE actor
ADD COLUMN middle_name VARCHAR(20)
AFTER first_name;
  	
# 3b. You realize that some of these actors have tremendously long last names. Change the data type of the `middle_name` column to `blobs`.
ALTER TABLE actor
MODIFY COLUMN middle_name blob;

# 3c. Now delete the `middle_name` column.
ALTER TABLE actor
DROP COLUMN middle_name;

# 4a. List the last names of actors, as well as how many actors have that last name.
SELECT 
    last_name, COUNT(last_name)
FROM
    actor
GROUP BY last_name;
  	
# 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
SELECT 
    last_name, COUNT(last_name)
FROM
    actor
GROUP BY last_name
HAVING COUNT(last_name) >= 2;
  	
# 4c. Oh, no! The actor `HARPO WILLIAMS` was accidentally entered in the `actor` table as `GROUCHO WILLIAMS`, the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record.
SET SQL_SAFE_UPDATES = 0;
UPDATE actor 
SET 
    first_name = 'HARPO'
WHERE
    UPPER(first_name) = 'GROUCHO'
        AND UPPER(last_name) = 'WILLIAMS';
  	
# 4d. Perhaps we were too hasty in changing `GROUCHO` to `HARPO`. It turns out that `GROUCHO` was the correct name after all! In a single query, if the first name of the actor is currently `HARPO`, change it to `GROUCHO`. Otherwise, change the first name to `MUCHO GROUCHO`, as that is exactly what the actor will be with the grievous error. BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO `MUCHO GROUCHO`, HOWEVER! (Hint: update the record using a unique identifier.)
SET SQL_SAFE_UPDATES = 0;
UPDATE actor 
SET 
    first_name = 'GROUCHO'
WHERE
    UPPER(first_name) = 'HARPO'
        AND UPPER(last_name) = 'WILLIAMS';

# 5a. You cannot locate the schema of the `address` table. Which query would you use to re-create it?
-- Table structure for table `address`
--
CREATE TABLE address (
  address_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  address VARCHAR(50) NOT NULL,
  address2 VARCHAR(50) DEFAULT NULL,
  district VARCHAR(20) NOT NULL,
  city_id SMALLINT UNSIGNED NOT NULL,
  postal_code VARCHAR(10) DEFAULT NULL,
  phone VARCHAR(20) NOT NULL,
  /*!50705 location GEOMETRY NOT NULL,*/
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY  (address_id),
  KEY idx_fk_city_id (city_id),
  /*!50705 SPATIAL KEY `idx_location` (location),*/
  CONSTRAINT `fk_address_city` FOREIGN KEY (city_id) REFERENCES city (city_id) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

# 6a. Use `JOIN` to display the first and last names, as well as the address, of each staff member. Use the tables `staff` and `address`:
SELECT 
    first_name, last_name, address
FROM
    staff
        JOIN
    address ON staff.address_id = address.address_id;


# 6b. Use `JOIN` to display the total amount rung up by each staff member in August of 2005. Use tables `staff` and `payment`. 
SELECT 
    staff.staff_id, CONCAT(last_name, ',', first_name) AS staff_name, SUM(amount)
FROM
    staff
        JOIN
    payment ON staff.staff_id = payment.staff_id
GROUP BY payment.staff_id;
  	
# 6c. List each film and the number of actors who are listed for that film. Use tables `film_actor` and `film`. Use inner join.
SELECT 
    film.title, COUNT(actor_id) AS 'Number of Actors'
FROM
    film
        JOIN
    film_actor ON film.film_id = film_actor.film_id
GROUP BY film.film_id;

# 6d. How many copies of the film `Hunchback Impossible` exist in the inventory system?
SELECT 
    COUNT(*)
FROM
    inventory
WHERE
    film_id IN (SELECT 
            film_id
        FROM
            film
        WHERE
            title = 'Hunchback Impossible');

# 6e. Using the tables `payment` and `customer` and the `JOIN` command, list the total paid by each customer. List the customers alphabetically by last name:
SELECT 
    customer.customer_id, last_name, first_name, SUM(amount)
FROM
    customer
        JOIN
    payment ON customer.customer_id = payment.customer_id
GROUP BY customer.customer_id
ORDER BY last_name;

# 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters `K` and `Q` have also soared in popularity. Use subqueries to display the titles of movies starting with the letters `K` and `Q` whose language is English. 
SELECT 
    title
FROM
    film
WHERE
    (UPPER(title) LIKE 'K%'
        OR UPPER(title) LIKE 'Q%')
        AND language_id IN (SELECT 
            language_id
        FROM
            language
        WHERE
            name = 'English');

# 7b. Use subqueries to display all actors who appear in the film `Alone Trip`.
SELECT 
    CONCAT(last_name, ',', first_name) AS 'Actor Name'
FROM
    actor
WHERE
    actor_id IN (SELECT 
            actor_id
        FROM
            film_actor
        WHERE
            film_id IN (SELECT 
                    film_id
                FROM
                    film
                WHERE
                    title = 'Alone Trip'));

# 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
SELECT CONCAT(last_name,",",first_name) AS 'Customer Name', country.country FROM customer JOIN store ON customer.store_id=store.store_id
JOIN address ON store.address_id=address.address_id
JOIN city ON address.city_id=city.city_id
JOIN country ON city.country_id=country.country_id
WHERE country.country="Canada";

# 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
SELECT 
    title
FROM
    film
WHERE
    film_id IN (SELECT 
            film_id
        FROM
            film_category
        WHERE
            category_id IN (SELECT 
                    category_id
                FROM
                    category
                WHERE
                    name = 'Family'));

# 7e. Display the most frequently rented movies in descending order.
SELECT 
    title, COUNT(*) AS 'Number of Rentals'
FROM
    film
        JOIN
    inventory ON film.film_id = inventory.film_id
        JOIN
    rental ON inventory.inventory_id = rental.inventory_id
GROUP BY film.title
ORDER BY COUNT(*) DESC;
  	
# 7f. Write a query to display how much business, in dollars, each store brought in.
SELECT 
    inventory.store_id, SUM(amount) AS 'Total Amount ,in dollars'
FROM
    payment
        JOIN
    rental ON payment.rental_id = rental.rental_id
        JOIN
    inventory ON rental.inventory_id = inventory.inventory_id
GROUP BY inventory.store_id;

# 7g. Write a query to display for each store its store ID, city, and country.
SELECT 
    store_id, city.city, country.country
FROM
    store
        JOIN
    address ON store.address_id = address.address_id
        JOIN
    city ON address.city_id = city.city_id
        JOIN
    country ON city.country_id = country.country_id;
  	
# 7h. List the top five genres in gross revenue in descending order. (##Hint##: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
SELECT category.name, SUM(payment.amount) AS 'gross revenue' FROM category 
JOIN film_category ON category.category_id=film_category.category_id
JOIN inventory ON film_category.film_id=inventory.film_id
JOIN rental ON inventory.inventory_id=rental.inventory_id
JOIN payment ON rental.rental_id=payment.rental_id
GROUP BY category.name
ORDER BY SUM(payment.amount) DESC
LIMIT 5;

# 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
CREATE VIEW top_five_genres_by_grossrevenue AS
SELECT category.name, SUM(payment.amount) AS 'gross revenue' FROM category 
JOIN film_category ON category.category_id=film_category.category_id
JOIN inventory ON film_category.film_id=inventory.film_id
JOIN rental ON inventory.inventory_id=rental.inventory_id
JOIN payment ON rental.rental_id=payment.rental_id
GROUP BY category.name
ORDER BY SUM(payment.amount) DESC
LIMIT 5;

# 8b. How would you display the view that you created in 8a?
SELECT * FROM top_five_genres_by_grossrevenue;

# 8c. You find that you no longer need the view `top_five_genres`. Write a query to delete it.
DROP VIEW top_five_genres_by_grossrevenue;