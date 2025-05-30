#include "Recombiner.h"

void E0_Scheme::recombine(const fastjet::PseudoJet& pa,
			     const fastjet::PseudoJet& pb,
			     fastjet::PseudoJet& pab) const {
  double pabMag = sqrt((pa.px() + pb.px()) * (pa.px() + pb.px()) + (pa.py() + pb.py()) * (pa.py() + pb.py()) +
		       (pa.pz() + pb.pz()) * (pa.pz() + pb.pz()));
  double E0scale = (pa.E() + pb.E()) / pabMag;
  pab.reset(
	    (pa.px() + pb.px()) * E0scale, (pa.py() + pb.py()) * E0scale, (pa.pz() + pb.pz()) * E0scale, pa.E() + pb.E());

}

void p_Scheme::recombine(const fastjet::PseudoJet& pa,
			     const fastjet::PseudoJet& pb,
			     fastjet::PseudoJet& pab) const {
  double pabMag = sqrt((pa.px() + pb.px()) * (pa.px() + pb.px()) + (pa.py() + pb.py()) * (pa.py() + pb.py()) +
		       (pa.pz() + pb.pz()) * (pa.pz() + pb.pz()));

  pab.reset(pa.px() + pb.px(), pa.py() + pb.py(), pa.pz() + pb.pz(), pabMag);

}
