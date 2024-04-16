CREATE DATABASE biblioteca_virtual;
USE biblioteca_virtual;

CREATE TABLE categorias (
categoriaID INT AUTO_INCREMENT PRIMARY KEY,
categoriaNome VARCHAR(255),
Descricao TEXT
);

CREATE TABLE usuarios (
usuarioID INT AUTO_INCREMENT  PRIMARY KEY,
NomeUsuario VARCHAR(55),
Email VARCHAR(55),
Senha VARCHAR(55)
);

CREATE TABLE receitas (
receitaID INT PRIMARY KEY,
Titulo VARCHAR(55),
Descricao TEXT,
Instrucoes TEXT,
TempoPreparo INT,
Dificuldade VARCHAR(50),
CategoriaID INT,
FOREIGN KEY (CategoriaID) REFERENCES Categoria(categoriaID)
);

CREATE TABLE ingredientes (
ingredienteID INT PRIMARY KEY,
nome VARCHAR(255),
quantidade DECIMAL(10,2),
unidadeMedida VARCHAR(100),
receitaID INT,
FOREIGN KEY (ReceitaID) REFERENCES Receita(receitaID)
);

CREATE TABLE modo_preparo (
preparoID int auto_increment primary key,
receitaID int,
ordem_preparo int,
descricao text,
foreign key (receitaID) references receita (receitaID)
);

CREATE TABLE comentarios (
receitaID int,
usuarioID int,
cometario text,
data_hora datetime,
foreign key (receitaID) references receitas (receitaID),
foreign key (usuarioID) references usuarios (usuarioID)
);