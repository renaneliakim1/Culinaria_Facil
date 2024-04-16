CREATE DATABASE biblioteca_virtual;
USE biblioteca_virtual;

CREATE TABLE categorias (
categoriaID INT AUTO_INCREMENT PRIMARY KEY,
categoriaNome VARCHAR(200),
Descricao TEXT
);

CREATE TABLE usuarios (
usuarioID INT AUTO_INCREMENT  PRIMARY KEY,
NomeUsuario VARCHAR(55),
Email VARCHAR(55),
Senha VARCHAR(8)
);

CREATE TABLE receitas (
receitaID INT PRIMARY KEY,
Titulo VARCHAR(55),
Descricao TEXT,
Instrucoes TEXT,
TempoPreparo INT,
Dificuldade VARCHAR(50),
CategoriaID INT,
FOREIGN KEY (CategoriaID) REFERENCES categorias(categoriaID)
);

CREATE TABLE ingredientes (
ingredienteID INT PRIMARY KEY,
nome VARCHAR(70),
quantidade DECIMAL(10,2),
unidadeMedida VARCHAR(100),
receitaID INT,
FOREIGN KEY (receitaID) REFERENCES receitas(receitaID)
);

CREATE TABLE modo_preparo (
preparoID int auto_increment primary key,
receitaID int,
ordem_preparo int,
descricao text,
foreign key (receitaID) references receitas (receitaID)
);

CREATE TABLE comentarios (
receitaID int,
usuarioID int,
cometario text,
data_hora datetime,
foreign key (receitaID) references receitas (receitaID),
foreign key (usuarioID) references usuarios (usuarioID)
);

-- Exemplo de um banco bem mais otimizado ( segundo meu conhecimento , pode estar errado )
-- Os index são maneira de fazer buscar mais otimizadas 

-- CREATE DATABASE biblioteca_virtual;
-- USE biblioteca_virtual;

-- CREATE TABLE categorias (
-- categoriaID INT AUTO_INCREMENT PRIMARY KEY,
-- categoriaNome VARCHAR(255) NOT NULL,
-- Descricao TEXT
-- );

-- CREATE TABLE usuarios (
-- usuarioID INT AUTO_INCREMENT  PRIMARY KEY,
-- NomeUsuario VARCHAR(55) NOT NULL,
-- Email VARCHAR(55) NOT NULL UNIQUE,
-- Senha VARCHAR(10) NOT NULL
-- );

-- CREATE TABLE receitas (
-- receitaID INT PRIMARY KEY,
-- Titulo VARCHAR(55) NOT NULL,
-- Descricao TEXT,
-- Instrucoes TEXT,
-- TempoPreparo INT UNSIGNED,
-- Dificuldade ENUM('Fácil', 'Médio', 'Difícil'),
-- CategoriaID INT,
-- FOREIGN KEY (CategoriaID) REFERENCES categorias(categoriaID)
-- );

-- CREATE INDEX idx_receitas_CategoriaID ON receitas(CategoriaID);

-- CREATE TABLE ingredientes (
-- ingredienteID INT PRIMARY KEY,
-- nome VARCHAR(100) NOT NULL,
-- quantidade DECIMAL(10,2) UNSIGNED,
-- unidadeMedida ENUM('g', 'kg', 'ml', 'l', 'colher de sopa', 'colher de chá', 'xícara', 'unidade'),
-- receitaID INT,
-- FOREIGN KEY (receitaID) REFERENCES receitas(receitaID)
-- );

-- CREATE INDEX idx_ingredientes_receitaID ON ingredientes(receitaID);

-- CREATE TABLE modo_preparo (
-- preparoID int auto_increment primary key,
-- receitaID int,
-- ordem_preparo int UNSIGNED,
-- descricao text,
-- foreign key (receitaID) references receitas (receitaID)
-- );

-- CREATE INDEX idx_modo_preparo_receitaID ON modo_preparo(receitaID);

-- CREATE TABLE comentarios (
-- receitaID int,
-- usuarioID int,
-- cometario text,
-- data_hora datetime,
-- foreign key (receitaID) references receitas (receitaID),
-- foreign key (usuarioID) references usuarios (usuarioID)
-- );

-- CREATE INDEX idx_comentarios_receitaID ON comentarios(receitaID);
-- CREATE INDEX idx_comentarios_usuarioID ON comentarios(usuarioID);
