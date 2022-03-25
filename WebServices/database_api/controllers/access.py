from .. import models as models_ga

def get_access(equipment_number, direction, datetime_start, datetime_end):
    ''' Gets equipment parameters in database, for the specific IP informed.
    Ref: https://docs.djangoproject.com/en/3.2/topics/db/queries/
    '''

    #eq = models_ga.TbEquipamento.objects.all().filter

    query = models_ga.TbEquipamento




    return True



''' SQL Query to get necessary data:

select
TB_PESSOA.NO_PESSOA,
TB_CARGO.NO_CARGO,
TB_EQUIPAMENTO.NO_EQUIPAMENTO, 
TB_TIPO_ACESSO.DS_ACESSO,
TB_REGISTRO_ACESSO.DT_REGISTRO

from TB_EQUIPAMENTO																													-- Equipment
join TB_SOLICITACAO_ACESSO on TB_EQUIPAMENTO.CO_SEQ_EQUIPAMENTO = TB_SOLICITACAO_ACESSO.CO_EQUIPAMENTO								-- Access requested.
join TB_REGISTRO_ACESSO on TB_SOLICITACAO_ACESSO.CO_SEQ_SOLICITACAO = TB_REGISTRO_ACESSO.CO_SOLICITACAO								-- Access made
join TB_TIPO_ACESSO on TB_REGISTRO_ACESSO.CO_TIPO_ACESSO = TB_TIPO_ACESSO.CO_SEQ_TIPO_ACESSO										-- Access description
join TB_PESSOA_IDENTIFICADOR on TB_SOLICITACAO_ACESSO.CO_PESSOA_IDENTIFICADOR = TB_PESSOA_IDENTIFICADOR.CO_SEQ_PESSOA_IDENTIFICADOR	-- Relantionship person/identifier
join TB_PESSOA on TB_PESSOA_IDENTIFICADOR.CO_PESSOA = TB_PESSOA.CO_SEQ_PESSOA														-- Person
join TB_CARGO on TB_PESSOA.CO_CARGO = TB_CARGO.CO_SEQ_CARGO                                                                         -- Job description.

where TB_EQUIPAMENTO.CO_SEQ_EQUIPAMENTO = 5										-- Equipment
and TB_REGISTRO_ACESSO.CO_TIPO_ACESSO = 1										-- Access made
and TB_REGISTRO_ACESSO.DT_REGISTRO between '2019-01-01' and '2019-02-23'		-- Dates

order by TB_REGISTRO_ACESSO.DT_REGISTRO


-- select top 10 * from TB_SOLICITACAO_ACESSO
-- select top 10 * from TB_REGISTRO_ACESSO
-- select top 10 * from TB_PESSOA_IDENTIFICADOR 

'''