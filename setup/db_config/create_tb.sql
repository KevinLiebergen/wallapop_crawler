
use wallapop_db;

CREATE TABLE vendedor(
	id INT NOT NULL AUTO_INCREMENT,
	barrio INT,
	ciudad VARCHAR(30),
	puntuacion VARCHAR(4),
	PRIMARY KEY ( id)
);
 
CREATE TABLE busqueda(
	id INT NOT NULL AUTO_INCREMENT,
	busqueda VARCHAR(70),
	PRIMARY KEY ( id)
);

CREATE TABLE productos(
	id_producto INT NOT NULL AUTO_INCREMENT,
	titulo VARCHAR(50),
	precio INT,
	url VARCHAR(150),
	imagen VARCHAR(150),
	id_vendedor INT, 
	id_busqueda INT,
	PRIMARY KEY (id_producto),
	FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id),
	FOREIGN KEY (id_busqueda) REFERENCES Busqueda(id)
);
