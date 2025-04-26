#include <fastjet/JetDefinition.hh>

#ifndef __E0_Scheme__
#define __E0_Scheme__

class E0_Scheme : public fastjet::JetDefinition::Recombiner {
public:
  E0_Scheme() {;}
  ~E0_Scheme() {;}

  std::string description() const override {return "The E0 Schema";}

  void recombine(const fastjet::PseudoJet& pa,
		 const fastjet::PseudoJet& pb,
		 fastjet::PseudoJet& pab) const;

  static fastjet::JetDefinition::Recombiner* instance() { return new E0_Scheme(); }
};

#endif

#ifndef __p_Scheme__
#define __p_Scheme__

class p_Scheme : public fastjet::JetDefinition::Recombiner {
public:
  p_Scheme() {;}
  ~p_Scheme() {;}

  std::string description() const override {return "The p Schema";}

  void recombine(const fastjet::PseudoJet& pa,
		 const fastjet::PseudoJet& pb,
		 fastjet::PseudoJet& pab) const;

  static fastjet::JetDefinition::Recombiner* instance() { return new p_Scheme(); }
};

#endif
