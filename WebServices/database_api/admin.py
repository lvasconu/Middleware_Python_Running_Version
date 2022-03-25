from django.contrib import admin
from django.http import HttpResponseRedirect

from . import models, models_methods    # https://medium.com/hackernoon/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5

# Registering all models in admin page.
model_list = models_methods.get_all_models()
for model in model_list:
    try:
        admin.site.register(model)
    except:
        pass

""" Registering specifically TbPessoa
@admin.register(models.TbPessoa)
class PessoaAdmin(admin.ModelAdmin):
    ''' Customize the Django Admin
    Ref: https://realpython.com/customize-django-admin-python/
    '''

    ''' Fields:
    co_seq_pessoa
    co_importacao
    co_tipo_pessoa
    no_pessoa
    st_pne
    id_risco
    ds_link_foto
    co_empresa
    co_departamento
    co_cargo
    nu_andar
    co_zona_tempo
    nu_cpf
    nu_rg
    ds_orgao_emissor
    nu_passaporte
    nu_cnh
    nu_telefone_principal
    nu_telefone_celular
    ds_email_particular
    ds_email_profissional
    dt_nascimento
    ds_observacao
    st_ativo
    co_pessoa_visitada
    co_motivo_bloqueio
    dt_inicio_bloqueio
    dt_fim_bloqueio
    co_pessoa_cadastro
    dt_cadastro
    '''

    change_form_template = 'database_api\pessoa_change_form.html'   # Changing the template.
    list_display = ('no_pessoa', 'nu_cpf')                          # Editing what collumns will be displayed.
    #list_filter = ('no_pessoa', 'nu_cpf')                          # Adding filter.
    search_fields = ('no_pessoa', 'nu_cpf')                         # Adding search bar.
    fields = (                                                      # Fields to be shown.
                #'co_seq_pessoa',
                #'co_importacao',
                'co_tipo_pessoa',
                'no_pessoa',
                'st_pne',
                #'id_risco',
                #'ds_link_foto',
                'co_empresa',
                'co_departamento',
                'co_cargo',
                'nu_andar',
                'co_zona_tempo',
                'nu_cpf',
                'nu_rg',
                'ds_orgao_emissor',
                'nu_passaporte',
                'nu_cnh',
                'nu_telefone_principal',
                'nu_telefone_celular',
                'ds_email_particular',
                'ds_email_profissional',
                'dt_nascimento',
                'ds_observacao',
                'st_ativo',
                'co_pessoa_visitada',
                'co_motivo_bloqueio',
                'dt_inicio_bloqueio',
                'dt_fim_bloqueio'
                #'co_pessoa_cadastro',
                #'dt_cadastro',
    )

    def get_form(self, request, obj=None, **kwargs):
        ''' Editing form labels. '''
        form = super().get_form(request, obj, **kwargs)

        for field in form.base_fields:
            form.base_fields[field].label = form.base_fields[field].label[3:]                                               # Removing three first characters.
            form.base_fields[field].label = form.base_fields[field].label.replace('_',' ')                                  # Changing undescore to space.
            form.base_fields[field].label = form.base_fields[field].label[0].upper() + form.base_fields[field].label[1:]    # Putting 1st letter to uppercase.
                
        form.base_fields['co_tipo_pessoa'].label = 'Tipo'
        form.base_fields['no_pessoa'].label = 'Nome'
        form.base_fields['st_pne'].label = 'É PNE?'
        #form.base_fields['id_risco'].label = 'id_risco'
        #form.base_fields['ds_link_foto'].label = 'Link para foto'
        #form.base_fields['co_empresa'].label = 'Empresa'
        #form.base_fields['co_departamento'].label = 'Departamento'
        #form.base_fields['co_cargo'].label = 'Cargo'
        #form.base_fields['nu_andar'].label = 'Andar'
        form.base_fields['co_zona_tempo'].label = 'Zona de Tempo'
        form.base_fields['nu_cpf'].label = 'CPF'
        form.base_fields['nu_rg'].label = 'RG'
        #form.base_fields['ds_orgao_emissor'].label = 'Órgão Emissor'
        #form.base_fields['nu_passaporte'].label = 'Passaporte'
        form.base_fields['nu_cnh'].label = 'CNH'
        #form.base_fields['nu_telefone_principal'].label = 'Telefone principal'
        #form.base_fields['nu_telefone_celular'].label = 'Telefone celular'
        #form.base_fields['ds_email_particular'].label = ''
        #form.base_fields['ds_email_profissional'].label = ''
        #form.base_fields['dt_nascimento'].label = ''
        form.base_fields['ds_observacao'].label = 'Observação'
        form.base_fields['st_ativo'].label = 'Ativo'
        #form.base_fields['co_pessoa_visitada'].label = ''
        #form.base_fields['co_motivo_bloqueio'].label = ''
        #form.base_fields['dt_inicio_bloqueio'].label = ''
        #form.base_fields['dt_fim_bloqueio'].label = ''
        #form.base_fields['co_pessoa_cadastro'].label = 'Pessoa que realizou o cadastro'
        #form.base_fields['dt_cadastro'].label = 'Data de cadastro'

        return form

    def response_change(self, request, obj):
        ''' Overriding method to add custom actions.
            Ref: https://books.agiliq.com/projects/django-admin-cookbook/en/latest/custom_button.html
        '''

        if '_anonymize' in request.POST:
            obj.anonymize()
            self.message_user(request, 'Pessoa tornada anônima.')
            return HttpResponseRedirect('.')

        return super().response_change(request, obj)


"""