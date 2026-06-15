-- Cria View que contém registro de logs com nome de usuários e zonas
DROP VIEW IF EXISTS registro;
CREATE VIEW registro AS
	SELECT 
		a.data_hora, 
		u.nome, 
		z.nome_zona, 
		a.resultado, 
		a.motivo 
	FROM auditoria_logs AS a
	INNER JOIN usuarios AS u ON u.rfid_tag = a.rfid_tentativa
	INNER JOIN zonas as z ON z.id = a.zona_id