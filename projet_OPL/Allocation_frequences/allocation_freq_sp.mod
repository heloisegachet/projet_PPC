/*********************************************
 * OPL 12.10.0.0 Model
 * Author: camille
 * Creation Date: 4 janv. 2023 at 21:21:06
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

// commenter ou non la ligne selon si on veut une solution faisable ou optimale
minimize max(i in 1..7) x[i];

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
  var f = cp.factory;
  var phase1 = f.searchPhase(
		thisOplModel.x,
		f.selectSmallest(f.domainSize()),
		f.selectSmallest(f.value()));
  cp.setSearchPhases(phase1);
  cp.param.SearchType="DepthFirst";
  cp.param.Workers=1;
  thisOplModel.generate();
  if(cp.solve()){
    writeln(thisOplModel.x);
  }
}