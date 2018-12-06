CREATE OR REPLACE FUNCTION rolagem_boi(date1 date, date2 date)
  RETURNS TABLE (
	data_ajuste date,
  	codigo varchar,
  	vencimento varchar,
  	volume real,
  	contratos integer,
  	preco_abertura real,
  	preco_minimo real,
  	preco_maximo real,
  	ajuste_fechamento real,
  	ajuste_anterior real) AS
$func$
BEGIN
   RETURN QUERY
   SELECT * FROM boi WHERE boi.data_ajuste >= $1 AND boi.data_ajuste <= $2 AND CASE 
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 1 THEN boi.cafe.vencimento = CONCAT('F', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 2 THEN boi.cafe.vencimento = CONCAT('G', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 3 THEN boi.cafe.vencimento = CONCAT('H', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 4 THEN boi.cafe.vencimento = CONCAT('J', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 5 THEN boi.cafe.vencimento = CONCAT('K', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 6 THEN boi.cafe.vencimento = CONCAT('M', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 7 THEN boi.cafe.vencimento = CONCAT('N', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 8 THEN boi.cafe.vencimento = CONCAT('Q', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 9 THEN boi.cafe.vencimento = CONCAT('U', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 10 THEN boi.cafe.vencimento = CONCAT('V', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 11 THEN boi.cafe.vencimento = CONCAT('X', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM boi.data_ajuste) = 12 THEN boi.cafe.vencimento = CONCAT('Z', SUBSTRING(CAST((EXTRACT(YEAR FROM boi.data_ajuste)) AS TEXT), 3, 2))
	END;
	END
$func$  LANGUAGE plpgsql;

#SELECT * FROM rolagem_boi('01/01/2018', '31/01/2018');

CREATE OR REPLACE FUNCTION rolagem_milho(date1 date, date2 date)
  RETURNS TABLE (
	data_ajuste date,
  	codigo varchar,
  	vencimento varchar,
  	volume real,
  	contratos integer,
  	preco_abertura real,
  	preco_minimo real,
  	preco_maximo real,
  	ajuste_fechamento real,
  	ajuste_anterior real) AS
$func$
BEGIN
   RETURN QUERY
  	SELECT * FROM milho WHERE milho.data_ajuste >= $1 AND milho.data_ajuste <= $2 AND CASE 
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 1 THEN milho.cafe.vencimento = CONCAT('H', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 2 THEN milho.cafe.vencimento = CONCAT('H', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 3 THEN milho.cafe.vencimento = CONCAT('K', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 4 THEN milho.cafe.vencimento = CONCAT('K', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 5 THEN milho.cafe.vencimento = CONCAT('N', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 6 THEN milho.cafe.vencimento = CONCAT('N', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 7 THEN milho.cafe.vencimento = CONCAT('Q', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 8 THEN milho.cafe.vencimento = CONCAT('U', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 9 THEN milho.cafe.vencimento = CONCAT('X', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 10 THEN milho.cafe.vencimento = CONCAT('X', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 11 THEN milho.cafe.vencimento = CONCAT('F', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM milho.data_ajuste) = 12 THEN milho.cafe.vencimento = CONCAT('F', SUBSTRING(CAST((EXTRACT(YEAR FROM milho.data_ajuste)) AS TEXT), 3, 2))
	END;
	END
$func$  LANGUAGE plpgsql;

#SELECT * FROM rolagem_milho('01/01/2018', '31/01/2018');


CREATE OR REPLACE FUNCTION rolagem_cafe(date1 date, date2 date)
  RETURNS TABLE (
	data_ajuste date,
  	codigo varchar,
  	vencimento varchar,
  	volume real,
  	contratos integer,
  	preco_abertura real,
  	preco_minimo real,
  	preco_maximo real,
  	ajuste_fechamento real,
  	ajuste_anterior real) AS
$func$
BEGIN
   RETURN QUERY
  	SELECT * FROM cafe WHERE cafe.data_ajuste >= $1 AND cafe.data_ajuste <= $2 AND CASE 
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 1 THEN cafe.vencimento = CONCAT('H', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 2 THEN cafe.vencimento = CONCAT('H', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 3 THEN cafe.vencimento = CONCAT('K', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 4 THEN cafe.vencimento = CONCAT('K', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 5 THEN cafe.vencimento = CONCAT('N', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 6 THEN cafe.vencimento = CONCAT('N', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 7 THEN cafe.vencimento = CONCAT('U', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 8 THEN cafe.vencimento = CONCAT('U', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 9 THEN cafe.vencimento = CONCAT('Z', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 10 THEN cafe.vencimento = CONCAT('Z', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste)= 11 THEN cafe.vencimento = CONCAT('Z', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM cafe.data_ajuste) = 12 THEN cafe.vencimento = CONCAT('H', SUBSTRING(CAST((EXTRACT(YEAR FROM cafe.data_ajuste)) AS TEXT), 3, 2))
	END;
	END
$func$  LANGUAGE plpgsql;

#SELECT * FROM rolagem_cafe('01/01/2018', '31/01/2018');

CREATE OR REPLACE FUNCTION rolagem_soja(date1 date, date2 date)
  RETURNS TABLE (
	data_ajuste date,
  	codigo varchar,
  	vencimento varchar,
  	volume real,
  	contratos integer,
  	preco_abertura real,
  	preco_minimo real,
  	preco_maximo real,
  	ajuste_fechamento real,
  	ajuste_anterior real) AS
$func$
BEGIN
   RETURN QUERY
  	SELECT * FROM soja WHERE soja.data_ajuste >= $1 AND soja.data_ajuste <= $2 AND CASE 
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 1 THEN soja.vencimento = CONCAT('H', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 2 THEN soja.vencimento = CONCAT('H', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 3 THEN soja.vencimento = CONCAT('J', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 4 THEN soja.vencimento = CONCAT('K', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 5 THEN soja.vencimento = CONCAT('M', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 6 THEN soja.vencimento = CONCAT('N', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 7 THEN soja.vencimento = CONCAT('Q', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 8 THEN soja.vencimento = CONCAT('U', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 9 THEN soja.vencimento = CONCAT('X', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 10 THEN soja.vencimento = CONCAT('X', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 11 THEN soja.vencimento = CONCAT('X', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	WHEN EXTRACT(MONTH FROM soja.data_ajuste) = 12 THEN soja.vencimento = CONCAT('X', SUBSTRING(CAST((EXTRACT(YEAR FROM soja.data_ajuste)) AS TEXT), 3, 2))
	END;
	END
$func$  LANGUAGE plpgsql;

#SELECT * FROM rolagem_soja('01/01/2018', '31/01/2018');





















