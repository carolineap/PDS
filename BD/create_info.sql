CREATE TABLE info_geral (
	cpf VARCHAR(11) NOT NULL,
	senha VARCHAR(10) NOT NULL,
	ultima_atualizacao DATE NOT NULL,
	PRIMARY KEY(cpf)
)

INSERT INTO info_geral VALUES('00000000000', '1234', '17/10/2018');
