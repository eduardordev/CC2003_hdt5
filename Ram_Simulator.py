#Eduardo Ramírez Herrera 19946
#Simulacion de la ejecucion de procesos en una computadora con RAM y CPU. 

import simpy
import random

#Funcion para la ejecucion de procesos
def processes(nombre, env,arrival_time, cpu, ram, waiting):
    
    global totalTime #Variable global para el tiempo que le toma ejecutar todos los procesos
    global timesProcesses #Lista para almacenar cuanto le tomo a cada proceso y poder calcular la desviacion estandar
    
    yield env.timeout(arrival_time) #Tiempo de llegada, determinado por la distribucion aleatoria
    startTime = env.now #Momento en el que inicia el procesamiento del proceso
    departureTime = 0
    print ('Llegada del proceso %d en el momento %s ' % (nombre, startTime))
    
    instructions = random.randint(1,1) #Asignacion de la cantidad de instrucciones del proceso
    ramNeeded = random.randint(1,100) #Asignacion de la cantidad de memoria que necesita el proceso
    
    with ram.get(ramNeeded) as queue1:
        
        print ('Proceso %d entra a la RAM en %s' % (nombre, env.now))
        print ('Espacio que ocupa el proceso %d en la RAM: %s' % (nombre, ramNeeded))
        
        while instructions>0:
            
            with cpu.request() as queue2: #Uso del CPU como recurso con colas
                
                yield queue2
                print ('Proceso %d entra al CPU en %s' % (nombre, env.now))
                
                yield env.timeout(1)
                instructions = instructions -3 #Ejecucion del CPU de 3 instrucciones del proceso
                
                if instructions<=0: #Saca el proceso de la computadora, ya que esta terminado
                    
                    instructions = 0
                    departureTime = env.now 
                    print ('Proceso %d sale del CPU en el momento %s' %(nombre,departureTime))
                    
                else: #Determina si el proceso entra directamente al CPU nuevamente si todavia tiene instrucciones o si debe hacer cola
                    
                    choose = random.randint(1,2)
                    
                    if choose == 1:
                        
                        with waiting.request() as queue3:
                            
                            yield queue3
                            yield env.timeout(1)
                            
    timeSpent = departureTime - startTime #Tiempo que le tomo ejecutar el proceso
    timesProcesses.append(timeSpent) #Se agrega el tiempo a la lista de tiempos
    totalTime = departureTime #Se actualiza el tiempo total

#Funcion para calcular la desviacion estandar                            
def standardDeviation (data, average):
    
    totals = 0
    for i in range(len(data)):
        
        totals = (data[i]-average)**2
        
    sd = (totals/(len(data)-1.0))**(0.5)
    
    return sd


#Creacion de las variables necesarias para la simulacion

env = simpy.Environment()
ram = simpy.Container(env, capacity=100)
cpu = simpy.Resource(env, capacity=1)
waiting = simpy.Resource(env, capacity = 1)
random.seed(12345)
interval = 10.0
totalTime = 0
timesProcesses = []
totalProcesses=200 #Varoable para cambiar la cantidad de procesos por instruccion

#Implementacion de la funcion de processing
for i in range (totalProcesses):
    
    env.process(processes(i,env,random.expovariate(1.0/interval),cpu,ram,waiting))

#Ejecucion de la simulacion
env.run()
Average = float(totalTime)/float(totalProcesses)
StandardDeviation = standardDeviation(timesProcesses,Average)

#Mostrar datos obtenidos
print ('Tiempo total: %d \nPromedio de tiempo por instruccion: %s \nDesviacion Estandar: %f' % (totalTime, Average, StandardDeviation))
