# coding: utf-8 -*-
from datetime import datetime
from api.mixins import APIViewMixin

from data.models import OcorrenciasMesData, PoliciaDpsAreas

class OcorrenciasView(APIViewMixin):
    get_services = ("get_ocorrencias", "get_top_ocorrencias")

    def _get_ocorrencias(self, data):
        response = {
            "ocorrencias": []
        }

        ano = data.get("ano")
        if not ano:
            ano = datetime.now().year - 1

        ocorrencias = OcorrenciasMesData.objects.all().filter(
            ano__gte=ano
        )
        for o in ocorrencias:
            response["ocorrencias"].append(o.to_json())
            
        
        return response
    
    def _get_top_ocorrencias(self, data):
        response = {}
        ano = data.get("ano")
        if not ano:
            ano = datetime.now().year - 1
        
        ocorrencias = OcorrenciasMesData.objects.all().filter(
            ano__gte=ano
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

