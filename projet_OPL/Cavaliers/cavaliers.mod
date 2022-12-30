/*********************************************
 * OPL 12.10.0.0 Model
 * Author: camille
 * Creation Date: 29 déc. 2022 at 23:15:38
 *********************************************/

//using CP;

 int n = 8;
 
 int N = n+4;
 
 dvar boolean x[1..N, 1..N];
 
 minimize sum(i in 1..N, j in 1..N) x[i,j];
 
 constraints{
   forall(i in 1..2, j in 1..N)
     x[i][j]==0;
   forall(i in N-1..N, j in 1..N)
     x[i][j]==0;
   forall(i in 1..N, j in 1..2)
     x[i][j]==0;
   forall(i in 1..N, j in N-1..N)
     x[i][j]==0;
   forall(i in 3..N-2, j in 3..N-2)
     x[i,j] + x[i-2, j+1]+x[i-1, j+2]+x[i+1, j+2]+x[i+2, j+1]+x[i+2, j-1]+x[i+1 ,j-2]+x[i-1, j-2]+x[i-2, j-1] >=1;
 }
 
 execute{
   for(var i=3; i<=N-2; i++){
     for(var j=3; j<=N-2; j++){
       if(x[i][j]==1){
         write("O ");
       } else {
         write("X ");
       }
     }
     writeln("");
   }
 }