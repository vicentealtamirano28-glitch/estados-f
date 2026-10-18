import content_guia, content_otros
O='/projects/sandbox/Guia_CCI/'
content_guia.build(O+'01_Guia_Completa_CCI.docx')
content_otros.resumen(O+'02_Resumen_Express_CCI.docx')
content_otros.ejercicios(O+'05_Ejercicios_Resueltos_CCI.docx')
content_otros.plantilla(O+'08_Plantilla_Estrategia_Equipo.docx')
print('ok')
