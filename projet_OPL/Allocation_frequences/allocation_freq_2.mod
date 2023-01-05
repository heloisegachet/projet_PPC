/*********************************************
 * OPL 12.10.0.0 Model
 * Author: camille
 * Creation Date: 28 déc. 2022 at 15:11:38
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
	var n=1;
	var nMax = 10;
	cp.param.SearchType="DepthFirst";
	cp.param.Workers=1;
	cp.startNewSearch();
	while (cp.next() && n<=nMax) {
		n++;
		writeln(thisOplModel.x);
	}
	cp.endSearch();
}