from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np
from qiskit.providers.aer import QasmSimulator
import tracemalloc
'''
 #state: array of 0s and 1s denoting the state to be encoded
 #basis: array of 0s and 1s denoting the basis to be used for encoding
             #0 -> Computational Basis
             #1 -> Hadamard Basis
 #meas_basis: array of 0s and 1s denoting the basis to be used for measurement
             #0 -> Computational Basis
             #1 -> Hadamard Basis
 '''
tracemalloc.start()
def bb84_circuit(state, basis, measurement_basis):
    num_qubits = len(state)
    
    circ = QuantumCircuit(num_qubits)

    # Sender prepares qubits
    for i in range(len(basis)):
        if state[i] == 1:
            circ.x(i)
        if basis[i] == 1:
            circ.h(i)
   

    # Measuring action performed by Bob
    for i in range(len(measurement_basis)):
        if measurement_basis[i] == 1:
            circ.h(i)

       
    circ.measure_all()
    
    return circ

num_qubits = 32
alice_basis = np.random.randint(2, size=num_qubits)
alice_state = np.random.randint(2, size=num_qubits)
bob_basis = np.random.randint(2, size=num_qubits)
# print(f"Alice's State:\t {np.array2string(alice_state)}")
# print(f"Alice's Basis:\t {np.array2string(alice_basis)}")
# print(f"Bob's Basis:\t {np.array2string(bob_basis)}")
      
circuit = bb84_circuit(alice_state, alice_basis, bob_basis)
key = execute(circuit.reverse_bits(),backend=QasmSimulator(),shots=1).result().get_counts().most_frequent()
encryption_key = ''
for i in range(num_qubits):
    if alice_basis[i] == bob_basis[i]:
         encryption_key += str(key[i])
# print(f"Key: {encryption_key}")
x= list(tracemalloc.get_traced_memory())
print(x[1]-x[0])
tracemalloc.stop()

