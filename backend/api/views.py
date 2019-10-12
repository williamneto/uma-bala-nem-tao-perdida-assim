# coding: utf-8 -*-
from datetime import datetime
from api.mixins import APIViewMixin

from data.models import OcorrenciasMesData, PoliciaDpsAreas

CRIMES_VIOLENTOS = ["roubo_transeunte", "roubo_celular", "lesao_corp_dolosa", "outros_roubos", "roubo_veiculo", "roubo_comercio", "roubo_em_coletivo", "tentat_hom", "roubo_apos_saque", "estupro", "roubo_bicicleta", "roubo_carga", "roubo_residencia", "hom_doloso", "hom_por_interv_policial", "roubo_conducao_saque", "roubo_banco", "sequestro_relampago", "sequestro", "latrocinio", "lesao_corp_morte", "pol_civis_mortos_serv", "pol_militares_mortos_serv"]
class OcorrenciasView(APIViewMixin):
    get_services = ("get_ocorrencias", "get_top_ocorrencias")

    def _get_ocorrencias(self, data):
        response = {}

        aisp = data.get("aisp")
        risp = data.get("risp")
        ano = data.get("ano")
        if not ano:
            ano = datetime.now().year
        
        if aisp:
            ocorrencias = OcorrenciasMesData.objects.all().filter(
                ano=int(ano),
                mes__lte=9,
                aisp=aisp
            )
        elif risp:
            ocorrencias = OcorrenciasMesData.objects.all().filter(
                ano=int(ano),
                mes__lte=9,
                risp=risp
            )
        else:
            ocorrencias = OcorrenciasMesData.objects.all().filter(
                ano=int(ano),
                mes__lte=9,
            )

        indice = {
            "crimes_violentos": 0,
            "roubos_furtos": 0
        }
        fields = ["apf", "cmp", "cmba", "fase", "aaapai"]
        for o in ocorrencias:
            for key, value in o.ocorrencias.items():
                if not key in fields:
                    if key in CRIMES_VIOLENTOS:
                        indice["crimes_violentos"] += int(value or 0)
            indice["roubos_furtos"] += int(o.ocorrencias["total_roubos"]) + int(o.ocorrencias["total_furtos"])
        
        response["top_ocorrencias"] = [{k: indice[k]} for k in sorted(indice, key=indice.get, reverse=True)]

        return response
    
    def _get_top_ocorrencias(self, data):
        response = {}

        aisp = data.get("aisp")
        risp = data.get("risp")
        ano = data.get("ano")
        if not ano:
            ano = datetime.now().year
        
        if aisp:
            ocorrencias = OcorrenciasMesData.objects.all().filter(
                ano=int(ano),
                aisp=aisp
            )
        elif risp:
            ocorrencias = OcorrenciasMesData.objects.all().filter(
                ano=int(ano),
                risp=risp
            )

        indice = {}
        fields = ["apf", "cmp", "cmba", "fase", "aaapai", "registro_ocorrencias", "indicador_roubo_rua", "outros_furtos"]
        for o in ocorrencias:
            for key, value in o.ocorrencias.items():
                if not key in fields and not "furto_" in key and not "roubo" in key:
                    if len(key) > 1 and key in indice:
                        indice[key] += int(value or 0)
                    else:
                        indice[key] = int(value or 0)
        
        response["top_ocorrencias"] = [{k: indice[k]} for k in sorted(indice, key=indice.get, reverse=True)]
    
        return response

