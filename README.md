A simple **FastAPI** application using **SQLite** as the database, with support for **Users** and **Todos**.  
This project demonstrates basic CRUD operations, user management, and database integration using FastAPI.
mysql> create database TodoApplicationDatabase;
Query OK, 1 row affected (0.02 sec)

mysql> use TodoApplicationDatabase;
Database changed
mysql> CREATE TABLE `users` (
    ->   `id` INT NOT NULL AUTO_INCREMENT,
    ->   `email` VARCHAR(255) NOT NULL,
    ->   `username` VARCHAR(255) NOT NULL,
    ->   `first_name` VARCHAR(255),
    ->   `last_name` VARCHAR(255),
    ->   `hashed_password` VARCHAR(255) NOT NULL,
    ->   `is_active` TINYINT(1) DEFAULT 1,
    ->   `role` VARCHAR(255),
    ->
    ->   PRIMARY KEY (`id`),
    ->   UNIQUE KEY `uq_users_email` (`email`),
    ->   UNIQUE KEY `uq_users_username` (`username`)
    -> ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
Query OK, 0 rows affected, 1 warning (0.12 sec)

mysql> CREATE TABLE `todos` (
    ->   `id` INT NOT NULL AUTO_INCREMENT,
    ->   `title` VARCHAR(255) NOT NULL,
    ->   `description` VARCHAR(255),
    ->   `priority` INT,
    ->   `complete` TINYINT(1) DEFAULT 0,
    ->   `owner_id` INT NOT NULL,
    ->
    ->   PRIMARY KEY (`id`),
    ->   CONSTRAINT `fk_todos_users`
    ->     FOREIGN KEY (`owner_id`)
    ->     REFERENCES `users` (`id`)
    ->     ON DELETE CASCADE
    -> ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;