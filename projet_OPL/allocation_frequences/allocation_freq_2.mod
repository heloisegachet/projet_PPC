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

{Offset} offset = {
   <1,2,3>,
   <1,5,2>,
   <2,3,2>,
   <2,4,1>,
   <2,5,2>,
   <3,4,3>,
   <3,5,1>,
   <6,3,1>,
   <6,4,2>,
   <7,2,3>,
   <7,3,2>
};

dvar int x[1..7] in 1..10;

constraints {
  forall(i in 1..7 : i%2==0)
    x[i]%2 == 1;
  forall(i in 1..7 : i%2==1)
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