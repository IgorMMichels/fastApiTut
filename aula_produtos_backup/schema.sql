CREATE DATABASE IF NOT EXISTS petshop CHARACTER SET utf8mb4;
USE petshop;

CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);

INSERT INTO produtos (nome, categoria, preco) VALUES
('Ração Premium 10kg', 'Alimentação', 159.90),
('Coleira Ajustável', 'Acessórios', 29.90),
('Shampoo Pet 500ml', 'Higiene', 24.50),
('Bolinha de Borracha', 'Brinquedos', 12.00);
