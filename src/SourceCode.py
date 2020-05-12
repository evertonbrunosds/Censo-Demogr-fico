'''
/*******************************************************************************
Autor: Everton Bruno Silva dos Santos
Concluido em:04/08/2019
/*******************************************************************************
'''
import os #BIBLIOTECA QUE HABILITA O USO DE COMANDO EXTERNOS

def ShowVisualMenu():#MENU PRINCIPAL: LAYOUT
        ClearScreen()
        print('|'+'-'*68+'|\n|'+'-'*26+'MENU DE CONTROLE'+'-'*26+'|\n|'+'-'*68+'|')
        print('|      1) Números de domicílios utilizados para a coleta             |')
        print('|      2) Número de domicílios particulares que já estão pagos,      |')
        print('|          quantos ainda estão pagando e alugados                    |')
        print('|      3) Quantos domicílios por cidade possuem banheiro e           |')
        print('|          quantos não possuem                                       |')
        print('|      4) A forma mais comum de abastecimento de água por cidade     |')
        print('|      5) O percentual de domicílios por cidade que ainda não        |')
        print('|          possuem energia elétrica                                  |')
        print('|      6) O percentual de moradores que participaram da entrevista   |')
        print('|          por cor ou raça                                           |')
        print('|      7) A região com maior número de municípios pesquisados        |')
        print('|      8) Exibir todas as estatísticas                               |')
        print('|      9) Para sair do programa'+' '*38+'|\n|'+'-'*68+'|\n\n')

def ConsiderLoading(data,ShowMenu):#CONSIDERA O TEMPO DE CARREGAMENTO DE OUTRAS FUNÇÕES ANTES DE LIMPAR "CARREGADO..." DA TELA
    if (ShowMenu == True):
        ShowVisualMenu()
    else:
        ClearScreen()
    return(data)

def ClearScreen():#LIMPAR A TELA DO CONSOLE
    if(os.name == 'posix'):#CONSIDERA QUE O SISTEMA SEJA LINUX, ANDROID OU MAC
        os.system('clear')#EXECUTA COMANDO DE LIMPAR A TELA ADAPTADO AO LINUX, ANDROID OU MAC
    elif(os.name == 'nt'):#CONSIDERA QUE O SISTEMA SEJA WINDOWS
        os.system('cls')#EXECUTA COMANDO DE LIMPAR A TELA ADAPTADO WINDOWS

def DirectoryBase():#RETORNA DIRETÓRIO DOS ARQUIVOS ADAPTADO AO SISTEMA
    if (os.name == 'posix'):#CONSIDERA QUE O SISTEMA SEJA LINUX, ANDROID OU MAC
        return('FileBase/')#RETORNA A ESTRUTURA DE DIRETÓRIO ADAPTADA AO LINUX, ANDROID, MAC
    elif (os.name == 'nt'):#CONSIDERA QUE O SISTEMA SEJA WINDOWS
        return('FileBase\\')#RETORNA A ESTRUTURA DE DIRETÓRIO ADAPTADA AO WINDOWS

def LoadFromFile(fileName):#RETORNA ARQUIVO COMO MATRIZ
    fileToMatrix = []
    try:
        fileStream = open((DirectoryBase()+fileName),'r',encoding='UTF-8')#CARREGA ARQUIVO NA MEMÓRIA
    except:
        print('Falha ao carregar o arquivo "'+fileName+'" no diretório "FileBase"!')
        pause=input('O software não funcionará corretamente!\nDigite [ENTER] para continuar...')
        return(fileToMatrix)
    for fileElement in fileStream:
        fileToMatrix.append(fileElement.split(';'))
    fileStream.close()#DESCARREGA ARQUIVO DA MEMÓRIA
    return(fileToMatrix)

def FormatLength(data):#RETORNA UM DADO CENTRALIZADO EM 70 CARACTERES, EX: |---DADO---|
    lenChar=int((len(data))/2)
    if (lenChar<=35):
        DataFormated=('|'+' '*(34-lenChar)+data)
        if (len(DataFormated) < 70):
        	DataFormated+=(' '*(69-len(DataFormated))+'|')
        	return(DataFormated)
    return(data)

def SearchInBase(dataBase,searchData,inIndex):#FUNÇÃO DE BUSCA DE DADOS
    for dataBaseElement in dataBase:       
        if (dataBaseElement[inIndex] == searchData):
            return(dataBaseElement)#SE ENCONTRADO UMA DADO, RETORNA A LINHA ONDE SE ENCONTRA
    return(False)#SE NÃO ENCONTRADO, RETORNA FALSE

def DataVerification(primaryData,secondaryData,primaryIndex,secondaryIndex):#EFETUA O PROCESSO DE VALIDAÇÃO DE DADOS
    verifiedData = []
    for primaryElement in primaryData:#PERCORRE CADA LINHA DA MATRIZ A SER VALIDADA
        for secondaryElement in secondaryData:#PERCORRE CADA LINHA DA MATRIZ VALIDANTE
            try:#EVITA ERRO CASO A LINHA ESTEJA VAZIA
                if (primaryElement[primaryIndex] == secondaryElement[secondaryIndex]):#SE UM DADO FOR ENCONTRADO:
                    verifiedData.append(primaryElement)#GUARDA A LINHA DA MATRIZ A SER VALIDADA
                    break#INTERROMPE O LOOP INTERNO
            except:
                break#INTERROMPE O LOOP INTERNO
    return(verifiedData)#RETORNA A MATRIZ VALIDADA

def CountBathroom(dataBase,dataRegions):#CONTA QUANTOS DOMICÍLIOS TEM BANHEIRO
    resultString = ''
    for dataRegionsElement in dataRegions:#PERCORRE TODAS AS CIDADES DE REGIÕES
        numOfCity = 0
        numOfBathroom = 0
        for dataBaseElement in dataBase:#PERCORRE TODAS AS CASAS PESQUISADAS E VALIDADAS
            if (dataRegionsElement[0] == dataBaseElement[1]):#VERIFICA EM QUANTAS CASAS A ATUAL CIDADE FOI PESQUISADA
                numOfCity+=1#ARMAZENA O NÚMERO DE CASAS NA CIDADE
                if (0 < int(dataBaseElement[6])):#VERIFICA SE NA CASA HÁ BANHEIROS
                    numOfBathroom+=1#ARMAZENA O NÚMERO DE CASAS COM BANHEIRO
        if (numOfCity > 0):#SE EM DETERMINADA CIDADE FORAM FEITAS PESQUISAS
            resultString+=('|'+('-'*68)+'|\n'+FormatLength('NA CIDADE DE '+dataRegionsElement[1]+'-'+dataRegionsElement[3])
            	+'\n|'+'-'*68+'|\n')
            resultString+=(FormatLength(str(numOfBathroom)+' DOMICÍLIOS POSSUEM BANHEIRO')+'\n')
            resultString+=(FormatLength(str(numOfCity-numOfBathroom)+' DOMICÍLIOS NÃO POSSUEM BANHEIRO')+'\n|'+'-'*68+'|\n')
    return(resultString)

def CountEnergy(dataBase,dataRegions):#RETORNA PERCENTUAL DE DOMICÍLIOS COM ENERGIA POR CIDADE
    resultString = ''
    for dataRegionsElement in dataRegions:#PERCORRE TODAS AS CIDADES DE REGIÕES
        numOfCity = 0
        numOfEnergy = 0
        for dataBaseElement in dataBase:#PERCORRE TODAS AS CASAS PESQUISADAS E VALIDADAS
            if (dataRegionsElement[0] == dataBaseElement[1]):#VERIFICA EM QUANTAS CASAS A ATUAL CIDADE FOI PESQUISADA
                numOfCity+=1#ARMAZENA O NÚMERO DE CASAS NA CIDADE
                if (3 == int(dataBaseElement[11])):#VERIFICA SE NA CASA NÃO HÁ ENERGIA ELÉTRICA
                    numOfEnergy+=1#ARMAZENA O NÚMERO DE CASAS SEM ENERGIA
        if (numOfCity > 0):#SE EM DETERMINADA CIDADE FORAM FEITAS PESQUISAS
            resultString+=('|'+'-'*68+'|\n'+FormatLength('NA CIDADE DE '+dataRegionsElement[1]+'-'+dataRegionsElement[3])+'\n')
            resultString+=('|'+'-'*68+'|\n'+FormatLength('O PERCENTUAL DE DOMICÍLIOS SEM ENERGIA ELÉTRICA É DE %2.f'%
            ((numOfEnergy/numOfCity)*100)+'%')+'\n|'+'-'*68+'|\n')
    return(resultString)

def HouseSituation(dataBase,inIndex):#CONTA AS CASAS PAGAS, ALUGADAS, OU SENDO PAGAS
    situations = {0:'DOMICÍLIOS PARTICULARES PAGOS:         %i\n',1:'DOMICÍLIOS PARTICULARES SENDO PAGOS:   %i\n',
        2:'DOMICÍLIOS PARTICULARES ALUGADOS:      %i\n'}
    vaules = [0,0,0]#CADA ÍNDICE REPRESENTA A SITUAÇÃO EM QUE AS CASAS PODEM ESTAR
    for dataBaseElement in dataBase:
        if ((int(dataBaseElement[inIndex]) >= 1) and (int(dataBaseElement[inIndex]) <= 3)):
            vaules[int(dataBaseElement[inIndex])-1]+=1
    return(situations[0]%vaules[0]+situations[1]%vaules[1]+situations[2]%vaules[2])

def WaterSupply(dataBase,dataRegions):#RETORNA O MODO MAIS COMUM DE ABASTECIMENTO
    supplyModesDicionary = {0:'REDE GERAL DE DISTRIBUIÇÃO',1:'POÇO OU NASCENTE NA PROPRIEDADE',
    2:'POÇO OU NASCENTE FORA DA PROPRIEDADE',3:'CARRO-PIPA',4:'ÁGUA DA CHUVA ARMAZENADA EM CISTERNA',
    5:'ÁGUA DA CHUVA ARMAZENADA DE OUTRA FORMA',6:'RIOS, AÇUDES, LAGOS E IGARAPÉS',
    7:'OUTRA',8:'POÇO OU NASCENTE NA ALDEIA',9:'POÇO OU NASCENTE FORA DA ALDEIA'}#10 FORMAS DE ABASTECIMENTO
    resultString = ''
    for dataRegionsElement in dataRegions:#PERCORRE TODAS AS REGIÕES
        cityFound = False
        vaule = 0#RECEBE OS VALORES DA MAIS COMUM FORMA DE ABASTECIMENTO
        commonMode = [0,0,0,0,0,0,0,0,0,0]#CADA ÍNDICE REPRESENTA UM MODO DE ABASTECIMENTO ONDE O MAIOR VALOR SERÁ O MAIS COMUM
        commonModeSorted = [0,0,0,0,0,0,0,0,0,0]#CADA ÍNDICE REPRESENTA UM MODO DE ABASTECIMENTO ONDE O MAIOR VALOR SERÁ O MAIS COMUM
        for dataBaseElement in dataBase:#PERCORRE TODAS AS CASAS PESQUISADAS E VALIDADAS
            if (dataRegionsElement[0] == dataBaseElement[1]):#VERIFICA SE UMA CIDADE FOI PESQUISADA
                cityFound = True
                commonMode[int(dataBaseElement[9])-1]+=1#ACRESCENTA VALORES AO MODO DE ABASTECIMENTO ENCONTRADO
                commonModeSorted[int(dataBaseElement[9])-1]+=1#ACRESCENTA VALORES AO MODO DE ABASTECIMENTO ENCONTRADO
        if (cityFound == True):#SE A CIDADE FOI PESQUISADA:
            commonModeSorted.sort(reverse=True)#ORGANIZA OS VALORES EM ORDEM DECRESCENTE
            if (commonModeSorted[0] != commonModeSorted[1]):#SE OS DOIS MAIORES VALORES FOREM DIFERENTES, ENTÃO NÃO HÁ MAIS DE UMA FORMA COMUM DE ABASTECIMENYO
                    for i in range(len(commonMode)):#PERCORRER TODAS AS FORMAS DE ABASTECIMENTO
                        if (vaule < commonMode[i]):#BUSCA PELO MAIOR VALOR
                            vaule = commonMode[i]#SE O MODO ATUAL TIVER MAIS EXEMPLARES, ESSE ASSUME O LUGAR DO ANTERIOR
                            modeInCity = supplyModesDicionary[i]#O MODO MAIS COMUM FICA ARMAZENADO
                    resultString+=('|'+'-'*68+'|\n'+FormatLength('FORMA MAIS COMUM DE ABASTECIMENTO EM '+
                        dataRegionsElement[1]+'-'+dataRegionsElement[3])+'\n')
                    resultString+=('|'+'-'*68+'|\n'+FormatLength(modeInCity)+'\n|'+'-'*68+'|\n')
            else:#SE OS DOIS MAIORES VALORES FOREM IGUAIS, ENTÃO HÁ MAIS DE UMA FORMA COMUM DE ABASTECIMENYO
                resultString+=('|'+'-'*68+'|\n'+FormatLength('FORMA MAIS COMUM DE ABASTECIMENTO EM '+
                    dataRegionsElement[1]+'-'+dataRegionsElement[3])+'\n')
                resultString+=('|'+'-'*68+'|\n'+FormatLength('HÁ MAIS DE UMA FORMA MAIS COMUM')+'\n|'+'-'*68+'|\n')
    return(resultString)

def ColorOrRace(dataBase):#RETORNA O PERCENTUAL POR COR OU RAÇA
    groupDicionary={0:'PERCENTUAL DE BRANCOS:   %2.f',1:'PERCENTUAL DE PRETOS:    %2.f',
        2:'PERCENTUAL DE AMARELOS:  %2.f',3:'PERCENTUAL DE PARDOS:    %2.f',4:'PERCENTUAL DE INDÍGENAS: %2.f'}
    groupList = [0,0,0,0,0]#CADA ÍNDICE REPRESENTA OS VALORES DE CADA GRUPO
    result = ''
    for dataBaseElement in dataBase:#PERCORRE TODAS AS CASAS VÁLIDAS PESQUISDAS
        groupList[int(dataBaseElement[18])-1]+=1#ARMAZENA UM EXEMPLAR DO GRUPO ENCONTRADO NA LISTA
    for i in range(len(groupList)):#PERCORRE O GRUPO DE COR OU RAÇA OBTIDO
        result+=(groupDicionary[i]%(groupList[i]/len(dataBase)*100)+'%\n')#ARMAZENA OS DADOS DE CADA GRUPO
    return(result)

def LargestRegion(dataBase,dataRegions):#RETORNA A REGIÃO COM MAIOR NÚMERO DE MINICÍPIOS PESQUISADOS
    regionListVaule = [0,0,0,0,0]#CADA ÍNDICE REPRESENTA OS VALORES DE UMA REGIÃO
    regionNamesDicionary = ['REGIÃO NORTE','REGIÃO NORDESTE', 'REGIÃO CENTRO-OESTE',
        'REGIÃO SUDESTE','REGIÃO SUL']#CADA ÍNDICE É UMA REGIÃO
    resultRegion = False
    highestValue = 0#MAIOR VALOR DE MUNICÍPIOS DE UMA REGIÃO
    regionDictionary = {'AM':0,'RR':0,'AP':0,'PA':0,'TO':0,'RO':0,'AC':0,'MA':1,
        'PI':1,'CE':1,'RN':1,'PE':1,'PB':1,'SE':1,'AL':1,'BA':1,'MT':2,
        'MS':2,'GO':2,'SP':3,'RJ':3,'ES':3,'MG':3,'PR':4,'RS':4,'SC':4}#CADA VALOR DE CHAVE É UM ESTADO
    for dataRegionsElement in dataRegions:#PERCORRE TODAS AS CIDADES REGISTRADAS
        if (SearchInBase(dataBase,dataRegionsElement[0],1) != False):#SE UMA CIDADE FOI PESQUISADA:
            regionListVaule[regionDictionary[dataRegionsElement[3]]]+=1#ARMAZENA A REGIÃO A QUAL SEU ESTADO PERTENCE
    for i in range(len(regionListVaule)):#PERCORRE A LISTA DE REIGÕES
        if (highestValue < regionListVaule[i]):#VERIFICA QUAL DAS 5 REGIÕES TEVE MAIS CASAS PESQUISADAS
            resultRegion = regionNamesDicionary[i]#ARMAZENA O NOME DA REGIÃO
            highestValue = regionListVaule[i]#ARMAZENA OS VALORES DE RESIDÊNCIAS PESQUISADAS NA REGIÃO
    regionListVaule.sort(reverse=True)#ORDENA A LISTA EM ORDEM DECRESCENTE
    if ((regionListVaule[0] == regionListVaule[1]) and (regionListVaule[0] != 0)):#SE OS DOIS MAIORES VALORES FOREM IGUAIS, DUAS REGIÕES SÃO AS MAIS PESQUISADAS
    	return('NÃO HÁ APENAS UMA REGIÃO COM MAIOR NÚMERO DE MUNICÍPIOS PESQUISADOS...')
    if (resultRegion == False):
        return('NÃO FORAM FEITAS PESQUISAS EM NENHUMA DAS 5 REGIÕES BRASILEIRAS...')
    else:
        return('REGIÃO COM MAIOR NÚMERO DE MUNICÍPIOS PESQUISADOS: %s'%resultRegion)

def MainMenu():#MENU PRINCIPAL: FUNCIONALIDADES
    ClearScreen()
    print('Carregando, aguarde...')
    dataRegions = LoadFromFile('regioes.txt')#CARREGA O ARQUIVO DE REGIÕES
    dataBase=DataVerification(LoadFromFile('exemploPesquisa.txt'),LoadFromFile('tecnicosIBGE.txt'),0,0)#FAZ 1ª VALIDAÇÃO
    dataBase = (DataVerification((dataBase),(dataRegions),1,0))#FAZ ÚLTIMO PROCESSO DE VALIDAÇÃO
    while True:#LAÇO PRINCIPAL DO PROGRAMA
        ShowVisualMenu()
        command = input('Digite: ')
        ClearScreen()
        print('Carregando, aguarde...')
        if (command == '1'):
            ShowVisualMenu()
            pause=input('NÚMERO DE DOMICÍLIOS COLETADOS: %i'%len(dataBase)+'\nDigite [ENTER] para continuar...')
        elif(command == '2'):
            pause=input(ConsiderLoading(HouseSituation(dataBase,5),True)+'Digite [ENTER] para continuar...')
        elif(command == '3'):
            pause=input(ConsiderLoading(CountBathroom(dataBase,dataRegions),False)+'\nDigite [ENTER] para continuar...')
        elif(command == '4'):
            pause=input(ConsiderLoading(WaterSupply(dataBase,dataRegions),False)+'\nDigite [ENTER] para continuar...')
        elif(command == '5'):
            pause=input(ConsiderLoading(CountEnergy(dataBase,dataRegions),False)+'\nDigite [ENTER] para continuar...')
        elif(command == '6'):
            pause=input(ConsiderLoading(ColorOrRace(dataBase),True)+'\nDigite [ENTER] para continuar...')
        elif(command == '7'):
            pause=input(ConsiderLoading(LargestRegion(dataBase,dataRegions),True)+'\nDigite [ENTER] para continuar...')
        elif(command == '8'):
            heavyData = (HouseSituation(dataBase,5)+CountBathroom(dataBase,dataRegions)+WaterSupply(dataBase,dataRegions)
                +CountEnergy(dataBase,dataRegions)+ColorOrRace(dataBase)+LargestRegion(dataBase,dataRegions))
            ClearScreen()
            print('NÚMERO DE DOMICÍLIOS COLETADOS: %i'%len(dataBase))
            pause=input(heavyData+'\nDigite [ENTER] para continuar...')
        elif(command == '9'):
            ClearScreen()
            break
        
MainMenu()#INICIA O PROGRAMA
