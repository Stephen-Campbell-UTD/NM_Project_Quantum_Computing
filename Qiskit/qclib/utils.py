from typing import Iterable
import numpy as np
from qiskit import QuantumCircuit, Aer
from qiskit.compiler.transpiler import transpile
from qiskit.visualization import plot_bloch_multivector
import warnings
warnings.filterwarnings("ignore")

def plot_current_bloch_state(qc : QuantumCircuit, *args, **kwargs):
  sim = Aer.get_backend("aer_simulator")
  qc_to_plot =qc.copy()
  qc_to_plot.save_statevector()
  statevector = sim.run(transpile(qc_to_plot)).result().get_statevector()
  fig = plot_bloch_multivector(statevector,*args, **kwargs)
  display(fig)

def statevector_to_binary(statevector,start =0 ,stop=-1, *args, **kwargs):
  import numpy as np
  indices = np.where(statevector == 1)
  assert(len(indices) == 1)
  num =  indices[0][0]
  # convert to binary -> truncate 0b -> reverse to qubit order 
  # -> slice start,stop -> reverse to num order -> cast to int
  # print(num, bin(num))
  # print(bin(num)[2:][::-1][start:])#[::-1])
  # print(start,stop)
  num = int(bin(num)[2:][::-1][start:stop][::-1].zfill(1),base=2)
  return num

def get_binary_number_representation(qc : QuantumCircuit,start =0 ,stop=-1,  *args, **kwargs):
  sim = Aer.get_backend("aer_simulator")
  qc_to_plot =qc.copy()
  qc_to_plot.save_statevector()
  qobj =transpile(qc_to_plot, sim)
  statevector = sim.run(qobj).result().get_statevector()
  stop = qc.num_qubits if stop == -1 else stop
  return statevector_to_binary(statevector, start, stop, *args, **kwargs)

def not_qubits_from_num(qc,num : int, indices : Iterable = None):
  indices = range(qc.num_qubits) if indices is None else indices
  indices = list(indices)
  word_size = len(indices)
  num_as_bits = bin(num)[2:].zfill(word_size)[::-1]
  for i in range(word_size):
    should_not = num_as_bits[i] == '1'
    if should_not:
      qc.x(indices[i])