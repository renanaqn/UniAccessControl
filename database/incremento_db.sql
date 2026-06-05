-- ==========================================
-- ZONAS ADICIONAIS
-- ==========================================

INSERT INTO zonas (nome_zona) VALUES
('Biblioteca'),
('Laboratorio de Quimica'),
('Centro de Pesquisa'),
('Sala de Servidores');

-- ==========================================
-- REGRAS DE ACESSO
-- ==========================================

INSERT INTO regras_acesso
(zona_id, perfil_id, hora_inicio, hora_fim)
VALUES

-- Biblioteca
(5, 1, '06:00:00', '23:00:00'),
(5, 2, '07:00:00', '22:00:00'),
(5, 3, '05:00:00', '23:00:00'),
(5, 5, '07:00:00', '23:00:00'),

-- Laboratório de Química
(6, 1, '07:00:00', '20:00:00'),
(6, 4, '07:00:00', '19:00:00'),
(6, 5, '08:00:00', '22:00:00'),

-- Centro de Pesquisa
(7, 1, '07:00:00', '22:00:00'),
(7, 5, '08:00:00', '23:00:00'),

-- Sala de Servidores
(8, 3, '05:00:00', '23:00:00'),
(8, 4, '07:00:00', '19:00:00');

-- ==========================================
-- REGRAS DE ACESSO
-- ==========================================

INSERT INTO usuarios (nome, rfid_tag, perfil_id) VALUES

-- Professores (9)
('Carlos Mendes',    'A2B3C4D5', 1),
('Patricia Rocha',   'B3C4D5E6', 1),
('Marcos Vinicius',  'C4D5E6F7', 1),
('Luciana Alves',    'D5E6F7G8', 1),
('Ricardo Gomes',    'E6F7G8H9', 1),
('Fernanda Costa',   'F7G8H9I0', 1),
('Paulo Henrique',   'G8H9I0J1', 1),
('Juliana Freitas',  'H9I0J1K2', 1),
('Rafael Martins',   'J1K2L3M4', 1),

-- Alunos (18)
('Lucas Ferreira',   'K2L3M4N5', 2),
('Amanda Lima',      'L3M4N5O6', 2),
('Pedro Santos',     'N5O6P7Q8', 2),
('Marina Oliveira',  'O6P7Q8R9', 2),
('Gabriel Ribeiro',  'Q8R9S0T1', 2),
('Camila Duarte',    'R9S0T1U2', 2),
('Thiago Araujo',    'S0T1U2V3', 2),
('Larissa Melo',     'U2V3W4X5', 2),
('Bruno Carvalho',   'V3W4X5Y6', 2),
('Isabela Nunes',    'W4X5Y6Z7', 2),
('Gustavo Dias',     'X5Y6Z7A8', 2),
('Natasha Barros',   'Y6Z7A8B9', 2),
('Leonardo Pinto',   'Z7A8B9C0', 2),
('Aline Monteiro',   'A8B9C0D1', 2),
('Felipe Cardoso',   'B9C0D1E2', 2),
('Vanessa Reis',     'C0D1E2F3', 2),
('Rodrigo Teixeira', 'D1E2F3G4', 2),
('Carolina Lopes',   'F3G4H5I6', 2),

-- Zeladores (7)
('Jose Pereira',     'G4H5I6J7', 3),
('Antonio Lima',     'H5I6J7K8', 3),
('Sandra Costa',     'J7K8L9M0', 3),
('Maria Helena',     'K8L9M0N1', 3),
('Francisco Alves',  'L9M0N1O2', 3),
('Edna Gomes',       'N1O2P3Q4', 3),
('Roberto Souza',    'O2P3Q4R5', 3),

-- Técnicos (5)
('Diego Martins',    'Q4R5S6T7', 4),
('Tatiane Rocha',    'R5S6T7U8', 4),
('Marcelo Azevedo',  'S6T7U8V9', 4),
('Helena Moura',     'U8V9W0X1', 4),
('Victor Fernandes', 'V9W0X1Y2', 4),

-- Pesquisadores Bolsistas (5)
('Daniel Castro',    'W0X1Y2Z3', 5),
('Julia Almeida',    'X1Y2Z3A4', 5),
('Eduardo Braga',    'Y2Z3A4B5', 5),
('Priscila Moraes',  'Z3A4B5C6', 5),
('Mateus Farias',    'A4B5C6D7', 5);