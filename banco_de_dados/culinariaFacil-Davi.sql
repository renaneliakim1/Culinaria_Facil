CREATE DATABASE biblioteca_virtual;
USE biblioteca_virtual;

-- Adicionei a restrição NOT NULL a todas as colunas para garantir que elas não possam conter valores NULL.
-- Reduzi o tamanho do campo categoriaNome de VARCHAR(80) para VARCHAR(50).

CREATE TABLE categorias (
  categoriaid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  categorianome VARCHAR(50) NOT NULL,
  descricao TEXT NOT NULL
);

-- Reduzi o tamanho dos campos NOMEUSUARIO e EMAIL para 50 caracteres. .
-- Mudei o tipo de dados do campo SENHA para CHAR(8).
-- Mudei o tipo de dados do campo CPF para CHAR(11). Isso é suficiente para armazenar um CPF sem formatação (apenas números) e economiza espaço em comparação com VARCHAR(14).
-- Adicionei a restrição NOT NULL aos campos NOMEUSUARIO e EMAIL para garantir que cada usuário tenha um nome e um email.
-- Adicionei a restrição UNIQUE aos campos EMAIL e CPF para garantir que cada usuário tenha um email e um CPF únicos.

CREATE TABLE usuarios (
usuarioid INT AUTO_INCREMENT PRIMARY KEY,
nomeusuario VARCHAR(50) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
senha CHAR(8),
cpf CHAR(11) UNIQUE
);

-- Reduzi o tamanho do campo TITULO para 40 caracteres. Isso pode economizar espaço se você souber que o título não excederá esse limite.
-- Adicionei o tipo de dados BLOB para o campo VIDEO, supondo armazenar vídeos.
-- Mudei o tipo de dados do campo TEMPOPREPARO para SMALLINT, que é suficiente para armazenar minutos e economiza espaço em comparação com INT.
-- Mudei o tipo de dados do campo DIFICULDADE para ENUM. Isso pode melhorar a eficiência se você tiver um número fixo de níveis de dificuldade.
-- Adicionei a restrição NOT NULL ao campo TITULO para garantir que cada receita tenha um título.

CREATE TABLE receitas (
receitaid INT AUTO_INCREMENT PRIMARY KEY,
titulo VARCHAR(40) NOT NULL,
descricao TEXT,
imagem BLOB,
video BLOB,
instrucoes TEXT,
tempopreparo SMALLINT,
dificuldade ENUM('Fácil', 'Médio', 'Difícil'),
categoria_id INT,
FOREIGN KEY (categoriaid) REFERENCES categorias(categoriaid)
);

-- Reduzi o tamanho do campo NOME para 50 caracteres. Isso pode economizar espaço se você souber que o nome do ingrediente não excederá esse limite.
-- Mudei o tipo de dados do campo QUANTIDADE para DECIMAL(5,2), que é suficiente para a maioria das receitas e economiza espaço em comparação com DECIMAL(10,2).
-- Mudei o tipo de dados do campo UNIDADEMEDIDA para ENUM. Isso pode melhorar a eficiência se você tiver um número fixo de unidades de medida.
-- Adicionei a restrição NOT NULL ao campo NOME para garantir que cada ingrediente tenha um nome.

CREATE TABLE ingredientes (
ingredienteid INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(50) NOT NULL,
quantidade DECIMAL(5,2),
unidademedida ENUM('g', 'kg', 'ml', 'l', 'colher de sopa', 'colher de chá', 'xícara', 'unidade'),
receitaid INT,
FOREIGN KEY (receitaid) REFERENCES receitas(receitaid)
);

-- Adicionei a restrição NOT NULL a todas as colunas para garantir que elas não possam conter valores NULL.

CREATE TABLE modopreparo (
preparoid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
receitaid INT NOT NULL,
ordempreparo INT NOT NULL,
descricao TEXT NOT NULL,
PRIMARY KEY (preparoid),
FOREIGN KEY (receitaid) REFERENCES receitas (receitaid)
);

-- Adicionei a restrição NOT NULL a todas as colunas para garantir que elas não possam conter valores NULL.

CREATE TABLE comentarios (
receitaid INT NOT NULL,
usuarioid INT NOT NULL,
comentario TEXT NOT NULL,
datahora DATETIME NOT NULL,
FOREIGN KEY (receitaid) REFERENCES receitas (receitaid),
FOREIGN KEY (usuarioid) REFERENCES usuarios (usuarioid)
);

create view ReceitasPorCategoria AS
select rs.receitaID, rs.Titulo, rs.Descricao, rs.Instrucoes, rs.TempoPreparo, rs.Dificuldade, ct.categoriaNome 
from receitas rs 
join categorias ct on rs.categoriaID = ct.categoriaID;

SELECT * FROM ReceitasPorCategoria WHERE categoriaNome = 'Lanches';

INSERT INTO categorias (categoriaNome, Descricao) VALUES
('Sobremesas', 'Receitas de deliciosas sobremesas'),
('Pratos Principais', 'Receitas para o prato principal'),
('Lanches', 'Receitas rápidas e saborosas para lanches'),
('Saladas', 'Receitas de saladas refrescantes');

INSERT INTO usuarios (CPF, NomeUsuario, Email, Senha) VALUES
('111.222.333-44', 'Joao', 'joao@example.com', 'senha123'),
('222.333.444-55', 'Maria', 'maria@example.com', 'senha456'),
('333.444.555-66', 'Pedro', 'pedro@example.com', 'senha789');

INSERT INTO receitas (Titulo, Descricao, Instrucoes, TempoPreparo, Dificuldade, CategoriaID) VALUES
(1, 'Pudim de Leite Condensado', 'Delicioso pudim cremoso feito com leite condensado.', '1. Misture o leite condensado com os ovos.\n2. Adicione o leite e misture bem.\n3. Caramelize uma forma e despeje a mistura.\n4. Asse em banho-maria por 1 hora.', 60, 'Fácil', 1),
(2, 'Lasanha de Frango', 'Uma lasanha deliciosa e reconfortante feita com frango.', '1. Cozinhe o frango e desfie.\n2. Faça um molho branco.\n3. Monte a lasanha em camadas alternadas de massa, molho branco, frango desfiado e queijo.\n4. Asse no forno por 30 minutos.', 90, 'Média', 2),
(3, 'Sanduíche Natural', 'Um lanche saudável e delicioso com recheio de frango.', '1. Cozinhe o peito de frango e desfie.\n2. Misture o frango desfiado com maionese e temperos a gosto.\n3. Monte o sanduíche com alface, tomate, e o recheio de frango.\n4. Sirva gelado.', 15, 'Fácil', 3);

INSERT INTO ingredientes (nome, quantidade, unidadeMedida, receitaID) VALUES
(1, 'Leite condensado', 1, 'lata', 1),
(2, 'Ovos', 4, 'unidades', 1),
(3, 'Leite', 500, 'ml', 1),
(4, 'Frango', 500, 'g', 2),
(5, 'Massa de lasanha', 1, 'pacote', 2),
(6, 'Queijo', 200, 'g', 2),
(7, 'Peito de frango', 300, 'g', 3),
(8, 'Pão de forma integral', 6, 'fatias', 3);

INSERT INTO modo_preparo (receitaID, ordem_preparo, descricao) VALUES
(1, 1, 'Misture o leite condensado com os ovos.'),
(1, 2, 'Adicione o leite e misture bem.'),
(1, 3, 'Caramelize uma forma e despeje a mistura.'),
(1, 4, 'Asse em banho-maria por 1 hora.'),
(2, 1, 'Cozinhe o frango e desfie.'),
(2, 2, 'Faça um molho branco.'),
(2, 3, 'Monte a lasanha em camadas alternadas de massa, molho branco, frango desfiado e queijo.'),
(2, 4, 'Asse no forno por 30 minutos.'),
(3, 1, 'Cozinhe o peito de frango e desfie.'),
(3, 2, 'Misture o frango desfiado com maionese e temperos a gosto.'),
(3, 3, 'Monte o sanduíche com alface, tomate, e o recheio de frango.'),
(3, 4, 'Sirva gelado.');

INSERT INTO comentarios (receitaID, usuarioID, cometario, data_hora) VALUES
(1, 1, 'Essa receita é maravilhosa!', NOW()),
(1, 2, 'Fiz esse pudim para o aniversário da minha mãe e todos adoraram.', NOW()),
(2, 1, 'A lasanha de frango ficou deliciosa!', NOW());