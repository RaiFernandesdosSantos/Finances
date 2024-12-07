create database if not exists finance;

-- Criação dos ENUMs

CREATE TYPE tipo_instituicao_enum AS ENUM ('C', 'P', 'I');
CREATE TYPE tipo_categoria_enum AS ENUM ('D', 'R');
CREATE TYPE tipo_movimentacao_enum AS ENUM ('R', 'D', 'T');
CREATE TYPE status_fatura_enum AS ENUM ('PG', 'PD');
create type periodicidade_enum as enum ('M', 'A');

-- Criação das tabelas

create table if not exists finance.conta (
    id serial primary key,
    descricao varchar(50) not null
);

create table if not exists finance.banco(
    tipo_instituicao tipo_instituicao_enum not null,
    agencia varchar(10) not null,
    conta varchar(10) not null
) inherits (finance.conta);

create table if not exists finance.cartao(
    limite double precision not null,
    dia_vencimento int not null,
    fk_banco int not null,
    bandeira varchar(10) not null,
    constraint fk_banco foreign key (fk_banco) references finance.conta(id)
) inherits (finance.conta);

create table if not exists finance.saldo(
    id serial primary key,
    data date not null,
    saldo double precision not null,
    fk_banco int not null,
    constraint fk_banco foreign key (fk_banco) references finance.conta(id)
);

create table if not exists finance.categoria(
    id serial primary key,
    descricao varchar(50) not null,
    tipo tipo_categoria_enum not null
);

create table if not exists finance.movimentacao(
    id serial primary key,
    descricao varchar(50) not null,
    valor_total double precision not null,
    fk_conta int not null,
    fk_categoria int not null,
    data_movimentacao date not null,
    repetivel boolean not null,
    periodicidade periodicidade_enum,
    parcelas int not null,
    valor_parcelas int not null,
    fk_fatura int,
    tipo_movimentacao tipo_movimentacao_enum not null,
    fk_conta_destino int,
    constraint fk_conta_destino foreign key (fk_conta_destino) references finance.conta(id),
    constraint fk_conta foreign key (fk_conta) references finance.conta(id),
    constraint fk_categoria foreign key (fk_categoria) references finance.categoria(id),
    constraint fk_fatura foreign key (fk_fatura) references finance.fatura(id),
    constraint fk_conta_destino foreign key (fk_conta_destino) references finance.conta(id)
);

create table if not exists finance.fatura(
    id serial primary key,
    fk_cartao int not null,
    fechamento date not null,
    vencimento date not null,
    estado status_fatura_enum not null, 
    valor_total double precision not null,
    constraint fk_cartao foreign key (fk_cartao) references finance.conta(id)
);

-- Criacao das Views

