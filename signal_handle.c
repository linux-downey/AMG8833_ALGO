
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <signal.h>


void handler(int num)
{
    printf("num = %d\r\n",num);
    sleep(3);
    _exit(0);
}


void handler2(int num)
{
    printf("num = %d\r\n",num);
    printf("do nothing!!!");
    //sleep(3);
    //_exit(0);
}



void *thr_fn(void *arg)
{
    signal(SIGINT, handler);
    while(1)
    {
        sleep(4);
        printf("fuck!!!\r\n");
    }
}


void *T_func(void *arg)
{
    signal(SIGINT, handler2);
    while(1)
    {
        sleep(1);
        printf("fuck!!!\r\n");
    }
}



pthread_t ntid;
pthread_t Tnid;

int main()
{
    pthread_create(&ntid, NULL, thr_fn, NULL);
    usleep(10000);
    pthread_create(&Tnid, NULL, T_func, NULL);
    pthread_join(ntid,NULL);
    pthread_join(Tnid,NULL);
}