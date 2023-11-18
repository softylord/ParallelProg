from mpi4py import MPI
from numpy import empty , array , int32 , float64 , zeros , arange , dot
import random
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numprocs = comm.Get_size()

def conjugate_gradient_method(A_part , b_part , x , N):
    eps=0.000000001
    r = empty(N , dtype=float64)
    q = empty(N , dtype=float64)
    s = 1
    p = zeros(N , dtype=float64)
    #print(b_part)

    while True:
        if s == 1:
            #comm.Allgatherv([x_part , N_part , MPI.DOUBLE], [x, rcounts_N , displs_N , MPI.DOUBLE])
            r_temp = dot(A_part.T, dot(A_part , x) - b_part)
            comm.Allreduce([r_temp, N, MPI.DOUBLE], [r, N, MPI.DOUBLE], op=MPI.SUM)
            #comm.Reduce_scatter([r_temp , N, MPI.DOUBLE], [r_part , N_part , MPI.DOUBLE], recvcounts=rcounts_N , op=MPI.SUM)
        else:
            #ScalP_temp[0] = dot(p_part , q_part)
            #comm.Allreduce([ScalP_temp , 1, MPI.DOUBLE], [ScalP , 1, MPI.DOUBLE], op=MPI.SUM)
            r -= q / dot(p, q)

        ch=dot(r.T, r)
        if ch<eps:
            #print('[[[[[]]]]]')
            break
        
        #print("r", r)
        p+=r/dot(r,r)
        q_temp = dot(A_part.T, dot(A_part , p))
        
        comm.Allreduce([q_temp, N, MPI.DOUBLE], [q, N, MPI.DOUBLE], op=MPI.SUM)
        x-=p/dot(p, q)
        #print(x)
        s += 1
    #print('rank', rank, A_part)
    #print('rank', rank, x)
    return x


if rank == 0:
    N = array(int32(10000))
    M = N
    start=time.time()
else:
    N = array(0, dtype=int32)

comm.Bcast([N, 1, MPI.INT], root=0)

def auxiliary_arrays_determination(M, numprocs):
    ave, res = divmod(M, numprocs -1)
    rcounts = empty(numprocs , dtype=int32)
    displs = empty(numprocs , dtype=int32)
    rcounts[0] = 0
    displs[0] = 0

    for k in range(1, numprocs):
        if k <= res:
            rcounts[k] = ave + 1
        else:
            rcounts[k] = ave

        displs[k] = displs[k-1] + rcounts[k-1]

    return rcounts , displs

if rank == 0:
    rcounts_M , displs_M = auxiliary_arrays_determination(M, numprocs)
    #rcounts_N , displs_N = auxiliary_arrays_determination(N, numprocs)
else:
    rcounts_M , displs_M = None, None
    #rcounts_N = empty(numprocs , dtype=int32)
    #displs_N = empty(numprocs , dtype=int32)

#comm.Bcast([rcounts_N , numprocs , MPI.INT], root=0)
#comm.Bcast([displs_N , numprocs , MPI.INT], root=0)

M_part = array(0, dtype=int32)
comm.Scatter([rcounts_M , 1, MPI.INT], [M_part , 1, MPI.INT], root=0)
if rank == 0:
    for k in range(1, numprocs):
        A_part = empty((rcounts_M[k], N), dtype=float64)
        for j in range(rcounts_M[k]):
            for i in range(N):
                if i==j:
                    A_part[j, i] = 2
                else:
                    A_part[j, i]=1
        comm.Send([A_part , rcounts_M[k]*N, MPI.DOUBLE], dest=k, tag=0)
    A_part = empty((M_part , N), dtype=float64)

else: # rank != 0
    A_part = empty((M_part , N), dtype=float64)
    comm.Recv([A_part , M_part*N, MPI.DOUBLE], source=0, tag=0, status=None)

if rank == 0:
    b = empty(M, dtype=float64)
    for j in range(M):
        b[j] = float64(N+1)
else:
    b = None

b_part = empty(M_part , dtype=float64)
comm.Scatterv([b, rcounts_M , MPI.DOUBLE], [b_part , M_part , MPI.DOUBLE], root=0)

# if rank == 0:
#     x = zeros(N, dtype=float64)
# else:
#     x = None
x=zeros(N, dtype=float64)

#x_part = empty(rcounts_N[rank], dtype=float64)
#comm.Scatterv([x, rcounts_N , displs_N , MPI.DOUBLE], [x_part , rcounts_N[rank], MPI.DOUBLE], root=0)

#x_part = conjugate_gardient_method(A_part , b_part , x_part , N, rcounts_N[rank], rcounts_N , displs_N)
x= conjugate_gradient_method(A_part , b_part , x, N)

#comm.Gatherv([x_part , rcounts_N[rank], MPI.DOUBLE], [x, rcounts_N , displs_N , MPI.DOUBLE], root=0)

if rank==0:
    end=time.time()
    #print("x is:", x)
    print('time is', (end-start))

