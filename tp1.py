#!usr/bin/env python3
import re
import json

#abrir o medicina.xml e ler o ficheiro
medicina = open("medicina.xml", 'r')
medicina = medicina.read()

#Criação de um ficheiro json
file = open("dicionario.json", "w")

########################## LIMPEZA DO DOCUMENTO ##################################

#Eliminação das linhas iniciais que não fazem parte das entradas do dicionário em si
medicina = re.sub(r'xml[\s\S]+?\n*<b>A</b>', r'<b>A</b>', medicina)

#Eliminação das linhas finais que não fazem parte das entradas do dicionário em si
medicina = re.sub(r'Í[\s\n]*ndice[\s\S]*', r'', medicina)
medicina = re.sub(r'Í[\s\S]*<b>', r'', medicina)

#Eliminação do <? que sobrou
medicina = re.sub(re.escape('<?'), r'', medicina)

#Eliminação das linhas FFVocabulario
medicina = re.sub(r'V.*\n.*ocabulario.*\n.*\d+', r'', medicina)

#Eliminação da 1ª tag <text > de cada linha
medicina = re.sub(r'<text.+?>', r'', medicina)

#Eliminação dos </text> 
medicina = re.sub(r'</text>', r'', medicina)

#Eliminação das <page>
medicina = re.sub(r'<page.*>', r'', medicina)

#Eliminação das </page> 
medicina = re.sub(r'</page>', r'', medicina)

#Eliminação das tags <fontspec >
medicina = re.sub(r'<fontspec.*>', r'', medicina)

#Eliminação das tags <b> </b> que não tem texto no seu interior
medicina = re.sub(r'<b>[\s\n]*</b>', r'', medicina)

#Eliminação das tags <i> </i> que não tem texto no seu interior
medicina = re.sub(r'<i>[\s\n]*</i>', r'', medicina)

#Eliminação de espaços antes do início das palavras
medicina = re.sub(r'<b>\s+(.*)</b>', r'<b>\1</b>', medicina)
medicina = re.sub(r'<i>\s+(.*)</i>', r'<i>\1</i>', medicina)

#Eliminação das tags <i><b> e </b></i> juntas
medicina = re.sub(r'<i><b>(.*)</b></i>', r'\1', medicina)


########################## CORREÇÕES ##################################

#Expressões regulares que fazem match com todas as abreviaturas e com todos os temas
abreviaturas=r"\b(a|abrev|arc|Br|col|cult|EE UU|f|lit|loc|m|pl|pop|Pt|s|sb|sg)\b"
temas = r'''(Patoloxías|Etiopatoxenia|Probas complementarias|Terapéutica|Medicina preventiva|Farmacoloxía|Anatomía|Anatomía patolóxica|
Semioloxía|Fisioloxía|Epidemioloxía|Histoloxía|Bioquímica|Xenética|Organización sanitaria|Instrumental|Termos xerais|Preventiva)'''

#Substituir as linhas das entradas normais que ficam em 2 linhas por uma linha só
medicina = re.sub(r'<b>(\d+.*)</b>\n\n<b>(.*)', r'<b>\1 \2', medicina)

#Substituir as linhas das entradas normais que ficam em 3 linhas por 1 só linha
medicina = re.sub(r'<b>(\d+).*</b>\n(.+)\n<b>(.+)</b>', r'<b>\1 \2 \3 </b>', medicina)

#Substituir as linhas das entradas normais que ficam com a abreviatura na linha seguinte por 1 linha só
medicina = re.sub(r'<b>(\d+)(.*)</b>\n<b>(.*)</b>', r'<b>\1 \2 \3 </b>', medicina)

#Substituir as linhas das entradas normais que tem o índice numa linha e o resto da entrada noutra linha por uma única linha com tudo
def processa_espacos(matching):
    res = matching[0]
    res = re.sub(r'\n', r' ', res)
    res = re.sub(r'<b>|</b>', r'', res)
    res = re.sub(r'(\d{2,})', r'<b>\1', res)
    res = re.sub(abreviaturas, r'\1</b>\n', res)
    return res

medicina = re.sub(r'\d{2,}\s*\n<b>[^\d]+?</b>[\s\S]+?<i>', processa_espacos, medicina)

#Substituir as linhas das entradas remissivas que ficam em 2 linhas por 1 linha só
medicina = re.sub(r'<b>(.+)</b>\n(.+)([\n\s]+Vid)', r'<b>\1 \2</b> \3', medicina)


########################## IDENTIFICAÇÃO DAS ENTRADAS ##################################

#Marcação do início de entradas normais e remissivas com #@. De @ em @ está toda a informação de um termo
medicina = re.sub(r'(.*[\s\n]+?Vid)', r'#@ \1', medicina)
medicina = re.sub(r'<b>(\d[^<]*)</b>', r'#@ <b>\1</b>', medicina)

#Fazer o split do documento por @, em que entre cada 2 @ tem uma entrada diferente
entradas =  re.split(r'@', medicina)


########################## PROCESSAMENTO DAS ENTRADAS ##################################

dic = {}

#função auxiliar para separar os vários campos das traduções (es, en, pt e la), dos sinónimos e das variantes
def separa(lista):
    dic = {}
    for ele in lista:
        ele = ele.strip()
        campo = re.findall(r'(.*)' + re.escape('[') + r'(.*)'+ re.escape(']'), ele)
        abv = re.findall(r'(.*)' + re.escape('(') + r'(.*)'+ re.escape(')'), ele)
        if campo != []:
            dic[campo[0][1]] = campo[0][0]
        elif abv != []:
            if abv[0][1] in dic.keys():
                dic[abv[0][1]].append(abv[0][0])
            else:
                dic[abv[0][1]] = [abv[0][0]]
        else:
            if 'definicao(oes)' in dic.keys():
                dic['definicao(oes)'].append(ele)
            else:
                dic['definicao(oes)'] = [ele]
    return dic

def processa_tema(matching):
    tema = matching[0]
    tema = re.sub(r'<i>|</i>', r'', tema)
    tema = re.sub(r'[\s]{2,}', r'; ', tema)
    if re.search(r';', tema):
        tema = re.split(r';', tema)
    return tema

def processa_trad(matching):
    if matching != None:
        trad = matching[0]
        trad = re.sub(r'\n|en\s\n|pt\s\n|en\s\n|la\s\n|Nota|#|<i>|</i>|es\s\n|<b>|</b>', r'',trad)
        trad = re.split(r';', trad)
        traducao = separa(trad)
        return traducao

def processa_extra(matching):
    if matching != None:
        extra = matching[0]
        extra = re.sub(r'\n\s\n\s*(.+)', r'\1',extra)
        extra = re.sub(r'SIN.-|<i>|</i>|VAR.-|es\s\n|</b>|#', r'',extra)
        extra = re.split(r';', extra)
        extras = separa(extra)
        return extras

def processa_notas(matching):
    if matching != None:
        nots = matching[0]
        nots = re.sub(r'\s{2,}', r' ',nots)
        nots = re.sub(r'Nota.-|<b>|</b>|\n|#|”|“|‘|’', r'',nots)
        nots = re.split(r';', nots)
        notas = separa(nots)
        return notas

def processa_vid(matching):
    if matching != None:
        termo_remissivo = matching[1]
        entrada = matching[2]
        termo_remissivo = re.sub(r'-|\s', r'', termo_remissivo)
        termo_remissivo = re.sub(re.escape('*'), r'', termo_remissivo)
        termo_remissivo = re.sub(r'<b>|\n|</b>|<i>|</i>', r'', termo_remissivo)
        entrada = re.sub(re.escape('.'), r'', entrada)
        entrada = re.sub(r'-|\s', r'', entrada)
        return termo_remissivo, entrada

def processa_entradas(entradas):
    c = 0
    for entrada in entradas:

        #para entradas normais
        if re.search(r'<b>(\d+)(.+)</b>', entrada):
            
            #a entrada tem mais de uma abreviatura
            if re.search(r'<b>(\d+)(.+)' + abreviaturas + r' ' + abreviaturas + r'.*</b>', entrada):
                ent = re.search(r'<b>(\d+)(.+)' + abreviaturas + r' ' + abreviaturas + r'.*</b>', entrada)
                abv = [ent.group(3), ent.group(4)]
            
            else:
                ent = re.search(r'<b>(\d+)(.+)' + abreviaturas + r'.*</b>', entrada)
                #a entrada não tem abreviatura
                if ent == None:
                    ent = re.search(r'<b>(\d+)(.+)(.*)</b>', entrada)
                    abv = None
                #a entrada tem apenas uma abreviatura
                else:
                    abv = ent.group(3)

            tema = re.search(r'<i>' + temas + r'.*', entrada)
            espanhol = re.search(r'es\s\n<i>[\s\S]+?en\s\n', entrada)
            ingles = re.search(r'en\s\n<i>[\s\S]+?pt\s\n', entrada)
            portugues = re.search(r'pt\s\n<i>([\s\S]+?la\s\n|[\s\S]+?Nota|[\s\S]+)', entrada)
            latim = re.search(r'la\s\n<i>([\s\S]+?Nota|[\s\S]+)', entrada)
            sinonimos = re.search(r'SIN[\s\S]+?(VAR|es\s\n)', entrada)
            variantes = re.search(r'VAR[\s\S]+?es\s\n', entrada)
            notas = re.search(r'Nota[\s\S]+?\n*#', entrada)
            tem = processa_tema(tema)
            es = processa_trad(espanhol)
            en = processa_trad(ingles)
            pt = processa_trad(portugues)
            la = processa_trad(latim)
            sin = processa_extra(sinonimos)
            var = processa_extra(variantes)
            nots = processa_notas(notas)
            dic[ent.group(1).strip()] = {
                "termo: " : ent.group(2).strip(),
                "abv: " : abv,
                "tema: " : tem,
                "es: " : es,
                "en: " : en,
                "pt: " : pt,
                "la: " : la,
                "sin: " : sin,
                "var: " : var,
                "notas: " : nots
            }

        #para entradas remissivas que se devem evitar
        elif re.search(re.escape('*'), entrada):
            c += 1
            remissiva = re.search(r'(.*)[\s\n]+?Vid(.*)', entrada)
            termo_remissivo, entrada = processa_vid(remissiva)
            dic["vid "+str(c)] = {
                "termo: " : termo_remissivo,
                "entrada: " : entrada,
                "utilizacao" : "evitar usar esse termo"
            }
        
         #para entradas remissivas que não se precisam de evitar
        elif re.search(r'(Vid.+)', entrada):
            c += 1
            remissiva = re.search(r'(.*)[\s\n]+?Vid(.*)', entrada)
            termo_remissivo, entrada = processa_vid(remissiva)
            dic["vid "+str(c)] = {
                "termo: " : termo_remissivo,
                "entrada: " : entrada
            }
    return dic


########################## ELIMINAÇÃO DOS VALORES NULOS ##################################

def elimina_nulos(d):
    limpo = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = elimina_nulos(v)
            if len(nested.keys()) > 0:
                limpo[k] = nested
        elif v is not None:
            limpo[k] = v
    return limpo


########################## EXECUÇÃO DO CÓDIGO PARA CRIAR O DICIONÁRIO E GUARDÁ-LO NO FICHEIRO JSON ##################################

dic = processa_entradas(entradas)
limpo = elimina_nulos(dic)

#Guardar o dicionário no jsonfile
json.dump(limpo, file, indent=4, ensure_ascii = False)