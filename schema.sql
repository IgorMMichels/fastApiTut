CREATE DATABASE IF NOT EXISTS petshop CHARACTER SET utf8mb4;
USE petshop;

CREATE TABLE IF NOT EXISTS tutores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raca VARCHAR(50),
    data_nascimento DATE,
    tutor_id INT NOT NULL,
    FOREIGN KEY (tutor_id) REFERENCES tutores(id)
);

INSERT INTO tutores (nome, telefone, email) VALUES
('Maria Silva', '51999990001', 'maria@email.com'),
('João Souza', '51999990002', 'joao@email.com');

INSERT INTO pets (nome, especie, raca, data_nascimento, tutor_id) VALUES
('Rex', 'Cachorro', 'Labrador', '2020-03-10', 1),
('Mia', 'Gato', 'Siamês', '2021-07-22', 1),
('Thor', 'Cachorro', 'Bulldog', '2019-11-05', 2);
