import io

import requests
from django import forms
from django.conf import settings
from django.core.serializers import deserialize
from django.forms import inlineformset_factory, formset_factory


from core.forms import BaseForm
from .models import Telefone, Projeto, Autor, Avaliador, Avaliacao, Cronograma, Premio


class TelefoneForm(BaseForm):
    class Meta:
        exclude = ['deleted', 'enabled', 'pessoa']
        model = Telefone


class ProjetoForm(BaseForm):
    class Meta:
        exclude = ['deleted', 'enabled', 'autor']
        model = Projeto


class AutorForm(BaseForm):
    class Meta:
        exclude = ['deleted', 'enabled']
        model = Autor


class AvaliadorForm(BaseForm):
    class Meta:
        exclude = ['deleted', 'enabled']
        model = Avaliador


class AvaliacaoForm(BaseForm):
    avaliador_id = forms.ChoiceField(choices=[], widget=forms.Select())
    projeto_id = forms.ChoiceField(choices=[], widget=forms.Select())

    class Meta:
        exclude = ['deleted', 'enabled', 'avaliador', 'projeto']
        model = Avaliacao
        fields = ['avaliador_id', 'projeto_id', 'parecer', 'nota', 'data']

    def __init__(self, *args, **kwargs):
        super(AvaliacaoForm, self).__init__(*args, **kwargs)

        lista_projeto = Projeto().listar_projetos_nao_avaliados()

        if self.instance.projeto_id:
            projeto_atual = Projeto().get_list_all('projeto/list/%s'%self.instance.projeto_id)
            projeto_atual.pop('autor')
            projeto_atual = Projeto(**projeto_atual)
            lista_projeto += [(projeto_atual.id, str(projeto_atual))]

        self.fields.get('projeto_id').choices = lista_projeto
        self.fields['projeto_id'].initial = self.instance.projeto_id

        lista_avaliador = Avaliador().get_list_choice_all()
        self.fields.get('avaliador_id').choices = lista_avaliador
        self.fields['avaliador_id'].initial = self.instance.avaliador_id


class CronogramaForm(BaseForm):
    class Meta:
        exclude = ['deleted', 'enabled', 'premio']
        model = Cronograma


class PremioForm(BaseForm):
    projeto_id = forms.ChoiceField(choices=[], widget=forms.Select())

    # metodo colocado pois o onetoonefileld valida de acordo com o banco
    def _get_validation_exclusions(self):
        return super()._get_validation_exclusions() + ['projeto']

    def __init__(self, *args, **kwargs):
        super(PremioForm, self).__init__(*args, **kwargs)

        lista_projeto = Projeto().get_list_choice_all('ProjetosNaoPremiados/')
        if self.instance.projeto_id:
            projeto_atual = Projeto().get_list_all('projeto/list/%s'%self.instance.projeto_id)
            projeto_atual.pop('autor')
            projeto_atual = Projeto(**projeto_atual)
            lista_projeto += [(projeto_atual.id, str(projeto_atual))]

        self.fields.get('projeto_id').choices = lista_projeto

        self.fields['projeto_id'].initial = self.instance.projeto_id

    class Meta:
        exclude = ['deleted', 'enabled', 'projeto']
        model = Premio
        fields = ['projeto_id', 'nome', 'descricao', 'ano']


TelefoneFormSet = formset_factory(TelefoneForm, extra=0, min_num=0, max_num=3, can_delete=True)

ProjetoFormSett = formset_factory(ProjetoForm, extra=0, min_num=1, max_num=1, can_delete=True)

CronogramaFormSet = formset_factory(CronogramaForm, extra=0, min_num=1, max_num=1, can_delete=True)
