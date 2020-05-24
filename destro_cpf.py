import time
import concurrent.futures
#importa bibliotecas de time para medir tempo de processamento
#importa concurrent.futures para dividir o processamento em paralelo

#calculo digito verificador CPF
def calcCPF(pos,docPronto):
    prim = 0
    val = 10
    #realiza soma dos produtos do valor do cpf com as respectivas variáveis
    for n in pos:
        n = int(n)
        prim = prim + (n*val)
        val = val - 1
    #realiza contas para verificar se o número será o resto ou 0
    prim = 11 - (prim%11)
    if prim >= 10:
        prim = 0    
    #cocatena o novo valor ao CPF
    pos = pos + str(prim)
    seg = 0
    val = 11
    #repete o processo com um digito a mais
    for n in pos:
        n = int(n)
        seg = seg + (n*val)
        val = val - 1
    seg = seg%11
    seg = 11 - seg
    if seg >= 10:
        seg = 0
    pos = pos + str(seg)
    #cocatena o CPF, com os digitos verificadores, a respectiva lista
    docPronto.append(pos)

#calculo digito verificador CNPJ    
def calcCNPJ(pos,docPronto):
    prim = 0
    val = 5
    #realiza soma dos produtos do valor do CNPJ com as respectivas variáveis
    for n in pos:
        if val <2:
            val = 9
        n = int(n)
        prim = prim + (n*val)
        val = val - 1
    #realiza contas para verificar se o número será o resto ou 0
    prim = 11 - (prim%11)
    if prim >= 10:
        prim = 0  
    #cocatena o novo valor ao CNPJ
    pos = pos + str(prim)
    seg = 0
    val = 6
    #repete o processo com um digito a mais
    for n in pos:
        if val <2:
            val = 9
        n = int(n)
        seg = seg + (n*val)
        val = val - 1
    seg = 11 - (seg%11)
    if seg >= 10:
        seg = 0    
    pos = pos + str(seg)
    #cocatena o CNPJ, com os digitos verificadores, a respectiva lista
    docPronto.append(pos)

#chama as funções de cálculo de CPF e CNPJ
def calc(vet,r):
    #identifica se é um CPF ou CNPJ dependendo do tamanho da sequência
    for line in vet:
        if len(line)==9:
            calcCPF(line,r)
        elif len(line)==12:
            calcCNPJ(line,r)
    #retorna o valor da lista com os CPFs e CNPJs contendo o digito verificador
    return r

#poupar processamento para não realizar a importação das bibliotecas em loop
if __name__=='__main__':
    #abre o arquivo txt 
    with open('BASEPROJETO.txt','r+') as banco:
        #preenche uma lista com os valores do txt
        total =  [linha.strip(' ').strip('\n') for linha in banco.readlines()]
    #declaração dos vetores que serão utilizados em cada subprocesso
    global r1,r2,r3,r4
    r1 = []
    r2 = []
    r3 = []
    r4 = []
    
    #divisao da lista em 4 pedaços para dividi-las entre os processadores    
    vet1 = total[:300000]
    vet2 = total[300000:600000]
    vet3 = total[600000:900000]
    vet4 = total[900000:1200000]
    
    #declara o uso de 4 de no máximo 4 processadores para essa tarefa
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        #inicio do calculo para o tempo
        init = time.time()
        #chamada dos subprocessos com seus respectivos parametros:
        a = executor.submit(calc,vet1,r1)
        print('mult1')
        b = executor.submit(calc,vet2,r2)
        print('mult2')
        c = executor.submit(calc,vet3,r3)
        print('mult3')
        d = executor.submit(calc,vet4,r4)
        print('mult4')
        #força os processos a retornarem o resultado das funções
        r1 = a.result()
        r2 = b.result()
        r3 = c.result()
        r4 = d.result()
        #cocatena os resultados ao terminar os subprocessos
        listas = r1 + r2 + r3 + r4
    #imprime o tempo total do procedimento
    total = time.time() - init
    print(total)


        
        
        
        
        
        
        
        