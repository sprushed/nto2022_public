CREATE DATABASE nto;

USE nto;

DROP TABLE IF EXISTS `users`;
CREATE TABLE users (
  id INT AUTO_INCREMENT,
  username varchar(50) NOT NULL,
  password varchar(50) NOT NULL,
  is_admin BOOLEAN NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (username)
);

INSERT INTO `users` (username, password, is_admin)
VALUES ('admin','b7dc41bdfcda8a3df728807f9babe74c',TRUE);

FLUSH PRIVILEGES;

CREATE USER 'moderator'@'%' IDENTIFIED WITH mysql_native_password BY 'moderator';
GRANT USAGE,SELECT,INSERT ON nto.users TO 'moderator'@'%';