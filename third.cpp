#include <stdio.h>
#include <omp.h>
#include <ctime>
#include <math.h>
#include <iostream>
//#include <unistd.h>
#define M 4000
#define E 0.00001
/* Исходные данные задаются статически */
double A[M][M], F[M], Xk[M], Zk[M];
static double Rk[M], Sz[M], alf, bet, mf;
static double Spr, Spr1, Spz;
int main()
{
    int i, j, v, size, Np, it;
    // struct timeval tv1, tv2;
    double Ax, r, r1, z, alph, betta, z1;

    time_t start, end;
    long int dt1;
    int threads;
    std::cout << "Input threads: ";
    std::cin >> threads;
    mf = 0;
    it = 0;

    /* Генерация исходной матрицы коэффициентов и
    правых частей уравнений */
    for (i = 0; i < M; i++)
    {
        for (j = 0; j < M; j++)
        {
            if (i == j)
                A[i][j] = rand();
            else
                A[i][j] = rand();
        }
        F[i] = rand();
        mf += F[i] * F[i];
    }
    /* Вычисление нормы ||f|| */
    mf = sqrt(mf);
    /* Задание начального приближения решений */
    for (i = 0; i < M; i++)
    {
        Xk[i] = 0;
        Sz[i] = 0;
    }
    /* Задание начальных значений векторов невязки
    и сопряженного направления */
    for (i = 0; i < M; i++)
    {
        for (j = 0; j < M; j++)
            Sz[i] += A[i][j] * Xk[j];
        Rk[i] = F[i] - Sz[i];
        Zk[i] = Rk[i];
    }

    start = time(NULL);
    omp_set_num_threads(threads);
    do
    {
        Spz = 0;
        Spr = 0;
        Spr1 = 0;
/* Начало параллельного блока праграммы */
#pragma omp parallel private(size, i)
        {
            size = omp_get_num_threads();
            Np = M / size;
            //printf("here");
/* Распараллеливание цикла, вычисляющего
числитель и знаменатель коэф. αk */
#pragma omp for schedule(static, Np) private(j) reduction(+ : Spz, Spr)
            for (i = 0; i < M; i++)
            {
                for (Sz[i] = 0, j = 0; j < M; j++)
                    Sz[i] += A[i][j] * Zk[j];
                Spz += Sz[i] * Zk[i];
                Spr += Rk[i] * Rk[i];
            }
/* Вычисление коэффициента αk */
#pragma omp critical
            alf = Spr / Spz;
/* Распараллеливание цикла, вычисляющего
вектора решений и невязки */
#pragma omp for schedule(static, Np) reduction(+ : Spr1)
            for (i = 0; i < M; i++)
            {
                Xk[i] += alf * Zk[i];
                Rk[i] -= alf * Sz[i];
                Spr1 += Rk[i] * Rk[i];
            }
/* Вычисление коэффициента βk */
#pragma omp critical
            bet = Spr1 / Spr;
/* Распараллеливание цикла, вычисляющего вектор
сопр. направления */
#pragma omp for schedule(static, Np)
            for (i = 0; i < M; i++)
                Zk[i] = Rk[i] + bet * Zk[i];
        } 
        //std::cout<<sqrt(Spr1) / mf <<std::endl;
        it++;
    } while (sqrt(Spr1) / mf > E);
    end = time(NULL);
    std::cout<<"TIME "<<end-start<<"s"<<std::endl;
    /* Вывод значений первых восьми корней для
    контроля */
    /*printf(" %f %f %f %f %f %f %f %f\n", Xk[0],

           Xk[1], Xk[2], Xk[3], Xk[4], Xk[5], Xk[6], Xk[7]);*/
    return (0);
}