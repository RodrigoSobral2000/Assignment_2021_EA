#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007

int counter;
int n,h,max_h,limit,lim_up,lim_down;
int maior;

int mod_abs(int a, int mod) {
    return ((a % mod) + mod) % mod;
}
int mod_add(int a, int b, int mod) {
    return (mod_abs(a, mod) + mod_abs(b, mod)) % mod;
}
int mod_sub(int a, int b, int mod) {
    return mod_add(a, -b, mod);
}

void arcs_for_k_blocks(int k, int *dp, int *new_dp){
    int i;

    int index=k-4;
    int aux,aux1,cum=0,last_max=max_h;


    if((max_h=(h-1)*(n-k+1))>limit){ //para o calc na function rec
        max_h=limit;
    }


    if(last_max>lim_up){
        last_max=lim_up;
    }
    //printf("\nk:%d\n",k);

    if((aux=index+h-1)>max_h-1){
        aux=max_h-1;
    }

    //printf("DP\n");
    /*
    printf("down\t|\tup\n");
    for(i=0;i<lim_up;i++){
        printf("%d\t|\t%d\n",dp[i*2],dp[i*2+1]);
    }printf("\n");*/

    for(i=index;i<aux;i++){ //index é a partir de onde começa a contar na dp
        cum=mod_add(cum,dp[i*2+1],MOD);
        new_dp[(i+1)*2+1]=cum; 
        if(lim_up+(h-2)-(i-index)<=max_h){
            new_dp[(lim_up+(h-2)-(i-index))*2+1]=cum;
        }

        ////
        if(i+2<h){
            //printf("0-->+%d counter=%d\n",cum,counter);
            counter=mod_add(counter,cum,MOD);
        }
        //printf("i:%d | i:%d\n",i+1,(lim+(h-2)-(i-index)));
    }
    if((aux=lim_up-1)>max_h-1){ //lim é o final da dp
        aux=max_h-1;
    }
    
    for(i=i;i<aux;i++){
        cum=mod_add(cum,mod_add(dp[i*2+1],-dp[(i-(h-1))*2+1],MOD),MOD);
        new_dp[(i+1)*2+1]=cum; 
        if(i+2<h){
            //printf("1-->+%d counter=%d\n",cum,counter);
            counter=mod_add(counter,cum,MOD);
        }
    }

    
    //primeiro olhar para os downs na dp e só dps olhar para os ups
    
    cum=0;
    
    if((aux1=lim_down-h+1)<0){
        aux1=0;
    }

    for(i=lim_down;i>aux1;i--){
        cum=mod_add(cum,dp[i*2],MOD);
        new_dp[(i-1)*2]=cum; 
        if(i<h){
            //printf("2-->+%d counter=%d\n",cum,counter);
            counter=mod_add(counter,cum,MOD);
        }
    }
    for(i=i;i>0;i--){
        cum=mod_add(cum,mod_add(dp[i*2],-dp[(i+(h-1))*2],MOD),MOD);
        new_dp[(i-1)*2]=cum;
        if(i<h){
            //printf("3-->+%d counter=%d\n",cum,counter);
            counter=mod_add(counter,cum,MOD);
        }
    }
    /*
    printf("NEW DP 0\n");
    printf("down\t|\tup\n");
    for(i=0;i<=lim_up+h-2;i++){
        printf("%d\t|\t%d\n",new_dp[i*2],new_dp[i*2+1]);
    }printf("\n");*/

    //ups to downs
    
    cum=0;
    if((aux1=last_max-h)<0){
        aux1=0;
    }
    
    for(i=last_max-1;i>aux1;i--){
        cum=mod_add(cum,dp[i*2+1],MOD);
        new_dp[(i-1)*2]=mod_add(new_dp[(i-1)*2],cum,MOD); 
        ///
        if(i<h){
           // printf("4-->+%d counter=%d\n",cum,counter);
            counter=mod_add(counter,cum,MOD);
        }
    }
    for(i=i;i>0;i--){
        cum=mod_add(cum,mod_add(dp[i*2+1],-dp[(i+(h-1))*2+1],MOD),MOD);
        new_dp[(i-1)*2]=mod_add(new_dp[(i-1)*2],cum,MOD);
        if(i<h){
           // printf("5-->+%d counter=%d\n",cum,counter);
            counter=mod_add(counter,cum,MOD);
        }
    }
/*
    printf("NEW DP 1\n");
    printf("down\t|\tup\n");
    for(i=0;i<=lim_up+h-2;i++){
        printf("%d\t|\t%d\n",new_dp[i*2],new_dp[i*2+1]);
    }printf("\n");*/
    /*
    if((aux=h-1)>lim_down){
        aux=lim_down;
    }
    for(i=0;i<aux;i++){
        printf("3-->+%d counter=%d\n",dp[i*2],counter);
        counter=mod_add(counter,dp[i*2],MOD);
    }*/

    lim_down=last_max-1;
    lim_up+=h-1;
    memset(dp, 0, limit*2*sizeof(int));


/*
[1,3,6,7,6,3,1]
 +[1,3,6,7,6,3,1]
   +[1,3,6,7,6,3,1]
        =
[1,4,10,16,19,16,10,4,1]
*/


}

void func(){
    int k,i;
    int dp[limit*2]; //[false,true]
    int new_dp[limit*2];
    int *pt_aux,*pt_dp,*pt_new_dp;
    /*
    dp=(int*)malloc(limit*2*sizeof(int));
    new_dp=(int*)malloc(limit*2*sizeof(int));*/
    pt_dp=dp;
    pt_new_dp=new_dp;
    memset(dp, 0, limit*2*sizeof(int));
    memset(new_dp, 0, limit*2*sizeof(int)); 

    if(h<=1 || n<3){
        return; //impossivel
    }

    //k>=3 !!!!!
    //calculate for k==3 first to fill dp
    //rec(0,1,1,3,dp,1,miss);

    //init set k=3
    lim_down=0;
    if((lim_up=h-1)>max_h){
        lim_up=max_h;
    }
    for(i=0;i<lim_up;i++){
        dp[i*2+1]=1;  
    }counter=lim_up;

    for(k=4;k<=n;k++){ //before was n instead of n+1
        pt_aux=pt_dp;
        arcs_for_k_blocks(k,pt_dp,pt_new_dp);
        pt_dp=pt_new_dp;
        pt_new_dp=pt_aux;
    }

    /*
    free(dp);
    free(new_dp);*/

    /*
    printf("----\n"); 
        for(i=0;i<limit;i++){
        if(miss[i]!=0){
            printf("k = %d | missed height %d , %d times\n",k-1,i+1,miss[i]);
        }
        }*/
}    

int main(void){
    int case_tests_qnt,H;
    scanf("%d",&case_tests_qnt);
    for(int i=0;i<case_tests_qnt;i++){
        scanf("%d %d %d",&n,&h,&H);
        counter=0;
        //calculate max possible height for given n blocks of height h
        //max_h=limit=H-h;
        if((max_h=limit=(h-1)*(n/2+n%2)+1-h)>H-h){
            max_h=limit=H-h;
        }

        func();
        printf("%d\n",counter);
    }
}