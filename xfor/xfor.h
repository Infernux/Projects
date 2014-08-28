#ifndef XFOR__DEF
#define XFOR__DEF

#include <stdlib.h>
#include <stdio.h>
#include <p99/p99.h>

typedef struct strlist{
    int numBoucle;
    int *indice;
    int *ref;
    struct strlist *next;
}List;

List* insertion_1(List* a, List* v){
		if(a==NULL){
            v->next=NULL;
            return v;
        }else{
            List* tmp=a;
            while(tmp->next!=NULL){
                tmp=tmp->next;
            }
            v->next=NULL;
            tmp->next=v;
            return a;
        }
}

List* sup_1(List* a, List* v){
    return a;
}

List* rech_1(List* a, List* v){
    return a;
}

void destruction(List* a){
    free(a->ref);
    free(a->indice);
    free(a);
}

void afficheListe(List* l){
	if(l!=NULL){
		List* tmp=l;
        printf("%d:%d %d\n", l->numBoucle, l->indice[0], l->indice[1]);
		while(tmp->next!=NULL){
			tmp=tmp->next;
            printf("%d:%d %d\n", tmp->numBoucle, tmp->indice[0], tmp->indice[1]);
		}
	}else{
		printf("NULL!\n");
	}
}

List* merge(int p, List* l1, List* l2){
    List* final=NULL;
    while(l1!=NULL || l2!=NULL){
        if(l1==NULL){
            while(l2!=NULL){
                List* tmp = l2->next;
                final=insertion_1(final, l2);
                l2=tmp;
            }
            return final;
        }else if(l2==NULL){
            while(l1!=NULL){
                List* tmp = l1->next;
                final=insertion_1(final, l1);
                l1=tmp;
            }
            return final;
        }
        int found = 0;
        for(int i=0; i<=p; ++i){
            if(l1->ref[i]<l2->ref[i]){
                found=1;
                List* tmp = l1->next;
                final=insertion_1(final, l1);
                l1=tmp;
                break;
            }else if(l1->ref[i]>l2->ref[i]){
                found=1;
                List* tmp = l2->next;
                final=insertion_1(final, l2);
                l2=tmp;
                break;
            }
        }
        if(!found){
            List* tmp = l1->next;
            final=insertion_1(final, l1);
            l1=tmp;
        }
    }
    return final;
}

#define XFOR_MAX_PROF 10

#define XFOR_OU(NAME,I,REC,RES) REC || RES

#define XFOR_CC(NAME,X,I) }

#define XFOR_ITDOMAIN_SCAL(NAME, X, I) \
    X

#define XFOR_ITDOMAIN_ASSIGNITERATOR(NAME, X, I) \
    &X

#define XFOR_ITDOMAIN_ASSIGN(NAME,X,I)\
    NAME[I]=X-1

#define XFOR_ITDOMAIN_LT(NAME,X,I)\
    (superIteratorTmp[NAME-1>=0?NAME-1:0][I]!=NULL && \
    superIteratorTmp[NAME][I]!=NULL \
     && *P99_PASTE2(iter,NAME)[I]<X-1)

#define XFOR_ITDOMAIN_TEST(NAME,X,I)\
    if(superIteratorTmp[NAME-1>=0?NAME-1:0][I]!=NULL && \
        superIteratorTmp[NAME][I]!=NULL &&\
            *P99_PASTE2(iter,NAME)[I]<X-1)\
            ++(*P99_PASTE2(iter,NAME)[I]); else P99_PASTE2(iter,NAME)[I]=NULL;

#define XFOR_POINTERTOARR(NAME,X,I)\
        NAME[I]=&X

#define XFOR_ITDOMAIN_ZE(NAME,X,I)\
        int P99_PASTE2(P99_PASTE2(NAME,_),I)

#define XFOR_ITDOMAIN_ZA(NAME,X,I)\
        &P99_PASTE2(P99_PASTE2(NAME,_),I)

#define XFOR(p, k, ...){\
    if(p==0){\
        lists=malloc(sizeof(List**)*k);\
        P99_FOR(superIterator,XFOR_MAX_PROF,P00_SEP,XFOR_ITDOMAIN_SUPERITERATOR,);\
        P99_FOR(lists,k,P00_SEP,XFOR_ITDOMAIN_SUPERITERATOR,);\
    }\
    int *P99_PASTE2(iter,p)[k]={P99_FOR(,k,P00_SEQ,XFOR_ITDOMAIN_ASSIGNITERATOR,\
                P99_SUB(0,k,__VA_ARGS__))\
    };\
    superIteratorTmp[p]=P99_PASTE2(iter,p);\
\
    if(superIterator[p]==NULL){\
        int **P99_PASTE2(iterr,p)=malloc(sizeof(int*)*k);\
        P99_FOR(P99_PASTE2(iterr,p),k,P00_SEP,XFOR_POINTERTOARR,\
                P99_SUB(0,k,__VA_ARGS__)\
                );\
        superIterator[p]=P99_PASTE2(iterr,p);\
	/*superIterator[p]=superIterator[p]==NULL?(int*[k]){}:...*/\
    }\
\
    int P99_PASTE2(grain,p)[k]={P99_FOR(,k,P00_SEQ,XFOR_ITDOMAIN_SCAL,P99_REVS(P99_SUB(k,k,P99_REVS(__VA_ARGS__))))};\
    int P99_PASTE2(offset,p)[k]={P99_FOR(,k,P00_SEQ,XFOR_ITDOMAIN_SCAL,P99_REVS(P99_SUB(0,k,P99_REVS(__VA_ARGS__))))};\
    int P99_PASTE2(ref,p)[k]={P99_FOR(,k,P00_SEQ,XFOR_ITDOMAIN_SCAL,P99_SUB(k,k,__VA_ARGS__))};\
\
    for(P99_FOR(P99_PASTE2(*iter,p),k, P00_SEQ, XFOR_ITDOMAIN_ASSIGN,P99_SUB(k,k,__VA_ARGS__));\
        P99_FOR(p,k, XFOR_OU, XFOR_ITDOMAIN_LT,P99_SUB(k,k,P99_SKP(k,__VA_ARGS__)));\
        ){\
            P99_FOR(p,k,P00_SER,XFOR_ITDOMAIN_TEST,P99_SUB(k,k,P99_SKP(k,__VA_ARGS__)))





/** le test à l'intérieur du last for
  * on y trouve donc les calculs de ref et d'indice
  **/
#define XFOR_ITDOMAIN_TEST2(NAME,X,I)\
        l->ref[I]=(*P99_PASTE2(iter,I)[iterk]-P99_PASTE2(ref,I)[iterk])*\
            P99_PASTE2(grain,I)[iterk]+P99_PASTE2(offset,I)[iterk];\
        l->indice[I]=(*P99_PASTE2(iter,I)[iterk]);\

#define XFOREND(p, k, ...) \
    if(p==0){\
        lists=malloc(sizeof(List**)*k);\
        P99_FOR(superIterator,XFOR_MAX_PROF,P00_SEP,XFOR_ITDOMAIN_SUPERITERATOR,);\
        P99_FOR(lists,k,P00_SEP,XFOR_ITDOMAIN_SUPERITERATOR,);\
    }\
    \
    int *P99_PASTE2(iter,p)[k]={P99_FOR(,k,P00_SEQ,XFOR_ITDOMAIN_ASSIGNITERATOR,\
                P99_SUB(0,k,__VA_ARGS__))\
    };\
    superIteratorTmp[p]=P99_PASTE2(iter,p);\
\
    if(superIterator[p]==NULL){\
        int **P99_PASTE2(iterr,p)=malloc(sizeof(int*)*k);\
        P99_FOR(P99_PASTE2(iterr,p),k,P00_SEP,XFOR_POINTERTOARR,\
                P99_SUB(0,k,__VA_ARGS__)\
                );\
        superIterator[p]=P99_PASTE2(iterr,p);\
    }\
\
    int P99_PASTE2(grain,p)[k]={P99_FOR(,k,P00_SEQ,XFOR_ITDOMAIN_SCAL,P99_REVS(P99_SUB(k,k,P99_REVS(__VA_ARGS__))))};\
    int P99_PASTE2(offset,p)[k]={P99_FOR(,k,P00_SEQ,XFOR_ITDOMAIN_SCAL,P99_REVS(P99_SUB(0,k,P99_REVS(__VA_ARGS__))))};\
    int P99_PASTE2(ref,p)[k]={P99_FOR(,k,P00_SEQ,XFOR_ITDOMAIN_SCAL,P99_SUB(k,k,__VA_ARGS__))};\
\
    for(P99_FOR(P99_PASTE2(*iter,p),k, P00_SEQ, XFOR_ITDOMAIN_ASSIGN,P99_SUB(k,k,__VA_ARGS__));\
        P99_FOR(p,k, XFOR_OU, XFOR_ITDOMAIN_LT,P99_SUB(k,k,P99_SKP(k,__VA_ARGS__)));\
        ){\
            int lastUpperBound[k]={P99_FOR(,k,P00_SEQ,XFOR_ITDOMAIN_SCAL,P99_SUB(k,k,P99_SKP(k,__VA_ARGS__)))};\
            for(int iterk=0;iterk<k;++iterk){\
                if(superIteratorTmp[p-1>=0?p-1:0][iterk]!=NULL && *P99_PASTE2(iter,p)[iterk]<lastUpperBound[iterk]-1){\
                    ++(*P99_PASTE2(iter,p)[iterk]);\
                    List* l=malloc(sizeof(List));\
                    lists[iterk]=insertion_1(lists[iterk], l);\
                    l->indice=malloc(sizeof(int)*(p+1));\
                    l->ref=malloc(sizeof(int)*(p+1));\
                    l->next = NULL;\
                    l->numBoucle=iterk;\
                    P99_FOR(,p,P00_SEP,XFOR_ITDOMAIN_TEST2,)\
                    l->ref[p]=(*P99_PASTE2(iter,p)[iterk]-P99_PASTE2(ref,p)[iterk])*\
                    P99_PASTE2(grain,p)[iterk]+P99_PASTE2(offset,p)[iterk];\
                    l->indice[p]=(*P99_PASTE2(iter,p)[iterk]);\
                }\
            }\
        }\
    P99_FOR(,p,P00_SER,XFOR_CC,)\
    P99_FOR(,p,P00_SER,XFOR_CC,)\
    final=NULL;\
    for(int i=0;i<k;++i){\
        final=merge(p,final,lists[i]);\
    }\
    for(struct {int superSize; int found;List* last; List *act;}s\
            ={p+1,0,NULL,final};s.act!=NULL;s.found=0, s.last=s.act, s.act=s.act->next, destruction(s.last))\
        switch(s.act->numBoucle)

//grain positifs

#define XFOR_CASE(cas)\
            case cas: \
                      if(s.found)break;\
        s.found=1;\
        for(int cpt=0; cpt<s.superSize; ++cpt){\
            if(superIterator[cpt][cas]!=NULL)\
                *superIterator[cpt][cas]=s.act->indice[cpt];\
        }\
        if(s.act->next==NULL){\
            for(int cpt=0; cpt<s.superSize; ++cpt)\
                free(superIterator[cpt]);\
            free(lists);\
        }

#define XFOR_ITDOMAIN_SUPERITERATOR(NAME,X,I)\
    NAME[I]=NULL

#define XFOR_INIT\
    int **superIterator[XFOR_MAX_PROF];\
    int **superIteratorTmp[XFOR_MAX_PROF];\
    List *final=NULL;\
    List **lists=NULL

#endif
