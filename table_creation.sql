DROP TABLE order_item
DROP TABLE cart_item
DROP TABLE vendor_application
DROP TABLE "order"
DROP TABLE product
DROP TABLE cart
DROP TABLE product_category
DROP TABLE "user"

CREATE TABLE "user" (
	id SERIAL NOT NULL, 
	email TEXT NOT NULL, 
	first_name VARCHAR(50) NOT NULL, 
	last_name VARCHAR(50) NOT NULL, 
	phone_number VARCHAR(20) NOT NULL, 
	password VARCHAR(128) NOT NULL, 
	password_plain TEXT NOT NULL, 
	is_vendor BOOLEAN NOT NULL, 
	is_admin BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
)

CREATE TABLE product_category (
	id SERIAL NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id)
)

CREATE TABLE cart (
	id SERIAL NOT NULL, 
	owner_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES "user" (id)
)

CREATE TABLE product (
	id SERIAL NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(1024) NOT NULL, 
	price NUMERIC(8, 2) NOT NULL CHECK (price > 0), 
	stock INTEGER NOT NULL CHECK (stock >= 0), 
	is_listed BOOLEAN NOT NULL, 
	vendor_id INTEGER, 
	category_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(vendor_id) REFERENCES "user" (id), 
	FOREIGN KEY(category_id) REFERENCES product_category (id)
)

CREATE TABLE "order" (
	id SERIAL NOT NULL, 
	customer_id INTEGER NOT NULL, 
	is_complete BOOLEAN NOT NULL, 
	is_filled BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	completed_at TIMESTAMP WITHOUT TIME ZONE, 
	delivery_charge NUMERIC(8, 2) NOT NULL CHECK (delivery_charge >= 0), 
	taxes NUMERIC(8, 2) NOT NULL CHECK (taxes >= 0), 
	sub_total NUMERIC(8, 2) NOT NULL CHECK (sub_total >= 0), 
	total NUMERIC(8, 2) NOT NULL CHECK (total >= 0), 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_id) REFERENCES "user" (id)
)

CREATE TABLE vendor_application (
	id SERIAL NOT NULL, 
	owner_id INTEGER NOT NULL, 
	title VARCHAR(100) NOT NULL, 
	description VARCHAR(1024) NOT NULL, 
	approved BOOLEAN, 
	completed_by_id INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	completed_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES "user" (id), 
	FOREIGN KEY(completed_by_id) REFERENCES "user" (id)
)

CREATE TABLE cart_item (
	cart_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	quantity INTEGER NOT NULL CHECK (quantity > 0), 
	PRIMARY KEY (cart_id, product_id), 
	FOREIGN KEY(cart_id) REFERENCES cart (id) ON DELETE CASCADE, 
	FOREIGN KEY(product_id) REFERENCES product (id)
)

CREATE TABLE order_item (
	order_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	product_price NUMERIC(8, 2) NOT NULL CHECK (product_price >= 0), 
	product_quantity INTEGER NOT NULL CHECK (product_quantity > 0), 
	sub_total NUMERIC(8, 2) NOT NULL CHECK (sub_total >= 0), 
	is_delivered BOOLEAN NOT NULL, 
	PRIMARY KEY (order_id, product_id), 
	FOREIGN KEY(order_id) REFERENCES "order" (id) ON DELETE CASCADE, 
	FOREIGN KEY(product_id) REFERENCES product (id)
)