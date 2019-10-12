# coding: utf-8 -*-
from datetime import datetime
from api.mixins import APIViewMixin

from data.models import OcorrenciasMesData, PoliciaDpsAreas

CRIMES_VIOLENTOS = ["lesao_corp_dolosa", "lesao_corp_culposa", "tentat_hom", "estupro", "hom_culposo", "hom_doloso", "latrocinio"]
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
                aisp=aisp
            )
        elif risp:
            ocorrencias = OcorrenciasMesData.objects.all().filter(
                ano=int(ano),
                risp=risp
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
        fields = ["apf", "cmp", "cmba", "fase", "aaapai"]
        for o in ocorrencias:
            for key, value in o.ocorrencias.items():
                if not key in fields:
                    if len(key) > 1 and key in indice:
                        indice[key] += int(value or 0)
                    else:
                        indice[key] = int(value or 0)
        
        response["top_ocorrencias"] = [{k: indice[k]} for k in sorted(indice, key=indice.get, reverse=True)]
    
        return response

