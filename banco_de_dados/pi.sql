create database sitereceita;
use sitereceita;

create table usuario(
id int auto_increment primary key,
nome varchar(100) not null,
email varchar(100) not null unique,
senha varchar(255) not null
);



CREATE TABLE categorias (
categoriaID INT AUTO_INCREMENT PRIMARY KEY,
categoriaNome VARCHAR(200),
Descricao TEXT
);

CREATE TABLE receitas (
receitaID INT AUTO_INCREMENT PRIMARY KEY,
Titulo VARCHAR(55),
Descricao TEXT,
Instrucoes TEXT,
ingredientes TEXT,
TempoPreparo INT,
Dificuldade VARCHAR(50),
CategoriaID INT,
AutorID INT,
data_hora datetime,
FOREIGN KEY (CategoriaID) REFERENCES categorias(categoriaID),
foreign key (autorID) references usuario(id)
);

CREATE TABLE comentarios (
receitaID int,
usuarioID int,
cometario text,
data_hora datetime,
foreign key (receitaID) references receitas (receitaID),
foreign key (usuarioID) references usuario(id)
);

insert into categorias(categorianome, descricao) values('Vegano', 'Ajuda os animais');

select * from receitas;


INSERT INTO receitas (Titulo, Descricao, Instrucoes, ingredientes, TempoPreparo, Dificuldade, CategoriaID, AutorID, data_hora)
VALUES ('Bolo de Chocolate', 'Um delicioso bolo de chocolate para todas as ocasiões.', '1. Pré-aqueça o forno a 180°C. 2. Misture os ingredientes secos. 3. Adicione os ovos e o leite. 4. Asse por 30 minutos.', 'Farinha, açúcar, cacau em pó, ovos, leite', 30, 'Fácil', 1, 1, NOW());

-- Exemplo 2:
INSERT INTO receitas (Titulo, Descricao, Instrucoes, ingredientes, TempoPreparo, Dificuldade, CategoriaID, AutorID, data_hora)
VALUES ('Salada de Quinoa', 'Uma salada saudável e nutritiva.', '1. Cozinhe a quinoa. 2. Misture com legumes picados. 3. Tempere com azeite e limão.', 'Quinoa, tomate, pepino, cebola, azeite, limão', 20, 'Médio', 1, 2, NOW());