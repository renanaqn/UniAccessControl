-- ==========================================
-- SCRIPT DE INICIALIZAÇÃO
-- ==========================================

-- PREPARAÇÃO DO BANCO
CREATE DATABASE IF NOT EXISTS db_acesso;
USE db_acesso;

-- Limpa as tabelas se elas já existirem (na ordem certa para evitar da bronca nas Foreign Keys)
DROP TABLE IF EXISTS auditoria_logs;
DROP TABLE IF EXISTS regras_acesso;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS zonas;
DROP TABLE IF EXISTS perfis;

-- ==========================================
-- CRIAÇÃO DAS TABELAS
-- ==========================================

CREATE TABLE perfis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_perfil VARCHAR(50) NOT NULL
);

CREATE TABLE zonas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_zona VARCHAR(100) NOT NULL
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    rfid_tag VARCHAR(50) UNIQUE NOT NULL,
    perfil_id INT,
    FOREIGN KEY (perfil_id) REFERENCES perfis(id) ON DELETE SET NULL
);

CREATE TABLE regras_acesso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    zona_id INT NOT NULL,
    perfil_id INT NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    FOREIGN KEY (zona_id) REFERENCES zonas(id) ON DELETE CASCADE,
    FOREIGN KEY (perfil_id) REFERENCES perfis(id) ON DELETE CASCADE,
    UNIQUE KEY uk_regra (perfil_id, zona_id)
);

CREATE TABLE auditoria_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_hora DATETIME NOT NULL,
    resultado VARCHAR(20) NOT NULL,
    motivo VARCHAR(255),
    usuario_id INT,
    rfid_tentativa VARCHAR(20) NOT NULL,
    zona_id INT,
    CONSTRAINT fk_auditoria_logs_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    CONSTRAINT fk_auditoria_logs_zona FOREIGN KEY (zona_id) REFERENCES zonas(id) ON DELETE SET NULL
);


-- ==========================================
-- GATILHOS DE SEGURANÇA (LOGS IMUTÁVEIS)
-- ==========================================

DELIMITER //

-- Gatilho para impedir a DELEÇÃO de qualquer log
CREATE TRIGGER trg_impede_delecao_log
BEFORE DELETE ON auditoria_logs
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'SEGURANÇA: Os logs de auditoria são imutáveis e não podem ser apagados.';
END //

-- Gatilho para impedir a ALTERAÇÃO de qualquer log
CREATE TRIGGER trg_impede_update_log
BEFORE UPDATE ON auditoria_logs
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'SEGURANÇA: Os logs de auditoria são imutáveis e não podem ser alterados.';
END //

DELIMITER ;

-- ==========================================
-- INSERÇÃO DOS DADOS DE TESTE
-- ==========================================

-- Popula os Perfis
INSERT INTO perfis (id, nome_perfil) VALUES 
(1, 'Professor'),
(2, 'Aluno'),
(3, 'Zelador'),
(4, 'Tecnico de Laboratorio'),
(5, 'Pesquisador Bolsista');

-- Popula as Zonas
INSERT INTO zonas (id, nome_zona) VALUES 
(1, 'Lab. de Eletronica'),
(2, 'Sala dos Professores'),
(3, 'Almoxarifado'),
(4, 'Lab. de Informatica');

-- Popula os Usuários (Mantendo as Tags Reais)
INSERT INTO usuarios (id, nome, rfid_tag, perfil_id) VALUES 
(1, 'Ana Maria', 'A1B2C3D4', 1),     -- Professora
(2, 'Joao Silva', 'E5F6G7H8', 2),    -- Aluno
(3, 'Beatriz Souza', 'I9J0K1L2', 2), -- Aluna
(4, 'Carlos Miguel', 'M1N2O3P4', 3), -- Zelador
(5, 'Roberto Alves', 'T5U6V7X8', 4), -- Técnico
(6, 'Fernanda Lima', 'P9Q0R1S2', 5); -- Bolsista

-- Popula as Regras de Acesso
INSERT INTO regras_acesso (zona_id, perfil_id, hora_inicio, hora_fim) VALUES 
(1, 1, '07:00:00', '22:00:00'),  -- Professor na Eletronica
(2, 1, '06:00:00', '22:00:00'),  -- Professor na Sala dos Professores
(4, 1, '00:00:00', '23:59:59'),  -- Professor 24h em Informatica
(1, 2, '08:00:00', '21:00:00'),  -- Aluno na Eletronica
(2, 2, '10:00:00', '15:00:00'),  -- Aluno na Sala dos Professores
(4, 2, '10:00:00', '15:00:00'),  -- Aluno na Sala dos Professores
(1, 3, '06:00:00', '22:00:00'),  -- Zelador na Eletronica
(2, 3, '06:00:00', '22:00:00'),  -- Zelador nos Servidores
(3, 3, '06:00:00', '22:00:00'),  -- Zelador no Almoxarifado
(1, 4, '07:00:00', '19:00:00'),  -- Tecnico em Eletronica
(4, 4, '07:00:00', '19:00:00'),  -- Tecnico em Informatica
(4, 5, '08:00:00', '22:00:00');  -- Bolsista em Informatica


-- Popula os Logs de Auditoria Anteriores (Histórico do Grupo)
INSERT INTO auditoria_logs (id, data_hora, resultado, motivo, usuario_id, rfid_tentativa, zona_id) VALUES 
(1, '2026-06-01 14:21:21', 'NEGADO', 'Tag desconhecida ou sem permissao', NULL, 'A1B2C3D3', 1),
(2, '2026-06-01 14:21:31', 'PERMITIDO', 'Acesso autorizado', 1, 'A1B2C3D4', 1),
(3, '2026-06-01 14:22:38', 'NEGADO', 'Fora do horario', 1, 'A1B2C3D4', 1),
(4, '2026-06-01 14:24:21', 'PERMITIDO', 'Acesso autorizado', 3, 'I9J0K1L2', 1),
(5, '2026-06-01 14:24:50', 'NEGADO', 'Fora do horario', 3, 'I9J0K1L2', 1),
(6, '2026-06-01 14:31:50', 'PERMITIDO', 'Acesso autorizado', 4, 'M1N2O3P4', 1),
(7, '2026-06-01 14:34:11', 'PERMITIDO', 'Acesso autorizado', 4, 'M1N2O3P4', 1),
(8, '2026-06-01 14:52:30', 'PERMITIDO', 'Acesso autorizado', 4, 'M1N2O3P4', 3),
(9, '2026-06-01 15:03:12', 'PERMITIDO', 'Acesso autorizado', 1, 'A1B2C3D4', 1),
(10, '2026-06-01 15:08:40', 'PERMITIDO', 'Acesso autorizado', NULL, 'R9G7A0', 1);