

from leitura_op import ler_dados # for data reading

K = 0

C =0

#K = int(len(numJobs)/2) #number of ants


############################## CLASSES --- START


class Jobs:
    def __init__(self, jobSequence, Nodes, num):
        self.jobSequence = jobSequence
        self.Nodes = Nodes
        self.num = num
        
class Node:
    def __init__(self, dependents, duration, machine, nodeNum):
        self.duration = duration
        self.dependents = [dependents for i in range(K)]
        self.machine = machine
        self.visited = False
        self.num = nodeNum
        self.startTime = 0
        self.endTime = 0
        self.scheduled = False
        self.antsVisited = [False for i in range(K)]
        self.name = 'name goes here' #fill in names via constructor
        self.discovered = False

class Ant:
    def __init__(self, num):
        self.num = num #label each ant by a number 0 to (k-1)
        self.tabu = []
        self.position = -1
        self.T = [[0 for i in range(numNodes)] for j in range(numNodes)] #pheromone matrix 
        self.pheromoneAccumulator = [[0 for i in range(numNodes)] for j in range(numNodes)] #accumulator
        self.transitionRuleMatrix = [[0 for i in range(numNodes)] for j in range(numNodes)] #for equation 1 transition probability
        self.makespan = 0
        self.species = 'none'
        self.cycleDetected = False


class param_seq:

    numJobs = 0
    numMachines = 0
    sinkDependents = []
    JOBSLIST =[]
    NODESLIST = []
    ordens_producao = {}
    
    def __init__(self):        

        ########################### Leitura dos Dados##############################

        seq_process = ler_dados(3) # lendo dados dos tabela da seqûencia;   
            
        print("\n")
        print("\n")

        print("Os dados são:")

        print(seq_process.sort_values(by=['Ord Prod', 'Oper'])) #ordenando por job

        ############################# Criação dos conjuntos #################################

        self.numJobs = seq_process['Ord Prod'].drop_duplicates().values

        self.numMachines = seq_process['Grp Maq'].drop_duplicates().values

        numNodes =  len(self.numJobs)*len(self.numMachines) + 2
        
        global K
        K = int(len(self.numJobs/2)) #number of ants

        C = 10 #number of cycles

        ##########################################################################################

        Node0 = Node([],1,0,1) #dummy node

        print("\n")
        print("\n")

        print(self.numJobs)


        print("\n")
        print("\n")

        print(self.numMachines)

        self.NODESLIST = []
        num_node=0
        num_job=1 #varivale auxiliar que incrementa com job

        aux2=0

        JobNodes = []

        self.JOBSLIST = []

        self.sinkDependents = [] #list of the last operation of each job; these will be dependents for the sink



        ################################ Criando as instâncias dos nós ###############################

        #(self, dependent,duration,machine,number)
        
        for job in self.numJobs:
            dependent = []
            dependent.append(Node0)
            operacoes = seq_process.loc[seq_process['Ord Prod']==job,['Oper', 'Grp Maq', 'Tmp Máq']]

            aux_JobNodes=[]

            seq_jobs= [] #lista de sequencia de operações para cada job
            

            for idx,recurso in operacoes.iterrows():
                num_node = num_node +1
                aux = Node(dependent,recurso['Tmp Máq'], recurso['Grp Maq'], num_node)
                self.NODESLIST.append(aux)#criando a lista de nós
                dependent.append(self.NODESLIST[-1]) #adicionando os nós dependentes
                seq_jobs.append(num_node)
                aux_JobNodes.append(self.NODESLIST[-1]) #adicionando os nós na lista
                self.ordens_producao.update({num_node: job})
            #JobNodes.append(aux_JobNodes) #adiconando os nós de cada job

            for machine in self.numMachines:
                print(machine)
                if len(operacoes.loc[operacoes['Grp Maq'].isin([machine])]) ==0:
                    num_node = num_node +1
                    aux = Node([],0.00, machine, num_node)
                    self.NODESLIST.append(aux)#criando a lista de nós
                    #dependent.append(self.NODESLIST[-1]) #adicionando os nós dependentes
                    seq_jobs.append(num_node)
                    aux_JobNodes.append(self.NODESLIST[-1]) #adicionando os nós na lista
            self.sinkDependents.append(self.NODESLIST[-1]) # adicionando os últimos nós 
            JobNodes.append(aux_JobNodes) #adiconando os nós de cada job 
            
            OF = Jobs(seq_jobs, aux_JobNodes,num_job) #OF = Ordem de fabricação
            self.JOBSLIST.append(OF)
            num_job = num_job +1   


        print(self.NODESLIST)
        print("\n")
        print("\n")

        print(self.JOBSLIST)

    def get_joblist(self):
        print(len(self.JOBSLIST))
        return self.JOBSLIST

    def get_nodelist(self):


        # for node in self.NODESLIST: #reset nodes visited to false since this is a new cycle
        #     print("#"*100)
        #     print(len(node.antsVisited))
        #     #print(len(ANTLIST))
        # #input()    


        return self.NODESLIST

    def get_numJobs(self):
        return len(self.numJobs)

    def get_numMachines(self):
        return len(self.numMachines)

    def get_numNodes(self):
        return len(self.NODESLIST) + 2
    
    def get_sinkDependents(self):
        return self.sinkDependents

    def get_ordens_producao(self):
        return self.ordens_producao
    
    