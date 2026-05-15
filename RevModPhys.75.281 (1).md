REVIEWS OF MODERN PHYSICS, VOLUME 75, JANUARY 2003 

## Quantum dynamics of single trapped ions 

## D. Leibfried 

University of Colorado and National Institute of Standards and Technology, Boulder, Colorado 80305-3328 

## R. Blatt 

Institut fu[¨] r Experimentalphysik, Universita[¨] t Innsbruck, A-6020 Innsbruck, Austria 

## C. Monroe 

FOCUS Center and Department of Physics, University of Michigan, Ann Arbor, Michigan 48109-1120 

## D. Wineland 

National Institute of Standards and Technology, Boulder, Colorado 80305-3328 

## (Published 10 March 2003) 

Single trapped ions represent elementary quantum systems that are well isolated from the environment. They can be brought nearly to rest by laser cooling, and both their internal electronic states and external motion can be coupled to and manipulated by light fields. This makes them ideally suited for quantum-optical and quantum-dynamical studies under well-controlled conditions. Theoretical and experimental work on these topics is reviewed in the paper, with a focus on ions trapped in radio-frequency (Paul) traps. 

|ONTENTS||C. Electromagnetically induced transparency||
|---|---|---|---|
|||cooling|300|
|I. Introduction<br>II. Radio-Frequency Traps for Single Charged Particles<br>A. Classical motion of charged particles in rf traps<br>1.<br>Classical equations of motion<br>2.<br>Lowest-order approximation<br>3.<br>Typical realizations<br>B. Quantum-mechanical motion of charged<br>particles in rf traps<br>1.<br>Quantum-mechanical equations of motion<br>2.<br>Lowest-order quantum approximation<br>C. Special quantum states of motion in ion traps<br>1.<br>The number operator and its eigenstates<br>2.<br>Coherent states|282<br>283<br>283<br>283<br>284<br>285<br>285<br>286<br>287<br>287<br>287<br>288|1.<br>Cooling in the Lamb-Dicke regime<br>2.<br>Scattering rates in EIT cooling<br>3.<br>Experimental results<br>V. Resonance Fluorescence of Single Ions<br>A. Excitation spectroscopy, line shapes<br>B. Nonclassical statistics, antibunching, and<br>squeezing<br>C. Spectrum of resonance fuorescence, homodyne<br>detection of fuorescence<br>VI. Engineering and Reconstruction of Quantum States<br>of Motion<br>A. Creation of special states of motion and<br>internal-state/motional-state entanglement|301<br>302<br>303<br>303<br>303<br>304<br>305<br>307<br>307|
|3.<br>Squeezed vacuum states<br>4.<br>Thermal distribution|288<br>289|1.<br>Creation of number states<br>2.<br>Creation of coherent states|307<br>308|
|III. Trapped Two-Level Atoms Coupled to Light Fields|289|3.<br>Creation of squeezed states|310|
|A. The two-level approximation|290|4.<br>‘‘Schro¨dinger-cat’’ states of motion|310|
|B. Theoretical description of the coupling|290|5.<br>Arbitrary states of motion|312|
|1.<br>Total Hamiltonian and interaction||B. Full determination of the quantum state of||
|Hamiltonian|290|motion|312|
|2.<br>Rabi frequencies|291|1.<br>Reconstruction of the number-state density||
|3.<br>Lamb-Dicke regime|292|matrix|313|
|4.<br>Resolved sidebands|292|2.<br>Reconstruction of _s_-parametrized||
|5.<br>Unresolved sidebands|293|quasiprobability distributions|313|
|6.<br>Spectrum of resonance fuorescence|293|3.<br>Experimental state reconstruction|314|
|C. Detection of internal states|294|VII. Quantum Decoherence in the Motion of a Single||
|1.<br>The electron shelving method|294|Atom|315|
|2.<br>Experimental observations of quantum||A. Decoherence background|316|
|jumps|295|B. Decoherence reservoirs|316|
|D. Detection of motional-state populations|295|1.<br>High-temperature amplitude reservoir|316|
|IV. Laser Cooling of Ions|296|2.<br>Zero-temperature amplitude reservoir|318|
|A. Doppler cooling|296|3.<br>High-temperature phase reservoir|319|
|B. Resolved-sideband cooling|298|C. Ambient decoherence in ion traps|320|
|1.<br>Theory|298|VIII. Conclusions|320|
|2.<br>Experimental results|299|Acknowledgments|320|



## CONTENTS 

0034-6861/2003/75(1)/281(44)/$35.00 

©2003 The American Physical Society 

281 

282 

Leibfried et al.: Quantum dynamics of single trapped ions 

|Appendix:|Couplings of Light Fields to The Internal Electronic|Couplings of Light Fields to The Internal Electronic||
|---|---|---|---|
|State|||320|
||1.|Dipole coupling|321|
||2.|Quadrupole coupling|321|
||3.|Raman coupling|321|
|References|||322|



‘‘. . . _we never experiment with just one electron or atom or (small) molecule_ .’’—E. Schro[¨] dinger, 1952 

## I. INTRODUCTION 

In the last 30 years, experiments with single trapped ions or charged fundamental particles have provided key contributions to many fields in physics. This review does not attempt to cover all these fields and will therefore concentrate on the use of trapped ions in quantum optics and the closely related field of coherent control of the internal state and the motional state of ions in the trap potential. With the availability of spectrally narrow light sources based on lasers, these fields have prospered in the last 15 years and are still in rapid development, gaining momentum as a result of the new challenges encountered in quantum information processing. While there are several review papers and books covering the more traditional work in ion traps [see, for example, Brown and Gabrielse (1986); Paul (1990); Gosh (1995)], those on ion-trap-based frequency standards (Diddams _et al._ , 2001, and references therein), and those that concentrate on quantum information processing (Steane, 1997; Wineland _et al._ , 1998), there is no comprehensive work covering quantum optics, coherent control of the motion, and motional-state reconstruction with trapped ions. The purpose of this review is to fill this gap. 

One seemingly obvious approach to understanding the interaction of atoms and light is to isolate and confine a single atomic system, put it to rest or at least into a well-characterized state of motion, and then direct light fields onto that isolated system in a precisely controlled manner. This idea seems quite straightforward, but can be difficult to convert into a feasible experiment. Traps for neutral atoms often have a rather shallow trapping potential that can also depend on the electronic state of the atom, thus perturbing the internal states and entangling them with the motion. With ion traps, which couple to the excess charge of the trapped particle, potential wells that are up to several electron volts deep and do not depend on the internal electronic state of the ion can be realized. The most popular forms of ion traps are the Penning trap (Penning, 1936), in which the charged particles are held in a combination of electrostatic and magnetic fields, and the traps developed by Wolfgang Paul (Paul, 1990), in which a spatially varying time-dependent field, typically in the radio-frequency (rf) domain, confines the charged particles in space. In this review only the latter type will be considered. 

The intrinsically low signal levels one faces in the detection of single particles can be overcome by laserinduced fluorescence. On a dipole allowed transition a single ion can scatter several million photons per second and a sufficient fraction may be detected even with de- 

tectors covering a small solid angle and having low quantum efficiencies. Moreover, several variations of the electron shelving technique suggested by Dehmelt (1975) can distinguish internal electronic states of the trapped ion with a detection efficiency close to unity. 

The first single-particle trapping experiments in the present context were those on electrons confined in a Penning trap at the University of Washington by Wineland, Ekstrom, and Dehmelt (1973). The same paper contained a proposal to store a single atomic ion, an idea further discussed by Dehmelt (1973) in the same year. It took another seven years until Neuhauser _et al._ (1980) reported the first experiment with a single barium ion in an rf trap. This experiment was followed by one of Wineland and Itano (1981), who used a single magnesium ion in a Penning trap. To date there are about 20 groups all over the world that work with single ions in rf traps. 

An important ingredient for work with atomic systems was the advent of laser cooling. It was independently proposed by Ha[¨] nsch and Schawlow (1975) for free particles and by Wineland and Dehmelt (1975a) for trapped particles. The first atomic laser cooling experiments were reported independently by Wineland, Drullinger, and Walls (1978) on Mg[�] ions and by Neuhauser _et al._ (1978) on Ba[�] ions. In the following years laser cooling of collections of ions or single ions found widespread use in many different research groups around the world. Laser cooling to the ground state of the trapping potential was first achieved on a single Hg[�] ion by the National Institute of Standards and Technology (NIST) group (Diedrich _et al._ , 1989). 

Many experiments with single ions have the goal of using a narrow optical or microwave transition between electronic states of the ion(s) for frequency standards (Diddams _et al._ , 2001, and references therein). Others deal with the quantum-mechanical aspects of the light emitted by a single ion and the quantum dynamics of the ions’ motion in the trapping potential. The latter field gained considerable interest after it was realized that these dynamics closely resemble the Jaynes-Cummings model that was well known from cavity QED (Blockley, Walls, and Risken, 1992). These are the experiments that will be preferentially covered in this review. In recent years a number of groups have also started working with single ions in an effort to implement quantum information processing following the proposal by Cirac and Zoller (1995), a field that is very closely related to our subject (Steane, 1997; Wineland _et al._ , 1998). 

Following this Introduction, the second section consists of a discussion of the classical and quantum motion of single ions in rf traps, including the driven motion due to the trapping rf field (micromotion). Section III introduces two-level atoms and describes the coupling of trapped ions to the light field. With these tools at hand, we study laser cooling in Sec. IV and resonance fluorescence in Sec. V. In Sec. VI we review experimentally realized methods for engineering and reconstructing 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

283 

Leibfried et al.: Quantum dynamics of single trapped ions 

quantum states of motion. Section VII summarizes experiments on decoherence and reservoir engineering with single trapped ions. 

## II. RADIO-FREQUENCY TRAPS FOR SINGLE CHARGED PARTICLES 

In this section the equations of motion of a charged particle in different common types of rf traps are discussed. Only trap types that lead to an electric potential �( _x_ , _y_ , _z_ , _t_ ) of approximately quadrupolar spatial shape in the center of the trapping region are considered here. It is further assumed that the potential can be decomposed into a time-dependent part that varies sinusoidally at the rf drive frequency �rf and a time-independent static part: 

**==> picture [229 x 75] intentionally omitted <==**

The condition that this potential has to fulfill the Laplace equation ���0 at every instant in time leads to restrictions in the geometric factors, namely, 

**==> picture [229 x 29] intentionally omitted <==**

From these restrictions it is obvious that no local threedimensional minimum in free space can be generated, so the potential can only trap charges in a dynamical way. As we shall see below, the drive frequency and voltages can be chosen in such a way that the time-dependent potential will give rise to stable, approximately harmonic motion of the trapped particles in all directions. 

One choice for the geometric factors is 

**==> picture [229 x 29] intentionally omitted <==**

leading to three-dimensional confinement in a pure oscillating field. A second choice is 

**==> picture [229 x 29] intentionally omitted <==**

leading to dynamical confinement in the _x_ - _y_ plane and static potential confinement for positively charged particles in the _z_ direction as used in linear traps (Paul, 1990). 

First we give an overview of the classical equations of motion and their solutions, and approximations to these solutions are studied. A quantum-mechanical picture of ions trapped in rf fields following the approach of Glauber (1992) is then derived and it is shown that in the range of trapping parameters used in the experiments discussed here, the quantized motion of trapped ions can be modeled by static potential harmonic oscillators to a very good approximation. 

## A. Classical motion of charged particles in rf traps 

## 1. Classical equations of motion 

The classical equations of motion of a particle with mass _m_ and charge _Z_ � _e_ � in a potential of the form given by Eq. (1) were first studied by Paul, Osberghaus, and Fischer (1958). They are decoupled in the spatial coordinates. Only the motion in the _x_ direction will be discussed below; the other directions can be treated analogously. The equation of motion is 

**==> picture [229 x 24] intentionally omitted <==**

and can be transformed to the standard form of the Mathieu differential equation 

**==> picture [229 x 27] intentionally omitted <==**

by the substitutions 

**==> picture [229 x 27] intentionally omitted <==**

The Mathieu equation belongs to the general class of differential equations with periodic coefficients. The general form of the stable solutions follows from the Floquet theorem (McLachlan, 1947; Abramowitz and Stegun, 1972), 

**==> picture [121 x 26] intentionally omitted <==**

**==> picture [200 x 26] intentionally omitted <==**

where the real-valued characteristic exponent � _x_ and the coefficients _C_ 2 _n_ are functions of _a x_ and _q x_ only and do not depend on initial conditions. _A_ and _B_ are arbitrary constants that may be used to satisfy boundary conditions or normalize a particular solution. By inserting Eq. (8) into Eq. (6) one obtains a recursion relation, 

**==> picture [229 x 29] intentionally omitted <==**

that connects the coefficients and � _x_ to _a x_ and _q x_ . Simple rearrangements and recursive use of Eq. (9) yield continued fraction expressions for the _C_ 2 _n_ , 

**==> picture [247 x 134] intentionally omitted <==**

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

284 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [481 x 260] intentionally omitted <==**

FIG. 1. Trap stability: (a) Stability diagram for a cylindrically symmetric trap with rf confinement in all three axes (��� ���/2,���������/2); (b) stability diagram for a linear trap (������,������,���0). 

**==> picture [230 x 66] intentionally omitted <==**

Numerical values for � _x_ and the coefficients can be extracted by truncating the continued fractions after the desired accuracy is reached. The contributions of higher orders in the continued fraction rapidly drop for typical values of _a x_ and _q x_ used in the experiments described here. 

The region of stability in the _a i_ - _q i_ plane ( _i_ �� _x_ , _y_ , _z_ �) is bounded by pairs of _a i_ and _q i_ that yield either � _i_ �0 or � _i_ �1 (Paul, Osberghaus, and Fischer, 1958; Gosh, 1995). The stable region that contains the points ( _a i_ , _q i_ )�(0,0) for all _i_ �� _x_ , _y_ , _z_ � is often called the lowest stability region. The traps relevant for the experiments discussed here work inside this lowest stable region with _a i_ �0. 

The exact shape of the stability regions depends on the actual parameters in Eq. (1). For three-dimensional (3D) rf confinement, for example, with the parameters as in Eq. (3), the trap electrodes are often cylindrically symmetric around one axis (usually labeled the _z_ axis), leading to the parameter relations ���������/2 and ������/2. The parameters _a i_ and _q i_ in the Mathieu equations along the different axes will then obey 

**==> picture [229 x 12] intentionally omitted <==**

A trapped particle will be stable in all three dimensions if 

**==> picture [229 x 11] intentionally omitted <==**

Figure 1(a) shows a plot of the lowest stability region for the cylindrically symmetric Paul trap. The axes displayed are _a z_ and _q z_ , and the corresponding values for the _x_ and _y_ dimensions can be found from Eq. (12). The borderlines of stability in the _x_ and _y_ direction are identical. For the linear trap, the parameters have the relations 

**==> picture [229 x 12] intentionally omitted <==**

In this case the first stability region is symmetric around the _q x_ axis, since the borderlines of stability in the two directions are mirror images of each other [see Fig. 1(b)]. General traps with no intrinsic symmetry can have even more complicated stability diagrams, because the borderlines of stability might not be connected by simple relations such as in the two cases discussed here [see Eq. (4)]. The radially defocusing effects of the static potential along the _z_ axis in a linear Paul trap can also lead to modifications in the stability diagram, especially if the confinement along this axis becomes comparable in strength to the radial confinement (Drewsen and Brøner, 2000). 

## 2. Lowest-order approximation 

The lowest-order approximation to the ion trajectory 2 _x_ ( _t_ ) in the case (� _a x_ �, _q x_ )�1 can be found by assuming _C_ �4�0. Then, together with the initial condition _B_ � _A_ , Eq. (9) yields 

**==> picture [229 x 47] intentionally omitted <==**

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

285 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [217 x 143] intentionally omitted <==**

FIG. 2. Schematic drawing of the electrodes for a cylindrically symmetric 3D rf trap. Typical dimensions are _r_ 0�& _z_ 0 �100 �m– 1 cm with _U[˜]_ �100– 500 V, � _U_ ��0 – 50 V, and �rf/2��100 kHz– 100 MHz. 

identical to the solution found by the _pseudopotential approximation_ (Dehmelt, 1967; Gosh, 1995). The trajectory consists of harmonic oscillations at frequency � �� _x_ �rf/2��rf , the _secular motion_ , superposed with driven excursions at the rf frequency �rf . The driven excursions are 180° out of phase with the driving field and a factor _q x_ /2 smaller than the amplitude of the secular motion. These fast, small oscillations are therefore dubbed _micromotion_ . If micromotion is neglected, the secular motion can be approximated by that of a harmonic oscillator with frequency �. Most theoretical papers covering the subject of this review assume this approximation. In the course of this paper we shall see that it is justified in most cases if the ions are at reasonably low kinetic energy, even if we treat the center-of-mass motion of the ion quantum mechanically. 

## 3. Typical realizations 

One of the most popular trap configurations is the cylindrically symmetric 3D rf trap ( _a z_ ��2 _a x_ ��2 _a y_ ; _q z_ ��2 _q x_ ��2 _q y_ ). It can be realized with the electrode configuration shown in Fig. 2 where ���� �������2���2�� and where, to a good approximation, ��2/( _r_ 20�2 _z_ 20). This last expression holds exactly when the electrode surfaces coincide with equipotentials of Eq. (1) and holds reasonably well with truncated electrodes as shown in Fig. 2. Typically, the traps are operated in the left-hand portion of the stability diagram [Fig. 1(a)], where _q z_ �0.5; however, the entire stability diagram has been experimentally explored, including parametric instabilities, in an impressive series of experiments by the group of Werth (Alheit _et al._ , 1996). 

A second very useful trap electrode configuration is that for the linear rf trap ( _q z_ ����0; _q y_ �� _q x_ ) shown schematically in Fig. 3. This trap is essentially a linear quadrupole mass filter (Paul, 1990) that has been plugged on the ends with a static axial _z_ potential. If the axial potential is made fairly weak compared to the _x_ , _y_ potentials, two or more trapped ions will line up along the trap axis. This can be useful for addressing individual ions with laser beams. Typically these traps are 

**==> picture [193 x 179] intentionally omitted <==**

FIG. 3. Schematic drawing of the electrodes for a linear rf trap. A common rf potential _U[˜]_ cos(�rf _t_ ) is applied to the dark electrodes; the other electrodes are held at rf ground through capacitors (not shown) connected to ground. The lower right portion of the figure shows the _x_ - _y_ electric fields from the applied rf potential at an instant when the rf potential is positive relative to the ground. A static electric potential well is created (for positive ions) along the _z_ axis by applying a positive potential to the outer segments (gray) relative to the center segments (white). Typical dimensions are _r_ 0 �100 �m– 1 cm with _U[˜]_ �100– 500 V, � _U_ ��0 – 50 V, and �rf/2��100 kHz– 100 MHz. 

also operated in the left-hand portion of the stability diagram [Fig. 1(b)] with _q x_ �0.5. 

## B. Quantum-mechanical motion of charged particles in rf traps 

Even a simple account of the cooling process in ion traps, as well as the description of nonclassical states, relies on a quantum-mechanical picture of the motion. Since the trapping potential is not a static, but rather a time-dependent potential, it cannot be taken for granted that quantization of the motion in the effective timeaveraged potential already gives an adequate picture. In the first quantum-mechanical treatment of the timedependent potential by Cook, Shankland, and Wells (1985), the authors derived an approximate solution of the Schro[¨] dinger equation and concluded that the stability regions of classical and quantum-mechanical motion are identical. They also found that the dominant effect of the time-dependent potential is to multiply the wave function of the static pseudopotential by a timedependent phase factor. The essence of these findings was confirmed and further elaborated upon by Combescure (1986), who first derived an exact solution, and later by Brown (1991) and Glauber (1992). All these treatments are semiclassical in the sense that the trapping rf field is not quantized, but rather represented as a classical electromagnetic potential of the form of Eq. (1). The treatment given here follows the elegant approach of Glauber (1992). 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

286 

Leibfried et al.: Quantum dynamics of single trapped ions 

## 1. Quantum-mechanical equations of motion 

For the quantum-mechanical treatment of the motion we assume that the time-dependent potential is quadratic in each of the three Cartesian coordinates of the center of mass of the trapped particle. Then, as in the classical motion, the problem is separable into three one-dimensional problems. In one dimension and replacing the coordinate _x_ by the respective operator _xˆ_ , we can write the time-dependent potential _V_ ( _t_ ) as 

**==> picture [229 x 21] intentionally omitted <==**

where 

**==> picture [229 x 25] intentionally omitted <==**

can be thought of as a time-varying spring constant that will play a role similar to �[2] in the static potential harmonic oscillator. With these definitions, _H_[(] _[m]_[)] , the Hamiltonian of the motion, takes a form very similar to the familiar Hamiltonian of a static potential harmonic oscillator: 

**==> picture [229 x 25] intentionally omitted <==**

and we can immediately write down the equations of motion of these operators in the Heisenberg picture: 

**==> picture [229 x 56] intentionally omitted <==**

which can be combined into 

**==> picture [229 x 12] intentionally omitted <==**

It is easy to verify that this equation is equivalent to the Mathieu equation (6) if one replaces the operator _xˆ_ with a function _u_ ( _t_ ). This fact can be used to find solutions to Eq. (20) by utilizing a special solution of the Mathieu equation subject to the boundary conditions 

**==> picture [229 x 11] intentionally omitted <==**

This solution can be constructed from Eq. (8) with _A_ �1, _B_ �0, 

**==> picture [229 x 26] intentionally omitted <==**

where �( _t_ ) is a periodic function with period _T_ �2�/�rf . In terms of the coefficients of this solution, Eq. (21) takes the form 

**==> picture [229 x 39] intentionally omitted <==**

This solution and its complex conjugate are linearly independent; they therefore obey the Wronskian identity 

**==> picture [229 x 28] intentionally omitted <==**

The unknown coordinates _xˆ_ ( _t_ ) and _u_ ( _t_ ) satisfy the same differential equation, so the complex linear combination 

**==> picture [229 x 25] intentionally omitted <==**

is proportional to their Wronskian identity and also constant in time: 

**==> picture [229 x 27] intentionally omitted <==**

Moreover the right-hand side is exactly the annihilation operator of a static potential harmonic oscillator of mass _m_ and frequency �, 

**==> picture [229 x 12] intentionally omitted <==**

which immediately implies the commutation relation 

**==> picture [229 x 12] intentionally omitted <==**

This static potential oscillator will be called the _reference oscillator_ in the remainder of this section. 

The Heisenberg operators _xˆ_ ( _t_ ) and _pˆ_ ( _t_ ) can be reexpressed in terms of _u_ ( _t_ ) and the operators of the reference oscillator using Eq. (25): 

**==> picture [229 x 59] intentionally omitted <==**

so their entire time dependence is given by the special solution _u_ ( _t_ ) and its complex conjugate. 

For later calculations it is convenient to have expressions for a basis of time-dependent wave functions in the Schro[¨] dinger picture. Again the reference oscillator used above is very helpful in this task. In analogy to the static potential case we shall consider a set of basis states � _n_ , _t_ � in which _n_ �1,2,. . . ,�. These states are the dynamic counterpart of the harmonic-oscillator number (Fock) states. The ground state of the reference oscillator � _n_ �0� � obeys the condition 

**==> picture [229 x 13] intentionally omitted <==**

but since the Heisenberg operator _C[ˆ]_ is connected to the Schro[¨] dinger picture counterpart _C[ˆ] S_ by _C[ˆ]_ ( _t_ ) � _U[ˆ]_[†] ( _t_ ) _C[ˆ] SU[ˆ]_ ( _t_ ), with _U[ˆ]_ ( _t_ )�exp��( _i_ /�) _H[ˆ]_[(] _[m]_[)] �, we immediately get 

**==> picture [229 x 13] intentionally omitted <==**

by multiplying Eq. (30) with _U[ˆ]_ ( _t_ ) from the left and noting that _U[ˆ]_ ( _t_ )� _n_ �0� � is the Schro[¨] dinger state of the time-dependent oscillator that evolves from the ground state of the static potential reference oscillator. Since the time dependence of the Schro[¨] dinger operator _C S_ ( _t_ ) is due entirely to the explicit time dependence of _u_ ( _t_ ), Eq. (31) is equivalent to 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

287 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [229 x 11] intentionally omitted <==**

or reexpressed in coordinate space 

**==> picture [229 x 27] intentionally omitted <==**

The normalized solution is 

**==> picture [229 x 38] intentionally omitted <==**

In complete analogy to the static potential harmonic oscillator, all other states of a complete orthonormal base can be created by repeated operation on the ground † state with the creation operator _C[ˆ] S_ ( _t_ ): 

**==> picture [229 x 29] intentionally omitted <==**

expressed in coordinate space, and by rewriting _u_ ( _t_ ) such as in Eq. (22), these states are 

**==> picture [229 x 26] intentionally omitted <==**

with 

**==> picture [187 x 98] intentionally omitted <==**

where _H n_ is the Hermitian polynomial of order _n_ . The classical micromotion appears in the wave functions as a pulsation with the period of the rf driving field. For a static potential harmonic oscillator the evolution of the energy eigenstates only multiplies the wave function by a phase factor (which is why they are called stationary states). In the time-dependent potential studied here, the same is true, but only for times that are integer multiples of the rf period _T_ rf�2�/�rf . The states given by Eq. (36) are not energy eigenstates (they periodically exchange energy with the driving field in analogy to the classical micromotion), but they are the closest approximation to stationary states possible in the timedependent potential. Therefore they are often called _quasistationary states_ . 

These features will be illustrated in the next few sections, where we shall find the lowest-order corrections to the static potential oscillator picture in close analogy to the classical pseudopotential solution presented in Sec. II.A.2. We also discuss the analogous operator to the number operator for the static potential harmonic oscillator and some special classes of motional states in the ion trap. 

## 2. Lowest-order quantum approximation 

The lowest-order approximation for the quantummechanical states will be studied by first deriving an approximate expression for the special solution _u_ ( _t_ ). Again � _a x_ �, _q_ 2 _x_ �1 and _C_ �4�0 is assumed. Together with the initial conditions of Eq. (21) one finds 

**==> picture [229 x 47] intentionally omitted <==**

essentially the lowest-order classical solution found earlier in Eq. (15). It still must be stressed that the frequency of the reference oscillator � is equal to the characteristic exponent � _x_ �rf/2 only in this lowest-order approximation. The periodic breathing of � _n_ ( _t_ ) with period _T_ rf is now obvious, as one can see in the approximate expression �0( _t_ ) for the ground-state wave function: 

**==> picture [229 x 71] intentionally omitted <==**

while the phase factor in Eq. (36) is governed by the ground-state pseudoenergy ��/2. This expression is identical to the static harmonic potential ground-state wave function if one sets �rf�0. 

## C. Special quantum states of motion in ion traps 

In this section various classes of motional states in ion traps will be discussed, some nonclassical in nature and some more reminiscent of classical motion. For each of the classes theoretical proposals on how to create them in an ion trap have been brought forward and all have been created and observed experimentally. 

## 1. The number operator and its eigenstates 

To exploit the close analogy between the confinement in an rf ion trap and that in a static harmonic potential, it is advantageous to express the motional states in the basis of the eigenstates of the reference oscillator number operator. We shall first do this in the Heisenberg picture. Since _C[ˆ]_ ( _t_ ) is time independent [see Eq. (27)], the operator 

**==> picture [229 x 12] intentionally omitted <==**

is also time independent and the eigenstates are just the familiar number or Fock states of the static potential harmonic reference oscillator with the usual ladder algebra, 

**==> picture [229 x 34] intentionally omitted <==**

Transforming to the Schro[¨] dinger picture we get 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

288 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [229 x 34] intentionally omitted <==**

The eigenstates and eigenvalues of these operators are easily inferred from Eq. (35) in the last section: 

**==> picture [229 x 34] intentionally omitted <==**

implying 

**==> picture [229 x 13] intentionally omitted <==**

These Schro[¨] dinger-picture eigenstates can therefore be used in complete analogy to the static potential harmonic oscillator, and all algebraic properties of the static potential ladder operators carry over to _C[ˆ] S_ ( _t_ ) and † _C[ˆ] S_ ( _t_ ). The only difference is that these states are _not energy eigenstates_ of the system, since the micromotion periodically changes the total kinetic energy of the ion. Nevertheless, due to the periodicity of the micromotion, it makes sense to connect the quantum number _n_ to the energy of the ion averaged over a period _T_ rf�2�/�rf of the drive frequency. This connection will be further explored in Sec. IV on laser cooling. 

Any motional state can be expressed as a superposition of the number states 

**==> picture [229 x 26] intentionally omitted <==**

and a number of these expansions will be used in what follows in this paper. For convenience we shall set � _n_ , _t_ � �� _n_ � and only write the time dependence explicitly if it helps to clarify matters. 

## 2. Coherent states 

In a static potential harmonic oscillator, a coherent state of motion ��� of the ion corresponds to a Gaussian minimum-uncertainty wave packet in the position representation whose center oscillates classically in the harmonic well and retains its shape. The wave packet has the same shape as the ground-state wave function. Glauber has shown that the states that evolve out of an initial coherent state in the dynamic trapping potential are also displaced forms of the Gaussian ground-state Eq. (34) (Glauber, 1992). The displaced Gaussian does the same breathing as the ground state, but does not spread, and its center of gravity follows the classical trajectory of an ion in the trap (now secular motion and micromotion). States of this type were first considered by Schro[¨] dinger (1926) when he tried to construct wave packets that reflected the classical motion of a harmonic oscillator.[1] 

1One curiosity in his paper is that he considered the real part of the constructed wave packet to reflect the physical state, since the probability interpretation of quantum mechanics was not yet established then. 

The term ‘‘coherent state’’ was first used by Glauber (1963, 1964) in connection with quantum states of a light field. There are different ways to define a coherent state (see Klauder and Skagerstam, 1985, for a review); for example, they are the eigenstates of the annihilation operator with complex eigenvalue �: 

**==> picture [229 x 12] intentionally omitted <==**

It is easy to prove that states with coefficients in the number-state basis expansion Eq. (44), 

**==> picture [229 x 27] intentionally omitted <==**

are eigenstates of this operator, and the probability distribution among number states is Poissonian, 

**==> picture [209 x 13] intentionally omitted <==**

**==> picture [19 x 10] intentionally omitted <==**

Another popular choice is to represent coherent states as the action of a displacement operator, 

**==> picture [229 x 13] intentionally omitted <==**

on the vacuum state, namely, 

**==> picture [229 x 12] intentionally omitted <==**

The action of successively applied displacement operators is also additive up to phase factors, 

**==> picture [229 x 13] intentionally omitted <==**

so the displacements form a group with _D[ˆ]_ (0)� _I[ˆ]_ as a neutral element. Note that the extra phase on the righthand side makes the displacement operations noncommutative in general. 

## 3. Squeezed vacuum states 

In any quantum state the product of the variance in position and momentum has a lower bound of �[2] /4, given by the Heisenberg uncertainty relation. The ground state of a static potential harmonic oscillator and all other coherent states are minimum-uncertainty states in which the variance in position is (� _x_ )[2] �� _x_[2] ��� _x_ �[2] �1/( _m_ �)�/2 and the variance in momentum is (� _p_ )[2] �( _m_ �)�/2. If one now ‘‘squeezes’’ the position variance the momentum variance must become wider, so the Heisenberg uncertainty relation is still fulfilled. In the course of the time evolution the squeezed position wave packet will not retain its shape, but will become wider for half an oscillation period before it contracts back to the original width after a full period. The momentum wave packet contracts and expands accordingly so that at any time the uncertainty is minimal (Walls 1986; Walls and Milburn, 1995). The coefficients in expansion (44) for the so-called _squeezed vacuum state_ are 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

289 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [492 x 44] intentionally omitted <==**

The parameter � _s_ describes the squeezing of the state, namely, the position variance of the squeezed state is reduced at certain times by 

**==> picture [229 x 11] intentionally omitted <==**

where � _x_ 0 is the variance of the ground state. The ground state is recovered for � _s_ �1 (therefore the name ‘‘squeezed vacuum state’’). For � _s_ �1 the position wave function is narrower than that of the coherent state, while for 0�� _s_ �1 the momentum wave function has this property. The angle �describes the alignment of the squeezed state with respect to the position and momentum directions. This can best be visualized in phase space. The Wigner function of squeezed states has elliptical equicontour lines (Walls and Milburn, 1995). If one of the major axes of these ellipses is aligned with the position coordinate axis, � is equal to zero. The center of mass of the Wigner function of a squeezed vacuum state coincides with the origin of phase space. 

The probability distribution _P n_ for a squeezed vacuum state is independent of �and again restricted to the even states, 

**==> picture [229 x 28] intentionally omitted <==**

For strong squeezing this distribution has a tail that reaches to very high _n_ ; for example, with � _s_ �40, 16% of the population of the squeezed vacuum is in states above _n_ �20. 

Squeezed vacuum states, like coherent states, have a very compact operator representation. They are generated from the ground state by the operator 

**==> picture [229 x 26] intentionally omitted <==**

where �� _re[i]_[�] and _r_ is related to � _s_ by � _s_ � _e_[2] _[r]_ . 

## 4. Thermal distribution 

If the ion is in thermal equilibrium with an external reservoir at temperature _T_ the average weight of the excitation of the state � _n_ � will be proportional to the Boltzmann factor exp�� _n_ ��/( _kBT_ )�, where _k B_ is the Boltzmann constant. Of course it does not make sense to assign a temperature to a single realization of a cooled ion. However, if the ion is coupled to that reservoir and the number operator _N[ˆ]_ is measured many times (making sure that the ion reequilibrates after each measurement), one can extract a temperature from the average result _¯n_ from this ensemble of many different realizations according to 

**==> picture [229 x 40] intentionally omitted <==**

In considering an ensemble it is appropriate to characterize the state by a density matrix. Moreover, in the spirit of choosing the density matrix with the maximum ignorance (and therefore maximum entropy), the offdiagonal elements have to be zero. This makes it impossible to write the thermal distribution in the form of Eq. (44) that would correspond to a density matrix with nonzero off-diagonal elements for _T_ �0. So, even if the term ‘‘thermal state’’ is often used in the literature, ‘‘thermal distribution’’ seems to be a more appropriate reminder of the ensemble nature of this entity. 

After some minor algebra to normalize the trace of the states weighted by the Boltzmann factors, the density matrix may be written as 

**==> picture [229 x 27] intentionally omitted <==**

with level population probability 

**==> picture [229 x 25] intentionally omitted <==**

## III. TRAPPED TWO-LEVEL ATOMS COUPLED TO LIGHT FIELDS 

With the help of suitable electromagnetic fields the internal levels of trapped ions can be coherently coupled to each other and the external motional degrees of freedom of the ions. For strongly confined ions and a suitable tuning the coupling is formally equivalent to the Jaynes-Cummings Hamiltonian (Jaynes and Cummings, 1963). Consequently much of the work devoted to coherent interaction of trapped ions has been inspired by the important role this coupling plays in quantum optics. Beyond this special case there are many possibilities connected to the interchange of multiple motional quanta, in close analogy to multiphoton transitions in quantum optics. Moreover, the light field inducing the coupling can act as a source of energy, so that energy conservation implicit in atom-photon couplings does not have to be fulfilled in the interaction of internal states and the motion of trapped ions, allowing interactions in which both the internal state of the atom and its motion undergo a transition to a higher-energy level. Finally, if the full quantum-mechanical picture of the motion, including corrections due to micromotion, is considered, another class of transitions becomes possible that involves exchange of motional quanta at integer multiples 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

290 

Leibfried et al.: Quantum dynamics of single trapped ions 

of the rf driving field or combinations of integer multiples of the driving field and the secular motion (micromotion sidebands). 

## A. The two-level approximation 

In most of this review the internal electronic structure of the ion will be approximated by a two-level system with levels � _g_ � and � _e_ � of energy difference ����(� _e_ �� _g_ ). This is justified for real ions if the frequencies of the electromagnetic fields that induce the coupling are only close to resonance for two internal levels and if the Rabi frequencies describing the coupling strength are always much smaller than the detuning relative to offresonant transitions. Such a reduction is appropriate for most of the experimental situations described in this paper. 

this review. The generalized description of the coupling of internal states and motion follows the approaches of Cirac, Garay, _et al._ (1994) and Bardroff _et al._ (1996). 

It is also assumed that it is sufficient to treat the light field in the lowest order in its multipole expansion that yields a nonvanishing matrix element between the nearresonant electronic states in question. This assumption is justified by the fact that the extension of the electronic wave function is much less than the wavelength of the coupling field. For dipole allowed transitions the field will be treated in the familiar dipole approximation, while for dipole forbidden transitions only the quadrupole component of the field is considered. For Raman transitions, the near-resonant intermediate level will be adiabatically eliminated, making these transitions formally equivalent to the other transition types (see below). 

The corresponding two-level Hamiltonian _H[ˆ]_[(] _[e]_[)] is 

**==> picture [126 x 14] intentionally omitted <==**

**==> picture [210 x 55] intentionally omitted <==**

Since any operator connected to a two-level system can be mapped onto the spin-1/2 operator basis, _H[ˆ]_[(] _[e]_[)] and related operators can be conveniently expressed using the spin-1/2 algebra that is represented by _I[ˆ]_ , the 2�2 unity matrix, and the three Pauli matrices. In the particular case at hand the mapping is 

**==> picture [229 x 32] intentionally omitted <==**

**==> picture [182 x 13] intentionally omitted <==**

**==> picture [229 x 20] intentionally omitted <==**

where the energy is rescaled by ��(� _e_ �� _g_ )/2 to suppress the state-independent energy contribution in Eq. (58). 

## B. Theoretical description of the coupling 

To describe the interaction of the trapped atom with light fields in a simple but sufficient way, it is assumed, such as in the preceding section, that the motion of the atom bound in the trap is harmonic in all three dimensions. The descriptions presented below will include the explicit time dependence of the trapping potential, but in many cases it is sufficient to model the motion of the ion as a three-dimensional static potential harmonic oscillator, because the general theory introduces only very minor changes if the modulus of the dimensionless Paultrap parameters _a x_ and _q_ 2 _x_ related to the static and rf potential (see Sec. II.A) is much smaller than 1. This is true for the traps used in the experiments discussed in 

## 1. Total Hamiltonian and interaction Hamiltonian 

The total Hamiltonian _H[ˆ]_ of the systems considered here can be written as 

**==> picture [229 x 13] intentionally omitted <==**

where _H[ˆ]_[(] _[m]_[)] is the motional Hamiltonian along one trap axis, Eq. (18), as discussed in Sec. II. _H[ˆ]_[(] _[e]_[)] describes the internal electronic level structure of the ion (see Sec. III.A), and _H[ˆ]_[(] _[i]_[)] is the Hamiltonian of the interactions mediated by the applied light fields. 

As summarized in the Appendix, electric dipole allowed transitions, electric quadrupole allowed transitions, and stimulated Raman transitions can be described in a unified framework that associates a certain on-resonance Rabi frequency �, effective light frequency �, and effective wave vector _k_ with each of these transition types. The effective light frequencies and wave vectors are identical to the frequency and wave vector of the coupling light field for dipole and quadrupole transitions, but equal to the frequency difference ���1��2 and wave vector difference **k** � **k** 1� **k** 2 of the two light fields driving the stimulated Raman transitions. 

For running wave light fields all three transition types can be described by a coupling Hamiltonian of the form 

**==> picture [127 x 13] intentionally omitted <==**

**==> picture [201 x 13] intentionally omitted <==**

In the spin-1/2 algebra we can reexpress 

**==> picture [229 x 31] intentionally omitted <==**

For simplicity the discussion is again restricted to one dimension, and the effective wave vector **k** is chosen to lie along the _x_ axis of the trap. The generalization to more dimensions is straightforward. 

The simplest picture of the dynamics induced by the light field arises after transformation into the interaction 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

291 

Leibfried et al.: Quantum dynamics of single trapped ions 

picture with the free Hamiltonian _H[ˆ]_ 0� _H[ˆ]_[(] _[m]_[)] � _H[ˆ]_[(] _[e]_[)] and the interaction _V[ˆ]_ � _H[ˆ]_[(] _[i]_[)] . 

With _U[ˆ]_ 0�exp�� ( _i_ /�) _H[ˆ]_ 0 _t_ � the transformed interaction Hamiltonian is 

**==> picture [229 x 139] intentionally omitted <==**

Multiplying the time-dependent factors in the above expressions leads to exp�� _i_ (���0) _t_ �. Two terms are rapidly oscillating because � and �0 add up, while the two other terms oscillate with frequency �����0��0 . Since the contribution of the rapidly oscillating terms hardly affects the time evolution, they can be neglected. Doing so is called the _rotating-wave approximation_ for historical reasons. 

The transformation of the motional part of the Hamiltonion into the interaction picture is equivalent to a transformation of this part from the Schro[¨] dinger to the Heisenberg picture. The position operator _xˆ S_ will be replaced by its Heisenberg-picture version _xˆ_ ( _t_ ) as given in Eq. (29). Introducing the Lamb-Dicke parameter � � _kx_ 0 , where _x_ 0� ~~�~~ �/(2 _m_ �) is the extension along the _x_ axis of the ground-state wave function of the reference oscillator mentioned in Sec. II.B, yields 

dominant contribution in the time evolution of the trapped and illuminated ion will come from this term, while the others can be neglected in a second application of the rotating-wave approximation. For a given _l_ and _l_ � one would speak of a detuning to the _l_ th secular sideband of the _l_ �th micromotion sideband, a terminology coming from the classical picture of the ion vibrating in the trap’s well with secular and micromotion frequencies. In the frame of reference of the ion the monochromatic light field is therefore phase modulated at these two frequencies. For example, if one of the modulation sidebands coincides with the transition frequency �0 of the ion at rest, this sideband can induce internal state transitions. 

The exact general form of the resonant term can be calculated, in principle, by performing a polynomial expansion of the above expression, but this is unnecessary 2 for most practical cases since often ��1, (� _a x_ �, _q x_ )�1, so the coupling strength of higher orders in _l_ and _l_ � vanishes quickly. The coupling strength for some special cases will be calculated in Sec. III.B.2. In all experiments covered in this review only sidebands with _l_ ��0 were driven. Terms with � _l_ ���1 could then be neglected. Fur2 ther, it is assumed that (� _a x_ �, _q x_ )�1, so � _x_ �rf�� and _C_ 0�(1� _q x_ /2)[�][1] , as in Eq. (37). Then the interaction Hamiltonian simplifies to 

**==> picture [229 x 31] intentionally omitted <==**

with the scaled interaction strength � 0��/(1� _q x_ /2). This scaling reflects the reduction in coupling due to the wave packet’s breathing at the rf drive frequency. 

**==> picture [229 x 12] intentionally omitted <==**

and the interaction Hamiltonian in the rotating-wave approximation takes its final form as 

**==> picture [237 x 12] intentionally omitted <==**

**==> picture [209 x 11] intentionally omitted <==**

The time dependence of the exponent is governed by the frequency difference � and the time dependence of _u_ ( _t_ ). Recalling the form of the solution Eq. (22) and expanding part of the exponent in the Lamb-Dicke parameter 

exp„ _i_ ����� _aˆ u_ *� _t_ �� _aˆ_[†] _u_ � _t_ ���� _t_ �… 

**==> picture [230 x 66] intentionally omitted <==**

it is easily verified that anytime the detuning satisfies 

**==> picture [229 x 11] intentionally omitted <==**

with _l_ and _l_ � as integers and _l_ �0 if _l_ ��0, two of the terms in the Hamiltonian will be slowly varying. The 

## 2. Rabi frequencies 

Depending on the detuning �, the interaction Hamiltonian (69) will couple certain internal and motional states. If the exponent containing the ladder operators in Eq. (69) is expanded in � this will result in terms containing a combination of �� , with _l aˆ_ -operators and _m aˆ_[†] -operators rotating with a frequency of ( _l_ � _m_ )�� _s_ �. If �� _s_ � these combinations will be resonant, coupling the manifold of states � _g_ �� _n_ � with � _e_ �� _n_ � _s_ �. The coupling strength, often called the � _s_ �th blue (red) sideband Rabi frequency for _s_ �0 ( _s_ �0), is then (Cahill and Glauber, 1969; Wineland and Itano, 1979) 

**==> picture [229 x 48] intentionally omitted <==**

where _n_ � ( _n_ �) is the lesser (greater) of _n_ � _s_ and _n_ , and _L_ � _n_ ( _X_ ) is the generalized Laguerre polynomial 

**==> picture [229 x 26] intentionally omitted <==**

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

292 

Leibfried et al.: Quantum dynamics of single trapped ions 

## 3. Lamb-Dicke regime 

The interaction Hamiltonian [Eq. (69)] and the Rabi frequencies [Eq. (70)] are further simplified if the ion is confined to the Lamb-Dicke regime where the extension of the ion’s wave function is much smaller than 1/ _k_ . In this regime the inequality � ~~�~~ �( _a_ � _a_[†] )[2] ��1 must hold for all times. The exponent in Eq. (69) can then be expanded to the lowest order in �, 

**==> picture [229 x 31] intentionally omitted <==**

and will contain only three resonances. The first resonance for ��0 is called the _carrier resonance_ and has the form 

**==> picture [229 x 13] intentionally omitted <==**

This Hamiltonian will give rise to transitions of the type � _n_ �� _g_ � _↔_ � _n_ �� _e_ � with Rabi frequency � 0 . These transitions will not affect the motional state. 

The resonant part for ���� is called the _first red sideband_ and has the form 

**==> picture [229 x 12] intentionally omitted <==**

This Hamiltonian will give rise to transitions of the type � _n_ �� _g_ � _↔_ � _n_ �1�� _e_ � with Rabi frequency 

**==> picture [229 x 14] intentionally omitted <==**

that will entangle the motional state with the internal state of the ion. Indeed this Hamiltonian is formally equivalent to the Jaynes-Cummings Hamiltonian, the workhorse of quantum optics, and it is this analogy that inspired many workers originally coming from quantum optics to do investigations in the field of trapped ions. It is also responsible for the remarkable similarity of investigations done in cavity QED (Englert _et al._ , 1998; Varcoe _et al._ , 2000; Raimond _et al._ , 2001) to some of the experiments done in ion traps presented below. This interaction removes one quantum (phonon) of the secular motion while the ion goes to the excited state, similarly to the absorption of a light quantum in cavity QED. 

The counterpart of this interaction is the _first blue sideband_ , resonant for ����: 

**==> picture [229 x 12] intentionally omitted <==**

This Hamiltonian will give rise to transitions of the type � _n_ �� _g_ � _↔_ � _n_ �1�� _e_ � with Rabi frequency 

**==> picture [229 x 14] intentionally omitted <==**

It has no direct counterpart in the atom-photon realm because such a process would violate energy conservation and is sometimes called anti-James-Cummings coupling. Because of this interaction and the additional pos- 

sibility of driving higher-order sidebands (when � is not too small), trapped-ion experiments can yield inherently richer dynamics than cavity QED experiments. With suitable light pulses on the carrier, red and blue sidebands, a classical driving force to create coherent or squeezed states, and the ability to cool to the ground state, one can engineer and analyze a variety of states of motion as discussed in more detail in Sec. VI. 

By choosing larger detunings, �� _l_ � with � _l_ ��1, in principle, one can obtain a number of nonlinear couplings, for example, a ‘‘two-phonon’’ coupling, 

**==> picture [229 x 14] intentionally omitted <==**

for _l_ ��2. We note, however, that this interaction and those with � _l_ ��2 are not easy to realize in the laboratory since efficient ground-state cooling has been achieved only in the Lamb-Dicke regime. There the coupling strength will be significantly reduced compared to carrier and first sidebands, because ��1. 

## 4. Resolved sidebands 

So far we have assumed that the two internal levels of the ions have an infinite lifetime, leading to arbitrarily narrow carrier and sideband resonances. In practice this is only approximately true.[2] If the frequency of a sufficiently stable laser beam has intensity such that �� _n_ , _m_ � �� for all _n_ , _m_ it is possible to observe well-resolved carrier and sideband resonances. For a detuning �� _l_ � ��� with ���� the ion’s dynamics is governed by the few resonant terms in Eq. (69) to which the laser happens to be tuned. This allows for clean manipulation of the internal and motional states and also for cooling to the ground state, as will be described in Sec. IV.B. If we neglect dissipative terms, the time evolution of the general state 

**==> picture [229 x 27] intentionally omitted <==**

is governed by the Schro[¨] dinger equation 

**==> picture [229 x 12] intentionally omitted <==**

which is equivalent to the set of coupled equations 

**==> picture [229 x 14] intentionally omitted <==**

**==> picture [229 x 15] intentionally omitted <==**

This set of equations may be solved by the method of Laplace transforms, yielding the solution 

**==> picture [229 x 27] intentionally omitted <==**

with 

> 2For example, for quadrupole transitions with a lifetime on the order of 1 s, linewidths would be limited to about 1 Hz. 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

293 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [492 x 59] intentionally omitted <==**

ized form of sinusoidial Rabi flopping between the statesand _f nl_ � ~~�~~ ��[2] �� _n_ 2 � _l_ , _n_ . The solution describes a general� _n_ , _g_ � and � _e_ , _n_ � _l_ � and is essential for the quantum-state preparation and analysis experiments described later. 

## 5. Unresolved sidebands 

Allowed optical electric dipole transitions for ions have a linewidth of around several tens of MHz, typically beyond the highest secular motional frequencies observed in ion traps. In this case spontaneous emission cannot be neglected when considering the dynamics of the internal and motional states of an ion driven by the light field. Spontaneous emission will have two consequences: the coherent evolution of the internal two-level system is interrupted, and the recoil of the emitted photon leads to randomized momentum kicks in the external motion. 

A convenient picture of the dynamics is provided by the _master-equation formalism_ (Walls and Milburn, 1995; Schleich, 2001). The trapped ion is modeled as being coupled to a zero-temperature reservoir of optical modes in the vacuum state. This is a fair assumption since the average occupation number of optical modes at room temperature is extremely small. The master equation is an equation of motion for the reduced density matrix � that describes the time evolution of the internal and motional states of the ion only, the reduction of the total problem brought about by tracing over the many degrees of freedom of the environment or reservoir modes. The exact derivation is very technical, so the reader is referred to Stenholm (1986) and Cirac _et al._ (1992) for details. In brief, the reservoir modes are assumed to be coupled to the ion by an interaction of the Jaynes-Cummings form, 

**==> picture [229 x 18] intentionally omitted <==**

where _aˆ l_ , _g l_ ( _x_ ), and � _l_ are the destruction operator, position-dependent coupling strength, and detuning of the _l_ th reservoir mode, respectively. If we expand the equation of motion for � to second order in this reservoir interaction and assume the reservoir modes that are resonant with the two-level atom to be in zerotemperature distributions, we arrive at the master equation 

**==> picture [229 x 23] intentionally omitted <==**

Damping by spontaneous emission is contained in the Liouvillain 

**==> picture [229 x 23] intentionally omitted <==**

where � is the spontaneous emission rate. To account for the recoil of spontaneously emitted photons the first term of the Liouvillian contains 

**==> picture [229 x 24] intentionally omitted <==**

with �( _z_ )�3(1� _z_[2] )/4 the angular distribution pattern of spontaneous emission for a dipole transition. 

In most cases of interest the master equation has been solved numerically, often assuming the Lamb-Dicke limit as an additional restriction. One example of this work will be discussed in the context of laser cooling of a trapped ion. 

## 6. Spectrum of resonance 

The master equation (86) can also be used to derive a formal expression of the light emitted by a trapped ion in the Lamb-Dicke limit. Lindberg (1986) has studied the spectrum of light emitted by a harmonically trapped two-level atom and its interaction with a traveling-wave laser field. Later, Cirac, Parkins, _et al._ (1993) derived general relations applicable to multilevel systems, general trapping potentials, and traveling-wave and standing-wave configurations. The expressions for the motional sidebands appearing in the spectrum can be written in terms of correlation functions of internal operators and of steady-state expectation values of external operators. The internal operators can be evaluated with the optical Bloch equations for an atom at rest, while the external operators are derived from the applied trapping forces using the formalism introduced by Cirac _et al._ (1992). 

Specifically, for a single harmonically trapped ion in a traveling-wave field configuration, and for the lowintensity limit at which � 0��, one obtains for the motional sidebands the following spectral contributions: 

**==> picture [229 x 129] intentionally omitted <==**

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

294 

Leibfried et al.: Quantum dynamics of single trapped ions 

Here, �(�), � 0 , and � denote the angular distribution for the dipole radiation, the Rabi frequency, and the motional frequency, respectively. The width �ms of the motional sidebands is given by 

**==> picture [230 x 28] intentionally omitted <==**

and the final (steady-state) excitation energy is 

**==> picture [229 x 25] intentionally omitted <==**

with 

**==> picture [229 x 22] intentionally omitted <==**

and ��2/5 for a dipole transition and the spontaneous decay rate ���/2. 

Thus, aside from the coherent peak, the spectrum of resonance fluorescence consists of two Lorentzian functions centered at ���� with different heights which depend on the observation angle �. The width of the motional sidebands is given by half the cooling rate, which in the Lamb-Dicke limit is narrower than � 0�� by a factor of the order �[2] �1 (Lindberg, 1986). The asymmetry of the motional sidebands reflects the population of the trap levels � _n_ � and thus mirrors the ion’s residual excitation energy in the trap potential. 

For large intensities and on resonance the spectrum exhibits ac Stark splitting with a center line at the laser frequency, two symmetric sidebands at the Rabi frequency � 0 , and width proportional to � (the Mollow triplet; Mollow, 1969). The ion motion then leads to additional (narrow) sidebands such as in the low intensity case. 

For an ion in a standing-wave field configuration, expressions similar to Eq. (89) are found with an explicit dependence on the ion position with respect to the standing-wave phase. For details we refer the reader to the work by Cirac _et al._ (1992). 

## C. Detection of internal states 

The ions used in the experiments described here can be detected by laser-induced fluorescence on an electric dipole allowed transition, usually identical to the transition used for Doppler cooling. On such a transition a single ion can scatter several millions of photons per second and a sufficient fraction may be detected even with detectors covering a small solid angle and having 5–20 % quantum efficiencies. The fluorescence is either detected in a spatially resolved manner on chargecoupled-device (CCD) cameras or imager tubes, or on photomultipliers. Cameras and imager tubes have been used in a number of experiments to provide pictures of ion clouds and crystals (see, for example, Diedrich _et al._ , 1987; Wineland _et al._ , 1987; Drewsen _et al._ , 1998; Mitchell _et al._ , 1998; Na[¨] gerl _et al._ , 1998). Since the spatial extension of a cold ion’s wave function is typically smaller than the wavelength of the fluorescence light, single ions 

**==> picture [145 x 81] intentionally omitted <==**

FIG. 4. V-type three-level system for electron shelving. In addition to transitions � _g_ � _↔_ � _e_ �, transitions to a third level � _r_ � can be independently driven by laser fields. The lifetimes of � _g_ � and � _e_ � are usually much longer than that of � _r_ �. 

in a crystal show up as bright dots with a size determined by the resolution limit of the imaging optics, that is, around 1 �m with a good imaging lens. 

Photomultipliers usually do not offer spatial information directly, but rather pick up the collected fluorescence with better quantum efficiency than CCD cameras or imagers. With a total detection efficiency of 10[�][3] (including solid angle and quantum efficiency) of the fluorescence rate, even a single ion will lead to about 50 000 counts/s on a dipole allowed transition with a 10-ns upper state lifetime. 

This signal can be used not only to detect the ion itself, but also to distinguish between internal states of the ion with extremely high detection efficiency. This technique was suggested by Dehmelt (1975) as a tool for spectroscopy and was dubbed _electron shelving_ because the ion’s outer electron can be ‘‘shelved’’ into a state in which it does not 

## 1. The electron shelving method 

Electron shelving makes use of an internal level structure that is well described by a V-type three-level system. In addition to � _g_ � and � _e_ � there is a third level � _r_ �, and it is assumed that the transitions � _g_ � _↔_ � _e_ � and � _g_ � _↔_ � _r_ � can be independently driven by laser fields (see Fig. 4). If the lifetimes of � _g_ � and � _e_ � are much longer than that of � _r_ � the transition � _g_ � _↔_ � _r_ � may be strongly driven, resulting in many scattered photons if the ion is projected into � _g_ � by the first scattering event. On the other hand, if no photons are scattered, the ion was projected into state � _e_ � by the interaction with the driving 

Depending on the background light scattered into the photomultiplier and its dark count rate, � _g_ � and � _e_ � can be distinguished with high confidence in rather short detection periods (typically on the order of a few tens of �s). Apart from this convenient way of measuring the quantum state, Dehmelt’s proposal triggered a number of theoretical papers on ‘‘quantum jumps’’ between � _g_ � and � _e_ � that would manifest themselves by extended periods of time with few or many photons detected, respectively, if both transitions are driven simultaneously. The fact that one describes the behavior in the time of a 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

295 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [301 x 231] intentionally omitted <==**

FIG. 5. Quantum jumps of a single 138Ba� ion. If the ion makes the transition to � _e_ �� _D_ 5/2 , the fluorescence drops. After a mean time equal to the excited-state lifetime (ca. 32 s in this example), a spontaneous transition returns the ion to � _g_ �� _S_ 1/2 and the fluorescence on the � _g_ � _↔_ � _r_ �� _P_ 1/2 transition returns to a higher level. 

single atom, undergoing random transitions,[3] rendered the usual density-matrix approach inadequate, because it yields only ensemble averages, not individual trajectories. A number of different correlation functions were finally used by different workers to attack these problems. They are all related to _g_[(2)] (�), the probability of detecting another photon, originating from the � _r_ � _→_ � _g_ � spontaneous emission, at time _t_ ��, if one was detected at _t_ �0. A review of both theoretical and experimental work on this problem is presented by Blatt and Zoller (1988). 

## 2. Experimental observations of quantum jumps 

Experimental observations of quantum jumps of single trapped ions were first reported at about the same time in three different laboratories (Bergquist _et al._ , 1986; Nagourney _et al._ , 1986; Sauter _et al._ , 1986). 

In all three experiments the � _g_ � _↔_ � _r_ � transition was a dipole allowed transition also used for Doppler cooling, while the weak transition was a dipole forbidden quadrupole transition that was excited by an incoherent hollow cathode lamp (Nagourney _et al._ , 1986), was far offresonance scattering and collisional excitation (Sauter _et al._ , 1986), or was excited by a coherent laser source (Bergquist _et al._ , 1986). Indeed the observed fluorescence showed the random intensity jumps (see Fig. 5) and all statistical properties to be in accord with theoretical predictions (see Blatt and Zoller, 1988, and references therein). 

## D. Detection of motional-state populations 

A finite Lamb-Dicke parameter � implies that � _g_ � _↔_ � _e_ � transitions depend on the motional state of the 

> 3Indeed it was proposed to use the length of light and dark periods for the generation of perfect random numbers (Erber and Puttermann, 1985). 

ion [see Eqs. (83) and (84)]. In general the internal state may get entangled with the motional state for interactions on the carrier or any sideband. The dependence can also be used to map the motional state of the ion onto the internal state, which can subsequently be measured with high efficiency as described above. This mapping is straightforward in the resolved sideband regime, where dissipation plays no role. 

Practically, since ��1 and the ions are in the LambDicke regime, the most interesting transitions are the first red and blue sidebands, since their coupling to lowest order is linear in � [see Eq. (70)]. The first blue sideband proved to be very useful in characterizing the number-state distribution of various states of motion. By resonantly driving an ion in the starting state 

**==> picture [229 x 26] intentionally omitted <==**

on the blue sideband for various times _t_ and measuring the probability _P g_ ( _t_ )���( _t_ )�(� _g_ �� _g_ � � _I[ˆ] m_ )��( _t_ )� to find the ion in the ground state after the interaction, where _I[ˆ] m_ is the identity operator in the motional-state space, one obtains the following signal, which can be easily derived from Eq. (83) for the case _l_ ��1: 

**==> picture [229 x 29] intentionally omitted <==**

Here _P n_ �� _c n_ �[2] is the probability of finding the atom in the _n_ th motional number state. As long as � _n_ , _n_ �1 are distinct frequencies, the occupation of all number states _P n_ can be found by Fourier transforming the signal equation (95). The Rabi frequencies � _n_ , _n_ �1 are distinct inside the Lamb-Dicke regime, where the blue sideband frequencies scale as ~~�~~ _n_ �1 to lowest order in � [see Eqs. (70) and (76)]. Outside this regime the frequencies will not rise monotonically as a function of _n_ , so distinguishing them is more complicated. 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

296 

Leibfried et al.: Quantum dynamics of single trapped ions 

The _P n_ correspond to the diagonal elements of the density matrix � _nm_ of the motional state. One can also extend the method described above, using additional manipulations of the motional state, to yield the offdiagonal elements of � _nm_ and characterize the complete quantum state of motion. Theoretical methods and experimental implementation of two such methods will be described in Sec. VI.B. 

## IV. LASER COOLING OF IONS 

The general goal of cooling is to reduce the kinetic energy of an ion after it was loaded into the trap, ideally to a point at which the ion is in the ground state of the trapping potential with very high probability. Ion traps typically confine ions up to a temperature that corresponds to about one-tenth of their well depth, about 1 eV or 10 000 K. Cooling from these starting temperatures requires a high scattering rate of the cooling light, so it is advantageous to use a dipole transition to a fairly short-lived upper level for this stage. For most traps and ions commonly used the first cooling stage will therefore occur in the unresolved sideband regime, since the lifetime of the upper state is considerably shorter than one period of oscillation in the trap. In this case, cooling in a trap or cooling free atoms is essentially the same (Wineland and Itano, 1979). For example, the limiting kinetic energy under this type of cooling turns out to be the same as the limit of Doppler cooling for free atoms. 

To reach the motional ground state with high probability a second stage of cooling is necessary, typically with a lower scattering rate, but now in the resolvedsideband regime. For cooling to the ground state, three different methods have been used to date, namely, cooling on a dipole forbidden quadrupole transition, cooling by stimulated Raman transitions, and cooling utilizing electromagnetically induced transparency (EIT cooling). All these methods will be briefly discussed in this section. For a more comprehensive treatment the reader is referred to the literature cited below and a review of cooling techniques in ion traps by Itano _et al._ (1992). 

## A. Doppler cooling 

Cooling in a trap was examined in conjunction with the first Doppler cooling experiments (Neuhauser _et al._ , 1978; Wineland _et al._ , 1978; Wineland and Itano, 1979; Itano and Wineland, 1981). A semiclassical picture based on the master equation was developed by Stenholm and co-workers, as reviewed by Stenholm (1986). In these treatments a purely harmonic secular motion with no micromotion of the ion was assumed. This was somewhat unsatisfactory from the point of view of experiments in which additional cooling and heating effects related to micromotion were observed (Blu[¨] mel _et al._ , 1989; DeVoe _et al._ , 1989). Finally, the most complete picture of cooling to date, including micromotion, was derived by Cirac, Garay, _et al._ (1994). We first present a very simple, more qualitative picture of Dop- 

pler cooling, before introducing the basic building blocks and results of the general approach, including micromotion. 

In the simple picture micromotion is neglected and the trapping potential is approximated by the timeindependent pseudopotential 

**==> picture [229 x 23] intentionally omitted <==**

This description applies to axial motion in a linear trap [see Eq. (4)], where micromotion is absent. If the motion of the trapped ion is taken to be classical, its velocity obeys 

**==> picture [229 x 11] intentionally omitted <==**

If the radiative decay time is much shorter than one oscillation period, ���, one cycle of absorption and spontaneous emission occur in a time span in which the ion does not appreciably change its velocity. In this case the averaged radiation pressure can be modeled as a continuous force that depends on the ion’s velocity. If the cooling laser field is a single traveling wave along the ion’s direction of motion, every absorption will give the ion a momentum kick � _p_ �� _k_ in the wave-vector direction of the light field, while the emission will generally be symmetric about some point. Emission will then lead to zero-momentum transfer on average, but to a random walk in momentum space, similar to Brownian motion. The rate of absorption-emission cycles is given by the decay rate � times the probability of being in the excited state � _ee_ �� _e_ �� _ˆ_ � _e_ �. Therefore the average force is 

**==> picture [228 x 28] intentionally omitted <==**

and the excited-state probability is given by (Loudon, 1973) 

**==> picture [229 x 25] intentionally omitted <==**

where _s_ �2���[2] /�[2] is the saturation parameter proportional to the square of the on-resonance Rabi frequency �. The detuning is composed of the detuning ��� ��0 of the light wave with respect to the resonance frequency of the atom at rest and the Doppler shift: �eff��� **k** • **v** . For small velocities, close to the final temperature reached by laser cooling, where the Doppler broadening is small compared to �, _F a_ can be linearized in _v_ : 

**==> picture [229 x 11] intentionally omitted <==**

with 

**==> picture [229 x 24] intentionally omitted <==**

the averaged radiation pressure that displaces the ion slightly from the trap center and 

**==> picture [229 x 27] intentionally omitted <==**

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

297 

Leibfried et al.: Quantum dynamics of single trapped ions 

reached for a laser detuning ��� ~~�~~ 1� _s_ /2. 

the ‘‘friction coefficient’’ of the cooling force that will provide viscous drag if � is negative. The cooling rate, averaged over many oscillation periods, is then 

The simple picture presented so far provides some insight into the cooling mechanism but neglects several aspects of cooling in rf traps that can be important in practice. In many experiments using Doppler cooling, sidebands due to micromotion are observed in fluorescence spectra. Especially when the rf drive frequency is comparable to or larger than the natural linewidth of the cooling transition, one might wonder what effects this has on the cooling process. 

**==> picture [229 x 13] intentionally omitted <==**

since � _v_ ��0 for a trapped particle. Thus, without taking the random nature of the light-scattering events into account, the ion would cool to zero energy. In practice this cannot happen since even if the ion has zero velocity it will continue to absorb and emit photons. The emission rate for _v_ �0 is �� _ee_ ( _v_ �0), with the recoil taking directions dictated by the emission pattern of the transition used (typically an electric dipole transition). Since the emission pattern is symmetric the average momentum change is �� **p** ��0, but the momentum undergoes diffusion, �� _p_[2] ��0. As usual in random-walk processes the average distance covered by the diffusion is proportional to the square root of the number of recoil kicks or, in other words, the second moment of the distribution of random processes is proportional to the number _N_ of recoils: �� _p_[2] ��(� _k_ )[2] _N_ . Not only the emission, but also the random times of absorption of photons lead to momentum kicks, but this time only along the axis defined by the wave vector of the cooling beam. This still gives rise to diffusion due to the discreteness of the absorption processes. Again the diffusion will be proportional to the square root of the number of absorptions. Furthermore, unless the cooling transition is driven weakly, _s_ �1, absorption and emission will be correlated, leading to an altered diffusion. While all these effects are included in the more general approach discussed later and also discussed in the literature (Lindberg, 1984; Stenholm, 1986, and references therein), this correlation will be neglected for the simple picture here. The momentum kicks due to absorption and emission will then have the same rate but different directionality. This can be taken into account by scaling the emission term with a geometry factor � that reflects the average component of the emission recoil kick along the _x_ axis and takes the value ��2/5 for dipole radiation (Stenholm, 1986). For the final stage of cooling _v_ will be close to zero, so the heating rate is approximately 

For example, when including micromotion, the kinetic energy of the trapped particle has to be reconsidered. The forced oscillations at the rf drive frequency �rf add kinetic energy in excess of the energy in the secular motion. However, for the cooling dynamics, which evolve on a much slower time scale than this fast oscillation, it is appropriate to look at the kinetic energy averaged over one period 2�/�rf of the micromotion (denoted by the overbar): 

**==> picture [229 x 25] intentionally omitted <==**

The process of cooling can then be defined as an approach to minimizing this quantity. 

For Doppler cooling, the spatial extension of the final motional state is usually small compared to the cooling light wavelength, so it is appropriate to limit a study of cooling dynamics to the Lamb-Dicke regime. It is also 2 assumed that the trap operates in the (� _a x_ �, _q x_ )�1 regime of micromotion. Assuming that the cooling light is a traveling wave and following Cirac, Garay, _et al._ (1994), one may expand the interaction Hamiltonian (66) to first order in � (since the time origin for cooling is unimportant, the phase � is irrelevant and set to zero in the following): 

**==> picture [209 x 86] intentionally omitted <==**

**==> picture [492 x 70] intentionally omitted <==**

The interpretation is straightforward. The first term represents the strong carrier excitation with Rabi frequency �, while the other terms represent pairs of combined secular and micromotion sideband excitations at detunings �(�� _n_ �rf) ( _n_ �0,�1,�2, . . . ) with weaker Rabi frequencies ��� _C_ 2 _n_ �. For the assumed conditions the magnitude � _C_ 2 _n_ � rapidly drops with increasing � _n_ �. If all sidebands are resolved, ��rf�����, one may choose the detuning in such a way that only one term in Eq. (108) is resonant. This case will be described in the next section. In the case in which ���rf ,�, the dynamics are more involved and for quantitative insight the master equation connected to Hamiltonian (108) has to be solved. 

**==> picture [24 x 11] intentionally omitted <==**

Equilibrium will be reached if heating and cooling proceed at an equal rate, so one can infer the final temperature from equating Eqs. (103) and (104): 

**==> picture [229 x 27] intentionally omitted <==**

with _k B_ the Boltzmann constant. For this simple model, which neglects the correlation between absorption and emission, the minimum temperature will be 

**==> picture [229 x 27] intentionally omitted <==**

The sidebands and their relative strength are sketched in Fig. 6. The extra sidebands lead to additional channels 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

298 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [301 x 189] intentionally omitted <==**

FIG. 6. Spectrum of the secular and micromotion sidebands involved in the cooling process. The height of the bars represents the coupling strength. 

of absorption and emission. Absorption on the red secular sidebands will lead to a decrease in kinetic energy, while absorption on the blue secular sidebands will lead to an increase. Note that all sidebands at _n_ �rf�� will lead to heating even if _n_ �0. This means that although the laser might be red detuned from the resonance of the atom at rest (carrier), the ion can be heated, especially if the excess micromotion due to unwanted static potentials in the trap is not compensated (Blu[¨] mel _et al._ , 1989; DeVoe _et al._ , 1989; Berkeland _et al._ , 1998; Peik _et al._ , 1999). For good compensation the coupling strength quickly drops with � _n_ � and the effect of these extra resonances is not very dramatic. The ‘‘simple’’ Doppler limit stated in connection with Eq. (106) might not be reached in all experiments due to these additional heating contributions, but it still is a good rule of thumb. 

In the NIST[9] Be[�] experiments the rf drive frequency was quite high, �rf /(2�)�230 MHz, compared to a 20MHz natural linewidth of the _S_ 1/2 _→P_ 3/2 transition. The cooling laser was detuned by about half a linewidth, so in this experiment micromotion sidebands did not play a role. Indeed, at a trap frequency of 11.2 MHz, a Doppler withcoolingthelimittheoreticalof _¯n_ exp�limit0.47(5)of _¯n_ was �0.484reached,(Monroeconsistent _et al._ , 1995). 

## B. Resolved-sideband cooling 

In a regime where the effective linewidth due to decay from the excited state with rate _[˜]_ � is lower than the motional frequency �, the individual motional sidebands become resolved.[4] One can then tune the cooling laser to the first red sideband and cool the ion close to the motional ground state if no heating mechanisms other than the recoils of the cooling transition are present. 

> 4The effective rate � _˜_ can be modified to be different from the spontaneous decay rate of the excited state � nat ; see, for example, Eq. (116) below. 

To reach this regime on a dipole allowed transition one can use either a very stiff trap with high motional frequencies or a weakly allowed dipole transition. Both approaches have been pursued (Jefferts _et al._ , 1995; Peik _et al._ , 1999), but so far cooling to the ground state in the sense that the state � _g_ , _n_ �0� is produced with high probability has involved either dipole forbidden transitions or Raman transitions. 

## 1. Theory 

The cooling process in the resolved-sideband limit has previously been described (Neuhauser _et al._ , 1978; Wineland and Itano, 1979; Stenholm, 1986; Cirac _et al._ , 1992; Cirac, Garay, _et al._ , 1994). The essential physics can be understood with a simple model. To avoid unwanted motional-state diffusion due to transitions of high order in � it is very advantageous to start resolved-sideband cooling inside the Lamb-Dicke regime. In fact all successful experiments on ground-state cooling have featured an initial Doppler cooling stage that achieved the Lamb-Dicke regime. For a typical linewidth of several tens of MHz on the Doppler cooling transition a sufficiently high motional frequency greater than about 1 MHz is necessary. 

In the Lamb-Dicke regime and with no other heating mechanisms present, the cooling laser is detuned to � ���, the first red sideband. To first order in �, Eq. (108) is reduced to the resonant red sideband ( _n_ �0, since the micromotion sidebands are far off resonance and can be neglected), the carrier detuned by �, and the blue sideband detuned by 2�: 

**==> picture [229 x 32] intentionally omitted <==**

One way to find the final motional state would be to insert this interaction Hamiltonian into the master equation (86) and solve it numerically, as was done by Cirac, Garay, _et al._ (1994), but since every cooling cycle involves spontaneous emission, coherences never play a strong role and the problem can be approximately 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

299 

Leibfried et al.: Quantum dynamics of single trapped ions 

solved with rate equations. Every cooling cycle (absorption followed by spontaneous emission) involves a transition from the ground state � _g_ � to the excited state � _e_ � on the red sideband and a subsequent decay on the carrier (in the Lamb-Dicke regime the ion will predominantly decay on the carrier; therefore other decay channels can be neglected to lowest order in �). The cooling rate is then given by the product of the excited-state occupation probability _p e_ ( _n_ ) of a motional state � _n_ � and its decay rate _[˜]_ �. As in Eq. (99) a Lorentzian line shape is assumed for this excitation, but now with detuning ��: 

**==> picture [229 x 34] intentionally omitted <==**

This rate depends on _n_ and vanishes once the ground state is reached. The ground state is therefore a dark state of the red sideband excitation and the ion would be pumped into that state and reside there without any competing mechanisms. In the absence of any other heating sources the dominant channel out of the ground state is off-resonant excitation of the carrier and the first blue sideband. Actually both these processes contribute to the heating on the same order. The carrier is excited with a probability of ��/(2�)�[2] [see Eq. (99) with _[˜]_ � ��,���eff��] but will mostly decay back on the carrier transition. Decay on the blue sideband after carrier excitation that leads to heating only occurs with a rate of ��/(2�)�[2] � _˜_[2] _[˜]_ �. Note that the Lamb-Dicke factor � _˜_ for this decay is not equal to the one of the excitation, because the emitted photon can go in any direction, not only along the wave vector of the cooling beam, and some experimental arrangements use a three-level system in which the emitted photon does not have the same wavelength as the cooling light (see below). The second dominant heating process is excitation on the first blue sideband with probability ���/�2(2�)��[2] (see above, but now �eff�2�) followed by decay on the carrier with a rate of ���/�2(2�)��[2] _[˜]_ �. For the final stage of the cooling the problem may be restricted to the ground state and the first excited state with rate equations 

**==> picture [229 x 31] intentionally omitted <==**

_p˙_ 1�� _p˙_ 0 

for the probabilities _p_ 0 , _p_ 1 to be in the respective states. In the steady state, _p˙ i_ �0, _p_ 1�1� _p_ 0 , this yields 

**==> picture [229 x 30] intentionally omitted <==**

The factor in square brackets is of order one and � � _[˜]_ �, so the particle is cooled to the ground state with probability _p_ 0�1�� _[˜]_ �/(2�)�[2] very close to one. 

Several methods have been used in experiments to determine the final mean excitation number _¯n_ after resolved-sideband cooling. This review will be restricted 

to the simplest and most robust method used so far, the comparison of the probability _P e_ ( _t_ ) to end up in the excited electronic state � _e_ � after excitation of the ion on the red and blue sidebands. From Eq. (95) for the first blue sideband and the analogous expression for the red sideband [derived from Eq. (83) for _l_ ��1], using _P e_ ( _t_ )�1� _P g_ ( _t_ ) and the assumption that the final motional states after cooling have a thermal distribution (see Sec. II.C.4), one gets 

**==> picture [229 x 95] intentionally omitted <==**

using � _m_ �1, _m_ �� _m_ , _m_ �1 . This means that the ratio of these probabilities is 

**==> picture [229 x 29] intentionally omitted <==**

independent of drive time _t_ , carrier Rabi frequency �, or Lamb-Dicke parameter � (Turchette, Kielpinski, _et al._ , 2000). The ratio _R_ can be inferred from a frequency scan over both sidebands while keeping the light intensity and excitation time constant and will directly yield the mean occupation 

**==> picture [229 x 22] intentionally omitted <==**

of the thermal motional state. 

## 2. Experimental results 

Several groups have reported experiments that cool up to four ions close to the ground state. The first report of ground-state cooling was by the Boulder group, cooling[198] Hg[�] on a quadrupole allowed transition. The trap was adjusted to be nearly spherical, with a secular frequency of 2.96 MHz using an appropriate positive dc bias on the ring electrode. After 20 ms of Doppler cool2 2 ing on the strong _S_ 1/2 _→ P_ 1/2 transition this laser was shut off and another laser on the[2] _S_ 1/2 _→_[2] _D_ 5/2 first red sideband transition was turned on for 200–500 ms. Since the natural lifetime of the 2 _D_ 5/2�� _e_ � state limits the scatter rate to about (1/2)� nat�6 photons/s, the upper level was intentionally broadened by coupling it to the short-lived 2 _P_ 3/2�� _aux_ � level with an additional laser source (repumper). This effectively broadens the linewidth to (Marzoli _et al._ , 1994) 

**==> picture [229 x 28] intentionally omitted <==**

if the Rabi frequency on the � _e_ � _→_ � _aux_ � transition is � aux and the auxiliary laser is detuned from resonance by � aux . The choice of this Rabi frequency and detuning will determine the effective linewidth _[˜]_ � and in turn the 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

300 

Leibfried et al.: Quantum dynamics of single trapped ions 

cooling rate and final thermal distribution. After shutting off the sideband cooling laser, the repumper was left on for another 5 ms to ensure that the ion returned to the ground state � _g_ �. Following the cooling cycle another laser pulse with roughly saturation intensity was 2 swept over the red and blue sidebands of the _S_ 1/2 _→_[2] _D_ 5/2 transition to record the excitation probability on the sidebands. The probability was found with the electron shelving method by observing the[2] _S_ 1/2 _↔_[2] _P_ 1/2 fluorescence (see Sec. III.C) and averaging over about 40 sweeps consisting of one measurement for each frequency setting. From the strength of the sidebands the final mean occupation number of the motional state was determined as outlined in Sec. IV.B.1 to be _¯n_ �0.05 �0.012. In this experiment the final temperature could be determined in only two dimensions. 

Ground-state cooling in all three dimensions was first achieved by the NIST group (Monroe _et al._ , 1995). The trap used in this experiment had motional frequencies of (� _x_ ,� _y_ ,� _z_ )�2�(11.2,18.2,29.8) MHz. The 9Be� ion was first Doppler cooled well into the Lamb-Dicke regime in all three dimensions on the[2] _S_ 1/2 _→_[2] _P_ 3/2 transition. After Doppler cooling alone the motional states had ( _¯n x_ , _¯n y_ , _¯n z_ )�(0.47,0.30,0.18), measured with the sideband ratio method outlined above. Then a total of 15 cycles of interspersed resolved-sideband cooling pulses (order _xyz xyz_ . . . ) were applied, five cycles in each of the three directions. Each cycle consisted of a pulse on the red sideband of the stimulated Raman transition from the ([2] _S_ 1/2 , _F_ �2, _m F_ ��2)�� _g_ � to the ([2] _S_ 1/2 , _F_ �1, _m F_ ��1)�� _e_ � state using the[2] _P_ 1/2 state as a virtual intermediate state [see also the Appendix, Eq. (A3)]. The pulse time was adjusted to make a � pulse on the � _g_ �� _n_ �1� _→_ � _e_ �� _n_ �0� transition, typically taking 1–3 �s. Following this a resonant � _e_ � _→_[2] _P_ 3/2�[�] repump pulse of about 7-�s length optically pumped the ion to � _g_ � via the[2] _P_ 3/2 level. After the complete set of cooling pulses a probe pulse interrogated the transition probability to � _e_ �. Cooling and probe pulses made up one experiment, typically repeated 1000 times with the same settings. The probe pulse was swept over all six red and blue sidebands, thus mapping out all relevant transition probabilities. From the ratio of corresponding sidebands the final average motional quantum numbers were inferred to be ( _¯n x_ , _¯n y_ , _¯n z_ )�(0.033,0.022,0.029). 

Peik _et al._ (1999) report cooling a single[115] In[�] ion to _¯n_ �0.7(3) corresponding to 58% ground-state occupation. The cooling transition was the weakly allowed[1] 5 _s_[2] _S_ 0 _→_ 5 _s_ 5 _p_[3] _P_ 1 intercombination line with an experimentally observed linewidth of ��(2�)650 kHz. The trap frequency � was about (2�)1 MHz. 

At the University of Innsbruck, ground-state cooling was achieved on a single[40] Ca[�] ion for various motional frequencies from ��(2�)2 MHz up to 4 MHz (Roos _et al._ , 1999). The method used was very similar to the experiment in[198] Hg[�] . The cooling transition was the well-resolved red sideband on the � _g_ �� _S_ 1/2( _m_ ��1/2) _→_ � _e_ �� _D_ 5/2( _m_ ��5/2) quadrupole transition. The 1.045 s lifetime of the upper level was shortened by an additional laser that coupled � _e_ � to the quickly decaying _P_ 3/2 

**==> picture [241 x 145] intentionally omitted <==**

FIG. 7. Sideband absorption spectrum on the _S_ 1/2 _→D_ 5/2 transition of a single calcium ion (Roos _et al._ , 1999) in a trap with 4.51-MHz motional frequency along the cooled axis: �, after Doppler cooling; �, after resolved-sideband cooling; (a) red sideband; (b) blue sideband. Each data point represents 400 experiments. 

level. The most efficient cooling occurred when the red sideband Rabi frequency � 1,0 on the quadrupole transition was roughly equal to the effective linewidth _[˜]_ � [see Eq. (116)]. 

The ion was Doppler cooled into the Lamb-Dicke regime with a 2.6-ms pulse of light on the _S_ 1/2 _→P_ 1/2 transition. A second laser resonant with the _D_ 3/2 _→P_ 1/2 transition prevented optical pumping to the metastable _D_ 3/2 level. A short pulse of �[�] polarized light on the _S_ 1/2 _→P_ 1/2 transition optically pumped the ion to � _g_ �. Following this the two lasers for sideband cooling were switched on for varying times between 3 and 7 ms. Another �[�] pulse ensured that the ion was prepared in � _g_ � after the cooling, counteracting the possibility of the ion’s being pumped into the _S_ 1/2( _m_ ��1/2) state by the cooling. For the polarizations and branching ratios present in the experiment this would happen on average after about 90 (� _g_ � _→_ � _e_ � _→P_ 3/2) cooling cycles (Roos _et al._ , 1999). 

Finally the cooling result was detected by comparing the red and blue sideband transition probabilities on the � _g_ � _→_ � _e_ � transition as described above. Figure 7 shows the results for a single ion cooled at a 4.51-MHz motional frequency. From the residual noise around the red sideband transition frequency an upper limit of 99.9% ground-state occupation was inferred. We note that ground-state cooling using resolved-sideband transitions was also experimentally demonstrated for up to four ions (King _et al._ , 1998; Sackett _et al._ , 2000; Rohde _et al._ , 2001) and for neutral atoms in optical lattices (Hamann _et al._ , 1998; Perrin _et al._ , 1998; Vuletic _et al._ , 1998). 

## C. Electromagnetically induced transparency cooling 

From the previous sections it might have become intuitively clear that any type of laser cooling in a trap depends on the balance of absorption and emission of photons on the red and blue sidebands. Every absorption-emission cycle may be viewed as a scattering 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

301 

Leibfried et al.: Quantum dynamics of single trapped ions 

event, with some events leading to cooling, some to heating, and some to no change in the motional state. The ion will be cooled on average if the events that dissipate motional energy are more probable than the heating events. Typically the likelihood of cooling events decreases as the kinetic energy decreases, while the heating events settle at a fixed (possibly very low) rate. Equilibrium is reached when cooling and heating events on average balance each other. The derivation of the Doppler cooling limit, Eq. (105), in Sec. IV.A is an example of that mechanism in which the velocityindependent heating rate Eq. (104) is balanced with the velocity(and therefore kinetic-energy-) dependent cooling rate Eq. (103). 

Inspection of Eq. (106) and its derivation reveals that the minimum Doppler temperature is dictated by the line shape of the cooling transition [see Eq. (99)]. This implies that one might influence the cooling process by tailoring the line shape of the cooling transition. In the preceding sections our discussion was limited to effective two-level systems and laser intensities around or below saturation with not too strong coupling of the atom to the light field. The basic idea of electromagnetically induced transparency (EIT) cooling is to go beyond this scenario and utilize the strong coupling of one laser to the atom in a three-level �-type scheme to create an absorption profile for the second (weaker) laser that is advantageous for cooling (Morigi _et al._ , 2000). 

We shall first derive a generalized treatment of the cooling that works for an arbitrary scattering rate on the cooling transition. The cornerstones of this treatment are outlined in Stenholm (1986). We shall derive some general statements about what kind of dependence of the scattering rate on the relative detuning of atom and laser is most useful. We shall then derive the scattering rate in the � system for an atom at rest and set the parameters according to the design principles found earlier. 

## 1. Cooling in the Lamb-Dicke regime 

We shall now calculate the cooling and heating rates for a laser-driven, trapped ion with arbitrary scattering rate _W_ (�). A general scattering (absorption-emission) cycle will proceed from � _g_ , _n_ � over � _e_ , _n_ �� to � _g_ , _n_ ��, and, in principle, one could find the scattering rates for all possible combinations ( _n_ , _n_ �, _n_ �) and derive rate equations for the probability _P_ ( _n_ ) to be in a certain state _n_ based on all these scattering rates. Here we shall limit possible scattering paths by assuming that some sort of precooling (for example, Doppler cooling) has left the ion in a state with thermal distribution in or close to the Lamb-Dicke regime with �[2] _¯n_ �1. In this approximation the treatment cannot describe the complete cooling dynamics, but as long as the cooling method in question reaches the Lamb-Dicke regime, it will yield useful expressions for the cooling limit and the cooling rate towards the final state. We assume that we know the scattering rate _W_ (�) at laser detuning � of the atom at rest. This quantity can usually be found by solving Bloch equations for the atom and calculating the steady-state 

population �ex in the excited state. The scattering rate is then this population times the total decay rate � of the excited state, _W_ (�)���ex . In the Lamb-Dicke regime absorption and emission will be dominated by carrier and first-order red (blue) sidebands with transition probabilities proportional to �[2] and �[2] �[2] _n_ ��[2] �[2] ( _n_ �1)�, respectively, and we can neglect all processes of higher order in �. Scattering on the carrier (� _g_ , _n_ � _→_ � _g_ , _n_ �) will be the most frequent process but will not change the probabilities _P n_ to be in a certain _n_ state. Motionalstate-changing events are limited to � _g_ , _n_ � _→_ � _g_ , _n_ �(0,1)� via the intermediate states � _e_ , _n_ � or � _e_ , _n_ �1�. By comparing the Rabi frequencies on carrier and sideband we can see that the scattering rate on a path involving one red (blue) sideband transition (for example, � _g_ , _n_ � _→_ � _e_ , _n_ � _→_ � _g_ , _n_ �1�) will be suppressed by the factor �[2] _n_ ��[2] ( _n_ �1)� compared to the carrier transition. In more detail, the rates _R nn_ �1 will go as 

**==> picture [229 x 32] intentionally omitted <==**

where the first contribution comes from the scattering path through � _e_ , _n_ � and the second from the path � _e_ , _n_ �1�. For example, in the second path on _R nn_ �1 the atom absorbs at detuning ��� since the remaining energy �� goes into the motion. Knowing these rates we can immediately write down rate equations for the motional-level populations 

**==> picture [229 x 62] intentionally omitted <==**

with the _n_ -independent coefficients 

**==> picture [229 x 13] intentionally omitted <==**

The rate equation (118) can be converted into an equation of motion for the average motional quantum number 

**==> picture [229 x 26] intentionally omitted <==**

by appropriate pairing and resumming of the respective populations in connection with the _A_ � coefficients. As long as the cooling rate �( _A_ �� _A_ �)�0, _¯n_ will evolve towards the final state of cooling, the steady state of Eq. (120) given by 

**==> picture [229 x 24] intentionally omitted <==**

It is instructive to plug the scattering rates _W L_ (�) of a Lorentzian line into this formalism. Then the Doppler limit _¯n_ ���/2 is recovered for ��� while _¯n_ �1 for � _f_ ��. For best cooling results with a general scattering rate we want to minimize _n¯ f_ , which happens naturally if the scattering rate on the red sideband _W_ (���) is 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

302 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [181 x 110] intentionally omitted <==**

FIG. 8. Notation of levels, detunings, Rabi frequencies, and decay rates used in the calculation of an electromagnetically induced transparency (EIT) line shape. 

much bigger than the carrier and blue sideband rates, _W_ (�) and _W_ (���), respectively. 

**==> picture [169 x 140] intentionally omitted <==**

FIG. 9. Qualitative scattering rate on the � _g_ � _↔_ � _e_ � transition as � _g_ is varied for � _r_ �0. In addition to the broad resonance around � _g_ �0, a narrow bright resonance appears to the right of the dark resonance at � _g_ �� _r_ . The distance between the dark and the bright resonance is equivalent to the ac Stark shift of � _e_ � caused by the strong beam. 

## 2. Scattering rates in EIT cooling 

The general idea of EIT cooling in a � system is to use a dark resonance to completely suppress the carrier scattering (Morigi _et al._ , 2000). With a prudent choice of parameters of the two light fields driving the system we shall then also be able to fulfill _W_ (���)� _W_ (���). We denote the levels, detunings, and Rabi frequencies of the two transitions as indicated in Fig. 8. The equations of motion for the density matrix (Bloch equations) can, in principle, be derived from Eq. (86) or by adding phenomenological damping terms to the unitary evolution that correctly reflect the decay of the � _e_ � state. The Bloch equations in our system are 

**==> picture [229 x 169] intentionally omitted <==**

with ��� _g_ �� _r_ . We shall assume that reequilibration of the internal-state dynamics is much faster than the external motional dynamics, so we can solve for the steady state of the Bloch equations to describe the scattering events at all times. Doing so and using the conservation of probability � _rr_ �� _gg_ �� _ee_ �1 one can (after some algebra) derive the steady-state solution for � _ee_ (Janik _et al._ , 1985): 

**==> picture [229 x 25] intentionally omitted <==**

**==> picture [98 x 12] intentionally omitted <==**

**==> picture [229 x 54] intentionally omitted <==**

This rather complicated expression quickly simplifies if we set � _g_ ��� and assume � _r_ �� _g_ and � _g_ �(� _r_ ,� _r_ ), following the idea that the strong laser field on the � _r_ � _↔_ � _e_ � transition optically pumps the internal state to � _g_ � and also modifies the scattering rate of a comparably weaker beam on the � _g_ � _↔_ � _e_ � transition into _W_ (�) ��� _ee_ (�), which is advantageous for cooling. This yields 

**==> picture [229 x 30] intentionally omitted <==**

Figure 9 shows the qualitative behavior of the scattering rate vs detuning � for (� _r_ ,� _g_ )�0. Indeed _W_ (�) vanishes at ��0, so the carrier is completely suppressed. The position of the two maxima is given by 

**==> picture [229 x 23] intentionally omitted <==**

We want the narrow bright resonance at positive detuning to coincide with the red sideband, � ���: 

**==> picture [229 x 14] intentionally omitted <==**

The reader may recognize that this condition is equivalent to saying that the Stark shift of the � _r_ � _→_ � _g_ � resonance has to be equal to the motional frequency. For this choice of parameters, _W_ (��) takes the largest value possible, while _W_ (��) then assumes a comparatively small value from the wing of the broad bright resonance to the left of the origin. To find the cooling limit quantitatively, we can start from Eq. (121) with _W_ (0)�0. Using Eq. (127) we get after some algebra 

**==> picture [229 x 27] intentionally omitted <==**

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

303 

Leibfried et al.: Quantum dynamics of single trapped ions 

To ensure that _¯n s_ �1 we have to choose � _g_ �� _r_ ��, while � _r_ has to be set to accommodate Eq. (127). 

Finally we should note that our treatment of EIT cooling is only an approximation, since we neglected all recoils happening when the system is relaxing back into the steady state after scattering a photon on the sideband transitions. Fortunately, since we start in the Lamb-Dicke regime, the relaxation proceeds predominantly through carrier scattering, thus not altering the average motional quantum number. Morigi _et al._ (2000) have done a Monte Carlo simulation that also takes these effects into account. Indeed the cooling dynamics are slightly slower in this simulation, but very close to the approximate treatment. 

## 3. Experimental results 

The Innsbruck group has demonstrated EIT cooling with a single calcium ion (Roos _et al._ , 2000). The � system was implemented within the _S_ 1/2 _→P_ 1/2 transition, whose Zeeman sublevels _m_ ��1/2 and _m_ ��1/2 constitute a four-level system. By applying the strong laser on the �[�] transition (� _r_ ��� _S_ 1/2 , _m_ ��1/2�,� _e_ ��� _P_ 1/2 , _m_ �1/2�) and the weaker cooling laser on a � transition (from � _g_ ��� _S_ 1/2 , _m_ ��1/2�), they ensured that very little population would ever be in the extra � _P_ 1/2 , _m_ ��1/2� state, so this was effectively a three-level system. An additional laser is used to repump the ion from the _D_ 3/2 level, but the branching ratio to that level was so small that the above conclusion was not seriously compromised. 

The two beams were generated by splitting frequencydoubled light from a Ti:sapphire laser near 397 nm into two suitable beams with the help of two acousto-optic modulators (the same beam was also used for Doppler precooling of the ion). The second-order Bragg reflexes of two acousto-optical modulators driven at around 90 MHz had a blue detuning of about � ��� ��75 MHz relative to the _S_ 1/2 _↔P_ 1/2 line center (natural linewidth of the transition ��20 MHz). The beams (typically about 50 �W in the strong and 0.5 �W in the weak beam) were then focused into a �60-�m waist onto the single ion in a trap with oscillation frequencies (� _x_ ,� _y_ ,� _z_ ) �(1.69,1.62,3.32) MHz. The _k_ vectors of the two beams enclosed an angle of 125° and their _k_ -vector difference � **k** had a component along all three trap axes. The beam intensity was controlled with the power of the acoustooptical modulator rf drive. 

The ion was first Doppler precooled. The Doppler cooling limit on this was ( _¯n x_ , _¯n y_ , _¯n z_ )�(6,6,3) in the trap used. The EIT cooling beams were applied for periods between 0 and 7.9 ms, with _¯n_ reaching its asymptotic limit after about 1.8 ms. The final mean occupation number was probed on the resolved sidebands of the _S_ 1/2 _↔D_ 5/2 transition, either using the technique described in Sec. IV.B.1 or fitting experimental Rabi oscillations to those expected for a small state with thermal distribution (Meekhof _et al._ , 1996; Roos _et al._ , 1999). 

In this manner EIT cooling of the _y_ and the _z_ oscillations at 1.62 and 3.32 MHz was investigated. The inten- 

sity of the strong beam was fine-tuned by observing the resolved-sideband excitation on the red sideband of either mode and minimizing it. The lowest observed mean vibrational quantum number was _¯n y_ �0.18, corresponding to 84% ground-state probability. On the _z_ mode at � _z_ �3.3 MHz, after the intensity of the �[�] beam was increased to adjust the ac Stark shift, a minimum mean vibrational number of _¯n z_ �0.1 was observed, corresponding to a 90% ground-state probability. The cooling results were largely independent of the intensity of the � beam as long as it was kept much smaller than the �[�] intensity. The intensity ratio _I_ � / _I_ ��100 was varied by a _¯_ factor of 4, with no observable effect on the final _n_ . From the dependence of the mean vibrational quantum number on the EIT pulse length, an initial cooling rate of 1 quantum per 250 �s was found for the _y_ direction. 

In addition, both modes were simultaneously cooled by setting the intensity of the strong beam for an ac Stark shift roughly halfway between the two mode frequencies. Both modes were cooled simultaneously with ( _p_ 0) _y_ �58% and ( _p_ 0) _z_ �74% ground-state probability. 

## V. RESONANCE FLUORESCENCE OF SINGLE IONS 

The observation and analysis of resonance fluorescence emitted from atomic systems provide an important tool for investigation of the interaction between matter and radiation. Essentially there are three complementary strategies available for these measurements: 

- (i) Excitation spectroscopy comprises the observation of resonance fluorescence as a function of the detuning of the exciting electromagnetic radiation; 

- (ii) the spectrum of resonance fluorescence is obtained by measuring the spectral distribution of the emitted resonance fluorescence at a fixed detuning of the exciting radiation; 

- (iii) quantum-dynamical information can be obtained by measuring the time interval statistics of the photon-counting events from resonance fluorescence, usually in the form of correlation functions. 

All three techniques have been used to investigate single-ion resonance fluorescence. 

## A. Excitation spectroscopy, line shapes 

A single two-level atom at rest in free space (Dehmelt, 1973) is the ideal object for the observation of resonance fluorescence. The outcome of corresponding experiments can be completely described in terms of the optical Bloch equations, as given by Eq. (86), where the excited-state population � _ee_ as a function of the detuning � of the exciting radiation describes the observed line shapes. However, since the detuning also sensitively influences the cooling and heating dynamics, the observed line shape in excitation spectroscopy usually exhibits this influence as well. More precisely, for weak confinement (i.e., trap frequency ���, the natural line- 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

304 

Leibfried et al.: Quantum dynamics of single trapped ions 

width of the excited state) and a laser detuning far below resonance (i.e., ��0 or ‘‘red detuning’’), the Doppler-broadened line shape resembles that of a thermal ensemble of atoms; however, the Doppler broadening results from a convolution of overlapping sidebands. For a red detuning close to resonance, cooling sets in and the line shape can be described very well by the Lorentzian of an atom at rest. For a positive (or ‘‘blue’’) detuning ��0, heating dominates and the large number of resulting sidebands broadens the transition to such an extent that the absorption sharply drops near resonance ��0. Therefore excitation spectra of a single two-level ion exhibit an asymmetric (‘‘half-Lorentzian’’) shape due to the cooling and heating dynamics (Nagourney _et al._ , 1983). For three- and more-level systems with several lasers contributing to the cooling and heating dynamics the observed line shapes can become quite involved and difficult to interpret (Reiß _et al._ , 1996). Especially well-investigated cases are the three-level (eight-sublevel) systems of single trapped Ba[�] and Ca[�] ions (Janik _et al._ , 1985; Siemers _et al._ , 1992). These ions must be modeled by a �-shaped three-level _S_ 1/2 _↔P_ 1/2 _↔D_ 3/2 (or, accounting for all Zeeman sublevels, eight-level) system. The excitation usually involves two dipole transitions, sharing the fluorescing level _P_ 1/2 , and excitation spectroscopy is obtained by tuning only one exciting laser across resonance while the second one is kept fixed below resonance. Thus net cooling usually can be observed even for a certain range of blue detunings. Three-level (eight-sublevel) systems can exhibit line shapes that agree very well with the theoretical descriptions given by the optical Bloch equations for an atom at rest. In fact, the richness of these systems allows one to investigate in quantitative detail the effects of optical pumping, the appearance of dark resonances, and Raman processes (Schubert _et al._ , 1992, 1995; Siemers _et al._ , 1992). The excellent quantitative agreement between theory and experiment allows one to precisely derive all spectroscopic parameters, such as the detunings, the Rabi frequencies, and the orientation of the quantization axis required for more detailed quantumoptical calculations, e.g., correlation functions, as discussed below. 

## B. Nonclassical statistics, antibunching, and squeezing 

A powerful way to acquire detailed information about the quantum dynamics of an atom is the statistical analysis of the measured stream of photon counts. In particular, nonclassical features of the resonance fluorescence are observed in the second-order correlation functions (intensity correlations) 

**==> picture [229 x 26] intentionally omitted <==**

Here the scattered light field of the atomic resonance fluorescence is described by the electric-field operators **E**[�] and **E**[�] (Glauber, 1963, 1964) and for ��0. This function is proportional to the probability of detecting a second photon at time � after a first one has been ob- 

served at ��0. Whereas classical fields show correlation functions _g_[(2)] (0)�1 and _g_[(2)] (�)� _g_[(2)] (0), the nonclassical resonance fluorescence of a single atom exhibits the so-called _antibunching_ behavior, i.e., _g_[(2)] (0)�0 and _g_[(2)] (�)� _g_[(2)] (0). This condition entails sub-Poissonian emission probability for ��0. Both antibunching and sub-Poissonian statistics have been observed in quantum-optical experiments with atoms (Kimble, Dagenais, and Mandel, 1977; Short and Mandel, 1983); however, corrections for the fluctuating atom numbers in the atomic beam had to be applied. 

For a single two-level atom the intensity correlation function is 

**==> picture [229 x 25] intentionally omitted <==**

where � _ee_ represents the population of the excited state of the atom. Since _g_[(2)] (�) is a conditional probability as a function of time, it allows one to observe directly the quantum-dynamical behavior of the matter-radiation interaction. Likewise, any motional effects affecting the resonance fluorescence can be characterized from an analysis of _g_[(2)] (�). 

With a single trapped Mg[�] ion Diedrich and Walther (1987) observed antibunching and sub-Poissonian statistics of an individual two-level atom. In that experiment antibunching in the resonance fluorescence of one, two, and three trapped ions was observed and the antibunching property decreased as predicted for increasing ion numbers, since for an increasing number of independent atoms the photon counts become more and more uncorrelated. The dynamical interaction between matter and radiation leads to Rabi oscillations and for a single ion the observed intensity correlation agrees very well with the theoretically predicted function (Carmichael and Walls, 1976), 

**==> picture [229 x 27] intentionally omitted <==**

where �[2] �� 20�� 2�(�/4) 2, with the Rabi frequency � 0 at resonance, the natural linewidth �, and the detuning �. The single-atom resonance fluorescence clearly exhibited sub-Poissonian statistics. The deviation of the distribution from Poisson statistics is usually described in terms of Mandel’s _Q_ parameter, 

**==> picture [229 x 27] intentionally omitted <==**

� where � _n_ � _T_ � � _n_ �0 _np n_ ( _T_ ) denotes the mean number of detected photons, with _p n_ ( _T_ ) the probability for detecting _n_ photons within the time _T_ . This parameter is related to the photon correlation function (Mandel, 1979; Merz and Schenzle, 1990) by 

**==> picture [229 x 24] intentionally omitted <==**

where _Z_ �� _n_ � _T_ / _T_ is the mean count rate. While for any classical radiation _Q_ ( _T_ )�0 at all _T_ , the measurement of Diedrich and Walther revealed _Q_ ��7�10[�][5] . In that 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

305 

Leibfried et al.: Quantum dynamics of single trapped ions 

experiment the classical residual (driven) micromotion of the trapped ion was observed as a modulation in the intensity correlation; however, secular motion could not be detected. 

In an experiment with one and two trapped Hg[�] ions Itano _et al._ (1988) were able to observe antibunching and sub-Poissonian statistics on the _P_ 1/2 _↔D_ 3/2 transition. Spontaneous emission on this transition is very weak (��52 s[�][1] ); however, each decay can be observed since it interrupts the otherwise steady photon flow on the strong (��4�10[8] s[�][1] ) _P_ 1/2 _↔S_ 1/2 transition that is used for excitation and detection. Thus each spontaneous decay on the weak transition is detected by the absence of many photons due to electron shelving (see Sec. III.C). Using this technique, antibunching on the weak transition was observed and, due to the greater detection efficiency of the electron shelving technique (as compared to usual photon counting in the experiment by Diedrich and Walther), a _Q_ value of _Q_ ��0.25 for one and two ions could be measured. 

In a subsequent experiment at the University of Hamburg, Schubert _et al._ (1992, 1995) observed antibunching and sub-Poissonian statistics ( _Q_ ��7�10[�][4] due to limited efficiency of photon counting) in the resonance fluorescence of a single Ba[�] ion, which cannot be modeled as a two-level system. Aside from antibunching and sub-Poissonian statistics, the observed intensity correlations in this case revealed maximum photon correlations much larger than what is possible with two-level atoms, as well as photon antibunching with much larger time constants of the initial photon anticorrelation. Thus a detailed study of the internal dynamics due to optical pumping and the preparation of Zeeman coherences became possible. Furthermore, the exact form of the observed _g_[(2)] functions allowed the direct observation and quantitative description of the preparation of superposition states vs mixed states of a single trapped particle (Schubert _et al._ , 1995). 

Aside from the antibunching property, which directly reflects the photon nature of light, other nonclassical effects are observable in resonance fluorescence. An example is the _squeezing_ property, which is usually observed in a homodyne detection scheme (Slusher _et al._ , 1985; Wu _et al._ , 1986) and which describes an asymmetric noise behavior of the quadrature components of the electromagnetic radiation. Squeezing has also been predicted to appear in the resonance fluorescence of single two-level atoms (Walls and Zoller, 1981) and three-level atoms (Vogel and Blatt, 1992). Due to limited detection efficiency, Mandel (1982) has shown that the observable effect from squeezing in the photon statistics of the resonance fluorescence of a single atom is extremely weak. Alternatively, the detection of homodyne intensity correlations is expected to offer an easier way to observe squeezing in the resonance fluorescence of a single trapped ion, as was proposed by Vogel (1991) and Blatt _et al._ (1993). However, no experimental results are currently available. 

## C. Spectrum of resonance fluorescence, homodyne detection of fluorescence 

Information about the dynamics of the interaction between matter and radiation can also be gathered by spectral analysis of the emitted resonance fluorescence. The spectrum of resonance fluorescence emitted by a free two-level atom interacting with a traveling-wave laser field was studied by Mollow (1969). For low excitation intensities the fluorescence spectrum exhibits an elastic peak centered at the incident-laser frequency � _L_ , while for higher intensities an inelastic component becomes dominant, with contributions centered at the frequencies � _L_ and � _L_ �� 0 (for resonant excitation), where � 0 denotes the Rabi frequency. This so-called ‘‘Mollow triplet’’ arises from the dynamic (or ac) Stark splitting of the two-level transition. As outlined in Sec. III.B.6 above, the observation of the fluorescence spectrum provides an alternative method for detecting the internal quantum dynamics as well as the (quantum) motion in the trap. 

With a single trapped and laser-cooled Ba[�] ion, Stalgies _et al._ (1996) analyzed the spontaneously emitted light on the _P_ 1/2 _↔S_ 1/2 transition at 493 nm with a FabryPerot interferometer and recorded emission spectra of the single-ion fluorescence. The piezo-tuned confocal filter resonator provided a spectral resolution of about 16.7 MHz. This was sufficient to resolve the spectral components of the transition, which has a natural width of about 20 MHz. The observed spectra show the expected dynamical Stark effect and are in agreement with theoretical predictions based on calculations using optical Bloch equations and parameters that were derived from excitation spectra as outlined above in Sec. V.A. 

Refined spectroscopic information on the fluorescence spectrum can be gained by beating the fluorescent light with a local oscillator and subsequent homodyne or heterodyne analysis. The elastic component scattered by an ensemble of cold-trapped atoms was first detected by Westbrook _et al._ (1990) with atoms confined in an optical lattice. With a single trapped and laser-cooled Mg[�] ion, Rayleigh scattering on the _S_ 1/2 _↔P_ 3/2 transition was observed by Ho[¨] ffges, Baldauf, Eichler, _et al._ (1997) and Ho[¨] ffges, Baldauf, Lange, and Walther (1997). Heterodyne detection allowed for a spectral resolution of the elastic component with a linewidth of 0.7 Hz. 

As shown above in Sec. V.A, the motion of trapped particles in an external potential shows up as sidebands to the elastically scattered component. The height of the sidebands then presents a measure of the motional amplitude, and their width reflects the cooling rate. Such motional sidebands were first detected in the fluorescence spectrum of ensembles of cold atoms in optical lattices (Jessen _et al._ , 1992) and they were only recently observed in the homodyne spectra of single trapped ions. With a single trapped and laser-cooled Yb[�] ion, Bu[¨] hner and Tamm observed motional sidebands in the resonance fluorescence of the _P_ 1/2 _↔S_ 1/2 transition at 369 nm of[172] Yb[�] at a radial secular motion of 785 kHz (Bu[¨] hner and Tamm, 2000; Bu[¨] hner, 2001). The measured 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

306 

Leibfried et al.: Quantum dynamics of single trapped ions 

maximum width of the sidebands was about 1.5 kHz at saturation intensity and for an optimal detuning of the cooling laser of ���. Taking into account residual broadening by the detection technique (i.e., detection bandwidth of the spectrum analyzer and fluctuating trap voltages), the authors concluded that the observed cooling rate agreed well with predictions based on the twolevel cooling calculations. 

With a single trapped[171] Yb[�] ion that has a hyperfine splitting, a weak spontaneous decay to a hyperfine component of the excited _D_ 3/2 state leads to intermittent resonance fluorescence on the _P_ 1/2 _↔S_ 1/2 transition due to electron shelving. This results in an additional inelastic component of the observed fluorescence spectrum (Hegerfeldt and Plenio, 1995), and its height and width are uniquely determined by the shelving conditions. This leads to a Lorentzian component centered on the elastic scattering and is interpreted as a broadening due to a ‘‘stochastic intensity modulation.’’ In the experiment this feature was observed and found to be in agreement with the theoretical prediction (Bu[¨] hner and Tamm, 2000). 

With a single trapped Ba[�] ion, heterodyne measurements were also performed by the Innsbruck group. The measured width of the elastic component was limited by the resolution bandwidth of 64 MHz of the spectrum analyzer. Since the phase of the driven micromotion at �rf�2� 18.53 MHz is well defined, the corresponding micromotion sidebands were observed with the same linewidth. From the height of the sidebands a modulation index corresponding to a residual micromotion amplitude of 26 nm was derived. This measurement allows one to detect and compensate for residual micromotion, and it is sensitive to micromotion amplitudes of about 1 nm (Raab _et al._ , 2000). Furthermore, sidebands due to secular motion at frequencies (� _x_ ,� _y_ ,� _z_ )/2� �(0.62,0.65,1.3) MHz were observed using an excitation technique: By exciting the ion motion with a weak rf field (applied to nearby electrodes) one can detect coherent sidebands with a high signal-to-noise ratio, since this results in a driven motion and thus is similar to the detection of micromotion sidebands. Scanning the excitation across the sideband frequency results in a resonant enhancement of the ion motion, making the sidebands easily observed. Extrapolating the observed linewidth to zero amplitude of the exciting rf field eventually reveals the cooling rate limiting the width of the motional sidebands. The experimentally observed linewidths of about 750 Hz agree within the error limits with the calculated cooling rates (Raab _et al._ , 2000). These findings were corroborated by direct observation of the sidebands as shown in Fig. 10 (Raab _et al._ , 2001). No asymmetric sidebands were observed in either the Ba[�] experiment (Innsbruck) or the Yb[�] experiment (Braunschweig), since in both cases only Doppler cooling was available and the residual quantum numbers of the harmonic motion were between 10 and 30 (depending on the ion and the respective secular frequencies), leading to almost equal sideband amplitudes. 

Using a new technique, the Innsbruck group recently studied the interaction of a single trapped Ba[�] ion with 

**==> picture [181 x 186] intentionally omitted <==**

FIG. 10. Heterodyne signal on a secular sideband of the undriven motion of a single Ba[�] ion (Raab _et al._ , 2001). The fitted width corresponds to a cooling rate of 2� 900 s[�][1] . 

a part of the emitted resonance fluorescence (Eschner _et al._ , 2001). For this, part of the emitted light (about 4% of the solid angle) is collimated with a lens to a plane mirror about 25 cm away from the ion and then retroreflected (via the same lens) onto the ion. The fluorescence and its mirror image are then observed with a photomultiplier opposite the mirror collecting both the directly emitted and the back-reflected part. Moving the mirror using a piezoelectric transducer and overlapping the direct and reflected parts allows one to observe interference fringes that result from the interfering beam paths (direct and reflected paths) and the visibility of the interference fringes can be calculated from the firstorder correlation function 

**==> picture [229 x 26] intentionally omitted <==**

The emitted field **E**[�] ( **t** ) can be expressed in terms of the atomic polarization, which in turn can be calculated from the optical Bloch equations. As expected, the visibility decreases with increasing laser intensity due to the increasing ratio of inelastic to elastic scattering; that is, the internal dynamics of the interaction can be investigated through a study of the interference fringes. In addition, external atomic motion influences the interference since the ion oscillation results in a phase modulation of the field **E**[�] ( **t** ). This effect allows one to measure the amplitude of any residual ion motion via an observation of the interference fringes. Moreover, the ion position with respect to the mirror can be determined on the scale of the extension of the wave function, which is several nm. 

Including the back-reflected part of the emitted fluorescence in the optical Bloch equations reveals that the reflected part actually acts back on the ion and changes the excited-state populations and thus the overall resonance fluorescence. This back action has been detected by an independent observation of the excited-state population as a function of the mirror position (i.e., 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

307 

Leibfried et al.: Quantum dynamics of single trapped ions 

whether there is constructive or destructive interference). This can be considered inhibition and enhancement of the resonance fluorescence by the reflected (and phase-sensitive) presence of the self-emitted photon. This back action mediated by the external mirror has also been observed with the radiation of two ions; that is, two ions interfering with the mirror image of each other show the same effect (Eschner _et al._ , 2001). This technique opens the way for quantum feedback scenarios in which single emitted fluorescence quanta can be used to influence and eventually control the internal and external quantum dynamics of trapped ions. 

## VI. ENGINEERING AND RECONSTRUCTION OF QUANTUM STATES OF MOTION 

## A. Creation of special states of motion and internal-state/ motional-state entanglement 

Fueled by the strong analogy between cavity QED and the trapped-ion system, various theoretical proposals have been made on how to create nonclassical and arbitrary states of motion of trapped ions or even how to create states in which the internal degree of freedom is entangled with the external motion in a highly nonclassical way ( _Schro[¨] dinger-cat states_ ). The theoretical efforts were complemented by the first experiments on nonclassical states of motion by the groups at NIST and the University of Innsbruck. In the NIST experiments, coherent, quadrature squeezed number states and superpositions of number states of trapped Be[�] were prepared (Meekhof _et al._ , 1996). The preparation of number states was also achieved for trapped Ca[�] at the University of Innsbruck (Roos _et al._ , 1999). The NIST group succeeded in entangling coherent motional states with opposite phases to the two internal states (Schro[¨] dinger-cat state; Monroe _et al._ , 1996). 

The common starting point for all motional-state engineering experiments so far has been the ground state of motion, reached by resolved-sideband cooling methods as described in Sec. IV.B. Since resolved-sideband cooling has only been successfully applied inside the Lamb-Dicke regime, most of the state preparation also took place in this regime. The description of interactions will be restricted to this limit in the following and only generalized where appropriate. 

## 1. Creation of number states 

Several techniques for the creation of number states of motion have been proposed, using quantum jumps (Cirac, Blatt, _et al._ , 1993; Eschner _et al._ , 1995), adiabatic passage (Cirac, Blatt, and Zoller, 1994), or trapping states (Blatt _et al._ , 1995). Despite the possibilities described in these papers, a simple technique involving multiple � pulses is the only one to have been used in experiments so far. The ion is initially cooled to the � _g_ ,0� number state. Higher- _n_ number states are created by applying a sequence of resonant � pulses of laser radiation on the blue sideband, red sideband, or carrier. A � pulse corresponds to a time _t_ �, _n_ so that the argument in 

Eq. (84) is _f nl t_ �, _n_ ��� _n_ � _l_ , _n_ � _t_ �, _n_ ��. Here, resonant means ���0. The phase factors � _i_ and _e[i]_[�] are physically irrelevant in the present context since they factor out of the wave function; they are just kept for mathematical consistency. For these conditions the solution matrices _T nl_ take the simple forms 

**==> picture [229 x 28] intentionally omitted <==**

for the carrier and 

**==> picture [229 x 28] intentionally omitted <==**

for the red ( _l_ ��1) and blue ( _l_ ��1) sidebands. For creating pure number states, the phase factors of successive pulses will just add up to an overall phase factor that is irrelevant, therefore one can set these phase factors equal to one for all these pulses without losing generality. When generating superpositions of number states these phases will determine the relative phase of the number-state components and cannot be disregarded. Starting from the state � _g_ ,0�, with a blue sideband pulse, _T_ 10� _g_ ,0��� _e_ ,1�, the first excited motional state connected with the � _e_ � internal state is created. This may either be converted to � _i_ � _g_ ,1�� _T_ 01� _e_ ,1� or walked higher up the number-state ladder with a red sideband pulse _T_ �1 1� _e_ ,1��� _g_ ,2�. In this manner one can step through to high number states, as was done in an experiment of the NIST group using Raman transitions between two hyperfine levels of Be[�] (Meekhof _et al._ , 1996). Once the number state is created, the signature of the state can be found by driving transitions on the first blue sideband as described in Sec. III.D. The rate of the Rabi flopping, � _n_ , _n_ �1 in Eq. (70), depends on the value of _n_ of the number state occupied. According to Eq. (95) the expected signal is proportional to 1 �cos(� _n_ , _n_ �1 _t_ ). The experimentally observed signal also turned out to be damped, probably due to a combination of uncontrolled noise sources (see below). This was accounted for by introducing _n_ -dependent exponential damping with constants � _n_ in the fits of the blue sideband excitation curves, 

**==> picture [229 x 23] intentionally omitted <==**

The observed flopping curves are approximately described by Eq. (137), as can be seen in Fig. 11(a) for an initial � _g_ , _n_ �0� number state created in this experiment. The fit to Eq. (137) is drawn as a solid line and yielded � 0,1 /(2�)�188(2) kHz and �0�11.9(4) s[�][1] . 

In this experiment _P g_ ( _t_ ) was recorded for a series of number states � _g_ , _n_ � up to _n_ �16 and the Rabi-frequency ratios � _n_ , _n_ �1 /� 0,1 were extracted. They are plotted in Fig. 11(b), showing very good agreement with the theoretical frequencies, which include the trap’s finite LambDicke parameter ��0.202 [solid line in Fig. 11(b)]. 

The damping constant � _n_ was also extracted and observed to increase with _n_ [the data are consistent with � _n_ ��0( _n_ �1)[0.7] ]. The source of the damping was be- 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

308 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [241 x 251] intentionally omitted <==**

FIG. 11. Number states in the NIST experiment (Meekhof _et al._ , 1996): (a) Rabi oscillations on the blue sideband for the ground state in the trap ( _n_ �0); (b) �, measured ratio of Rabi frequencies for different number states; solid lines, theoretical predictions for several Lamb-Dicke parameters. 

lieved to be in part due to uncontrolled magnetic-field fluctuations at the position of the ion and frequency and intensity fluctuations of the two Raman light fields used in the experiment. One example of such noise sources, the magnetic fields due to currents switching at the 60-Hz line frequency and its harmonics, was successfully suppressed by producing a compensation field of the right amplitude and phase with extra coils close to the trap. 

Another source of dissipation was an unexpectedly high heating rate out of the motional ground state in these experiments. The observed heating rate was about one quantum per millisecond, about three orders of magnitude higher than expected from thermal electronic noise (Wineland _et al._ , 1998; Turchette, Kielpinski, _et al._ , 2000). 

The _n_[0.7] scaling of the damping constants with number state was extracted from fits to the data in this experiment. Theoretical work has incorporated spontaneous emission and heating to explain the observed scaling (Plenio and Knight, 1996, 1997; Bonifacio _et al._ , 2000; Di Fidio and Vogel, 2000; Budini, de Matos Filho, and Zagury, 2002). 

The second experiment on number states was carried out at the University of Innsbruck (Roos _et al._ , 1999). There a single[40] Ca[�] ion was cooled to the ground state on the _S_ 1/2 _→D_ 5/2 quadrupole transition (see also Sec. IV.B), leaving the ion in the _n_ �0 number state 99.9% of the time. The _n_ �1 number state was created by applying a � pulse on the blue sideband and then incoherently repumping the excited electronic state � _e_ � (in this experiment corresponding to the _m f_ ��5/2 sublevel of the 

**==> picture [241 x 83] intentionally omitted <==**

FIG. 12. Number states in the Innsbruck experiment (Roos _et al._ , 1999): (a) Rabi oscillations on the blue sideband for the ground state ( _n_ �0); (b) Rabi oscillations as in (a) but now for the number state � _n_ �1�. 

_D_ 5/2 state) via the _P_ 3/2 level with light at 854 nm. Since the repumping was done inside the Lamb-Dicke regime,[5] it did not change the motional state for most of the experiments, thus leaving the ion in the � _g_ �� _n_ �1� number state with high probability. Figure 12 shows the Rabi flopping dynamics on the blue sideband for the two prepared number states [(a) _n_ �0 and (b) _n_ �1]. The Rabi frequency � 0,1 is 21(1) kHz and the frequency ratio is � 1,2 /� 0,1�1.43, close to &, with the asymptotic value of Eq. (77) for the Lamb-Dicke parameter approaching zero. In this experiment a contrast over 0.5 was maintained for about 20 periods. Since a heating rate of about one quantum in 190 ms (1/70 ms) was measured along the axial (radial) direction for the Innsbruck trap, heating was not believed to play a leading role during the �1-ms duration of individual experiments. The decay in contrast was mainly attributed to magnetic-field fluctuations in the laboratory and intensity fluctuations in the laser beams. 

## 2. Creation of coherent states 

Coherent states of motion can be produced from the � _n_ �0� state by a spatially uniform classical driving field (Carruthers and Nieto, 1965), by a ‘‘moving standing wave’’ (Wineland _et al._ , 1992), by pairs of standing waves (Cirac, Blatt, and Zoller, 1994), or by a nonadiabatic shift of the trap center (Janszky and Yushin, 1986; Yi and Zaidi, 1988; Heinzen and Wineland, 1990). In experiments of the NIST group, the first two approaches were taken. For the classical drive, a sinusoidally varying potential at the trap oscillation frequency was applied to one of the trap compensation electrodes for a fixed time of typically 10 �s with varying amplitudes. This gave rise to an approximately spatially homogeneous force on the ion of the form 

**==> picture [229 x 11] intentionally omitted <==**

which can be associated with an interaction potential 

**==> picture [229 x 38] intentionally omitted <==**

> 5�854�0.03 for the _D_ 5/2 _→P_ 3/2 transition and �393�0.09 for the spontaneous decay, so the probability for two carrier transitions is (1��2854)(1��2393)�0.99. 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

309 

Leibfried et al.: Quantum dynamics of single trapped ions 

Putting in the lowest-order approximation, Eq. (15), _u_ ( _t_ )�exp( _i_ � _t_ )��1�( _qx_ /2)cos(�rf _t_ )�/(1� _q x_ /2)�, already displays the general behavior. As was pointed out by Carruthers and Nieto (1965), this interaction will change the quantum state of the oscillator only if the drive is resonant with its motion. In the lowest-order approximation this would mean a resonance at �drive�� and two weaker resonances at �drive����rf . To lowest order, the presence of micromotion will then just rescale the coupling strength by a factor 1/(1� _q x_ /2) for a drive frequency close to �. For �drive�� there are two stationary terms in Eq. (139) and two rotating at 2�. If we neglect the nonstationary terms (rotating-wave approximation) _H I_ becomes time independent and can easily be integrated, yielding the evolution operator 

**==> picture [229 x 12] intentionally omitted <==**

with 

**==> picture [229 x 27] intentionally omitted <==**

The drive coherently displaces an initial motional state ��� to 

**==> picture [229 x 13] intentionally omitted <==**

The coherent displacement is proportional to the time the drive is applied and the amplitude of the driving field. Experimentally the drive was calibrated by applying it to the motional ground state with a certain voltage amplitude and fitting the internal-state evolution on the blue sidebandstate ��� (see _P_ below) _g_ ( _t_ ) to the expected signal of a coherentwith the magnitude ���[2] � _¯n_ as the only free parameter. 

In the ‘‘moving standing-wave’’ approach, two laser beams with a frequency difference of �� and detuned by about � drive��12 GHz from the _S_ 1/2 _→P_ 1/2 transition in Be[�] were used. The detuning was much bigger than the linewidth � of the _P_ 1/2 state, so this state was populated with only an extremely small probability, 

**==> picture [229 x 27] intentionally omitted <==**

where � 0, _s_ �2�� _s_ � _e_ �( **r** • **E** 0)� _P_ 1/2�� **Õ** � is the on-resonance Rabi frequency of an ion in the hyperfine state � _s_ � and is driven by one of the equally strong beams **E** 1,2 � **E** 0 cos( _k_ 1,2 _x_ ��1,2 _t_ ��1,2), in complete analogy to the Appendix. At the position of the ion the interference of the two off-resonant light fields resulted in a timevarying light-field intensity _I_ ��( **E** 1� **E** 2)[2] � with a cross term modulated at ����1��2 (here the averaging brackets �•••� denote averaging over a time _T_ with ��1 ��2��1/ _T_ ��1,2). The other components are time independent and will not lead to any consequences for the ion’s motion. The difference frequency part leads to a spatially and time-varying intensity with a corresponding ac Stark shift of level � _s_ � that can resonantly drive the motion if ����1��2��. The dipole force on the ion is proportional to the spatial derivative of this ac Stark shift, 

**==> picture [241 x 156] intentionally omitted <==**

FIG. 13. Rabi oscillations for a coherent state (Meekhof _et al._ , 1996). The data (dots) are displayed together with a fit to a sum of number states having a coherent-state population distribution (line). The fitted value for the mean quantum number is _¯n_ �3.1�0.1. The inset shows the amplitudes of the number-state components (bars) with a fit to a Poisson distribution, corresponding to _¯n_ �2.9�0.1 (line). 

**==> picture [229 x 27] intentionally omitted <==**

for (��,� 0, _s_ )�� drive . If the oscillation amplitude of the ion remains in a small enough range, � _k_ � _x_ ��1, we can approximate sin(� _k_ � _x_ ���� _t_ ���)�sin(�� _t_ �� _˜_ ) for a _˜_ suitable � . Then the dipole force is of the form discussed in the context of Eq. (139) and will result in a coherent displacement of the motional wave function that grows linearly with the coupling time. Note that the range where this assumption is valid coincides with the definition of the Lamb-Dicke regime, so this drive will closely approximate a coherent drive while �[2] _¯n_ �1. 

By an appropriate choice of the internal levels and beam polarization, the dipole force can even create a state-dependent mechanical drive that allows one to entangle the internal states of the ion with the motion. As an example we shall discuss the level scheme used in Be[�] in the NIST experiment. Here the � _g_ � state was chosen to be the ( _F_ �2, _m F_ ��2) hyperfine substate and � _e_ � was ( _F_ �1, _m F_ ��1) of the[2] _S_ 1/2 manifold. The light fields were polarized �[�] and detuned �12 GHz from the[2] _P_ 1/2 level. This resulted in a driving dipole force for � _e_ � with the (1,�1) state coupling to the (2,�2) of the 2 _P_ 1/2 manifold, but there exists no (3,�3) substate in this manifold that could couple to � _g_ �. This level therefore remains unaffected by the drive. The dependence of the drive on the internal state was crucial for entangling internal and motional states as described in Sec. VI.A.4. 

As in the predictions of the Jaynes-Cummings model, the internal-state evolution _P g_ ( _t_ ) driven on the blue sideband, Eq. (95), will undergo collapses and revivals (von Foerster, 1975; Eberly _et al._ , 1980), a purely quantum effect (Shore and Knight, 1993). Figure 13 shows an example of _P g_ ( _t_ ) after the creation of a coherent state of motion. Similar behavior has been observed in the context of cavity QED (Brune, Schmidt-Kaler, _et al._ , 1996). The inset of Fig. 13 shows the probabilities of the 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

310 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [241 x 93] intentionally omitted <==**

FIG. 14. Rabi oscillations for a squeezed state (Meekhof _et al._ , 1996). The data (dots) are displayed together with a fit to a sum of number states having a squeezed-state population distribution with � _s_ �40�10, which corresponds to _¯n_ �7.1. 

number components, extracted by Fourier transformation of the signal. The probabilities of different motional levels display the expected Poissonian distribution over _n_ (see Sec. II.C.2). In the experiment the observed revival for higher- _¯n_ coherent states was attenuated due to progressively faster decay rates of the higher- _n_ number states (see Sec. VI.A.1); for states with _¯n_ �7 no revival was observed. 

## 3. Creation of squeezed states 

A ‘‘vacuum squeezed state’’ of motion can be created by a parametric drive at 2� (Janszky and Yushin, 1986; Yi and Zaidi, 1988; Heinzen and Wineland, 1990), by a combination of standing- and traveling-wave laser fields (Cirac, Blatt, and Zoller, 1994), or by a nonadiabatic change in the trap spring constant (Janszky and Yushin, 1986; Yi and Zaidi, 1988; Heinzen and Wineland, 1990). In the experiment of the NIST group the ion was cooled to the ground state and then irradiated with two Raman beams that differed in frequency by 2�, driving Raman transitions between the even- _n_ levels within the same hyperfine state. In analogy to the coherent drive described in Sec. VI.A.2 the interaction can be thought of as a parametric drive induced by an optical dipole force modulated at 2�. The squeeze parameter � _s_ (defined as the factor by which the variance of the squeezed quadrature is decreased) grows exponentially with the driving time. 

Figure 14 shows _P g_ ( _t_ ) for a squeezed state prepared by the NIST group in this way. The data were fitted to a vacuum squeezed-state distribution, allowing only � _s_ to vary. The fit of the data in Fig. 14 is consistent with a squeezed state with a squeeze parameter � _s_ �40�10 (corresponding to a noise level 16 dB below the zeropoint variance in the squeezed quadrature component). For this squeezing parameter, the average motional quantum number is _¯n_ �7.1. 

The probability distribution for a vacuum squeezed state is restricted to the even states, as can be seen from Eq. (53). This distribution is very flat; with � _s_ �40, 16% of the population is in states above _n_ � 20 (see Sec. II.C.3). The NIST experiment was conducted with a Lamb-Dicke parameter of 0.202. The Rabi-frequency differences of these high- _n_ levels were small [see Fig. 11(b)] and began to decrease with _n_ after _n_ �20. The 

levels could therefore no longer be well distinguished in frequency, so it was no longer possible to extract the level populations by Fourier transform of _P g_ ( _t_ ). 

## 4. ‘‘Schro[¨] dinger-cat’’ states of motion 

In Schro[¨] dinger’s original thought experiment (Schro[¨] - dinger, 1935) he describes how one could, in principle, transform a superposition inside an atom to a large-scale superposition of a live and dead cat by coupling cat and atom with the help of a ‘‘diabolical mechanism.’’ Subsequently the term ‘‘Schro[¨] dinger’s cat’’ developed a more general meaning, first referring to superposition states of macroscopic systems (the poor cat would be in such a state in the original paper) and later, especially in the context of quantum optics, referring to a superposition of two coherent states ��� and ��� (see Sec. II.C.2) with a separation in phase space ����� much larger than the variance of a coherent state. Such a state would allow one to distinguish the positions of the two coherent contributions by a position measurement with very high reliability, and they are macroscopic in the sense that their maximum spatial separation is much larger than the single-component wave-packet extension. 

In an experiment of the NIST group, an analogous state for a single trapped ion was engineered (Monroe _et al._ , 1996). Out of an equal superposition of internal states (� _e_ � and � _g_ �) a combined state of the motional and internal degrees of freedom of the form � _g_ ���� �� _e_ ��� _e[i]_[�] � was created in which the two coherent motional components had the same amplitude but different phases. The motional components of the superposition were indeed separated in space by distances much greater than their respective wave-packet spread for suitable phases �. 

This situation is interesting from the point of view of the quantum measurement problem associated with wave-function collapse, which was historically debated by Einstein and Bohr, among others. One practical approach toward resolving this controversy is the introduction of quantum decoherence, or the environmentally induced reduction of quantum superpositions into statistical mixtures and classical behavior (Zurek, 1991, 2001). Decoherence is commonly interpreted as a way of quantifying the elusive boundary between classical and quantum worlds, and almost always precludes the existence of macroscopic ‘‘Schro[¨] dinger-cat’’ states, except at extremely short-time scales. The creation of mesoscopic Scho[¨] dinger-cat states in controlled environments allows one to do controlled studies of quantum decoherence and the quantum/classical boundary (Brune, Hagley, _et al._ , 1996; Myatt _et al._ , 2000; Turchette, Myatt, _et al._ , 2000). Some of this work is described in Sec. VII. 

The creation of Schro[¨] dinger-cat states of a single ion in the experiments cited above relied on a sequence of laser pulses. The coherent states were excited with the use of a pair of Raman laser beams. The key to the experiment was that the displacement beams were both polarized �[�] , so that they did not affect the � _e_ � internal state (see Sec. VI.A.2). It is this selectivity that allowed 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

311 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [241 x 87] intentionally omitted <==**

FIG. 15. Steps for creation of a Schro[¨] dinger-cat state (Monroe _et al._ , 1996). For detailed explanation, see text. 

the components of a superposition of internal states to be associated to different motional states. 

The evolving state of the system during the sequence is summarized in Fig. 15. Following (a) laser cooling to the � _g_ �� _n_ �0� state, the Schro[¨] dinger-cat state was created by applying several sequential pulses of the Raman beams: (b) A �/2 pulse on the carrier transition split the wave function into an equal superposition of states � _g_ ��0� and � _e_ ��0�. (c) The selective dipole force of the coherent displacement beams excited the motion correlated with the � _e_ � component to a state ���. (d) A � pulse on the carrier transition then swapped the internal states of the superposition. (e) Next, the displacement beams excited the motion correlated with the new � _e_ � component to a second coherent state �� _e[i]_[�] �. (f) A final �/2 pulse on the carrier combined the two coherent states. The relative phases [� and the phases of steps (b), (d), and (f)] of the steps above were controlled by phase locking the rf sources that created the frequency splitting of the Raman or displacement beams, respectively. 

The state created after step (e) is a superposition of two independent coherent states, each correlated with an internal state of the ion (for ���), 

**==> picture [229 x 26] intentionally omitted <==**

In this state, the widely separated coherent states replace the classical notions of ‘‘dead’’ and ‘‘alive’’ in Schro[¨] dinger’s original thought experiment. The coherence of this mesoscopic superposition was verified by recombining the coherent wave-packet components in the final step (f). This resulted in different degrees of interference of the two wave packets as the relative phase � of the displacement forces [steps (c) and (e)] was varied. The nature of the interference depended on the phases of steps (b), (d), and (f) and was set to cause destructive interference of the wave packets in the � _g_ � state. The interference was directly measured by detecting the probability _P g_ (�) that the ion was in the � _g_ � internal state for a given value of �. The signal for particular choices of the phases in (b), (d), and (f) is 

**==> picture [229 x 23] intentionally omitted <==**

where � is the magnitude of the coherent states and _C_ �1 is the expected visibility of the fringes in the absence of any mechanisms decreasing the contrast, such as, for example, imperfect state preparation, motional heating, 

**==> picture [193 x 374] intentionally omitted <==**

FIG. 16. Phase signal of a Schro[¨] dinger-cat state for different magnitudes of the coherent displacement (Monroe _et al._ , 1996). 

or decoherence. The experiment was continuously repeated—cooling, state preparation, detection—while slowly sweeping the relative motional phase � of the coherent states. 

Figure 16 shows the measured _P g_ (�) for a few different values of the coherent-state amplitude �, which is set by changing the duration of application of the displacement beams [steps (c) and (e) from above]. The unit visibility ( _C_ �1) of the interference feature near ��0 verifies that superposition states were produced instead of statistical mixtures, and the feature clearly narrows as � increases. The amplitude of the Schro[¨] dinger-cat state was extracted by fitting the interference data to the expected form of the interference fringe. The extracted values of � agreed with an independent calibration of the displacement forces. Coherent-state amplitudes as high as ��2.97(6) were measured, corresponding to an average of _¯n_ �9 vibrational quanta in the state of motion. This indicates a maximum spatial separation of 4� _x_ 0�83(3) nm, which was significantly larger than the single wave-packet size characterized by _x_ 0�7.1(1) nm as well as a typical atomic dimension (�0.1 nm). The individual wave packets were thus clearly spatially sepa- 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

312 

Leibfried et al.: Quantum dynamics of single trapped ions 

rated and also separated in phase space. 

Of particular interest is the fact that as the separation of the cat state is made larger, the decay from superposition to statistical mixture accelerates. In the experiment, decoherence due to coupling to a thermal reservoir is expected to result in the loss of visibility in the interference pattern of _C_ � _e_[�][�][2][�] _[t]_ , where � is the coupling constant and _t_ the coupling time. This exponential reduction of coherence with the square of the separation (�[2] term) is thought to be the basic reason that bigger ‘‘cats’’ decay faster (Zurek, 1991). In Fig. 16(d), the observed loss of contrast at the largest observed separation already indicates the onset of decoherence. 

The precise control of quantum wave packets in the ion-trap version of Schro[¨] dinger’s cat provides a very sensitive indicator of quantum decoherence, whose characterization is of great interest to quantum measurement theory and applications such as quantum computing (Ekert and Josza, 1996) and quantum cryptography (Bennett, 1996). It was employed in a series of experiments that are described in Sec. VII. 

## 5. Arbitrary states of motion 

The methods presented above for creating a Schro[¨] dinger-cat state can be generalized to arbitrary states of motion. The general strategy for creating such states was first described by Law and Eberly (1996) in the context of cavity QED and later generalized to superpositions of internal states and arbitrary motional states of a trapped ion by Gardiner _et al._ (1997) and Kneer and Law (1998). No experiments to realize these proposals have been reported so far. 

## B. Full determination of the quantum state of motion 

The controlled interaction of light and rf electromagnetic fields with trapped ions allows one not only to prepare very general states of motion, but also to completely determine these quantum-mechanical states using novel techniques. The ability to prepare a variety of nonclassical input states in ion traps that can, for example, exhibit negative values of the Wigner function makes state reconstruction in ion traps an attractive goal. In addition, comparing the results of the state determination with the intended state allows one to quanitfy the accuracy of preparation and detrimental effects such as, for example, decoherence and motional heating. 

The first proposal for motional-state reconstruction in ion traps was put forward by Wallentowitz and Vogel (1995). Their method encodes the information on the motional state in the ground-state occupation of an atom driven on the first red and blue sidebands simultaneously. A Fourier integral transform of the measured data then yields the motional density matrix in a generalized position representation. Poyatos, Walser, _et al._ (1996) proposed to measure either the Husimi _Q_ function or the quadrature distribution function _P_ ( _x_ ,�) by applying a suitable sequence of phase shifts, coherent displacements, and squeezing operations to the motional 

state and subsequently measuring the occupation of the motional ground state with a method involving adiabatic passage (Cirac, Blatt, and Zoller, 1994). D’Helon and Milburn (1996) proposed to tomographically reconstruct the Wigner function of the vibrational state by measuring the electronic state population inversion after applying a standing-wave pulse to the ion that must reside at a node of the standing wave. Bardroff _et al._ (1996) proposed using a technique they called quantum-state endoscopy, exploiting the explicit time dependence of the rf trapping potential. The technique relies on driving the ion on combined secular and micromotion sidebands and monitoring the internal-state evolution. Leibfried _et al._ (1996) proposed and experimentally realized two techniques that reconstruct either the density matrix in the number-state basis or the Wigner function with the help of coherent displacements and monitoring of the internal-state evolution on the blue sideband, similar to the number-state population measurements described above. These techniques and the experimental results will be discussed in more detail below. Lutterbach and Davidovich (1997) proposed a very elegant method to directly measure the Wigner function from the inversion of the electronic states after a coherent displacement of the original motional state and a driving pulse of appropriate length on the blue sideband. Freyberger (1997) describes a scheme for measuring the motional density matrix in the number-state basis, which, like the proposal of Poyatos, Walser, _et al._ (1996), relies on coherent displacement and a filtering measurement to determine the population in the motional ground state. Finally, Bardroff _et al._ (1999) proposed a scheme to measure the characteristic function of the motional state by applying internal-state changing and coherent driving light pulses, very similar to the procedure for preparing a Schro[¨] - dinger cat described in Sec. VI.A.4. 

The two reconstruction methods described by Leibfried _et al._ (1996) were specially developed to fit the technical possibilities and constraints of the NIST apparatus and could therefore be experimentally realized. We shall restrict the more detailed discussion to these methods. The first method reconstructs the density matrix in the number-state basis, while the second yields the Wigner function of the motional state of a single trapped atom. 

Both measurement techniques rely on the ability to displace the input state to several different locations in phase space. Specifically, a coherent displacement (see Sec. VI.A.2) of the form _U_ (��)� _U_[†] (�)�exp(�* _a_ �� _a_[†] ) (�� simplifies the notation below) controlled in phase and amplitude is used in those schemes. In a manner similar to the characterization of motional-state populations described in the sections above, radiation on the blue sideband is then applied to the atom to extract the signal _P g_ ( _t_ ,�) (notice that this signal will vary for different displacements). The internal state at _t_ �0 is always prepared to be � _g_ � for the various motional input states, so, according to Eq. (95), modified for the rates of loss of contrast for different number states (see above), the signal averaged over many measurements is 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

313 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [229 x 40] intentionally omitted <==**

where _Q k_ (�) denotes the population of the coherently displaced number state _U_ (�)� _k_ �. For no coherent displacement the signal, Eq. (95), is recovered and contains information about the populations of the number states only. But since these measurements are repeated for several magnitudes and phases of the coherent displacement, information can be extracted about the coherence properties of the state, especially the off-diagonal elements of the density matrix—or the Wigner function can be reconstructed from the measured displaced populations _Q k_ (�). 

## 1. Reconstruction of the number-state density matrix 

As outlined above, the readily measurable quantities in an experiment are the number-state populations _Q k_ (�) of the coherently displaced unknown initial state characterized by the density matrix �. The quantities _Q k_ (�) are related to � by 

**==> picture [229 x 65] intentionally omitted <==**

with matrix elements 

**==> picture [229 x 64] intentionally omitted <==**

for every diagonal � _n_ , _n_ � _l_ of the density matrix. To keep the matrix dimension finite, a cutoff for the maximum _n_ in Eq. (151) is introduced, based on the magnitude of the input state. For an unknown input state, an upper bound on _n_ could be extracted from the populations _Q k_ (�). If these are negligible for _k_ higher than a certain _k_ max and all displacements �, they are negligible in the input state as well, and it is convenient to truncate Eq. (151) at _n_ max� _k_ max . The resulting matrix equation is overcomplete for some _l_ , but the diagonals � _n_ , _n_ � _l_ can still be reconstructed by a general linear least-squares method (Press _et al._ , 1992). 

**==> picture [229 x 12] intentionally omitted <==**

> where ��, _k_ � is a coherently displaced number state (Moya-Cessa and Knight 1993). Hence every _Q k_ (�) is the population of the displaced number state ��, _k_ � for an ensemble characterized by the input density matrix �. Rewriting Eq. (148) in terms of number-state densitymatrix elements � _n_ , _m_ yields 

**==> picture [228 x 158] intentionally omitted <==**

To separate the contributions of different matrix elements � _n_ , _m_ , one can choose the coherent displacements to lie on a circle in phase space, 

**==> picture [229 x 13] intentionally omitted <==**

where _p_ ��� _N_ , . . . , _N_ �1�. The number of angles 2 _N_ on that circle determines the maximum number of states _n_ max� _N_ �1 that can be included in the reconstruction. With a full set of measured populations _Q k_ (� _p_ ) of the state displaced along 2 _N_ points on a circle, a discrete Fourier transform of Eq. (149), evaluated at the values � _p_ , results in the following matrix equations: 

## 2. Reconstruction of s-parametrized quasiprobability distributions 

As pointed out by several authors, all _s_ -parametrized quasiprobability distributions _F_ (�, _s_ ) have a particularly simple representation when expressed in populations of displaced number states _Q k_ (�) (Royer, 1984; MoyaCessa and Knight, 1993; Banaszek and Wodkiewicz, 1996; Wallentowitz and Vogel, 1996): 

**==> picture [229 x 40] intentionally omitted <==**

For _s_ ��1 the sum breaks down to one term and _F_ (�,�1)� _Q_ 0(�)/� gives the value of the Husimi _Q_ quasiprobability distribution at the complex coordinate �. The reconstruction scheme of Poyatos, Walser, _et al._ (1996) is based on the Husimi _Q_ distribution. For _s_ �0 the Wigner function _F_ (�,0)� _W_ (�) for every point � in the complex plane can be determined by the single sum 

**==> picture [229 x 26] intentionally omitted <==**

In the reconstruction performed by the NIST group, the sum was carried out only to a finite _n_ max , as described above. Since truncation of the sum leads to artifacts in the quasiprobability distributions (Collett, 1996), the experimental data were averaged over different _n_ max . This smoothes out the artifacts to a high degree. 

In contrast to the density-matrix method described in Sec. VI.B.1, summing the displaced probabilities with their weighting factors provides a direct and local 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

314 

Leibfried et al.: Quantum dynamics of single trapped ions 

method of obtaining the quasiprobability distribution at the point � in phase space, without the need to measure at other values of �. This also distinguishes the method from experiments that determines the Wigner function by inversion of integral equations (tomography) (see, for example, Smithey _et al._ , 1993 and Dunn _et al._ , 1995). 

Finally, for a known density matrix the Wigner function can be derived by expanding Eq. (154) in the number-state basis, 

**==> picture [229 x 27] intentionally omitted <==**

with the matrix elements given by ( _l_ � _n_ ) (Cahill and Glauber, 1969) 

**==> picture [229 x 14] intentionally omitted <==**

where _L n_ ( _l_ � _n_ ) is a generalized Laguerre polynomial. Using this approach a plot of the Wigner function using reconstructed density-matrix data may be created (Leibfried, Meekhof, _et al._ , 1998). 

## 3. Experimental state reconstruction 

In the experiments of the NIST group (Leibfried _et al._ , 1996; Leibfried, Monroe, and Pfau, 1998), the coherent displacement needed for the reconstruction mapping was provided by a spatially uniform classical driving field at the trap oscillation frequency � (see Sec. VI.A.2). The field was applied on one of the trap compensation electrodes for a time of about 10 �s. The rf oscillators that created and displaced the states were phase locked to control their relative phase. Different displacements were realized by varying the amplitude and the phase of the displacement oscillator. For every displacement �, _P g_ ( _t_ ,�) was recorded. _Q n_ (�) was then extracted from the measured traces by a numerical singular-valued decomposition method (Press _et al._ , 1992). To determine the amplitude ��� of each displacement, the same driving field was applied to the � _n_ �0� ground state and the resulting collapse and revival trace (see Sec. VI.A.2) were fitted to that of a coherent state with the amplitude � as the only variable. 

The accuracy of the reconstruction was limited by the uncertainty in the applied displacements, the errors in the determination of the displaced populations, motional heating, and decoherence during the measurement. The value of the Wigner function was found by the sum, Eq. (154), with simple error propagation rules. The density matrix was reconstructed by a linear leastsquares method, and the error was estimated with the help of a covariance matrix (Press _et al._ , 1992). As the size of the input state increases, state preparation and the relative accuracy of the displacements become more critical, thereby increasing their uncertainties. 

Surface and contour plots of the Wigner function of an approximate � _n_ �1� number state are shown in Fig. 17. The plotted surface is the result of fitting a linear interpolation between the actual data points to a 0.1 �0.1 grid. The octagonal shape is an artifact of the eight 

**==> picture [241 x 188] intentionally omitted <==**

FIG. 17. Surface and contour plots of the reconstructed Wigner function _W_ (�) of an approximate _n_ �1 number state (Leibfried _et al._ , 1996). The negative values of _W_ (�) around the origin highlight the nonclassical nature of this state. 

measured phases per radius. The white contour represents _W_ (�)�0. The negative values around the origin highlight the nonclassical character of this state. The measured Wigner function _W_ (�) was rotationally symmetric within experimental errors. The minimum of the large negative part of the Wigner function around the origin has a value of �0.25, close to the largest negative value possible for a Wigner function in the chosen phase-space coordinates of �1/�. This highlights the fact that the prepared input state is very nonclassical. 

In contrast to the number state, the state closest to a classical state of motion in a harmonic oscillator is a coherent state. The reconstruction of the number-state density matrix of a small coherent state with amplitude ����0.67 is depicted in Fig. 18. The reconstructed offdiagonal elements are generally slightly smaller than those expected from the theory of a pure coherent state. In part this is attributed to decoherence during the measurement, so the reconstruction shows a mixed-state character rather than a pure coherent-state signature. 

The reconstructed Wigner function of a second coherent state with amplitude ����1.5 is shown in Fig. 19. The 

**==> picture [217 x 107] intentionally omitted <==**

FIG. 18. Experimental amplitudes � _nm_ and phases � _nm_ of the number-state density-matrix elements of an ����0.67 coherent state (Leibfried _et al._ , 1996). 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

315 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [241 x 184] intentionally omitted <==**

FIG. 19. Surface and contour plots of the reconstructed Wigner function _W_ (�) of an approximate coherent state (Leibfried _et al._ , 1996). The approximately Gaussian minimum-uncertainty wave packet is centered around a coherent amplitude of about 1.5 from the origin. The half width at half maximum is about 0.6, in accordance with the minimumuncertainty half width of ~~�~~ (1/2)ln(2)�0.59. 

plotted surface is the result of fitting a linear interpolation between the actual data points to a 0.13�0.13 grid. The approximately Gaussian minimum-uncertainty wave packet is centered around a coherent amplitude of about 1.5 from the origin. The half width at half maximum is about 0.6, in accordance with the minimumuncertainty half width of ~~�~~ ln(2)/2�0.59 in the chosen phase-space coordinates. To suppress truncation artifacts in the Wigner function summation (154), the data were averaged over _n_ max�5 and _n_ max�6. 

**==> picture [193 x 196] intentionally omitted <==**

FIG. 20. Reconstructed density-matrix amplitudes of an approximate (1/&)(�0�� _i_ �2�) number-state superposition. The amplitudes of the coherences indicate that the reconstructed density matrix is close to that of a pure state (Leibfried _et al._ , 1996). 

**==> picture [193 x 198] intentionally omitted <==**

FIG. 21. Reconstructed density-matrix amplitudes of a thermal distribution of states after imperfect Doppler cooling ( _¯n_ �1.3). As one would expect for a thermal distribution, no coherences are present within experimental uncertainties and the populations drop exponentially with _n_ (Leibfried _et al._ , 1996). 

The NIST group also created and reconstructed a coherent superposition of � _n_ �0� and � _n_ �2� number states. This state is ideally suited to demonstrate the sensitivity of the reconstruction to coherences. The only nonzero off-diagonal elements should be �02 and �20 , with a magnitude of ��02����20�� ~~�~~ �00�22�0.5 for a superposition with about equal probability of being measured in the � _n_ �0� or � _n_ �2� state. In the reconstruction shown in Fig. 20 the populations �00 and �22 are somewhat smaller, due to imperfections in the preparation, but the coherence has the expected value of ��20����02� ���00�22. 

Finally, a thermal distribution was generated by only Doppler cooling the ion. The reconstruction of the resulting state is depicted in Fig. 21. As expected, there are no coherences, and the diagonal, which gives the number-state occupation, shows an exponential behavior within the experimental errors, indicating a mean occupation number _¯n_ �1.3. 

## VII. QUANTUM DECOHERENCE IN THE MOTION OF A SINGLE ATOM 

Decoherence in quantum systems (for an overview see Zurek, 2001, and references therein) has been a subject of enduring interest because it relates to the fundamental distinction between quantum and classical behavior. More recently, quantum decoherence has come to the forefront because it is the most significant obstacle for applications in quantum information science (DiVincenzo, 2001). We shall review the decoherence studies of motional quantum states of a single harmonically bound atom. Since this problem is closely related to decoherence of superposition states of a single mode 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

316 

Leibfried et al.: Quantum dynamics of single trapped ions 

of the electromagnetic field, a large body of theoretical research in quantum optics can be applied.[6] 

As was briefly discussed in Sec. VI.A.5, arbitrary states of motion of a single atom can be prepared (in principle) using a variety of techniques. Following the discussion in Sec. VI.A.4, the motional and internal states can be manipulated with coherent radiation, generating operations of the form 

**==> picture [229 x 12] intentionally omitted <==**

This operation faithfully maps the motional state under study to the internal state, which can subsequently be measured with high accuracy. Before this mapping/ measurement step, superpositions of motional states can decay naturally due to ambient fluctuating fields. Applying larger fields that dominate over the ambient level improves experimental control and increases the data rate. More importantly, applying different types of decohering fields before mapping/measurement allows the study of a more general class of reservoir couplings. 

## A. Decoherence background 

Consider the decoherence of a superposition state _c_ 1��1�� _c_ 2��2�, where ��1� and ��2� are states of a single mode of motion. This mode of motion will be taken as the quantum ‘‘system’’ under investigation. In a basic model of decoherence (Zurek, 1991, 2001), it is assumed that the mode couples to an external environment having initial state �� _e_ �. The total initial state of the motion and environment is thus �0�( _c_ 1��1�� _c_ 2��2�) � �� _e_ �. Due to the coupling between the system and the environment, the joint state evolves to 

**==> picture [230 x 30] intentionally omitted <==**

To illustrate how this causes decoherence, we assume the coupling is such that ���1�� _e[i]_[�][1] ��1� and ���2� � _e[i]_[�][2] ��2�; then, after the interaction, �final � _c_ 1��1��� _e_ 1�� _e[i]_[(][�][2][�][�][1][)] _c_ 2��2��� _e_ 2�, with the initial states of the system correlated with different states of the environment. For strong coupling, the environmental states will typically be distinct, with �� _e_ 2�� _e_ 1��0. Now if the final environmental states are uncontrolled and unmeasured, these degrees of freedom must be ignored or mathematically traced over. In this case, the pure state �final becomes a statistical mixture expressed by the density matrix �final�� _c_ 1�[2] ��1���1� �� _c_ 2�[2] ��2���2�. Hence the off-diagonal or coherence terms of the pure-state density matrix ( _c_ 1��1� � _c_ 2��2�)( _c_ *1 ��1�� _c_ 2*��2�) are lost to the environment. 

6See, for example, Caldeira and Leggett, 1985; Walls and Milburn, 1985; Collett, 1988; Zurek, 1991; Vogel and Welsch, 1994; Buz[ˇ] ek and Knight, 1995; Poyatos, Cirac, and Zoller, 1996; Schleich, 2001. 

It is sometimes useful to incorporate a quantum measuring device or quantum ‘‘meter’’ into the scheme above using a von Neumann chain (Zurek, 1991). Here it is assumed that the quantum system, initially given by _c_ 1��1�� _c_ 2��2�, is first coupled to a quantum meter and the combination is then coupled to the environment. In the first stage of coupling, 

**==> picture [130 x 12] intentionally omitted <==**

**==> picture [230 x 12] intentionally omitted <==**

Upon coupling to the environment, the evolution is 

**==> picture [151 x 12] intentionally omitted <==**

**==> picture [230 x 11] intentionally omitted <==**

**==> picture [247 x 67] intentionally omitted <==**

Thus the correlation between the system and meter states is established, yielding the expected classical result, but the quantum coherence is lost. Including the quantum meter more closely describes the ion experiments discussed below because the system (the ion’s motion) is not directly measured but is instead coupled to the ion’s internal state, which acts as the meter. 

## B. Decoherence reservoirs 

Below, several simple decoherence reservoirs are discussed, and experimental demonstrations of decoherence in these reservoirs are summarized. Decoherence of harmonic-oscillator superposition states into a variety of reservoir environments has been investigated extensively in theory; see, for example, Caldeira and Leggett (1985), Walls and Milburn (1985, 1995), Collett (1988), Zurek (1991), Buz[ˇ] ek and Knight (1995), and Poyatos, Cirac, and Zoller (1996). Typically a system harmonic oscillator is coupled to a bath of environmental quantum oscillators, with particular couplings determined by the type of reservoir. 

## 1. High-temperature amplitude reservoir 

The interaction Hamiltonian for amplitude damping is 

**==> picture [229 x 26] intentionally omitted <==**

where _a_ is the lowering operator for the system oscillator, _b_ † _i_ is the raising operator for the _i_ th environmental oscillator, and � _i_ gives the strength of coupling between the system oscillator and the _i_ th environmental oscillator. The case in which the system oscillator is a single mode of the electromagnetic field has been investigated in the experiments of Brune, Hagley, _et al._ (1996). This model and similar ones specific to trapped-ion experiments are discussed theoretically (Murao and Knight, 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

317 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [193 x 142] intentionally omitted <==**

FIG. 22. Phase-space representation of interference experiment (Ramsey, 1963) for coherent-state superpositions coupled to an amplitude reservoir (from Myatt _et al._ , 2000 and Turchette, Myatt, _et al._ , 2000). Starting from the initial system/ meter state ���0�� _g_ �, the Schro[¨] dinger-cat state shown in panel (2) is created by applying a �/2 pulse on the internal state followed by a state-dependent optical dipole force. Noise is then applied to the motion simulating coupling to a hot resistor. This causes a random displacement � as shown in panel (3). The steps used to create the cat state are then reversed, but with a phase shift � _R_ on the final �/2 pulse. Finally, the probability _P g_ of finding the ion in the � _g_ � internal state is measured. Ideally, this results in _P g_ � 2[1][�][1][�][cos][�][�] _R_ �2 Im(�*��)��, having the sinusoidal oscillations with � _R_ characteristic of Ramsey interferometry. Noise reduces the Ramsey fringe contrast because � must be averaged over a distribution of values. For Gaussian noise with variance ��, this yields a contrast of exp(�4��2����2). 

1998; Schneider and Milburn, 1998, 1999; Wineland _et al._ , 1998; Bonifacio _et al._ , 2000). One model assumes that the motion of a trapped ion couples to the (noisy) uniform electric field **E** caused by the environmental oscillators through the potential _U_ �� _Z_ � _e_ � **x"E** , where _Z_ � _e_ � is the ion’s charge and **x** its displacement from the equilibrium position. Such a model corresponds to the case of a noisy electric field due to a resistor coupled between the trap electrodes (Wineland and Dehmelt, 1975b; Wineland _et al._ , 1998) and is described by the Hamiltonian in Eq. (162). 

In the experiments, a hot resistor is simulated by applying a random uniform electric field between the electrodes that has some spectral amplitude at the ion’s motional frequency � (Myatt _et al._ , 2000; Turchette, Myatt, _et al._ , 2000). This is achieved using a commercial function generator producing pseudorandom voltages that is connected through a bandpass filter to one of the trap electrodes. The initial coherence and subsequent decoherence of the motional-state superpositions were measured using single-atom interferometry, as described in detail by Myatt _et al._ (2000) and Turchette, Myatt, _et al._ (2000). 

Briefly, an initial state of the type shown in the lefthand side of Eq. (160) was first created, with ��1�� ����, �� _M_ 1��� _e_ �, ��2�������, �� _M_ 2��� _g_ �, and _c_ 1� _c_ 2 �1/&. This is illustrated schematically in part (2) of Fig. � 22. Here ��� and �� � are coherent states of amplitudes � � and � . 

**==> picture [241 x 203] intentionally omitted <==**

FIG. 23. Loss of coherence of a Schro[¨] dinger-cat state caused by coupling to an amplitude reservoir (from Myatt _et al._ , 2000). Amplitude noise was applied for a fixed duration of 3 �s but with varying amplitude. The fringe contrast for all experiments is normalized to that observed in the absence of applied noise. The scaling shows that the decoherence rate is proportional to the square of the phase-space separation �� of the superposition components. 

After preparation, the superposition was exposed to the fluctuating field for a fixed time [Fig. 22, part (3)]. The components of the motional-state superposition were then recombined by reversing the steps that created it [Fig. 22, part (4)] and a final �/2 pulse was applied to the internal states. Finally, the internal state was measured. This sequence was repeated many times for various values of the relative phase � _R_ between the creation and reversal steps. The contrast of the resulting interference fringe characterizes the amount of coherence remaining in the final state. The results are displayed in Fig. 23. The contrast of the fringe decays as exp(��������[2] � _En_ 2�), where ~~�~~ � _E n_ 2� is the root-meansquare value of the applied noise and � is a constant. Similar scaling was also observed for the ambient fluctuating fields after exposure for varying times (Myatt _et al._ , 2000; Turchette, Myatt, _et al._ , 2000). The exponential dependence of the decoherence rate on the size of � � the cat state ����� � � agrees with theoretical predictions and indicates why it is difficult to preserve superpositions on a macroscopic scale. 

The experimental situation here is slightly different from the theoretical models outlined above. First, the environment acted only on the system (motional state) and not the meter (internal state), so that �� _M_ � 1� ��� _M_ 1� and �� _M_ � 2���� _M_ 2� in Eq. (160). In addition, in this case the action of the system on the environment is nearly negligible, so that �� _e_ 1���� _e_ 2���� _e_ �. Because the noise voltage _E n_ in this experiment could, in principle, be measured classically without disturbing �� _e_ � appreciably one could subsequently apply an operation to the ion that reverses the environmental effect. In practice this could be readily done for the engineered noise 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

318 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [193 x 137] intentionally omitted <==**

FIG. 24. Technique for implementing a zero-temperature environment (Myatt _et al._ , 2000). A pair of laser beams drives the � _g_ �� _n_ � _↔_ � _e_ �� _n_ �1� transition at rate �, while spontaneous Raman scattering is used to make transitions � _e_ �� _n_ � to � _g_ �� _n_ � at rate �. When ���, the internal states together with the spontaneous events act as a _T_ �0 reservoir for motional states. 

but not for the ambient noise. Without performing such a measurement, however, it is necessary to average over the possible environmental states ��� _e_ ��, and this leads to the decoherence exhibited in Fig. 23. 

## 2. Zero-temperature amplitude reservoir 

In the cavity QED decoherence experiments of Brune, Hagley, _et al._ (1996), the system oscillator frequency was around 50 GHz and the ambient temperature was _T_ �0.6 K, so the quantum number of the equilibrium oscillator was around 0.05 and the reservoir temperature was effectively near zero. In the ion experiments, the oscillator frequency was around 5 MHz and the ambient temperature was 300 K or greater, implying a very large equilibrium oscillator number (Turchette, Kielpinski, _et al._ , 2000). Nevertheless, it is possible to simulate a _T_ �0 reservoir for the ions, following a sug- 

gestion by Poyatos, Cirac, and Zoller (1996). The technique relies on laser cooling, as illustrated in Fig. 24. Coherent Raman beams drive the � _g_ �� _n_ � _↔_ � _e_ �� _n_ �1� transition with Rabi rate �. At the same time, an optical pumping beam causes spontaneous Raman transitions from � _e_ �� _n_ � to � _g_ �� _n_ � at rate �. From the diagram in Fig. 24, it is clear that all populations tend towards the state � _g_ ��0�, which is characteristic of a _T_ �0 reservoir. By varying the intensities of the lasers, the reservoir parameters can be experimentally controlled. 

In these experiments, the evolution of the initial state �� 1/& (�0���2�)� _g_ � was observed for varying lengths of reservoir interaction time. The coherence was measured using an interference experiment similar to that of the previous section. However, here the internal state serves several functions: it allows the preparation of the motional superposition and is the quantity ultimately measured, but also, in the middle of any particular experiment, it acts as part of the environment due to the coupling of Fig. 24. The resulting data are shown in Fig. 25, where each point is the contrast of the interference fringes after interacting with the reservoir for the given time. Two cases are shown, ��� and ���. In the first case, the coherence simply decays due to coupling to the reservoir. Here it is natural to take the reservoir to be the internal state plus the rest of the environment, which includes the spontaneously scattered photons. The initial nonexponential decay is a manifestation of the quantum Zeno effect (Myatt _et al._ , 2000; Turchette, Myatt, _et al._ , 2000) and arises because the condition ��� is not rigorously satisfied. In contrast, when ��� the coherence between the �0� and �2� states disappears and reappears over time, with an overall decay of the fringe contrast. The underlying effect is population transfer back and forth (Rabi oscillation) between the states � _g_ ��2� and � _e_ ��1�. Indeed, for � _→_ 0, near-perfect revival of the 

**==> picture [293 x 247] intentionally omitted <==**

FIG. 25. Decoherence of the motional superposition state 1/& (�0���2�) coupled to the engineered zero-temperature reservoir (from Myatt _et al._ , 2000 and Turchette, Myatt, _et al._ , 2000). The superposition is prepared with a sequence of laser pulses and the reservoir applied for a variable time. The preparation pulses are then reversed with a variable phase shift, and the final state is recorded as a function of this phase. The data show the contrast of the resulting interference pattern for two cases of the relative values of � and �. The initial contrast is not unity due to imperfections in the state preparation and reversal pulses. 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

319 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [297 x 246] intentionally omitted <==**

FIG. 26. Loss of coherence of various Fockstate superpositions caused by coupling to a phase reservoir (from Myatt _et al._ , 2000). Phase noise was applied for a fixed duration of 20 �s but with varying amplitude. The fringe contrast for all experiments is normalized to that observed in the absence of applied noise. The scaling shows that the decoherence rate is proportional to the square of the Fock-state number � _n_ of the superposition components. 

fringe contrast is obtained (Turchette, Myatt, _et al._ , 2000), since in this case the environment is restricted to just the internal states and the apparent decoherence is easily reversed. A scheme for observing a similar reversal in the context of cavity QED is discussed in Raimond _et al._ (1997). 

In the zero-temperature experiment with ��0, once the atom scatters a photon through the spontaneous Raman process, no measurement can be made even in principle to restore the initial superposition. That is, the emission (and subsequent absorption by a measuring apparatus or the environment) of a spontaneous photon projects the atom into a definite state (� _g_ ��1� in the context of Fig. 24) and phase information is irreversibly lost. This situation is identical to that of the cavity experiments of Brune, Hagley, _et al._ (1996). The decoherence in this second ion experiment can be contrasted with the first, in which the environment could, in principle, be measured and its effects reversed. The data for ��� do illustrate how coherence lost to the environment can be recovered, and an alternative explanation states that transferring the � _g_ ��2� component of the superposition to the � _e_ ��1� state provides ‘‘which-path’’ information in the interferometer—the paths being the � _g_ ��0� and � _g_ ��2� parts of the superposition. The oscillation in which-path information is analogous to that seen in the experiments of Chapman _et al._ (1995), Du[¨] rr _et al._ (1998), Bertet _et al._ (2001), and Kokorowski _et al._ (2001). 

The zero-temperature experiment also illustrates a fundamental dilemma in explaining decoherence. If the environment is restricted to be the internal state by taking � _→_ 0, then the coherence information can be recovered. Even in the case of spontaneous emission, coherence need not be lost if the photon is emitted into a high-quality cavity from which it can later be recovered, as has been observed in the cavity QED experiments (Maı[ˆ] tre _et al._ , 1997; Varcoe _et al._ , 2000). Therefore it 

seems that decoherence is needed only to describe situations in which, for practical or technical reasons, information pertaining to the overall system is lost. These limitations seem only to be practical and not fundamental unless some mechanism that is so far missing in quantum mechanics is found to cause intrinsic decoherence. For a summary of such alternatives, see Leggett (1999). 

## 3. High-temperature phase reservoir 

The interaction Hamiltonian for a phase damping is 

**==> picture [229 x 26] intentionally omitted <==**

This interaction does not change the energy of the system oscillator and can be considered a model for quantum-nondemolition measurements (Walls and Milburn, 1985). 

In the experiments, a phase reservoir is realized by modulating the trap frequency, thus advancing (or retarding) the phase of harmonic motion in the trap. Gaussian noise is symmetrically applied to the trap electrodes to produce a noisy electric-field gradient, and the noise is uniform up to a cutoff frequency well below the trap frequency so that no energy is transferred to the ion motion. 

Motional decoherence caused by this phase noise is most clearly demonstrated in a superposition of Fock states of the form _c_ 1� _n_ �� _c_ 2� _n_ ��. Similar techniques to that described above were used to characterize phase decoherence in a variety of Fock-state superpositions (Myatt _et al._ , 2000; Turchette, Myatt, _et al._ , 2000), and the results are plotted in Fig. 26. In analogy to the case of amplitude damping, we find that the decoherence rate scales with the square of the distance between the superposition’s constituents, here meaning the squared difference in Fock-state indices. 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

320 

Leibfried et al.: Quantum dynamics of single trapped ions 

## C. Ambient decoherence in ion traps 

The ambient motional decoherence observed in all experiments can be characterized by high-temperature amplitude damping: its characteristics are the same as those caused by thermal electronic noise in the resistance of the electrodes or resistance coupled to the electrodes. At the relatively low ion oscillation frequencies, where the characteristic wavelength is much larger than the electrode spacing, the ambient decoherence is adequately described by thermal (Johnson) noise associated with lumped circuit elements attached to the electrodes, or equivalently, thermally fluctuating dipole oscillators in the electrode bulk (Turchette, Kielpinski, _et al._ , 2000). 

Typical heating rates (expressed as quanta per second from the motional ground state) are observed to be around � _dn_ / _dt_ ��10[3] �10[4] s[�][1] for � _z_ �10 MHz, and the distance from the ion to the nearest electrode surface is around 150 �m (Turchette, Kielpinski, _et al._ , 2000). However, given the estimated electrode resistance (Wineland _et al._ , 1998) and attached circuit elements, an electrode temperature of 10[6] K or greater is needed to explain most of the heating results (Turchette, Kielpinski, _et al._ , 2000). The principle cause of the anomalously large heating is not understood at this time, but some of its characteristics have been determined. The fluctuating field has no sharp spectral features in the range from 2 to 20 MHz, and it seems to be emanating from the electrodes themselves. More local-field sources such as collisions with background gas or free electrons are ruled out because these collisional sources would heat the internal modes of two ions at nearly the same rate as the center-of-mass modes. However, the internal mode heating is observed to be negligible compared to the heating of the center-of-mass modes (King _et al._ , 1998), indicating that the fields at the site of the ions are approximately uniform spatially. [We note that the experiments of Rohde _et al._ (2001) disagree with this finding.] In contrast, a more distant field source, such as electrical noise from laboratory equipment, is contradicted by observations that the heating rate depends sensitively on the trap size _R_ , scaling typically as _R_[�][�] for � on the order of 5. Thermal noise arising from circuit resistance should scale as ��2 (Wineland _et al._ , 1998), but noise from fluctuating patch potentials on the electrode surfaces is predicted to scale as ��4 (Turchette, Kielpinski, _et al._ , 2000). The scatter of the data for[9] Be[�] ions is rather large but is consistent with the patch potential model. Data on other traps (Diedrich _et al._ , 1989; Rohde _et al._ , 2001) also appear to be consistent with this value of �. 

Previous experiments (Turchette, Kielpinski, _et al._ , 2000) have given some indication that beryllium deposition onto the electrodes causes a higher heating rate. Such deposition occurs because these ions are created by ionization neutral beryllium atoms that pass near the center of the trap after being emitted from a wide-angle source. In this process, some of the atoms from the source miss the trap and are deposited on the electrodes. Preliminary evidence indicates that, by physically mask- 

ing the electrodes from direct deposition, one can achieve a decrease in heating rate by a factor on the order of 100 (Rowe _et al._ , 2002). In any case, we conjecture that for clean metal electrode surfaces, free from oxides or adsorbed gases that could support mobile electrons, the heating should approach that predicted by thermal electronic noise � _dn_ / _dt_ ��1 s[�][1] . 

## VIII. CONCLUSIONS 

Single ions confined in rf traps offer two nearly ideal basic quantum systems, a two-level system, represented by two of the internal electronic states, and an approximate harmonic oscillator, represented by the motion. With appropriate light fields these two subsystems can be coupled in a number of ways, leading to a wealth of possible studies. In this review the underlying theory and a number of experiments utilizing this system have been discussed, with special emphasis on laser cooling, resonance fluorescence, quantum-state engineering, quantum-state reconstruction, and motional decoherence of single ions. 

This system will continue to be studied and, very likely in the future, much more complicated superposition states will be realized. Although an important goal of ion-trap experiments is to realize arbitrary entangled states for many ions, as required in quantum computing, for example, the single-ion experiments discussed here will continue to be the test bed for studies of operation fidelity and decoherence. 

## ACKNOWLEDGMENTS 

We want to thank James Bergquist, John Bollinger, Ignacio Cirac, Ju[¨] rgen Eschner, Wayne Itano, Steven Jefferts, David Kielpinski, Brian King, Christopher Langer, Dawn Meekhof, Volker Meyer, Giovanna Morigi, Christopher Myatt, Hanns-Christoph Na[¨] gerl, Christian Roos, Mary Rowe, Cass Sackett, Ferdinand Schmidt-Kaler, Quentin Turchette, Christopher Wood, and Peter Zoller for their cooperation and many stimulating discussions. Work at the University of Innsbruck was supported by the Austrian Fonds zur Fo[¨] rderung der wissenschaftlichen Forschung (Grant No. SFB15 and START Grant No. Y147-PHY), by the European Commission [TMR networks ‘‘Quantum Information’’ (Grant No. ERBFRMX-CT96-0087) and ‘‘Quantum Structures’’ (Grant No. ERB-FMRX-CT96-0077)], and by the Institut fu[¨] r Quanteninformation GmbH. Work at NIST was supported by NSA/ARDA, ONR, ARO, and NRO. Work at Michigan was supported by NSA/ARDA, ARO, and NSF. 

## APPENDIX: COUPLINGS OF LIGHT FIELDS TO THE INTERNAL ELECTRONIC STATE 

The coupling of electromagnetic fields to charges is a complex subject. It has been extensively studied, for example, by Cohen-Tannoudji _et al._ (1989). Deriving the relevant interaction Hamiltonians _H I_ from first prin- 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

321 

Leibfried et al.: Quantum dynamics of single trapped ions 

ciples is beyond the scope of this review, so we shall restrict ourselves to stating these Hamiltonians and listing their properties as far as they are necessary to describe the atom-field couplings studied here. In all cases the electromagnetic field(s) will not be quantized, but treated as a classical plane-wave field of the form 

**==> picture [229 x 13] intentionally omitted <==**

with the real field amplitude **E** 0 . We shall assume (a) that ��� _E e_ � _E g_ so all electronic states except � _g_ � and � _e_ � can be neglected and (b) that all ac Stark shifts, represented by the diagonal elements � _j_ � _H I_ � _j_ �, _j_ �� _g_ , _e_ �, are lumped into the definitions of _E j_ , namely, _E j_ � _E j_ 0 �� _j_ � _H I_ � _j_ �, where _E j_ 0 is the energy of level _j_ in absence of the coupling. We can then expand _H I_ in the remaining off-diagonal terms, 

**==> picture [229 x 12] intentionally omitted <==**

where we have chosen a convention in which the matrix element � _g_ � _H I_ � _e_ � is real. 

In the remainder of this appendix we shall study these matrix elements for the types of transitions used in the described experiments. Doppler cooling and fluorescence experiments relied on dipole transitions. Experiments with resolved sidebands relied on the excitation of quadrupole transitions or stimulated Raman transitions between two long-lived states. 

## 1. Dipole coupling 

For dipole coupling to a single outer-shell electron the interaction Hamiltonian is 

**==> picture [229 x 26] intentionally omitted <==**

For a plane-wave electric field like Eq. (A1) the Hamiltonian simplifies to 

**==> picture [229 x 23] intentionally omitted <==**

and the matrix element is 

**==> picture [229 x 43] intentionally omitted <==**

Comparison of this equation with Eq. (62) yields 

**==> picture [229 x 12] intentionally omitted <==**

for quadrupole transitions, where the phase factor �/2 is lumped into � in Eq. (62). Since the quadrupole interaction is an even function of position, only matrix elements between states of the same parity differ from zero. Again the actual numerical value of the matrix element depends on the angular momentum values of � _g_ � and � _e_ � and the field polarization [see, for example, James (1998)]. To relate the order of magnitude of quadrupole transition matrix elements to those of the more familiar dipole transitions, one can deduce from Eqs. (A10) and (A5) that their approximate ratio is _a_ 0 _k_ �10[�][3] – 10[�][4] , where _a_ 0 is the Bohr radius, so quadrupole transitions have a much weaker decay and higher saturation intensity when driven by a laser source. 

**==> picture [229 x 11] intentionally omitted <==**

with the electron charge _e_ � . For a plane-wave electric field of the form of Eq. (A1) this becomes 

**==> picture [229 x 13] intentionally omitted <==**

and the matrix element is 

**==> picture [229 x 13] intentionally omitted <==**

Comparison of this equation with Eq. (62) yields 

**==> picture [229 x 11] intentionally omitted <==**

for dipole transitions. Since the dipole interaction is an odd function of position, only matrix elements between states of opposite parity differ from zero. The actual numerical value of the matrix element depends on the angular momentum values of � _g_ � and � _e_ � and the field polarization. Details on this can be found, for example, in James (1998). 

## 2. Quadrupole coupling 

For quadrupole coupling to a single outer-shell electron the interaction Hamiltonian is 

**==> picture [229 x 24] intentionally omitted <==**

with the quadrupole tensor 

## 3. Raman coupling 

An alternative way to create an effective two-level system is to couple two ground-state levels by twophoton stimulated Raman transitions (Heinzen and Wineland, 1990; Monroe _et al._ , 1995). The Raman transitions are induced by two light fields whose frequency difference matches the separation of the two groundstate levels (plus the relatively small detunings to, for example, a sideband). Each beam is close to resonance with an allowed dipole transition to a short-lived excited electronic state �3� but sufficiently detuned to make population of that state negligible. While the coupling is enhanced, the near-resonant excited state can be adiabatically eliminated in the theoretical treatment (Wineland _et al._ , 1998), leaving an effective two-level coupling between the two ground states. The coupling is formally equivalent to a narrow single-photon transition if one makes the following identifications: 

**==> picture [229 x 26] intentionally omitted <==**

Here �1 , **k** 1 (�2 , **k** 2) are the frequency and wave vector of the light fields coupling � _e_ � (� _g_ �) to �3�. If both fields are detuned from resonance by � _R_ , the coupling strength is given by 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

322 

Leibfried et al.: Quantum dynamics of single trapped ions 

**==> picture [229 x 26] intentionally omitted <==**

where �� _g_ 3 and �� _e_ 3 are the dipole matrix elements of � _g_ � and � _e_ � to �3� as discussed above and ��is the phase difference of the two light fields. This phase difference can be lumped into � in Eq. (62). 

The experimental advantages of stimulated Raman transitions lie in the fact that they combine strong optical electric-field gradients with good stability of the crucial frequency difference. The frequency difference usually is in the GHz range and can therefore be synthesized by rf sources with very long (� hours) coherence time. The linewidth of the laser plays a negligible role as long as it is small compared to the detuning � _R_ . The coupling strength can be considerably higher than that for narrow one-photon transitions to metastable levels (e.g., quadrupole transitions) for the same laser power. However, the coupling can lead to ac Stark shifts on the order of the Rabi frequency that have to be controlled and accounted for or compensated by judicious choice of polarizations, beam intensities, and detunings. The fact that the effective **k** is the vector difference of the two light-field wave vectors allows for variation of **k** by changing the relative angle of the two propagation directions. As a consequence the LambDicke factor can be tuned from almost zero [copropagating beams, ��(� _k_ 1��� _k_ 2�) _x_ 0] to ��(� _k_ 1��� _k_ 2�) _x_ 0 (counterpropagating beams). The ability to make transitions motionally insensitive (��0) can be very helpful in certain experimental situations. 

Blu[¨] mel, R., C. Kappler, W. Quint, and H. Walther, 1989, Phys. Rev. A **40** , 808. 

Bonifacio, R., S. Olivares, P. Tombesi, and D. Vitali, 2000, Phys. Rev. A **61** , 053802. 

Brown, L. S., 1991, Phys. Rev. Lett. **66** , 527. 

Brown, L. S., and G. Gabrielse, 1986, Rev. Mod. Phys. **58** , 233. 

Brune, M., E. Hagley, J. Dreyer, X. Maitre, A. Maali, C. Wunderlich, J. M. Raimond, and S. Haroche, 1996, Phys. Rev. Lett. **77** , 4887. 

Brune, M., F. Schmidt-Kaler, A. Maali, J. Dreyer, E. Hagley, J. M. Raimond, and S. Haroche, 1996, Phys. Rev. Lett. **76** , 1800. Budini, A. A., R. L. de Matos Filho, and N. Zagury, 2002, Phys. Rev. A **65** , 041402. 

Bu[¨] hner, V., Dissertation 2001, Physikalisch-Technischen Bundesanstalt Braunschweig, PTB-Opt-63. 

Bu[¨] hner, V., and C. Tamm, 2000, Phys. Rev. A **61** , 061801(R). Buz[ˇ] ek, V., and P. L. Knight, 1995, Prog. Opt. **34** , 1. 

Cahill, K. E., and R. J. Glauber, 1969, Phys. Rev. **177** , 1857. 

Caldeira, A. O., and A. J. Leggett, 1985, Phys. Rev. A **31** , 1059. Carmichael, H. J., and D. F. Walls, 1976, J. Phys. B **9** , L43. 

Carruthers, P., and M. M. Nieto, 1965, Am. J. Phys. **7** , 537. 

Chapman, M. S., T. D. Hammond, A. Lenef, J. Schmiedmayer, R. A. Rubenstein, E. Smith, and D. E. Pritchard, 1995, Phys. Rev. Lett. **75** , 3783. 

Cirac, J. I., R. Blatt, A. S. Parkins, and P. Zoller, 1993, Phys. Rev. Lett. **70** , 762. 

Cirac, J. I., R. Blatt, and P. Zoller, 1994, Phys. Rev. A **49** , R3174. 

Cirac, J. I., R. Blatt, P. Zoller, and W. D. Philips, 1992, Phys. Rev. A **46** , 2668. 

- Cirac, J. I., L. J. Garay, R. Blatt, A. S. Parkins, and P. Zoller, 1994, Phys. Rev. A **49** , 421. 

Cirac, J. I., A. S. Parkins, R. Blatt, and P. Zoller, 1993, Phys. Rev. Lett. **70** , 556. 

## REFERENCES 

- Abramowitz, M., and I. A. Stegun, 1972, _Handbook of Mathematical Functions_ , NBS Applied Mathematics Series No. 55 (Dover, New York). 

- Alheit, R., Th. Gudjons, S. Kleineidam, and G. Werth, 1996, Rapid Commun. Mass Spectrom. **10** , 583. 

- Banaszek, K., and K. Wodkiewicz, 1996, Phys. Rev. Lett. **76** , 4344. 

- Bardroff, P. J., M. T. Fontenelle, and S. Stenholm, 1999, Phys. Rev. A **59** , R950. 

- Bardroff, P. J., C. Leichtle, G. Schrade, and W. P. Schleich, 1996, Acta Phys. Slov. **46** , 1. 

- Bennett, C. H., 1996, Phys. Today **48** , 24. 

- Bergquist, J. C., R. G. Hulet, W. M. Itano, and D. J. Wineland, 1986, Phys. Rev. Lett. **57** , 1699. 

- Berkeland, D. J., J. D. Miller, J. C. Bergquist, W. M. Itano, and D. J. Wineland, 1998, J. Appl. Phys. **83** , 5025. 

- Bertet, P., S. Osnaghi, A. Rauschenbeutel, G. Nogues, A. Auffeves, M. Brune, J. M. Raimond, and S. Haroche, 2001, Science **411** , 166. 

- Blatt, R., J. I. Cirac, and P. Zoller, 1995, Phys. Rev. A **52** , 518. 

- Blatt, R., M. Schubert, I. Siemers, W. Neuhauser, and W. Vogel, 1993, in _Fundamentals of Quantum Optics III_ , edited by F. Ehlotzky, Lecture Notes in Physics No. 420 (Springer, Berlin/Heidelberg), p. 156. 

- Blatt, R., and P. Zoller, 1988, Eur. J. Phys. **9** , 250. 

- Blockley, C. A., D. F. Walls, and H. Risken, 1992, Europhys. Lett. **17** , 509. 

Cirac, J. I., and P. Zoller, 1995, Phys. Rev. Lett. **74** , 4091. 

Cohen-Tannoudji, C., J. Dupont-Roc, and G. Grynberg, 1989, _Photons & Atoms_ (Wiley, New York). 

Collett, M. J., 1988, Phys. Rev. A **38** , 2233. 

- Collet, M. J., 1996, private communication. 

Combescure, M., 1986, Ann. I. H. P. Phys. Theor. **44** , 293. 

- Cook, R. J., D. G. Shankland, and A. L. Wells, 1985, Phys. Rev. A **31** , 564. 

Dehmelt, H. G., 1967, Adv. At. Mol. Phys. **3** , 53. 

Dehmelt, H. G., 1973, Bull. Am. Phys. Soc. **18** , 1521. 

Dehmelt, H. G., 1975, Bull. Am. Phys. Soc. **20** , 60. 

DeVoe, R. G., J. Hoffnagle, and R. G. Brewer, 1989, Phys. Rev. A **39** , 4362. 

- D’Helon, C., and G. J. Milburn, 1996, Phys. Rev. A **54** , R25. 

Diddams, S. A., Th. Udem, J. C. Bergquist, E. A. Curtis, R. E. Drullinger, L. Hollberg, W. M. Itano, W. D. Lee, C. W. Oates, 

- K. R. Vogel, and D. J. Wineland, 2001, Science **293** , 825. 

Diedrich, F., J. C. Bergquist, W. M. Itano, and D. J. Wineland, 1989, Phys. Rev. Lett. **62** , 403. 

- Diedrich, F., E. Peik, J. M. Chen, W. Quint, and H. Walther, 1987, Phys. Rev. Lett. **59** , 2931. 

Diedrich, F., and H. Walther, 1987, Phys. Rev. Lett. **58** , 203. 

Di Fidio, C., and W. Vogel, 2000, Phys. Rev. A **62** , 031802. 

DiVincenzo, D. P., 2001, in _Scalable Quantum Computers_ , edited by S. L. Braunstein and H. K. Lo (Wiley-VCH, Berlin), p. 1. 

Drewsen, M., C. Brodersen, L. Hornekaer, J. S. Hangst, and J. P. Schiffer, 1998, Phys. Rev. Lett. **81** , 2878. 

Drewsen, M., and A. Brøner, 2000, Phys. Rev. A **62** , 045401. 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

323 

Leibfried et al.: Quantum dynamics of single trapped ions 

- Dunn, T. J., I. A. Walmsley, and S. Mukamel, 1995, Phys. Rev. Lett. **74** , 884. 

- Du[¨] rr, S., T. Nonn, and G. Rempe, 1998, Phys. Rev. Lett. **81** , 5705. 

- Eberly, J. H., N. B. Narozhny, and J. J. Sanchez-Mondragon, 1980, Phys. Rev. Lett. **44** , 1323. 

Ekert, A., and R. Josza, 1996, Rev. Mod. Phys. **68** , 733. Englert, B.-G., M. Lo[¨] ffler, O. Benson, B. Varcoe, M. Weidinger, and H. Walther, 1998, Fortschr. Phys. **46** , 897. 

- Erber, T., and S. Puttermann, 1985, Nature (London) **318** , 41. 

- Eschner, J., B. Appasamy, and P. E. Toschek, 1995, Phys. Rev. Lett. **74** , 2435. 

- Eschner, J., Ch. Raab, F. Schmidt-Kaler, and R. Blatt, 2001, Nature (London) **413** , 495. 

- Freyberger, M., 1997, Phys. Rev. A **55** , 4120. 

- Gardiner, S. A., J. I. Cirac, and P. Zoller, 1997, Phys. Rev. A **55** , 1683. 

- Glauber, R. J., 1963, Phys. Rev. **131** , 2766. 

- Glauber, R. J., 1964, in _Quantum Optics and Electronics_ , edited by C. DeWitt, A. Blandin, and C. Cohen-Tannoudji (Gordon and Breach, New York), p. 64. 

- Glauber, R. J., 1992, in _Laser Manipulation of Atoms and Ions_ , Proceedings of the International School of Physics ‘‘Enrico Fermi’’ Course 118, edited by E. Arimondo, W. D. Phillips, and F. Strumia (North-Holland, Amsterdam), p. 643. 

- Gosh, P. K., 1995, _Ion Traps_ (Clarendon, Oxford). 

- Hamann, S. E., D. L. Haycock, G. Klose, P. H. Pax, I. H. Deutsch, and P. S. Jessen, 1998, Phys. Rev. Lett. **80** , 4149. 

- Ha[¨] nsch, T. W., and A. L. Schawlow, 1975, Opt. Commun. **13** , 68. 

- Hegerfeldt, G. C., and M. B. Plenio, 1995, Phys. Rev. A **52** , 3333. 

- Heinzen, D. J., and D. J. Wineland, 1990, Phys. Rev. A **42** , 2977. 

- Ho[¨] ffges, J. T., H. W. Baldauf, T. Eichler, S. R. Helmfrid, and H. Walther, 1997, Opt. Commun. **133** , 170. 

- Ho[¨] ffges, J. T., H. W. Baldauf, W. Lange, and H. Walther, 1997, J. Mod. Opt. **44** , 1999. 

- Itano, W. M., J. C. Bergquist, J. J. Bollinger, and D. J. Wineland, 1992, in _NIST Technical Note No. 1353_ , edited by J. C. Bergquist, J. J. Bollinger, W. M. Itano, and D. J. Wineland (U.S. Government Printing Office, Washington), p. TN 166. 

- Itano, W. M., J. C. Bergquist, and D. J. Wineland, 1988, Phys. Rev. A **38** , 559(R). 

- Itano, W. M., and D. J. Wineland, 1981, Phys. Rev. A **25** , 35. 

- James, D. F. V., 1998, Appl. Phys. B: Lasers Opt. **B66** , 181. 

- Janik, G., W. Nagourney, and H. Dehmelt, 1985, J. Opt. Soc. Am. B **2** , 1251. 

- Janszky, J., and Y. Y. Yushin, 1986, Opt. Commun. **59** , 151. 

- Jaynes, E. T., and F. W. Cummings, 1963, Proc. IEEE **51** , 89. Jefferts, S. R., C. Monroe, E. Bell, and D. J. Wineland, 1995, Phys. Rev. A **51** , 3112. 

- Jessen, P. S., C. Gerz, P. D. Lett, W. D. Phillips, S. L. Rolston, R. J. C. Spreeuw, and C. I. Westbrook, 1992, Phys. Rev. Lett. **69** , 49. 

- Kimble, H. J., M. Dagenais, and L. Mandel, 1977, Phys. Rev. Lett. **39** , 691. 

- King, B. E., C. S. Wood, C. J. Myatt, Q. A. Turchette, D. Leibfried, W. M. Itano, C. Monroe, and D. Wineland, 1998, Phys. Rev. Lett. **81** , 1525. 

- Klauder, J. R., and B.-S. Skagerstam, 1985, _Coherent States_ (World Scientific, Singapore). 

- Kneer, B., and C. K. Law, 1998, Phys. Rev. A **57** , 2096. 

- Kokorowski, D. A., A. D. Cronin, T. D. Roberts, and D. E. Pritchard, 2001, Phys. Rev. Lett. **86** , 2191. 

- Law, C. K., and J. H. Eberly, 1996, Phys. Rev. Lett. **76** , 1055. Leggett, A. J., 1999, Phys. World **12** , 73. 

- Leibfried, D., D. M. Meekhof, B. E. King, C. Monroe, W. M. Itano, and D. J. Wineland, 1996, Phys. Rev. Lett. **77** , 4281. 

- Leibfried, D., D. M. Meekhof, C. Monroe, B. E. King, W. M. Itano, and D. J. Wineland, 1998, J. Mod. Opt. **44** , 2485. 

- Leibfried, D., C. Monroe, and T. Pfau, 1998, Phys. Today **51** , 22. 

- Lindberg, M., 1984, J. Phys. B **17** , 2129. 

- Lindberg, M., 1986, Phys. Rev. A **34** , 3178. 

- Loudon, R., 1973, _The Quantum Theory of Light_ (Clarendon, Oxford). 

- Lutterbach, L. G., and L. Davidovich, 1997, Phys. Rev. Lett. **78** , 2547. 

- Maı[ˆ] tre, X., E. Hagley, G. Nogues, C. Wunderlich, P. Goy, M. Brune, J. M. Raimond, and S. Haroche, 1997, Phys. Rev. Lett. **79** , 769. 

- Mandel, L., 1979, Opt. Lett. **4** , 205. 

- Mandel, L., 1982, Phys. Rev. Lett. **49** , 136. 

- Marzoli, I., J. I. Cirac, R. Blatt, and P. Zoller, 1994, Phys. Rev. A **49** , 2771. 

- McLachlan, N. W., 1947, _Theory and Applications of Mathieu Functions_ (Clarendon, Oxford). 

- Meekhof, D. M., C. Monroe, B. E. King, W. M. Itano, and D. J. Wineland, 1996, Phys. Rev. Lett. **76** , 1796; **77** , 2346(E). 

- Merz, M., and A. Schenzle, 1990, Appl. Phys. B: Photophys. Laser Chem. **50** , 115. 

- Mitchell, T. B., J. J. Bollinger, D. H. E. Dubin, X.-P. Huang, W. M. Itano, and R. H. Baughman, 1998, Science **282** , 1290. 

- Mollow, B., 1969, Phys. Rev. **188** , 1969. 

- Monroe, C., D. M. Meekhof, B. E. King, S. R. Jefferts, W. M. Itano, D. J. Wineland, and P. L. Gould, 1995, Phys. Rev. Lett. **75** , 4011. 

- Monroe, C., D. M. Meekhof, B. E. King, and D. J. Wineland, 1996, Science **272** , 1131. 

- Morigi, G., J. Eschner, and Ch. Keitel, 2000, Phys. Rev. Lett. **85** , 4458. 

- Moya-Cessa, H., and P. L. Knight, 1993, Phys. Rev. A **48** , 2479. 

- Murao, M., and P. L. Knight, 1998, Phys. Rev. A **58** , 663. 

- Myatt, C. J., B. E. King, Q. A. Turchette, C. A. Sackett, D. Kielpinski, W. M. Itano, and D. J. Wineland, 2000, Nature (London) **403** , 269. 

- Na[¨] gerl, H. C., D. Leibfried, F. Schmidt-Kaler, J. Eschner, and R. Blatt, 1998, Opt. Express **3** , 89. 

- Nagourney, W., G. Janik, and H. G. Dehmelt, 1983, Proc. Natl. Acad. Sci. U.S.A. **80** , 643. 

- Nagourney, W., J. Sandberg, and H. G. Dehmelt, 1986, Phys. Rev. Lett. **56** , 2797. 

- Neuhauser, W., M. Hohenstatt, P. E. Toschek, and H. G. Dehmelt, 1978, Phys. Rev. Lett. **41** , 233. 

- Neuhauser, W., M. Hohenstatt, P. E. Toschek, and H. G. Dehmelt, 1980, Phys. Rev. A **22** , 1137. 

- Paul, W., 1990, Rev. Mod. Phys. **62** , 531. 

- Paul, W., O. Osberghaus, and E. Fischer, 1958, Forschungsber. Wirtsch.-Verkehrminist. Nordrhein-Westfalen **415** . 

- Peik, E., J. Abel, Th. Becker, J. von Zanthier, and H. Walther, 1999, Phys. Rev. A **60** , 439. 

- Penning, F. M., 1936, Physica (Amsterdam) **3** , 873. 

- Perrin, H., A. Kuhn, I. Bouchoule, and C. Salomon, 1998, Europhys. Lett. **42** , 395. 

Plenio, M. B., and P. L. Knight, 1996, Phys. Rev. A **53** , 2986. 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

324 

Leibfried et al.: Quantum dynamics of single trapped ions 

Plenio, M. B., and P. L. Knight, 1997, Proc. R. Soc. London, Ser. A **453** , 2017. 

- Poyatos, J. F., J. I. Cirac, and P. Zoller, 1996, Phys. Rev. Lett. **77** , 4728. 

- Poyatos, J. F., R. Walser, J. I. Cirac, P. Zoller, and R. Blatt, 1996, Phys. Rev. A **53** , R1966. 

- Press, W. H., S. A. Teukolsky, W. T. Vetterling, and B. P. Flannery, 1992, _Numerical Recipes_ (Cambridge University, Cambridge, England). 

- Raab, Ch., J. Eschner, and R. Blatt, 2001, unpublished. 

- Raab, Ch., J. Eschner, J. Bolle, H. Oberst, F. Schmidt-Kaler, and R. Blatt, 2000, Phys. Rev. Lett. **85** , 538. 

- Raimond, J. M., M. Brune, and S. Haroche, 1997, Phys. Rev. Lett. **79** , 1964. 

- Raimond, J. M., M. Brune, and S. Haroche, 2001, Rev. Mod. Phys. **73** , 565. 

- Ramsey, N. F., 1963, _Molecular Beams_ (Oxford University, London). 

- Reiß, D., A. Lindner, and R. Blatt, 1996, Phys. Rev. A **54** , 5133. 

- Rohde, H., S. T. Gulde, C. F. Roos, P. A. Barton, D. Leibfried, J. Eschner, F. Schmidt-Kaler, and R. Blatt, 2001, J. Opt. B: Quantum Semiclassical Opt. **3** , S34. 

- Roos, Ch., D. Leibfried, A. Mundt, F. Schmidt-Kaler, J. Eschner, and R. Blatt, 2000, Phys. Rev. Lett. **85** , 5547. 

- Roos, Ch., Th. Zeiger, H. Rohde, H. C. Na[¨] gerl, J. Eschner, D. Leibfried, F. Schmidt-Kaler, and R. Blatt, 1999, Phys. Rev. Lett. **83** , 4713. 

- Rowe, M., A. Ben-Kish, B. DeMarco, D. Leibfried, V. Meyer, J. Beall, J. Britton, J. Hughes, W. M. Itano, B. Jelencovic[´] , C. Langer, T. Rosenband, and D. J. Wineland, 2002, Quantum Inf. Comput. **4** , 257. 

- Royer, A., 1984, Phys. Rev. Lett. **52** , 1064. 

- Sackett, C. A., D. Kielpinski, B. E. King, C. Langer, V. Meyer, C. J. Myatt, M. Rowe, Q. A. Turchette, W. M. Itano, D. J. Wineland, and C. Monroe, 2000, Nature (London) **404** , 256. 

- Sauter, T., W. Neuhauser, R. Blatt, and P. E. Toschek, 1986, Phys. Rev. Lett. **57** , 1696. 

- Schleich, W. P., 2001, _Quantum Optics in Phase Space_ (WileyVCH, Berlin). 

- Schneider, S., and G. J. Milburn, 1998, Phys. Rev. A **57** , 3748. Schneider, S., and G. J. Milburn, 1999, Phys. Rev. A **59** , 3766. Schro[¨] dinger, E., 1926, Naturwissenschaften **14** , 664. 

- Schro[¨] dinger, E., 1935, Naturwissenschaften **23** , 807. 

- Schubert, M., I. Siemers, R. Blatt, W. Neuhauser, and P. E. Toschek, 1992, Phys. Rev. Lett. **68** , 3016. 

- Schubert, M., I. Siemers, R. Blatt, W. Neuhauser, and P. E. Toschek, 1995, Phys. Rev. A **52** , 2994. 

- Shore, B. W., and P. L. Knight, 1993, J. Mod. Opt. **40** , 1195. 

- Short, R., and L. Mandel, 1983, Phys. Rev. Lett. **51** , 384. 

- Siemers, I., M. Schubert, R. Blatt, W. Neuhauser, and P. E. Toschek, 1992, Europhys. Lett. **18** , 139. 

- Slusher, R. E., L. W. Hollberg, B. Yurke, J. C. Mertz, and J. F. Valley, 1985, Phys. Rev. Lett. **55** , 2409. 

- Smithey, D. T., M. Beck, M. G. Raymer, and A. Faridani, 1993, Phys. Rev. Lett. **70** , 1244. 

- Stalgies, Y., I. Siemers, B. Appasamy, T. Altevogt, and P. E. Toschek, 1996, Europhys. Lett. **35** , 259. 

- Steane, A., 1997, Appl. Phys. B: Lasers Opt. **64** , 623. 

- Stenholm, S., 1986, Rev. Mod. Phys. **58** , 699. 

- Turchette, Q. A., D. Kielpinski, B. E. King, D. Leibfried, D. M. Meekhof, C. J. Myatt, M. A. Rowe, C. A. Sackett, C. S. Wood, W. M. Itano, C. Monroe, and D. J. Wineland, 2000, Phys. Rev. A **61** , 063418. 

- Turchette, Q. A., C. J. Myatt, B. E. King, C. A. Sackett, D. Kielpinski, W. M. Itano, C. Monroe, and D. J. Wineland, 2000, Phys. Rev. A **62** , 053807. 

- Varcoe, B. T. H., S. Brattke, M. Weidinger, and H. Walther, 2000, Nature (London) **403** , 743. 

- Vogel, W., 1991, Phys. Rev. Lett. **67** , 2450. 

- Vogel, W., and R. Blatt, 1992, Phys. Rev. A **45** , 3319. 

- Vogel, W., and D. G. Welsch, 1994, _Quantum Optics_ , 1st ed. (Akademie Verlag, Berlin). 

- von Foerster, T., 1975, J. Phys. A **8** , 95. 

- Vuletic, V., C. Chin, A. J. Kerman, and S. Chu, 1998, Phys. Rev. Lett. **81** , 5768. 

- Wallentowitz, S., and W. Vogel, 1995, Phys. Rev. Lett. **75** , 2932. Wallentowitz, S., and W. Vogel, 1996, Phys. Rev. A **53** , 4528. Walls, D. F., 1986, Nature (London) **324** , 210. 

- Walls, D. F., and G. J. Milburn, 1985, Phys. Rev. A **31** , 2403. 

- Walls, D. F., and G. J. Milburn, 1995, _Quantum Optics_ (Springer, Berlin), p. 91. 

- Walls, D. F., and P. Zoller, 1981, Phys. Rev. Lett. **47** , 709. 

- Westbrook, C. I., R. N. Watts, C. E. Tanner, S. L. Rolston, W. D. Phillips, P. D. Lett, and P. L. Gould, 1990, Phys. Rev. Lett. **65** , 33. 

Wineland, D. J., J. C. Bergquist, J. J. Bollinger, W. M. Itano, F. L. Moore, J. M. Gilligan, M. G. Raizen, D. J. Heinzen, C. S. Weimer, and C. H. Manney, 1992, in _Laser Manipulation of Atoms and Ions_ , Proceedings of the International School of Physics ‘‘Enrico Fermi’’ Course 118, edited by E. Arimondo, W. D. Phillips, and F. Strumia (North-Holland, Amsterdam), p. 553. 

- Wineland, D. J., J. C. Bergquist, W. M. Itano, J. J. Bollinger, and C. H. Manney, 1987, Phys. Rev. Lett. **59** , 2935. 

- Wineland, D. J., and H. G. Dehmelt, 1975a, Bull. Am. Phys. Soc. **20** , 637. 

Wineland, D. J., and H. G. Dehmelt, 1975b, J. Appl. Phys. **46** , 919. 

Wineland, D. J., R. E. Drullinger, and F. L. Walls, 1978, Phys. Rev. Lett. **40** , 1639. 

- Wineland, D. J., P. Ekstrom, and H. G. Dehmelt, 1973, Phys. Rev. Lett. **31** , 1279. 

Wineland, D. J., and W. M. Itano, 1979, Phys. Rev. A **20** , 1521. Wineland, D. J., and W. M. Itano, 1981, Phys. Lett. A **82** , 75. Wineland, D. J., C. Monroe, W. M. Itano, D. Leibfried, B. E. King, and D. M. Meekhof, 1998, J. Res. Natl. Inst. Stand. Technol. **103** , 259. 

- Wu, L.-A., H. J. Kimble, J. L. Hall, and H. Wu, 1986, Phys. Rev. Lett. **57** , 2520. 

Yi, F. H., and H. R. Zaidi, 1988, Phys. Rev. A **37** , 2985. 

Zurek, W. H., 1991, Phys. Today **44** , 36. 

- Zurek, W. H., 2001, e-print quant-ph/0105127. 

Rev. Mod. Phys., Vol. 75, No. 1, January 2003 

