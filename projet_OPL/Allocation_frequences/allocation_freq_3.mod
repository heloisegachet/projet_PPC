/*********************************************
 * OPL 12.10.0.0 Model
 * Author: camille
 * Creation Date: 28 déc. 2022 at 16:46:50
 *********************************************/
using CP;

tuple Offset{
  int ti;
  int tj;
  int valeur;
}

int n_transmitters = ...;
int n_freq = ...;

{Offset} offset = ...;

dvar int x[1..n_transmitters] in 1..n_freq;

constraints {
  forall(i in 1..n_transmitters : i%2==0)
    x[i]%2 == 1;
  forall(i in 1..n_transmitters : i%2==1)
    x[i]%2 == 0;
  forall(o in offset) {
    abs(x[o.ti]-x[o.tj]) >= o.valeur;
  }
}

main {
	thisOplModel.generate();
	while (cp.solve()) {
		writeln(thisOplModel.x);
		var MaxF = 0;
		for (var c in thisOplModel.x){
			if(thisOplModel.x[c]>MaxF){
			  MaxF = thisOplModel.x[c];
			}
 		}		
		for (var f in thisOplModel.x){
		  thisOplModel.x[f].UB = MaxF-1;
		}
	}
}