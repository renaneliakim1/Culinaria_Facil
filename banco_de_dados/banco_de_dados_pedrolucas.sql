create database sitereceita;
use sitereceita;

create table usuario(
id int auto_increment primary key,
nome varchar(100) not null,
email varchar(100) not null unique,
senha varchar(255) not null,
cpf varchar(11) unique,
imagem_perfil varchar(255)
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
imagem_receita varchar(255),
video_receita varchar(255),
FOREIGN KEY (CategoriaID) REFERENCES categorias(categoriaID),
foreign key (autorID) references usuario(id)
);

CREATE TABLE comentarios (
id int auto_increment primary key, 
receitaID int,
usuarioID int,
comentario text,
data_hora datetime,
foreign key (receitaID) references receitas (receitaID),
foreign key (usuarioID) references usuario(id)
);

select * from receitas;

select * from usuario;

select * from comentarios;

insert into categorias(categorianome, descricao) values
('Vegano', 'Ajuda os animais'),
('Sem Glútem', 'Ajuda os animais'),
('Massas', 'Ajuda os animais'),
('Doces e Sobremesas', 'Ajuda os animais'),
('Bebidas e Drinks', 'Ajuda os animais'),
('Carnes', 'Ajuda os animais');
