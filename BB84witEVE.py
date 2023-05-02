import numpy as np
import csv
# importing Qiskit
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, BasicAer

def SendState(qc1, qc2, qc1_name):
    ''' This function takes the output of a circuit qc1 (made up only of x and 
        h gates and initializes another circuit qc2 with the same state
    ''' 
    
    # Quantum state is retrieved from qasm code of qc1
    qs = qc1.qasm().split(sep=';')[4:-1]

    # Process the code to get the instructions
    for index, instruction in enumerate(qs):
        qs[index] = instruction.lstrip()

    # Parse the instructions and apply to new circuit
    for instruction in qs:
        if instruction[0] == 'x':
            old_qr = int(instruction[5:-1])
            qc2.x(qr[old_qr])
        elif instruction[0] == 'h':
            old_qr = int(instruction[5:-1])
            qc2.h(qr[old_qr])
        elif instruction[0] == 'm': # exclude measuring:
            pass
        else:
            raise Exception('Unable to parse instruction')

n=12

f = open("BB84EveKnow.csv", 'w')
writer = csv.writer(f)
writer.writerow(['bitsim'])
val1 = 0
qr = QuantumRegister(n, name='qr')
cr = ClassicalRegister(n, name='cr')

for i in range(5000):
    alice = QuantumCircuit(qr, cr, name='Alice')
    
    # Generate a random number in the range of available qubits [0,65536))
    alice_key = np.random.randint(0, high=2**n)
    
    # Cast key to binary for encoding
    # range: key[0]-key[15] with key[15] least significant figure
    alice_key = np.binary_repr(alice_key, n) # n is the width
    for index, digit in enumerate(alice_key):
        if digit == '1':
            alice.x(qr[index]) # if key has a '1', change state to |1>
            
    # Switch randomly about half qubits to diagonal basis
    alice_table = []        # Create empty basis table
    for index in range(len(qr)):       # BUG: enumerate(q) raises an out of range error
        if 0.5 < np.random.random():   # With 50% chance...
            alice.h(qr[index])         # ...change to diagonal basis
            alice_table.append('X')    # character for diagonal basis
        else:
            alice_table.append('Z')    # character for computational basis
    
    bob = QuantumCircuit(qr, cr, name='Bob')
    
    SendState(alice, bob, 'Alice')    
    # Bob doesn't know which basis to use
    bob_table = []
    for index in range(len(qr)): 
        if 0.5 < np.random.random():  # With 50% chance...
            bob.h(qr[index])        # ...change to diagonal basis
            bob_table.append('X')
        else:
            bob_table.append('Z')
    for index in range(len(qr)): 
        bob.measure(qr[index], cr[index])
        
    # Execute the quantum circuit 
    backend = BasicAer.get_backend('qasm_simulator')    
    result = execute(bob, backend=backend, shots=1).result()
    
    # Result of the measure is Bob's key candidate
    bob_key = list(result.get_counts(bob))[0]
    bob_key = bob_key[::-1] 
    keep = []
    discard = []
    for qubit, basis in enumerate(zip(alice_table, bob_table)):
        if basis[0] == basis[1]:
            #print("Same choice for qubit: {}, basis: {}" .format(qubit, basis[0])) 
            keep.append(qubit)
        else:
            #print("Different choice for qubit: {}, Alice has {}, Bob has {}" .format(qubit, basis[0], basis[1]))
            discard.append(qubit)
    acc = 0
    for bit in zip(alice_key, bob_key):
        if bit[0] == bit[1]:
            acc += 1
    val1 = round(acc/n,3)
    
    eve = QuantumCircuit(qr, cr, name='Eve')
    SendState(alice, eve, 'Alice')   
    eve_table = []
    for index in range(len(qr)): 
        if 0.5 < np.random.random(): 
            eve.h(qr[index])        
            eve_table.append('X')
        else:
            eve_table.append('Z')
    for index in range(len(qr)): 
        eve.measure(qr[index], cr[index])
        
    # Execute (build and run) the quantum circuit 
    backend = BasicAer.get_backend('qasm_simulator')    
    result = execute(eve, backend=backend, shots=1).result()
    
    # Result of the measure is Eve's key
    eve_key = list(result.get_counts(eve))[0]
    eve_key = eve_key[::-1]
    for qubit, basis in enumerate(zip(alice_table, eve_table)):
        if basis[0] != basis[1]:
            if eve_key[qubit] == alice_key[qubit]:
                eve.h(qr[qubit])
            else:
                if basis[0] == 'X' and basis[1] == 'Z':
                    eve.h(qr[qubit])
                    eve.x(qr[qubit])
                else:
                    eve.x(qr[qubit])
                    eve.h(qr[qubit])
    SendState(eve, bob, 'Eve')
              
    bob_table = []
    for index in range(len(qr)): 
        if 0.5 < np.random.random(): 
            bob.h(qr[index])      
            bob_table.append('X')
        else:
            bob_table.append('Z')
              
    for index in range(len(qr)): 
        bob.measure(qr[index], cr[index])
    result = execute(bob, backend=backend, shots=1).result()
    bob_key = list(result.get_counts(bob))[0]
    bob_key = bob_key[::-1]
    keep = []
    discard = []
    for qubit, basis in enumerate(zip(alice_table, bob_table)):
        if basis[0] == basis[1]:
            keep.append(qubit)
        else:
            discard.append(qubit)
            
    acc = 0
    for bit in zip(alice_key, bob_key):
        if bit[0] == bit[1]:
            acc += 1
    keyLength = len(alice_key)
    abKeyMismatches = 0 # number of mismatching bits in the keys of Alice and Bob
    eaKeyMismatches = 0 # number of mismatching bits in the keys of Eve and Alice
    ebKeyMismatches = 0 # number of mismatching bits in the keys of Eve and Bob
    
    for j in range(keyLength):
        if alice_key[j] != bob_key[j]: 
            abKeyMismatches += 1
        if eve_key[j] != alice_key[j]:
            eaKeyMismatches += 1
        if eve_key[j] != bob_key[j]:
            ebKeyMismatches += 1
    print(keyLength,eaKeyMismatches)
    eaKnowledge = (keyLength - eaKeyMismatches)/keyLength # Eve's knowledge of Bob's key
    ebKnowledge = (keyLength - ebKeyMismatches)/keyLength # Eve's knowledge of Alice's key

    row = [round((acc/n)*100,3),round(eaKnowledge * 100, 3),round(ebKnowledge * 100, 3)]
    print(row)
    writer.writerow(row)