#include "pfcandidate.h"

using namespace std;
using namespace fastjet;


MOD::PFCandidate::PFCandidate(double px, double py, double pz, double energy, int pdgId) : _pdgId(pdgId) {
  PseudoJet p = PseudoJet(px, py, pz, energy);
  p.set_user_index(pdgId);

  _pseudojet = p;
  _pdgId = pdgId;
}

MOD::PFCandidate::PFCandidate(istringstream & input_stream) {

   string tag;
   double px, py, pz, energy;
   int pdgId;

   input_stream >> tag >> px >> py >> pz >> energy >> pdgId;

   _pseudojet = PseudoJet(px, py, pz, energy);
   _pseudojet.set_user_index(pdgId);

   _pdgId = pdgId;
}

MOD::PFCandidate::PFCandidate(PseudoJet particle) {
  _pseudojet = particle;
  _pdgId = particle.user_index();
}

MOD::PFCandidate::PFCandidate() {}

PseudoJet MOD::PFCandidate::pseudojet() const {
   return _pseudojet;
}

int MOD::PFCandidate::pdgId() const {
   return _pdgId;
}


string MOD::PFCandidate::make_string() const {
   stringstream ss;
   ss << "  PFC"
        << setw(16) << fixed << setprecision(8) << _pseudojet.px()
        << setw(16) << fixed << setprecision(8) << _pseudojet.py()
        << setw(16) << fixed << setprecision(8) << _pseudojet.pz()
        << setw(16) << fixed << setprecision(8) << _pseudojet.E()
        << setw(8) << noshowpos << _pdgId
        << endl;

   return ss.str();
}

string MOD::PFCandidate::make_header_string() const {
   stringstream ss;
   ss << "# PFC" << "              px              py              pz          energy   pdgId" << endl;
   return ss.str();
}

bool MOD::PFCandidate::operator < (const MOD::PFCandidate& j1) const {
  if (pseudojet().pt() > j1.pseudojet().pt())
    return true;
  return false;
}

namespace MOD {
   ostream& operator<< (ostream& os, const PFCandidate& particle) {
      os << particle.make_string();
      return os;
   }
}
