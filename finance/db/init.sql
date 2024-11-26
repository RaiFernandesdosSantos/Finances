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
    total_ocorrencias int,
    fk_fatura int,
    fk_conta_destino int,
    tipo_movimentacao tipo_movimentacao_enum not null,
    constraint fk_conta foreign key (fk_conta) references finance.conta(id),
    constraint fk_categoria foreign key (fk_categoria) references finance.categoria(id),
    constraint fk_fatura foreign key (fk_fatura) references finance.fatura(id),
    constraint fk_conta_destino foreign key (fk_conta_destino) references finance.conta(id),
    constraint chk_transferencia_conta_destino check (fk_conta_destino is not null and tipo_movimentacao = 'T')
);

create table if not exists finance.fatura(
    id serial primary key,
    fk_cartao int not null,
    fechamento date not null,
    vencimento date not null,
    estado status_fatura_enum not null, 
    constraint fk_cartao foreign key (fk_cartao) references finance.conta(id)
);

-- Criação dos triggers

create or replace function atualiza_saldo() 
returns trigger as $$
begin
    if new.tipo_movimentacao = 'R' then
        update finance.saldo
        set saldo = saldo + new.valor_total
        where fk_banco = new.fk_conta;
    elseif new.tipo_movimentacao = 'D' then
        update finance.saldo
        set saldo = saldo - new.valor_total
        where fk_banco = new.fk_conta;
    elseif new.tipo_movimentacao = 'T' then
        update finance.saldo
        set saldo = saldo - new.valor_total
        where fk_banco = new.fk_conta;

        update finance.saldo
        set saldo = saldo + new.valor_total
        where fk_banco = new.fk_conta_destino;
    end if;

    return new;
end;
$$ language plpgsql;

create trigger atualiza_saldo_trigger
after insert on finance.movimentacao
for each row execute procedure atualiza_saldo();

create or replace function gera_movimentacoes_periodicas()
returns trigger as $$
begin
    if new.repetivel and new.periodicidade = 'M' then
        if new.total_ocorrencias is null then
            for i in 1..60 loop
                insert into finance.movimentacao (
                    descricao, 
                    valor_total, 
                    fk_conta, 
                    fk_categoria, 
                    data_movimentacao, 
                    repetivel, 
                    periodicidade, 
                    parcelas, 
                    valor_parcelas, 
                    total_ocorrencias, 
                    fk_fatura, 
                    fk_conta_destino, 
                    tipo_movimentacao
                ) values (
                    new.descricao, 
                    new.valor_total, 
                    new.fk_conta, 
                    new.fk_categoria, 
                    new.data_movimentacao,
                    new.repetivel,
                    new.periodicidade, 
                    new.parcelas, 
                    new.valor_parcelas, 
                    new.total_ocorrencias, 
                    new.fk_fatura, 
                    new.fk_conta_destino, 
                    new.tipo_movimentacao
                );
            end loop;
        else
            for i in 1..new.total_ocorrencias loop
                insert into finance.movimentacao (
                    descricao, 
                    valor_total, 
                    fk_conta, 
                    fk_categoria, 
                    data_movimentacao, 
                    repetivel, 
                    periodicidade, 
                    parcelas, 
                    valor_parcelas, 
                    total_ocorrencias, 
                    fk_fatura, 
                    fk_conta_destino, 
                    tipo_movimentacao
                ) values (
                    new.descricao, 
                    new.valor_total, 
                    new.fk_conta, 
                    new.fk_categoria, 
                    new.data_movimentacao, 
                    new.repetivel, 
                    new.periodicidade, 
                    new.parcelas,   
                    new.valor_parcelas, 
                    new.total_ocorrencias, 
                    new.fk_fatura, 
                    new.fk_conta_destino,
                    new.tipo_movimentacao
                );
            end loop;
        end if;
    elseif new.repetivel and new.periodicidade = 'A' then
    end if;

    return new;
end;
$$ language plpgsql;

create trigger gera_movimentacoes_periodicas_trigger
after insert on finance.movimentacao
for each row execute procedure gera_movimentacoes_periodicas();

-- Achar um jeito de assim que ele criar movimentacoes repetidar nao engatilhar os triggers