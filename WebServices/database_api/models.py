# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class TbAcao(models.Model):
    co_seq_acao = models.AutoField(db_column='CO_SEQ_ACAO', primary_key=True)
    ds_acao = models.CharField(db_column='DS_ACAO', max_length=150, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_ACAO'


class TbCargo(models.Model):
    co_seq_cargo = models.AutoField(db_column='CO_SEQ_CARGO', primary_key=True)
    co_importacao = models.DecimalField(db_column='CO_IMPORTACAO', max_digits=18, decimal_places=0, blank=True, null=True)
    no_cargo = models.CharField(db_column='NO_CARGO', max_length=50)
    ds_cargo = models.CharField(db_column='DS_CARGO', max_length=100, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_CARGO'

    def __str__(self):
        return self.no_cargo


class TbDepartamento(models.Model):
    co_seq_departamento = models.AutoField(db_column='CO_SEQ_DEPARTAMENTO', primary_key=True)
    co_empresa = models.ForeignKey('TbEmpresa', models.DO_NOTHING, db_column='CO_EMPRESA')
    no_departamento = models.CharField(db_column='NO_DEPARTAMENTO', max_length=100)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_DEPARTAMENTO'


class TbDiaSemana(models.Model):
    co_dia_semana = models.DecimalField(db_column='CO_DIA_SEMANA', primary_key=True, max_digits=18, decimal_places=0)
    ds_dia = models.CharField(db_column='DS_DIA', max_length=20)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_DIA_SEMANA'


class TbEmpresa(models.Model):
    co_seq_empresa = models.AutoField(db_column='CO_SEQ_EMPRESA', primary_key=True)
    co_importacao = models.DecimalField(db_column='CO_IMPORTACAO', max_digits=18, decimal_places=0, blank=True, null=True)
    co_pessoa_responsavel = models.ForeignKey('TbPessoa', models.DO_NOTHING, db_column='CO_PESSOA_RESPONSAVEL', blank=True, null=True)
    no_empresa = models.CharField(db_column='NO_EMPRESA', max_length=100, blank=True, null=True)
    ds_empresa = models.CharField(db_column='DS_EMPRESA', max_length=200, blank=True, null=True)
    nu_telefone = models.CharField(db_column='NU_TELEFONE', max_length=25, blank=True, null=True)
    ds_email = models.CharField(db_column='DS_EMAIL', max_length=50, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_EMPRESA'

    def __str__(self):
        return self.no_empresa


class TbEnderecoPessoa(models.Model):
    co_seq_endereco = models.AutoField(db_column='CO_SEQ_ENDERECO', primary_key=True)
    co_pessoa = models.ForeignKey('TbPessoa', models.DO_NOTHING, db_column='CO_PESSOA', blank=True, null=True)
    ds_endereco = models.CharField(db_column='DS_ENDERECO', max_length=100, blank=True, null=True)
    ds_complemento = models.CharField(db_column='DS_COMPLEMENTO', max_length=50, blank=True, null=True)
    ds_numero = models.CharField(db_column='DS_NUMERO', max_length=20, blank=True, null=True)
    no_bairro = models.CharField(db_column='NO_BAIRRO', max_length=50, blank=True, null=True)
    no_cidade = models.CharField(db_column='NO_CIDADE', max_length=50, blank=True, null=True)
    nu_cep = models.CharField(db_column='NU_CEP', max_length=8, blank=True, null=True)
    no_estado = models.CharField(db_column='NO_ESTADO', max_length=50, blank=True, null=True)
    no_pais = models.CharField(db_column='NO_PAIS', max_length=50, blank=True, null=True)
    st_principal = models.CharField(db_column='ST_PRINCIPAL', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_ENDERECO_PESSOA'


class TbEquipamento(models.Model):
    co_seq_equipamento = models.AutoField(db_column='CO_SEQ_EQUIPAMENTO', primary_key=True)
    co_modelo_equipamento = models.ForeignKey('TbModeloEquipamento', models.DO_NOTHING, db_column='CO_MODELO_EQUIPAMENTO')
    no_equipamento = models.CharField(db_column='NO_EQUIPAMENTO', max_length=100)
    co_perimetro = models.ForeignKey('TbPerimetro', models.DO_NOTHING, db_column='CO_PERIMETRO', blank=True, null=True)
    co_localidade_eqp = models.ForeignKey('TbLocalidade', models.DO_NOTHING, db_column='CO_LOCALIDADE_EQP', blank=True, null=True)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_motivo_bloqueio = models.ForeignKey('TbMotivoBloqueio', models.DO_NOTHING, db_column='CO_MOTIVO_BLOQUEIO', blank=True, null=True)
    dt_inicio_bloqueio = models.DateTimeField(db_column='DT_INICIO_BLOQUEIO', blank=True, null=True)
    dt_fim_bloqueio = models.DateTimeField(db_column='DT_FIM_BLOQUEIO', blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_EQUIPAMENTO'


class TbEvento(models.Model):
    co_seq_evento = models.AutoField(db_column='CO_SEQ_EVENTO', primary_key=True)
    co_status_evento = models.ForeignKey('TbStatusEvento', models.DO_NOTHING, db_column='CO_STATUS_EVENTO', blank=True, null=True)
    co_equipamento = models.ForeignKey(TbEquipamento, models.DO_NOTHING, db_column='CO_EQUIPAMENTO', blank=True, null=True)
    co_tipo_evento = models.ForeignKey('TbTipoEvento', models.DO_NOTHING, db_column='CO_TIPO_EVENTO', blank=True, null=True)
    ds_evento = models.CharField(db_column='DS_EVENTO', max_length=250, blank=True, null=True)
    dt_evento = models.DateTimeField(db_column='DT_EVENTO', blank=True, null=True)
    co_pessoa = models.DecimalField(db_column='CO_PESSOA', max_digits=18, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'TB_EVENTO'


class TbIdentificador(models.Model):
    co_seq_identificador = models.AutoField(db_column='CO_SEQ_IDENTIFICADOR', primary_key=True)
    co_importacao = models.DecimalField(db_column='CO_IMPORTACAO', max_digits=18, decimal_places=0, blank=True, null=True)
    co_modelo_identificador = models.ForeignKey('TbModeloIdentificador', models.DO_NOTHING, db_column='CO_MODELO_IDENTIFICADOR')
    co_tipo_identificador = models.ForeignKey('TbTipoIdentificador', models.DO_NOTHING, db_column='CO_TIPO_IDENTIFICADOR')
    nu_identificador = models.CharField(db_column='NU_IDENTIFICADOR', unique=True, max_length=50)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_IDENTIFICADOR'


class TbLocalidade(models.Model):
    co_seq_localidade = models.AutoField(db_column='CO_SEQ_LOCALIDADE', primary_key=True)
    co_importacao = models.DecimalField(db_column='CO_IMPORTACAO', max_digits=18, decimal_places=0, blank=True, null=True)
    co_localidade_pai = models.ForeignKey('self', models.DO_NOTHING, db_column='CO_LOCALIDADE_PAI', blank=True, null=True)
    co_perimetro = models.ForeignKey('TbPerimetro', models.DO_NOTHING, db_column='CO_PERIMETRO', blank=True, null=True)
    no_localidade = models.CharField(db_column='NO_LOCALIDADE', max_length=100)
    ds_localidade = models.CharField(db_column='DS_LOCALIDADE', max_length=200, blank=True, null=True)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_LOCALIDADE'


class TbLocalidadeEquipamento(models.Model):
    co_seq_localidade_eqp = models.AutoField(db_column='CO_SEQ_LOCALIDADE_EQP', primary_key=True)
    no_localidade = models.CharField(db_column='NO_LOCALIDADE', max_length=100, blank=True, null=True)
    ds_localidade = models.CharField(db_column='DS_LOCALIDADE', max_length=200, blank=True, null=True)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_LOCALIDADE_EQUIPAMENTO'


class TbModeloEqpParam(models.Model):
    co_seq_modelo_eqp_param = models.AutoField(db_column='CO_SEQ_MODELO_EQP_PARAM', primary_key=True)
    co_parametro = models.ForeignKey('TbParametro', models.DO_NOTHING, db_column='CO_PARAMETRO')
    co_modelo_equipamento = models.ForeignKey('TbModeloEquipamento', models.DO_NOTHING, db_column='CO_MODELO_EQUIPAMENTO')
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_MODELO_EQP_PARAM'


class TbModeloEquipamento(models.Model):
    co_seq_modelo_equipamento = models.AutoField(db_column='CO_SEQ_MODELO_EQUIPAMENTO', primary_key=True)
    no_modelo = models.CharField(db_column='NO_MODELO', max_length=50)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_MODELO_EQUIPAMENTO'


class TbModeloIdentificador(models.Model):
    co_seq_modelo_identificador = models.AutoField(db_column='CO_SEQ_MODELO_IDENTIFICADOR', primary_key=True)
    no_modelo = models.CharField(db_column='NO_MODELO', max_length=100)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_MODELO_IDENTIFICADOR'


class TbMotivoBloqueio(models.Model):
    co_seq_motivo_bloqueio = models.AutoField(db_column='CO_SEQ_MOTIVO_BLOQUEIO', primary_key=True)
    co_tipo_bloqueio = models.ForeignKey('TbTipoBloqueio', models.DO_NOTHING, db_column='CO_TIPO_BLOQUEIO', blank=True, null=True)
    ds_motivo = models.CharField(db_column='DS_MOTIVO', max_length=100)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_MOTIVO_BLOQUEIO'

    def __str__(self):
        return self.ds_motivo


class TbNotificacao(models.Model):
    co_seq_notificacao = models.AutoField(db_column='CO_SEQ_NOTIFICACAO', primary_key=True)
    ds_notificacao = models.CharField(db_column='DS_NOTIFICACAO', max_length=100)
    no_login_cadastro = models.CharField(db_column='NO_LOGIN_CADASTRO', max_length=25)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_NOTIFICACAO'


class TbOperador(models.Model):
    co_seq_operador = models.AutoField(db_column='CO_SEQ_OPERADOR', primary_key=True)
    co_pessoa = models.ForeignKey('TbPessoa', models.DO_NOTHING, db_column='CO_PESSOA', blank=True, null=True)
    no_login = models.CharField(db_column='NO_LOGIN', max_length=50, blank=True, null=True)
    ds_senha = models.CharField(db_column='DS_SENHA', max_length=255, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_OPERADOR'


class TbParametro(models.Model):
    co_seq_parametro = models.AutoField(db_column='CO_SEQ_PARAMETRO', primary_key=True)
    no_parametro = models.CharField(db_column='NO_PARAMETRO', max_length=100)
    ds_tipo = models.CharField(db_column='DS_TIPO', max_length=1)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PARAMETRO'


class TbParametroEquipamento(models.Model):
    co_seq_parametro_eqp = models.AutoField(db_column='CO_SEQ_PARAMETRO_EQP', primary_key=True)
    co_equipamento = models.ForeignKey(TbEquipamento, models.DO_NOTHING, db_column='CO_EQUIPAMENTO')
    co_parametro = models.ForeignKey(TbParametro, models.DO_NOTHING, db_column='CO_PARAMETRO')
    vl_parametro = models.CharField(db_column='VL_PARAMETRO', max_length=50, blank=True, null=True)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PARAMETRO_EQUIPAMENTO'


class TbParametroMiddleware(models.Model):
    co_seq_parametro_md = models.AutoField(db_column='CO_SEQ_PARAMETRO_MD', primary_key=True)
    co_parametro = models.ForeignKey(TbParametro, models.DO_NOTHING, db_column='CO_PARAMETRO')
    vl_parametro = models.CharField(db_column='VL_PARAMETRO', max_length=50)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PARAMETRO_MIDDLEWARE'


class TbPerfil(models.Model):
    co_seq_perfil = models.AutoField(db_column='CO_SEQ_PERFIL', primary_key=True)
    no_perfil = models.CharField(db_column='NO_PERFIL', max_length=50)
    ds_perfil = models.CharField(db_column='DS_PERFIL', max_length=200, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PERFIL'


class TbPerfilAcao(models.Model):
    co_seq_perfil_acao = models.AutoField(db_column='CO_SEQ_PERFIL_ACAO', primary_key=True)
    co_perfil = models.ForeignKey(TbPerfil, models.DO_NOTHING, db_column='CO_PERFIL')
    co_acao = models.ForeignKey(TbAcao, models.DO_NOTHING, db_column='CO_ACAO')
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PERFIL_ACAO'


class TbPerfilAcesso(models.Model):
    co_seq_perfil_acesso = models.AutoField(db_column='CO_SEQ_PERFIL_ACESSO', primary_key=True)
    co_tipo_perfil = models.ForeignKey('TbTipoPerfilAcesso', models.DO_NOTHING, db_column='CO_TIPO_PERFIL', blank=True, null=True)
    co_pessoa = models.ForeignKey('TbPessoa', models.DO_NOTHING, db_column='CO_PESSOA', blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PERFIL_ACESSO'


class TbPerfilAcessoLocalidade(models.Model):
    co_seq_perfilacessolocalidade = models.AutoField(db_column='CO_SEQ_PERFILACESSOLOCALIDADE', primary_key=True)
    co_tipo_perfil_acesso = models.ForeignKey('TbTipoPerfilAcesso', models.DO_NOTHING, db_column='CO_TIPO_PERFIL_ACESSO')
    co_localidade = models.ForeignKey(TbLocalidade, models.DO_NOTHING, db_column='CO_LOCALIDADE')
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0, blank=True, null=True)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'TB_PERFIL_ACESSO_LOCALIDADE'


class TbPerfilLocalidade(models.Model):
    co_seq_perfil_localidade = models.AutoField(db_column='CO_SEQ_PERFIL_LOCALIDADE', primary_key=True)
    co_perfil = models.ForeignKey(TbPerfil, models.DO_NOTHING, db_column='CO_PERFIL', blank=True, null=True)
    co_localidade = models.ForeignKey(TbLocalidade, models.DO_NOTHING, db_column='CO_LOCALIDADE', blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PERFIL_LOCALIDADE'


class TbPerfilOperador(models.Model):
    co_seq_perfil_operador = models.AutoField(db_column='CO_SEQ_PERFIL_OPERADOR', primary_key=True)
    co_operador = models.ForeignKey(TbOperador, models.DO_NOTHING, db_column='CO_OPERADOR')
    co_perfil = models.ForeignKey(TbPerfil, models.DO_NOTHING, db_column='CO_PERFIL')
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PERFIL_OPERADOR'


class TbPerimetro(models.Model):
    co_seq_perimetro = models.AutoField(db_column='CO_SEQ_PERIMETRO', primary_key=True)
    co_importacao = models.DecimalField(db_column='CO_IMPORTACAO', max_digits=18, decimal_places=0, blank=True, null=True)
    no_perimetro = models.CharField(db_column='NO_PERIMETRO', max_length=50)
    ds_perimetro = models.CharField(db_column='DS_PERIMETRO', max_length=200, blank=True, null=True)
    st_anti_passback = models.CharField(db_column='ST_ANTI_PASSBACK', max_length=1, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    st_recolher_cartao = models.CharField(db_column='ST_RECOLHER_CARTAO', max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'TB_PERIMETRO'


class TbPeriodoAcesso(models.Model):
    co_seq_periodo_acesso = models.AutoField(db_column='CO_SEQ_PERIODO_ACESSO', primary_key=True)
    co_zona_tempo = models.ForeignKey('TbZonaTempo', models.DO_NOTHING, db_column='CO_ZONA_TEMPO', blank=True, null=True)
    co_dia_semana = models.ForeignKey(TbDiaSemana, models.DO_NOTHING, db_column='CO_DIA_SEMANA')
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    hr_entrada = models.TimeField(db_column='HR_ENTRADA')
    hr_saida = models.TimeField(db_column='HR_SAIDA')
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PERIODO_ACESSO'


class TbPermissaoAcesso(models.Model):
    co_seq_permissao_acesso = models.AutoField(db_column='CO_SEQ_PERMISSAO_ACESSO', primary_key=True)
    co_pessoa = models.ForeignKey('TbPessoa', models.DO_NOTHING, db_column='CO_PESSOA', blank=True, null=True)
    co_localidade = models.ForeignKey(TbLocalidade, models.DO_NOTHING, db_column='CO_LOCALIDADE', blank=True, null=True)
    dt_inicio_vigencia = models.DateTimeField(db_column='DT_INICIO_VIGENCIA')
    dt_termino_vigencia = models.DateTimeField(db_column='DT_TERMINO_VIGENCIA', blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_motivo_bloqueio = models.ForeignKey(TbMotivoBloqueio, models.DO_NOTHING, db_column='CO_MOTIVO_BLOQUEIO', blank=True, null=True)
    dt_inicio_bloqueio = models.DateTimeField(db_column='DT_INICIO_BLOQUEIO', blank=True, null=True)
    dt_fim_bloqueio = models.DateTimeField(db_column='DT_FIM_BLOQUEIO', blank=True, null=True)
    ds_observacao = models.CharField(db_column='DS_OBSERVACAO', max_length=150, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PERMISSAO_ACESSO'


class TbPessoa(models.Model):
    co_seq_pessoa = models.AutoField(db_column='CO_SEQ_PESSOA', primary_key=True)
    co_importacao = models.DecimalField(db_column='CO_IMPORTACAO', max_digits=18, decimal_places=0, blank=True, null=True)
    co_tipo_pessoa = models.ForeignKey('TbTipoPessoa', models.DO_NOTHING, db_column='CO_TIPO_PESSOA')
    no_pessoa = models.CharField(db_column='NO_PESSOA', max_length=100)
    st_pne = models.CharField(db_column='ST_PNE', max_length=1, blank=True, null=True)
    id_risco = models.SmallIntegerField(db_column='ID_RISCO', blank=True, null=True)
    ds_link_foto = models.CharField(db_column='DS_LINK_FOTO', max_length=250, blank=True, null=True)
    co_empresa = models.ForeignKey(TbEmpresa, models.DO_NOTHING, db_column='CO_EMPRESA', blank=True, null=True)
    co_departamento = models.ForeignKey(TbDepartamento, models.DO_NOTHING, db_column='CO_DEPARTAMENTO', blank=True, null=True)
    co_cargo = models.ForeignKey(TbCargo, models.DO_NOTHING, db_column='CO_CARGO', blank=True, null=True)
    nu_andar = models.CharField(db_column='NU_ANDAR', max_length=20, blank=True, null=True)
    co_zona_tempo = models.ForeignKey('TbZonaTempo', models.DO_NOTHING, db_column='CO_ZONA_TEMPO', blank=True, null=True)
    nu_cpf = models.CharField(db_column='NU_CPF', max_length=11, blank=True, null=True)
    nu_rg = models.CharField(db_column='NU_RG', max_length=20, blank=True, null=True)
    ds_orgao_emissor = models.CharField(db_column='DS_ORGAO_EMISSOR', max_length=50, blank=True, null=True)
    nu_passaporte = models.CharField(db_column='NU_PASSAPORTE', max_length=25, blank=True, null=True)
    nu_cnh = models.CharField(db_column='NU_CNH', max_length=25, blank=True, null=True)
    nu_telefone_principal = models.CharField(db_column='NU_TELEFONE_PRINCIPAL', max_length=25, blank=True, null=True)
    nu_telefone_celular = models.CharField(db_column='NU_TELEFONE_CELULAR', max_length=25, blank=True, null=True)
    ds_email_particular = models.CharField(db_column='DS_EMAIL_PARTICULAR', max_length=50, blank=True, null=True)
    ds_email_profissional = models.CharField(db_column='DS_EMAIL_PROFISSIONAL', max_length=50, blank=True, null=True)
    dt_nascimento = models.DateField(db_column='DT_NASCIMENTO', blank=True, null=True)
    ds_observacao = models.CharField(db_column='DS_OBSERVACAO', max_length=150, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_visitada = models.DecimalField(db_column='CO_PESSOA_VISITADA', max_digits=18, decimal_places=0, blank=True, null=True)
    co_motivo_bloqueio = models.ForeignKey(TbMotivoBloqueio, models.DO_NOTHING, db_column='CO_MOTIVO_BLOQUEIO', blank=True, null=True)
    dt_inicio_bloqueio = models.DateTimeField(db_column='DT_INICIO_BLOQUEIO', blank=True, null=True)
    dt_fim_bloqueio = models.DateTimeField(db_column='DT_FIM_BLOQUEIO', blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0, blank=True, null=True)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PESSOA'
        ordering = ("no_pessoa", "nu_cpf")
    
    def __str__(self):
        return self.no_pessoa

    def anonymize(self):
        self.no_pessoa = 'Anonymized'
        self.ds_link_foto = 'Anonymized'
        self.nu_cpf = 'Anonymized'
        self.nu_rg = 'Anonymized'
        self.ds_orgao_emissor = 'Anonymized'
        self.nu_passaporte = 'Anonymized'
        self.nu_cnh = 'Anonymized'
        self.nu_telefone_principal = 'Anonymized'
        self.nu_telefone_celular = 'Anonymized'
        self.ds_email_particular = 'Anonymized'
        self.ds_email_profissional = 'Anonymized'
        self.save()


class TbPessoaIdentificador(models.Model):
    co_seq_pessoa_identificador = models.AutoField(db_column='CO_SEQ_PESSOA_IDENTIFICADOR', primary_key=True)
    co_pessoa = models.ForeignKey(TbPessoa, models.DO_NOTHING, db_column='CO_PESSOA')
    co_identificador = models.ForeignKey(TbIdentificador, models.DO_NOTHING, db_column='CO_IDENTIFICADOR', blank=True, null=True)
    dt_inicio_vigencia = models.DateTimeField(db_column='DT_INICIO_VIGENCIA')
    dt_termino_vigencia = models.DateTimeField(db_column='DT_TERMINO_VIGENCIA', blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_motivo_bloqueio = models.ForeignKey(TbMotivoBloqueio, models.DO_NOTHING, db_column='CO_MOTIVO_BLOQUEIO', blank=True, null=True)
    dt_inicio_bloqueio = models.DateTimeField(db_column='DT_INICIO_BLOQUEIO', blank=True, null=True)
    dt_fim_bloqueio = models.DateTimeField(db_column='DT_FIM_BLOQUEIO', blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_PESSOA_IDENTIFICADOR'


class TbRegistroAcesso(models.Model):
    co_seq_registro_acesso = models.AutoField(db_column='CO_SEQ_REGISTRO_ACESSO', primary_key=True)
    co_solicitacao = models.ForeignKey('TbSolicitacaoAcesso', models.DO_NOTHING, db_column='CO_SOLICITACAO')
    co_tipo_acesso = models.ForeignKey('TbTipoAcesso', models.DO_NOTHING, db_column='CO_TIPO_ACESSO', blank=True, null=True)
    dt_registro = models.DateTimeField(db_column='DT_REGISTRO')

    class Meta:
        managed = True
        db_table = 'TB_REGISTRO_ACESSO'


class TbRotaEquipamento(models.Model):
    co_seq_rota_equipamento = models.AutoField(db_column='CO_SEQ_ROTA_EQUIPAMENTO', primary_key=True)
    co_rota_fuga = models.ForeignKey('TbRotaFuga', models.DO_NOTHING, db_column='CO_ROTA_FUGA')
    co_equipamento = models.ForeignKey(TbEquipamento, models.DO_NOTHING, db_column='CO_EQUIPAMENTO')
    st_modo_operacao = models.CharField(db_column='ST_MODO_OPERACAO', max_length=1)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_ROTA_EQUIPAMENTO'


class TbRotaFuga(models.Model):
    co_seq_rota_fuga = models.AutoField(db_column='CO_SEQ_ROTA_FUGA', primary_key=True)
    ds_rota_fuga = models.CharField(db_column='DS_ROTA_FUGA', max_length=150, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_ROTA_FUGA'


class TbSolicitacaoAcesso(models.Model):
    co_seq_solicitacao = models.AutoField(db_column='CO_SEQ_SOLICITACAO', primary_key=True)
    co_tipo_acesso = models.ForeignKey('TbTipoAcesso', models.DO_NOTHING, db_column='CO_TIPO_ACESSO', blank=True, null=True)
    co_tipo_acesso_solicitado = models.DecimalField(db_column='CO_TIPO_ACESSO_SOLICITADO', max_digits=18, decimal_places=0, blank=True, null=True)
    co_equipamento = models.ForeignKey(TbEquipamento, models.DO_NOTHING, db_column='CO_EQUIPAMENTO', blank=True, null=True)
    co_pessoa_identificador = models.ForeignKey(TbPessoaIdentificador, models.DO_NOTHING, db_column='CO_PESSOA_IDENTIFICADOR', blank=True, null=True)
    dt_solicitacao = models.DateTimeField(db_column='DT_SOLICITACAO')

    class Meta:
        managed = True
        db_table = 'TB_SOLICITACAO_ACESSO'


class TbStatusEvento(models.Model):
    co_seq_status_evento = models.AutoField(db_column='CO_SEQ_STATUS_EVENTO', primary_key=True)
    ds_status = models.CharField(db_column='DS_STATUS', unique=True, max_length=50, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_STATUS_EVENTO'


class TbTipoAcesso(models.Model):
    co_seq_tipo_acesso = models.AutoField(db_column='CO_SEQ_TIPO_ACESSO', primary_key=True)
    ds_acesso = models.CharField(db_column='DS_ACESSO', max_length=100)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_TIPO_ACESSO'


class TbTipoBloqueio(models.Model):
    co_seq_tipo_bloqueio = models.AutoField(db_column='CO_SEQ_TIPO_BLOQUEIO', primary_key=True)
    ds_tipo = models.CharField(db_column='DS_TIPO', max_length=50)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_TIPO_BLOQUEIO'


class TbTipoDml(models.Model):
    co_dml = models.DecimalField(db_column='CO_DML', primary_key=True, max_digits=18, decimal_places=0)
    ds_dml = models.CharField(db_column='DS_DML', max_length=20, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_TIPO_DML'


class TbTipoEvento(models.Model):
    co_seq_tipo_evento = models.AutoField(db_column='CO_SEQ_TIPO_EVENTO', primary_key=True)
    ds_tipo = models.CharField(db_column='DS_TIPO', max_length=50, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_TIPO_EVENTO'


class TbTipoIdentificador(models.Model):
    co_seq_tipo_identificador = models.AutoField(db_column='CO_SEQ_TIPO_IDENTIFICADOR', primary_key=True)
    ds_tipo = models.CharField(db_column='DS_TIPO', max_length=50)
    st_saida_urna = models.CharField(db_column='ST_SAIDA_URNA', max_length=1)
    st_libera_2sentidos = models.CharField(db_column='ST_LIBERA_2SENTIDOS', max_length=1)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_TIPO_IDENTIFICADOR'


class TbTipoPerfilAcesso(models.Model):
    co_seq_tipo_perfil = models.AutoField(db_column='CO_SEQ_TIPO_PERFIL', primary_key=True)
    ds_tipo = models.CharField(db_column='DS_TIPO', max_length=100)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_TIPO_PERFIL_ACESSO'


class TbTipoPessoa(models.Model):
    co_seq_tipo_pessoa = models.AutoField(db_column='CO_SEQ_TIPO_PESSOA', primary_key=True)
    ds_tipo = models.CharField(db_column='DS_TIPO', max_length=50)
    ds_info_tipo = models.IntegerField(db_column='DS_INFO_TIPO', blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0, blank=True, null=True)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_TIPO_PESSOA'

    def __str__(self):
        return self.ds_tipo


class TbUltimoAcesso(models.Model):
    co_seq_ultimo_acesso = models.AutoField(db_column='CO_SEQ_ULTIMO_ACESSO', primary_key=True)
    co_registro_acesso = models.ForeignKey(TbRegistroAcesso, models.DO_NOTHING, db_column='CO_REGISTRO_ACESSO', blank=True, null=True)
    co_pessoa = models.DecimalField(db_column='CO_PESSOA', max_digits=18, decimal_places=0, blank=True, null=True)
    co_perimetro = models.DecimalField(db_column='CO_PERIMETRO', max_digits=18, decimal_places=0, blank=True, null=True)
    dt_ultimo_acesso = models.DateTimeField(db_column='DT_ULTIMO_ACESSO', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'TB_ULTIMO_ACESSO'


class TbZonaTempo(models.Model):
    co_seq_zona_tempo = models.AutoField(db_column='CO_SEQ_ZONA_TEMPO', primary_key=True)
    no_zona = models.CharField(db_column='NO_ZONA', max_length=50, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')

    class Meta:
        managed = True
        db_table = 'TB_ZONA_TEMPO'

    def __str__(self):
        return self.no_zona


class ThAcao(models.Model):
    co_seq_hist_acao = models.AutoField(db_column='CO_SEQ_HIST_ACAO', primary_key=True)
    co_acao = models.DecimalField(db_column='CO_ACAO', max_digits=18, decimal_places=0)
    ds_acao = models.CharField(db_column='DS_ACAO', max_length=150, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_ACAO'


class ThCargo(models.Model):
    co_seq_hist_cargo = models.AutoField(db_column='CO_SEQ_HIST_CARGO', primary_key=True)
    co_cargo = models.DecimalField(db_column='CO_CARGO', max_digits=18, decimal_places=0)
    no_cargo = models.CharField(db_column='NO_CARGO', max_length=50, blank=True, null=True)
    ds_cargo = models.CharField(db_column='DS_CARGO', max_length=100, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_CARGO'


class ThDepartamento(models.Model):
    co_seq_hist_dep = models.AutoField(db_column='CO_SEQ_HIST_DEP', primary_key=True)
    co_departamento = models.DecimalField(db_column='CO_DEPARTAMENTO', max_digits=18, decimal_places=0)
    co_empresa = models.DecimalField(db_column='CO_EMPRESA', max_digits=18, decimal_places=0)
    no_departamento = models.CharField(db_column='NO_DEPARTAMENTO', max_length=100)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_DEPARTAMENTO'


class ThEmpresa(models.Model):
    co_seq_hist_empresa = models.AutoField(db_column='CO_SEQ_HIST_EMPRESA', primary_key=True)
    co_empresa = models.DecimalField(db_column='CO_EMPRESA', max_digits=18, decimal_places=0)
    co_pessoa_responsavel = models.DecimalField(db_column='CO_PESSOA_RESPONSAVEL', max_digits=18, decimal_places=0, blank=True, null=True)
    no_empresa = models.CharField(db_column='NO_EMPRESA', max_length=100, blank=True, null=True)
    ds_empresa = models.CharField(db_column='DS_EMPRESA', max_length=200, blank=True, null=True)
    nu_telefone = models.CharField(db_column='NU_TELEFONE', max_length=25, blank=True, null=True)
    ds_email = models.CharField(db_column='DS_EMAIL', max_length=50, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_EMPRESA'


class ThEquipamento(models.Model):
    co_seq_hist_equipamento = models.AutoField(db_column='CO_SEQ_HIST_EQUIPAMENTO', primary_key=True)
    co_equipamento = models.DecimalField(db_column='CO_EQUIPAMENTO', max_digits=18, decimal_places=0)
    co_modelo_equipamento = models.DecimalField(db_column='CO_MODELO_EQUIPAMENTO', max_digits=18, decimal_places=0)
    no_equipamento = models.CharField(db_column='NO_EQUIPAMENTO', max_length=100)
    co_perimetro = models.DecimalField(db_column='CO_PERIMETRO', max_digits=18, decimal_places=0, blank=True, null=True)
    co_localidade_eqp = models.DecimalField(db_column='CO_LOCALIDADE_EQP', max_digits=18, decimal_places=0)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_motivo_bloqueio = models.DecimalField(db_column='CO_MOTIVO_BLOQUEIO', max_digits=18, decimal_places=0, blank=True, null=True)
    dt_inicio_bloqueio = models.DateTimeField(db_column='DT_INICIO_BLOQUEIO', blank=True, null=True)
    dt_fim_bloqueio = models.DateTimeField(db_column='DT_FIM_BLOQUEIO', blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_EQUIPAMENTO'


class ThLocalidadeEquipamento(models.Model):
    co_seq_hist_local_eqp = models.AutoField(db_column='CO_SEQ_HIST_LOCAL_EQP', primary_key=True)
    co_localidade_eqp = models.DecimalField(db_column='CO_LOCALIDADE_EQP', max_digits=18, decimal_places=0)
    no_localidade = models.CharField(db_column='NO_LOCALIDADE', max_length=100, blank=True, null=True)
    ds_localidade = models.CharField(db_column='DS_LOCALIDADE', max_length=200, blank=True, null=True)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'TH_LOCALIDADE_EQUIPAMENTO'


class ThOperador(models.Model):
    co_seq_hist_operador = models.AutoField(db_column='CO_SEQ_HIST_OPERADOR', primary_key=True)
    co_operador = models.DecimalField(db_column='CO_OPERADOR', max_digits=18, decimal_places=0)
    co_pessoa = models.DecimalField(db_column='CO_PESSOA', max_digits=18, decimal_places=0, blank=True, null=True)
    no_login = models.CharField(db_column='NO_LOGIN', max_length=50, blank=True, null=True)
    ds_senha = models.CharField(db_column='DS_SENHA', max_length=255, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1, blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_OPERADOR'


class ThParametro(models.Model):
    co_seq_hist_parametro = models.AutoField(db_column='CO_SEQ_HIST_PARAMETRO', primary_key=True)
    co_parametro = models.DecimalField(db_column='CO_PARAMETRO', max_digits=18, decimal_places=0)
    no_parametro = models.CharField(db_column='NO_PARAMETRO', max_length=100)
    ds_tipo = models.CharField(db_column='DS_TIPO', max_length=1)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_PARAMETRO'


class ThParametroEquipamento(models.Model):
    co_seq_hist_parametro_eqp = models.AutoField(db_column='CO_SEQ_HIST_PARAMETRO_EQP', primary_key=True)
    co_parametro_eqp = models.DecimalField(db_column='CO_PARAMETRO_EQP', max_digits=18, decimal_places=0)
    co_equipamento = models.DecimalField(db_column='CO_EQUIPAMENTO', max_digits=18, decimal_places=0)
    co_parametro = models.DecimalField(db_column='CO_PARAMETRO', max_digits=18, decimal_places=0)
    vl_parametro = models.CharField(db_column='VL_PARAMETRO', max_length=50, blank=True, null=True)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_PARAMETRO_EQUIPAMENTO'


class ThParametroMiddleware(models.Model):
    co_seq_hist_parametro_md = models.AutoField(db_column='CO_SEQ_HIST_PARAMETRO_MD', primary_key=True)
    co_parametro_md = models.DecimalField(db_column='CO_PARAMETRO_MD', max_digits=18, decimal_places=0)
    co_parametro = models.DecimalField(db_column='CO_PARAMETRO', max_digits=18, decimal_places=0)
    vl_parametro = models.CharField(db_column='VL_PARAMETRO', max_length=50)
    st_atualizado = models.CharField(db_column='ST_ATUALIZADO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_PARAMETRO_MIDDLEWARE'


class ThPerfil(models.Model):
    co_seq_hist_perfil = models.AutoField(db_column='CO_SEQ_HIST_PERFIL', primary_key=True)
    co_perfil = models.DecimalField(db_column='CO_PERFIL', max_digits=18, decimal_places=0)
    no_perfil = models.CharField(db_column='NO_PERFIL', max_length=50)
    ds_perfil = models.CharField(db_column='DS_PERFIL', max_length=200, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_PERFIL'


class ThPerfilOperador(models.Model):
    co_seq_hist_perfil_op = models.AutoField(db_column='CO_SEQ_HIST_PERFIL_OP', primary_key=True)
    co_perfil_operador = models.DecimalField(db_column='CO_PERFIL_OPERADOR', max_digits=18, decimal_places=0)
    co_operador = models.DecimalField(db_column='CO_OPERADOR', max_digits=18, decimal_places=0)
    co_perfil = models.DecimalField(db_column='CO_PERFIL', max_digits=18, decimal_places=0)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_PERFIL_OPERADOR'


class ThPerimetro(models.Model):
    co_seq_hist_perimetro = models.AutoField(db_column='CO_SEQ_HIST_PERIMETRO', primary_key=True)
    co_perimetro = models.DecimalField(db_column='CO_PERIMETRO', max_digits=18, decimal_places=0)
    no_perimetro = models.CharField(db_column='NO_PERIMETRO', max_length=50)
    ds_perimetro = models.CharField(db_column='DS_PERIMETRO', max_length=200, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'TH_PERIMETRO'


class ThPessoa(models.Model):
    co_seq_hist_pessoa = models.AutoField(db_column='CO_SEQ_HIST_PESSOA', primary_key=True)
    co_pessoa = models.DecimalField(db_column='CO_PESSOA', max_digits=18, decimal_places=0)
    co_tipo_pessoa = models.DecimalField(db_column='CO_TIPO_PESSOA', max_digits=18, decimal_places=0)
    no_pessoa = models.CharField(db_column='NO_PESSOA', max_length=100)
    st_pne = models.CharField(db_column='ST_PNE', max_length=1, blank=True, null=True)
    id_risco = models.SmallIntegerField(db_column='ID_RISCO', blank=True, null=True)
    ds_link_foto = models.CharField(db_column='DS_LINK_FOTO', max_length=250, blank=True, null=True)
    co_empresa = models.DecimalField(db_column='CO_EMPRESA', max_digits=18, decimal_places=0, blank=True, null=True)
    co_departamento = models.DecimalField(db_column='CO_DEPARTAMENTO', max_digits=18, decimal_places=0, blank=True, null=True)
    co_cargo = models.DecimalField(db_column='CO_CARGO', max_digits=18, decimal_places=0, blank=True, null=True)
    nu_andar = models.CharField(db_column='NU_ANDAR', max_length=20, blank=True, null=True)
    co_zona_tempo = models.DecimalField(db_column='CO_ZONA_TEMPO', max_digits=18, decimal_places=0, blank=True, null=True)
    nu_cpf = models.CharField(db_column='NU_CPF', max_length=11, blank=True, null=True)
    nu_rg = models.CharField(db_column='NU_RG', max_length=20, blank=True, null=True)
    ds_orgao_emissor = models.CharField(db_column='DS_ORGAO_EMISSOR', max_length=50, blank=True, null=True)
    nu_passaporte = models.CharField(db_column='NU_PASSAPORTE', max_length=25, blank=True, null=True)
    nu_cnh = models.CharField(db_column='NU_CNH', max_length=25, blank=True, null=True)
    nu_telefone_principal = models.CharField(db_column='NU_TELEFONE_PRINCIPAL', max_length=25, blank=True, null=True)
    nu_telefone_celular = models.CharField(db_column='NU_TELEFONE_CELULAR', max_length=25, blank=True, null=True)
    ds_email_particular = models.CharField(db_column='DS_EMAIL_PARTICULAR', max_length=50, blank=True, null=True)
    ds_email_profissional = models.CharField(db_column='DS_EMAIL_PROFISSIONAL', max_length=50, blank=True, null=True)
    dt_nascimento = models.DateField(db_column='DT_NASCIMENTO', blank=True, null=True)
    ds_observacao = models.CharField(db_column='DS_OBSERVACAO', max_length=150, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_visitada = models.DecimalField(db_column='CO_PESSOA_VISITADA', max_digits=18, decimal_places=0, blank=True, null=True)
    co_motivo_bloqueio = models.DecimalField(db_column='CO_MOTIVO_BLOQUEIO', max_digits=18, decimal_places=0, blank=True, null=True)
    dt_inicio_bloqueio = models.DateTimeField(db_column='DT_INICIO_BLOQUEIO', blank=True, null=True)
    dt_fim_bloqueio = models.DateTimeField(db_column='DT_FIM_BLOQUEIO', blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0, blank=True, null=True)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.DecimalField(db_column='TP_DML', max_digits=18, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'TH_PESSOA'


class ThRotaEquipamento(models.Model):
    co_seq_hist_rota_equip = models.AutoField(db_column='CO_SEQ_HIST_ROTA_EQUIP', primary_key=True)
    co_rota_equipamento = models.DecimalField(db_column='CO_ROTA_EQUIPAMENTO', max_digits=18, decimal_places=0)
    co_rota_fuga = models.DecimalField(db_column='CO_ROTA_FUGA', max_digits=18, decimal_places=0)
    co_equipamento = models.DecimalField(db_column='CO_EQUIPAMENTO', max_digits=18, decimal_places=0)
    st_modo_operacao = models.CharField(db_column='ST_MODO_OPERACAO', max_length=1)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_ROTA_EQUIPAMENTO'


class ThRotaFuga(models.Model):
    co_seq_hist_rota_fuga = models.AutoField(db_column='CO_SEQ_HIST_ROTA_FUGA', primary_key=True)
    co_rota_fuga = models.DecimalField(db_column='CO_ROTA_FUGA', max_digits=18, decimal_places=0)
    ds_rota_fuga = models.CharField(db_column='DS_ROTA_FUGA', max_length=150, blank=True, null=True)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_ROTA_FUGA'


class ThTipoAcesso(models.Model):
    co_seq_hist_tp_acesso = models.AutoField(db_column='CO_SEQ_HIST_TP_ACESSO', primary_key=True)
    co_tipo_acesso = models.DecimalField(db_column='CO_TIPO_ACESSO', max_digits=18, decimal_places=0)
    ds_acesso = models.CharField(db_column='DS_ACESSO', max_length=100)
    st_ativo = models.CharField(db_column='ST_ATIVO', max_length=1)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'TH_TIPO_ACESSO'


class ThTipoPessoa(models.Model):
    co_seq_hist_tp_pessoa = models.AutoField(db_column='CO_SEQ_HIST_TP_PESSOA', primary_key=True)
    co_tipo_pessoa = models.DecimalField(db_column='CO_TIPO_PESSOA', max_digits=18, decimal_places=0)
    ds_tipo = models.CharField(db_column='DS_TIPO', max_length=50)
    ds_info_tipo = models.IntegerField(db_column='DS_INFO_TIPO', blank=True, null=True)
    co_pessoa_cadastro = models.DecimalField(db_column='CO_PESSOA_CADASTRO', max_digits=18, decimal_places=0, blank=True, null=True)
    dt_cadastro = models.DateTimeField(db_column='DT_CADASTRO')
    tp_dml = models.SmallIntegerField(db_column='TP_DML')

    class Meta:
        managed = True
        db_table = 'TH_TIPO_PESSOA'
