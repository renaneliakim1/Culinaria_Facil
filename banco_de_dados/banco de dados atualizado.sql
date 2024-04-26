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

insert into categorias(categorianome, descricao) values('Vegano', 'Ajuda os animais');

INSERT INTO receitas (Titulo, Descricao, Instrucoes, ingredientes, TempoPreparo, Dificuldade, CategoriaID, AutorID, data_hora)
VALUES ('Bolo de Chocolate', 'Um delicioso bolo de chocolate para todas as ocasiões.', '1. Pré-aqueça o forno a 180°C. 2. Misture os ingredientes secos. 3. Adicione os ovos e o leite. 4. Asse por 30 minutos.', 'Farinha, açúcar, cacau em pó, ovos, leite', 30, 'Fácil', 1, 1, NOW()),
('Salada de Quinoa', 'Uma salada saudável e nutritiva.', '1. Cozinhe a quinoa. 2. Misture com legumes picados. 3. Tempere com azeite e limão.', 'Quinoa, tomate, pepino, cebola, azeite, limão', 20, 'Médio', 1, 2, NOW()),
('Hambúrguer de Lentilha', 'Um hambúrguer vegetariano rico em proteínas e sabor.', '1. Cozinhe a lentilha até ficar macia. 2. Amasse e misture com temperos e farinha. 3. Modele os hambúrgueres e grelhe.', 'Lentilha cozida, cebola, alho, cominho, páprica, farinha de trigo integral', 35, 'Médio', 1, 1, NOW()),
('Mousse de Chocolate Vegano', 'Uma sobremesa deliciosa e sem ingredientes de origem animal.', '1. Derreta o chocolate. 2. Bata com tofu e açúcar. 3. Leve à geladeira para firmar.', 'Chocolate meio amargo vegano, tofu firme, açúcar de coco', 120, 'Fácil', 1, 2, NOW()),
('Espaguete com Molho Pesto Vegano', 'Uma versão vegana do clássico italiano, cheia de sabor e frescor.', '1. Cozinhe o espaguete al dente. 2. Bata manjericão, nozes, alho e azeite. 3. Misture com o espaguete e sirva.', 'Espaguete, manjericão fresco, nozes, alho, azeite de oliva extra virgem', 25, 'Fácil', 1, 1, NOW()),
('Chilli Vegano', 'Um prato reconfortante, cheio de sabor e textura.', '1. Refogue cebola, pimentão e alho. 2. Adicione feijão, tomate e temperos. 3. Cozinhe até engrossar.', 'Feijão preto cozido, tomate, cebola, pimentão, alho, cominho, páprica, pimenta', 40, 'Médio', 1, 2, NOW()),
('Pudim de Chia Vegano', 'Uma sobremesa saudável e fácil de preparar, rica em ômega-3 e fibras.', '1. Misture leite vegetal com sementes de chia e açúcar. 2. Deixe descansar na geladeira por algumas horas.', 'Leite de amêndoas, sementes de chia, açúcar de coco', 180, 'Fácil', 1, 1, NOW());