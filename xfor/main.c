#include <stdlib.h>
#include <stdio.h>
#include <p99/p99.h>
#include "xfor.h"

int main(){
    XFOR_INIT;

    int i0=P99_INIT, j0=P99_INIT, i1=P99_INIT, j1=P99_INIT, k0=P99_INIT, k1=P99_INIT, t0=P99_INIT, t1=P99_INIT;

      /*XFOR(0,2,i0,i1,1,1,3,5,2,1,0,1)
        XFOR(1,2,k0,k1,1,1,3,5-i1,2,1,0,1){
            XFOREND(2,2,j0,j1,1,1,4,3,1,2,1,0)
            {
                XFOR_CASE(0) printf("cas 0:%d %d\n", i0, j0);
                XFOR_CASE(1) printf("cas 1:%d %d\n", i1, j1);
            }
        }*/

    XFOR(0,2,i0,i1,1,2,5,4,2,1,1,0)
        XFOREND(1,2,j0,j1,i0,1,5-i0,i1+1,1,2,0,1)
        {
            XFOR_CASE(0) printf("case 0:%d %d\n",i0,j0);
            XFOR_CASE(1) printf("case 1:%d %d\n",i1,j1);
        }

    printf("Xfor 2\n");

    XFOR(0,2,i0,i1,1,0,5,4,2,1,1,0)
        XFOREND(1,2,j0,j1,i0,1,5-i0,4,1,2,0,0)
        {
            XFOR_CASE(0) printf("case 0:%d %d\n",i0,j0);
            XFOR_CASE(1) printf("case 1:%d %d\n",i1,j1);
        }

/*    XFOR(0,2,i0,i1,1,1,3,5,2,1,0,1)
        XFOR(1,2,k0,k1,1,1+i1,3,5-i1,2,1,0,1)
            XFOREND(2,2,j0,j1,1,1,4,3,1,2,1,0)
            {
                XFOR_CASE(0) printf("cas 0:%d %d %d\n", i0, k0, j0);
                XFOR_CASE(1) printf("cas 1:%d %d %d\n", i1, k1, j1);
            }*/
    
    /*XFOREND(0,2,j0,j1,1,1,4,3,1,2,1,0)
    {
        XFOR_CASE(0) printf("cas 0:%d %d\n", i0, j0);
        XFOR_CASE(1) printf("cas 1:%d %d\n", i1, j1);
    }*/
    

    return 0;
}
