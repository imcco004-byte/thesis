**==> picture [87 x 86] intentionally omitted <==**

**==> picture [95 x 83] intentionally omitted <==**

**Laser Ablation Loading and Single Ion Addressing of Strontium in a Linear Paul Trap** 

**ANDREAS PÖSCHL** 

**==> picture [596 x 480] intentionally omitted <==**

**----- Start of picture text -----**<br>
KTH SCHOOL OF ENGINEERING SCIENCES<br>TUM DEPARTMENT OF PHYSICS<br>**----- End of picture text -----**<br>


## LASER ABLATION LOADING AND SINGLE ION ADDRESSING OF STRONTIUM IN A LINEAR PAUL TRAP 

## B.Sc. Andreas Pöschl 

Supervisor (SU): Prof. Markus Hennrich Examiner (TUM): Prof. Rudolf Gross Examiner (KTH): Prof. Gunnar Björk 

Submitted as master's thesis to the Faculty of Physics of the Technical University Munich and as degree project and project work to the School of Engineering Sciences of the Royal Institute of Technology in Stockholm in partial fullment for a double degree Master in Condensed Matter Physics (TUM) and 

Master in Engineering Physics (KTH) 

This work was carried out in the Trapped Ion Quantum Technologies Group at Stockholm University 

Copyright ©2018 by Andreas Pöschl. 

All rights reserved. No part of this thesis may be reproduced in any manner without written permission except in the case of brief quotations included in articles and reviews. For information, please contact the author. 

An electronic version of this thesis is published in DIVA. 

TRITA-SCI-GRU 2018:049 

## Abstract 

This thesis was performed in the Trapped Ion Quantum Technologies Group at Stockholm University. So far, measurements for the investigation of trapped Rydberg ions were limited by the time to load ions into a linear Paul trap. The main goal of this thesis was to decrease the loading time. Pulsed laser ablation loading was established for this purpose. The complete experimental setup was designed and the suitable optics was determined using Zemax OpticStudio. The pulsed laser ablation setup was characterized and integrated into the current experiment. The loading process was investigated and an automatic loading procedure was established. The time to load ions was reduced from 30 min to 36 s . For automatic loading, a new software for the existing electron multiplying CCD camera was developed paving the way towards fully automatic measurements. 

The current experimental setup only allows for the global manipulation of the internal quantum states of all ions in a chain of trapped ions. In order to manipulate the internal quantum state of an individual ion without aecting the neighbouring ions, an experimental setup was designed for the addressing of a selected ion with a tightly focused laser beam. Critical aspects of the design were determined and rst tests were performed with critical components. A detailed simulation was performed in Zemax OpticStudio to determine suitable optical components. It was shown that the used objective is able to focus a laser beam to a spot of 1 _/e_[2] waist (2 _._ 1 _±_ 0 _._ 5) µ m . For this purpose, a beam proler was developed on the basis of a Raspberry Pi camera module, which is able to measure tightly focused laser beams with high resolution and is going to be a useful tool in the future. In a nutshell, the preconditions for an experimental single-ion addressing setup were created. 

## Zusammenfassung 

Diese Masterarbeit wurde in der Trapped Ion Quantum Technologies Group der Universität Stockholm durchgeführt. Messungen am Experiment zur Erforschung von gefangenen Rydberg Ionen waren bisher limitiert durch die Zeit, die benötigt wird um ein Ion in eine lineare Paul Falle zu laden. Um diese Zeit zu verkürzen, wurde Laserablationsladen umgesetzt. Der experimentelle Aufbau hierfür wurde designed und die passenden optischen Komponenten wurden mit Hilfe von Zemax OpticStudio ermittelt. Der Laserablationsaufbau wurde getestet und characterisiert und in das Rydberg Experiment integriert. Die Sequenz zum Laden von Ionen wurde vollständig automatisiert. Die benötigte Zeit, um ein Ion zu laden, wurde von 30 min auf 36 s reduziert. Um automatisches Laden der Ionenfalle mit einer gewünschten Anzahl an Ionen zu ermöglichen, wurde eine neue Software für die verwendete Electron Multiplying CCD Kamera entwickelt, was auch die Basis für vollkommen automatisierte Messungen in der Zukunft bildet. 

Der experimentelle Aufbau in jetziger Form erlaubt nur die Manipulation des internen Quantenzustände aller Ionen in einer Kette gefangener Ionen. Um den internen Quantenzustand eines ausgewählten Ions manipulieren zu können ohne benachbarte Ionen zu beeinträchtigen, wurde ein experimenteller Aufbau designed, der einen stark fokusierten Laserstrahl auf ein bestimmtes Ion richten kann. Die kritischen Gesichtspunkte des Aufbaus wurden bestimmt und erste Tests mit den entsprechenden Komponenten durchgeführt. Eine detaillierte Fallstudie wurde in Zemax OpticStudio durchgeführt, um die optimalen optischen Komponenten zu bestimmen. Es wurde insbesondere gezeigt, dass das verwendete Objektiv in der Lage ist, einen Laser strahl auf einen Punkt mit einem 1 _/e_[2] Konturradius von (2 _._ 1 _±_ 0 _._ 5) µ m zu fokusieren. Für diesen Zweck wurde ein Beam Proler auf der Basis eines Raspberry Pi Kamera Moduls entwickelt, der in der Lage ist stark fokusierte Laserstrahlen mit hoher Auösung zu messen und der in der Zukunft ein nützliches Werkzeug sein wird. Zusammengefasst wurden die nötigen Grundvorraussetzungen für einen experimentellen Aufbau zum Adressieren einzelner Ionen geschaen. 

## Sammanfattning 

Denna avhandling gjordes på Stockholms Universitet i Trapped Ion Technology-gruppen. Hittills har undersökningar av fängslade Rydbergioner varit begränsade av tiden det tar att ladda en linjär Paulfälla med joner. Avhandlingens huvudsyfte var att minska denna laddningstid. För detta ändamål etablerades laddning med pulserande laser ablation. Den fullständiga experimentella uppställningen designades och den lämplig optik bestämdes med hjälp av Zemax OpticStudio. Uppställningen med pulserande laser ablation karakteriserades och integrerades i det existerande experimentet. Laddningsprocessen undersöktes och en automatisk laddningsprocedur etablerades. Jonladdningstiden kunde reduceras från 30 min till 36 s . För automatisk laddning utvecklades en ny mjukvara för redan existerande elektron multiplicerande CCD-kameror, vilket banar vägen för framtida helautomatiserade mätningar. 

Den nuvarande experimentuppställningen tillåter endast samtidig, global modiering av interna kvanttillstånd hos samtliga joner i en kedja av fångade joner. För att kunna modiera interna kvanttillstånd hos individuella joner utan att påverka angränsande joner designades en experimentuppställning för adressering av en utvald jon med en tätt fokuserad laserstråle. Kritiska aspekter hos designen bestämdes och de första experimenten utfördes med kritiska komponenter. En detaljerad undersökning utfördes i Zemax OpticStudio för att utröna lämpliga optiska komponenter. Vi visar att det använda objektivet klarar att fokusera en laserstråle till en punkt med 1 _/e_[2] midja (2 _._ 1 _±_ 0 _._ 5) µ m . För detta ändamål utvecklades en prolerare baserad på en kameramodul till Raspberry Pi som klarar att mäta tätt fokuserade laserstrålar med hög upplösning och som kommer att vara ett användbart verktyg i framtiden. Vi har därmed skapat förutsättningar för en experimentuppställning som tillåter adressering av enskilda joner. 

## Contents 

|1|Experiments with Trapped Ions|Experiments with Trapped Ions|1|
|---|---|---|---|
||1.1|Trapped Ion Quantum Computer ............................................................|2|
||1.2|Rydberg Atoms and Ions ........................................................................|3|
||1.3|Trapped Strontium Rydberg Ions ............................................................|5|
|2|Laser Ablation Loading||18|
||2.1|Pulsed Laser Ablation ............................................................................|19|
|||2.1.1<br>PLA from a Metal .......................................................................|19|
|||2.1.2<br>The Two-Temperature Model of PLA ............................................|20|
|||2.1.3<br>Numerical Calculation..................................................................|21|
|||2.1.4<br>Q-Switched Lasers for PLA ..........................................................|24|
||2.2|Experimental Realization of PLA Loading ................................................|25|
|||2.2.1<br>Requirements on the PLA Setup ...................................................|25|
|||2.2.2<br>Design of the PLA Setup..............................................................|26|
|||2.2.3<br>Test and Characterization of the PLA Setup ..................................|29|
|||2.2.4<br>Integration into Current Experiment..............................................|35|
|||2.2.5<br>Photo-Ionization..........................................................................|37|
|||2.2.6<br>Isotope Selective Loading .............................................................|38|
||2.3|Pulsed Laser Ablation Loading................................................................|40|
|||2.3.1<br>Cooling Time of PLA Loaded Ions ................................................|40|
|||2.3.2<br>Number of Loaded Ions per Ablation Pulse ....................................|43|
|||2.3.3<br>Time-of-Flight Measurements .......................................................|44|
|||2.3.4<br>Experimental Sequence for Automatic PLA Loading .......................|45|
|3|Single-Ion Addressing||47|
||3.1|Key components ....................................................................................|48|
|||3.1.1<br>Objective....................................................................................|49|
|||3.1.2<br>Acousto-Optic Deector ...............................................................|54|
||3.2|Zemax OpticStudio Simulations...............................................................|56|
|||3.2.1<br>A Suitable Combination of Achromat and AOD..............................|56|
|||3.2.2<br>The Complete Optical Design .......................................................|58|
||3.3|Next Steps ............................................................................................|60|
|4|Summary and Outlook||61|
|References|||63|
|Appendices|||69|
|A|Camera Software||70|
||A.1|qCamera...............................................................................................|70|
||A.2|GUI .....................................................................................................|72|
|||A.2.1<br>Checking the Ions' Position During an Ongoing Acquisition .............|73|
|||A.2.2<br>Integration of the EMCCD into Measurements ...............................|74|
||A.3|Ion Recognition Software ........................................................................|76|



|B|Raspberry Pi Beam Proler<br>81|Raspberry Pi Beam Proler<br>81|
|---|---|---|
||B.1|Raspberry Pi Camera Module V2 ............................................................ 81|
|||B.1.1<br>De-Bayering of the CMOS Sensor.................................................. 81|
||B.2|Beam Proler Software........................................................................... 84|
||B.3|User Guide ........................................................................................... 86|
||B.4|Conclusion ............................................................................................ 90|



## List of Figures 

|Figure|1|Rendered Image of the Linear Paul Trap ...............................................|6|
|---|---|---|---|
|Figure|2|Level Scheme of Strontium...................................................................|7|
|Figure|3|Optical Access of Trapped Ions in the Linear Paul Trap ..........................|9|
|Figure|4|Principle of Sideband Cooling...............................................................|12|
|Figure|5|Directions of State Detection, Single-Ion Addressing Beam, Microwave||
|||Dressing Beam and the Neutral Atomic Beam........................................|13|
|Figure|6|Histogram for State Detection by an EMCCD........................................|14|
|Figure|7|Numerical Results for the Surface Temperature and Velocity of the Ab-||
|||lation Front during PLA ......................................................................|22|
|Figure|8|Numerical Result for the Expected Values for the Ablation Depth and||
|||Number of Ablated Atoms during PLA .................................................|23|
|Figure|9|Beam Path of the Ablation Laser..........................................................|25|
|Figure|10|Schematic Sketch of the Pulsed Laser Ablation Setup..............................|27|
|Figure|11|Laser Pulse Energy Dependence on Warm-Up Time and Repetition Fre-||
|||quency...............................................................................................|29|
|Figure|12|Pulsed Laser Ablation Setup ................................................................|31|
|Figure|13|Optical Components inside the Vacuum Chamber...................................|32|
|Figure|14|Power Regulation and Stability of the PLA Setup...................................|33|
|Figure|15|Pulsed Laser Ablation from a SrTiO3 Test Target ..................................|34|
|Figure|16|Temperature Controlled Mount and Temperature Dependence of the Photo-||
|||Ionisation Laser ..................................................................................|38|
|Figure|17|Number of Ablation Loaded Ions vs Doppler Cooling Time......................|41|
|Figure|18|One Dimensional Phase Diagram for a Hot Strontium Ion .......................|42|
|Figure|19|Number of Ablation Loaded Ions vs Ablation Laser Pulse Energy.............|43|
|Figure|20|Components of the Home-Built Objective ..............................................|49|
|Figure|21|Layout and Image of the Home-Built Objective ......................................|50|
|Figure|22|Image of the USAF1951 Test Target .....................................................|51|
|Figure|23|Measurement of the Modulation Transfer Function .................................|52|
|Figure|24|Beam Propagation of the Focused 674 nm Addressing Laser.....................|53|
|Figure|25|Sketch of the compete Single-Ion Addressing Setup.................................|57|



Figure 26 Expected Intensity Distribution at the Entrance of the Acousto-Optic 

Deector ............................................................................................ 58 Figure 27 Expected Intensity Distribution at the Ions' Position .............................. 59 Figure 28 UML Class Diagram of qCamera .......................................................... 78 Figure 29 Screen Shot of the New Camera Software .............................................. 79 Figure 30 UML Class Diagram of the New Camera Software .................................. 80 Figure 31 Photo of the Raspberry Pi Camera Module V2 CMOS Sensor.................. 82 

## List of Tables 

Table 1 Material Parameters of Strontium............................................................ 22 Table 2 Abundance of Natural Strontium Isotopes ................................................ 39 Table 3 Measured Focal Spot Size and Expected Value from Zemax OpticStudio of the Focused 674 nm Addressing Beam ...................................................... 54 Table 4 Zemax Optic Stuio Results for Dierent Achromatic Lens Doublets ............. 57 Table 5 Errors of the Ion Recognition Software ..................................................... 77 

## Acronyms 

AOD - acousto-optic deector AOM - acousto-optic modulator CMOS - complementary metal-oxide-semiconductor CW - continuous wave DLL - dynamic link library EMCCD - electron-multiplying charge-coupled device EOD - Electro-optic deector 

FRET - Förster resonance excitation transfer GUI - graphical user interface 

MTF - modulation transfer function PCB - printed circuit board PCI - peripheral component interconnect PDH - Pound-Drever-Hall PLA - pulsed laser ablation PMT - photomultiplier tube 

qubit - quantum bit 

RF - radio frequency ROI - region of interest RPC - remote procedure call 

SDK - software development kit SMD - surface-mounted device STIRAP - stimulated Raman adiabatic passage 

TCP - transmission control protocol TrICS - Trapped Ion Control Software TTL - transistor-transistor logic UV - ultraviolet 

VUV - vacuum ultraviolet 

## 1. Experiments with Trapped Ions 

In the 1950s physicists around Wolfgang Paul started to investigate radio-frequency quadrupole elds in order to conne charged particles in two dimensions. It was realized quickly, that one can use a combination of oscillating and static electric elds for the trapping of ions in three dimensions [1]. These so-called ion traps oer a conning potential with a depth up to several eV which is eectively harmonic at its center. The invention of laser cooling opened the possibility of cooling trapped ions into their quantum ground state of motion [2]. This paved the way towards experiments with trapped ions as quantum mechanical particles. Some remarkable examples of those experiments are given in the following to underline the capabilities of ion trap experiments. 

Just like neutral atoms, ions possess discrete electronic energy levels n[2S+1] LJ with principal quantum number n, spin quantum number S, orbital angular momentum L and total angular momentum J. These may be labeled by the quantum number _N_ and dene the electronic quantum state _|N ⟩_ of a single trapped ion. Narrow linewidth, dipole forbidden transitions between internal ion states are used in optical clocks, which have set multiple records for optical frequency standards in the past with a relative uncertainty as small as 3 _×_ 10 _[−]_[18] at the time of writing [3]. This shows the major role of trapped ion experiments for metrology. 

A single trapped ion experiences a force due to the harmonic trapping potential with frequencies _ωi_ in all spatial directions _i ∈{x, y, z}_ . This is a three dimensional quantum harmonic oscillator and gives rise to the motional quantum state _|nxnynz⟩_ of a trapped ion, where _ni_ is the quantum number of the harmonic oscillator in the respective direction _i_ . The full quantum state is given by the tensor product _|N ⟩⊗|nxnynz⟩_ of motional and internal state. The quantum state of a trapped ion can be manipulated precisely by lasers due to light-matter interaction. This allows not only for the coherent control of the internal state of the ion, but also enables the coherent change of the motional state (for details see section 1.3). This can be exploited to cool a trapped ion to its motional ground state _{nx, ny, nz}_ = 0 and subsequently prepare it in an arbitrary motional state. It enabled the experimental realization of several interesting quantum states with trapped ions. Examples are Fock states, coherent states, squeezed states as well as the more exotic Schrödinger-cat states of motion [4]. These experiments illustrate how one can manipulate trapped ions as individual quantum systems. 

A linear Paul trap is operated at an axial frequency _ωz_ which is smaller than the other two almost equally large radial frequencies _ωx ≈ ωy_ . At sucient cooling and for _ωz ≪ ωx, ωy_ , several ions will crystallize in a Wigner crystal in the form of a linear ion chain along the z axis. Such a trapped ion crystal in a linear Paul trap recently served as a periodically 

driven Floquet system. The breaking of discrete time translation symmetry which comes along with the formation of a discrete time crystal was demonstrated this way [5]. This example underlines once more the outstanding experimental control that trapped ions oer and possible applications for many-body quantum physics. 

The internal energy levels of a trapped ion form a multi-level system. One can pick two of the energy levels, say _N_ = 0 and _N_ = 1 , and use the respective internal electronic states _|_ 0 _⟩, |_ 1 _⟩_ to store information. The resulting two level system formed by the internal ion states can be in any superposition state _c_ 0 _|_ 0 _⟩_ + _c_ 1 _|_ 1 _⟩_ with _c_ 0 _, c_ 1 _∈_ C and _|c_ 0 _|_[2] + _|c_ 1 _|_[2] = 1 . A two-level quantum system that is used for information storage and processing is called qubit (quantum bit). It is the analogue of the classical bit in the quantum world and forms the fundamental building-block of a quantum computer. The usage of trapped ions as qubits points to applications in quantum computing, which will be treated in the following section. 

## 1.1. Trapped Ion Quantum Computer 

Quantum computers use quantum mechanical properties for computation. Their basic elements of information storage and processing are qubits instead of classical bits. The logic gate operations comprising calculations on a classical computer are here substituted by quantum gates, which are unitary transformations acting on the qubits. Quantum computers hold the promise to speed up calculations. In particular, several problems are of lower complexity class when solved on a quantum computer compared to classical computers. Problems that are exponentially hard to solve on a classical computer include prime number factorization and ecient database search, for which possible quantum algorithms exist already [6, 7]. Running those algorithms on a quantum computer would lead to an exponential speed up of computations. 

Another intractable problem is the simulation of a quantum system with a large number _N_ of interacting constituents, like a chain of _N_ interacting spins. In this example, the dimension of the Hilbert space would scale like 2 _[N]_ assuming a chain of spin 1/2 particles. The state of such a system can be described by a density matrix with 2 _[N] ×_ 2 _[N]_ elements, which scales exponentially with the number of spins. The number of coupled dierential equations, that would have to be solved in order to describe the time evolution of the system for an arbitrary Hamiltonian, is correspondingly large and scales exponentially with _N_ as well. This illustrates how hard the simulation of an arbitrary quantum system is as a computational problem. This is often named quantum complexity. A quantum computer can be used as quantum simulator to simulate other quantum systems eciently [8, 9]. 

Several technologies aim for the realization of a quantum computer with trapped ions as a strong contender. Information can be encoded in the ions'metastable internal states, 

which makes them qubits with outstanding coherence times [10]. Single-qubit gates can be simply performed by resonantly (de-)exciting single ions by tightly focused laser beams (see chapter 3). Multi-qubit gates require interaction between ions. The ions in a linear trap interact with each other due to Coulomb interaction. The motion of a linear crystal of _d_ ions has to be treated as _d_ coupled 3 dimensional harmonic oscillators. This gives rise to 3 _d_ phonon modes as elementary collective excitations of the ion crystal. The energy of the collective quantized motion of _d_ ions is now dened by the number of phonons in the respective phonon modes. As all _d_ ions share the same collective motional state, it can be used as a bus to transmit information between the ions. As proposed by Cirac and Zoller, this can be used to perform a controlled-NOT gate [11]. The proposal by Cirac and Zoller and its experimental realization [12] proved the feasibility and potential of trapped ions for the realization of a quantum computer. 

Using the motional modes of a trapped ion string as bus-mode during the quantum computation leads to severe limitations, however. It demands that one cools the crystal into its motional ground state, which is experimentally demanding. When performing quantum gates in this scheme, one needs to coherently manipulate the ions on motional side-bands, which demands these motional sidebands to be spectrally resolved [11]. This limits the speed at which quantum gates may be performed to the inverse of the trapping frequency [13]. On top of that, the motional mode spectrum becomes more complex with an increasing number of ions in the chain, which makes the excitation of an individual motional side-band more dicult in large ion crystals [14]. This limits the scalability of such a quantum register. 

As a remedy, it was proposed to excite trapped ions to an energetically high Rydberg state instead. Ions in a Rydberg state strongly interact with each other, which may be used to perform fast quantum gates [13]. The exploration of trapped ions in a linear Paul trap and their use for quantum computation is the main goal in the trapped Rydberg ion project at the Trapped Ion Quantum Technologies Group at Stockholm University. 

## 1.2. Rydberg Atoms and Ions 

Neutral trapped Rydberg atoms are characterized by a large principal quantum number _n_ . Their small binding energy is well described by 

**==> picture [268 x 26] intentionally omitted <==**

with the Rydberg constant _R_ . The quantum defect _δLJ_ ( _n_ ) is a slowly varying function with principal quantum number _n_ . Rydberg states are marked by large radial dipole matrix elements _⟨n, L|er|n[′] , L_ + 1 _⟩_ and _⟨n, L|er|n[′] , L[′] ⟩_ that scale like _n_[2] _ea_ 0 . _e_ denotes the elementary charge of an electron and _a_ 0 is the Bohr radius. Rydberg energy levels are also 

very sensitive to electric elds which makes Rydberg states acquire a permanent dipole moment in the presence of an electric eld [15]. The permanent dipole moments give rise to a dipole-dipole interaction between Rydberg atoms, that can be tuned by the electric eld strength. The interaction of Rydberg atoms gives rise to rich physics. As an example, two atoms excited to the Rydberg state nP and nS , respectively, can undergo the transition _|_ nP _⟩|_ nS _⟩↔|_ nS _⟩|_ nP _⟩_ , which leads to diusion of the np excitation [16]. Similarly FRET (Förster resonance excitation transfer) can occur in the form _|_ nP _⟩|_ nP _⟩↔|_ nS _⟩|_ (n + 1)S _⟩_ . The coupling of Rydberg states with dierent angular momentum _L_ with a microwave eld leads to strong oscillating dipole moments. This is another way to induce and control interaction between Rydberg atoms [17]. 

The dipole-dipole interaction of Rydberg atoms is very strong at short distances. Within the so-called blockade radius it is sucently strong to shift the energy of a two-atom Rydberg excitation out of resonance with the exciting light eld, while the Rydberg excitation of a single atom is still resonant. It means a Rydberg excited atom can block atoms within the blockade radius from being excited to the same Rydberg state. This eect is called Rydberg blockade [18] and it is an important tool for fast two-qubit gates with neutral atoms [19, 20]. In particular when driving the transition to the Rydberg state a 2 _π_ oscillation will take place or not depending on whether another atom is already excited to the Rydberg state within the blockade radius. In the language of controlled two qubit gates, the rst atom would be the target qubit, while the second atom would serve as control qubit. If the control qubit is in the Rydberg state, the target cannot be excited to Rydberg state. If the control qubit is not in the Rydberg state, however, the target qubit can undergo the 2 _π_ rotation to the Rydberg state and acquire a _π_ phase shift. This can serve as a implementation of a controlled phase gate [21], which has been demonstrated successfully in [16]. 

According to a proposal by Markus Müller [13], trapped ions may be excited to Rydberg states as well. Interacting Rydberg ions may be used for fast quantum gates. Pulse sequences for Rydberg excitations are on a timescale below µ s and expected operation time for quantum gates with Rydberg ions is predicted to be below 10 µ s [13]. For quantum gates with trapped Rydberg ions it is not necessary to cool the ion chain to the motional ground state. Thus, trapped Rydberg ions may oer an experimental platform for the realization of a quantum computer with trapped ions, that does not suer from the same drawbacks as the Cirac-Zoller scheme. In particular, gate operations would not depend on the motional mode spectrum and the interaction of Rydberg ions is long ranged, which may allow for a scalable quantum register. 

The following section contains a description of the experiment in the Trapped Ion Quantum Technologies Group in Stockholm together with a short summary of the current experimental results on trapped Rydberg ions. 

## 1.3. Trapped Strontium Rydberg Ions 

In the experiment at Stockholm University, Sr[+] ions are trapped. Strontium is an alkaline earth metal, which has already been trapped and laser cooled in quantum information experiments before [14]. The element strontium has several properties, that make it an ideal candidate for the experimental investigation of trapped Rydberg ions. The single charged strontium ion, Sr[+] , has the electron conguration [Kr]5s[1] . The fact that Sr[+] has a single valence electron, while the other electrons form closed shells makes it possible to approximate the multi-electron system by a two-body system [12]. Sr[+] can be excited to Rydberg states by a two-photon transition. The necessary photon energy for each of the two steps lies below the energy of VUV (vacuum ultraviolet) radiation [22]. This simplies the experimental setup considerably, as laser systems and beam path do not have to be placed in vacuum. The most abundant strontium isotope strontium-88 is used in the experiment. 

## Trapping of Strontium Ions 

Particles are trapped in a potential minimum. For charged particles like ions, it appears obvious to use electric elds for this purpose. Unfortunately, as stated by Earnshaw's theorem, it is not possible, to trap charged particles solely by a static electric eld. Instead, one can use a periodically time-changing potential of the form 

**==> picture [288 x 27] intentionally omitted <==**

for the connement in two dimensions. This saddle potential forms an oscillating quadrupole electric eld. Such a potential can be created by a conguration of four innitely extended rods which are parrallel to each other. A linear Paul trap generates a potential that approximates 1.2 at its center. The trap used in the experiment is shown in gure 1. The potential is created by the four blade electrodes. Each opposing pair of blade electrodes are 2 _r_ 0 = 750 µ m apart from each other. A constant voltage of 1 _._ 5 V is applied to one of the two pairs, whereas a RF (radio frequency) voltage around 500 V to 1000 V with frequency Ω _RF_ = 2 _π ×_ 18 _._ 15 MHz is applied to the other pair. The stability of the trajectory of an ion with charge _e_ and mass _m_ at the center region of the trap depends upon the parameters [4] 

**==> picture [325 x 27] intentionally omitted <==**

In rst approximation, the resulting movement is the one in a harmonic potential with frequencies [23] 

**==> picture [350 x 24] intentionally omitted <==**

To allow for additional connement in the z direction, a voltage _UC ≈_ 1000 V is applied to the two end-cap electrodes. This leads to a trapped ion conned in a three dimensional quantum harmonic oscillator with the Hamiltonian 

**==> picture [293 x 30] intentionally omitted <==**

with _i ∈{x, y, z}_ labelling the spatial directions with the respective harmonic frequency _ωi_ . _ni_ labels the energy eigenstates _|ni⟩_ of the harmonic oscillator in the respective direction and can be thought of as phonon number. One can interpret each harmonic oscillator mode of the motional state as a bosonic quantum eld. 

**==> picture [225 x 166] intentionally omitted <==**

**==> picture [193 x 166] intentionally omitted <==**

Figure 1: Images of the ion trap electrodes are shown. On the left, the whole trap is shown. It consists of four blade electrodes and two end-cap electrodes. On the right, the trap is shown with one end-cap electrode removed, to allow for a view to the center of the trap. The images are rendered with KeyShot. 

In the experiment, all parts of the trap are made of gold coated titanium. The gold coating has a high conductivity and thus, avoids considerable heating of the trap blades due to the applied radio frequency eld. The high conductivity also reduces the impact of ohmic noise and patch-electric elds on the trapping potential [24]. The work function of gold Θ = 5 _._ 3 eV [25] is higher in comparison with titanium. This avoids, that UV (ultraviolet) lasers with a wavelength 243 nm produce free electrons through the photo-electric eect. Any free charges, like electrons, may accumulate on the insulating parts around the trap and lead to perturbing static electric elds. For this reason, the creation of free charges has to be minimized. The end-cap electrodes have a hole in the center allowing for laser beams to pass through. The trap is sitting in a vacuum chamber, that is equipped with seven viewports [23]. This allows addressing the trapped ions from dierent directions with laser beams. The vacuum chamber is evacuated by a combined non-evaporative get- 

ter and sputter pump. A pressure below 10 _[−]_[10] mbar is reached. 

## Laser Cooling of Strontium Ions 

A level scheme of[88] Sr[+] can be seen in gure 2. The ion is Doppler cooled on the 5S1 _/_ 2 _−_ 5P1 _/_ 2 dipole transition by a 422 nm laser. The wave vector _[⃗] k_ of the respective light eld has a component in all three trap directions x, y, z and is sucient to cool all three quantum harmonic oscillator modes. The 422 nm laser is red-detuned by ∆ _≈ −_ 2 _π ×_ 11 MHz for optimal Doppler cooling. The used transition is not closed and 6% of the ions in state 5P1 _/_ 2 decay to the dark state 4D3 _/_ 2 , which is metastable with lifetime _≈_ 400 ms . A re-pump laser at 1092 nm is used to shorten the lifetime of this dark state. 

**==> picture [255 x 215] intentionally omitted <==**

Figure 2: The energy level scheme of the internal electronic states of a trapped[88] Sr[+] ion is depicted. The scheme is not true to scale. The dipole transitions at 422 nm and 1092 nm are used for Doppler cooling. A narrow quadrupole transition at 674 nm connects the 5S1 _/_ 2 ground state with the metastable 4D5 _/_ 2 state. The ground state and one the metastable states serve as logical qubit states _|_ 0 _⟩, |_ 1 _⟩_ . The two-photon Rydberg excitation from the metastable state 4D5 _/_ 2 via 6P3 _/_ 2 is depicted. 

For a Doppler cooled ion in a three dimensional quantum harmonic oscillator, one would like to assign a temperature _Ti_ to each single one of the three oscillator modes. The mode with frequeny _ωi_ has the Hamilton operator 

**==> picture [260 x 27] intentionally omitted <==**

It is assumed, that the phonon mode is in a thermal state. The density operator is accordingly 

**==> picture [252 x 26] intentionally omitted <==**

with thermodynamic _β_ = 1 _/kBTi_ . Z is the partition sum given by 

**==> picture [429 x 45] intentionally omitted <==**

The fact that the phonons are bosons enters this calculation, as we accept any arbitrary non negative integer occupation number _ni_ . The expectation value _⟨ni_ + 1 _/_ 2 _⟩_ can now be calculated 

**==> picture [356 x 27] intentionally omitted <==**

From this, the usual form of the occupation number for the Bose-Einstein statistic is easily deduced 

**==> picture [310 x 26] intentionally omitted <==**

This can be solved for the temperature _Ti_ 

**==> picture [258 x 34] intentionally omitted <==**

After Doppler cooling, the ion is found to be in a thermal state with phonon numbers _⟨nz⟩≈_ 16 and _⟨nx⟩≈⟨ny⟩≈_ 12 for typical trapping frequencies of _ωz_ = 2 _π ×_ 840 kHz and _ωx_ = _ωy_ = 2 _π ×_ 1 _._ 7 MHz . This gives temperatures of _Tz_ = 0 _._ 7 mK , _Tx_ = _Ty_ = 1 mK . 

Sublevels of the 5S1 _/_ 2 ground state and 4D5 _/_ 2 metastable state serve as logical qubit states _|_ 0 _⟩_ and _|_ 1 _⟩_ . They are connected by the narrow quadrupole transition at 674 nm with a linewidth Γ = 2 _π ×_ 0 _._ 41 Hz [26]. The laser for this transition is stabilized by the PDH (Pound-Drever-Hall) technique to a high nesse ( _≈_ 100000 ) resonator. The achieved linewidth is 2 _π ×_ 1 kHz [22]. 

In the following, the Hamiltonian of a single trapped ion interacting with a light eld is explained in detail. The approach given in [4] is followed closely. The Hamiltonian _H_ 

**==> picture [423 x 314] intentionally omitted <==**

Figure 3: A simplied image of the trap illustrates how the ion can be accessed by laser beams. Note, that only the half of the incoming laser beam on the ion is depicted. The two UV lasers pass the trap along its symmetry axis z. The 422 nm laser for Doppler cooling and the two infrared lasers pass the trap diagonal in the direction 1 _/√_ 3( _−_ 1 _,_ 1 _,_ 1)[T] . The laser for the qubit transition at 674 nm propagates in the opposite direction 1 _/√_ 3(1 _, −_ 1 _, −_ 1)[T] . 

governing a single trapped ion and its interaction with a light eld is given by 

**==> picture [259 x 12] intentionally omitted <==**

_He_ accounts for the energy stored in the internal energy levels of the ion. Only focusing on the qubit transition, _He_ can be reduced to the simple form of a two level system with states _|_ 0 _⟩, |_ 1 _⟩_ separated by an energy ℏ _ω_ 0 

**==> picture [275 x 21] intentionally omitted <==**

**==> picture [259 x 21] intentionally omitted <==**

where we chose the denition _σz_ = _|_ 1 _⟩⟨_ 1 _| −|_ 0 _⟩⟨_ 0 _|_ for the Pauli matrix. _Hm_ corresponds to the energy of the motional state of the ion in the three-dimensional harmonic trapping potential. It has the form given by equation 1.5. 

In a semi-classical approach, a classical light eld with frequency _ω_ and wave vector _⃗k_ = _k ⃗ex_ along the x axis of the form 

**==> picture [289 x 21] intentionally omitted <==**

interacts with the ion at position _⃗rS_ = ( _xS, yS, zS_ )[T] . _⃗rS_ is the Schrödinger operator for the ion's position. The interaction Hamiltonian is described by 

**==> picture [340 x 23] intentionally omitted <==**

One can introduce the rising operator _σ_[+] = _|_ 1 _⟩⟨_ 0 _|_ and lowering operator _σ[−]_ = _|_ 0 _⟩⟨_ 1 _|_ for a shorthand notation. They are connected to the Pauli matrices by _σ[±]_ = ( _σx ± iσy_ ) _/_ 2 . Ω is the Rabi frequency. Ω is assumed to be real for simplicity. For a quadrupole transition, during which a single outer shell electron of charge e interacts with a light eld given by equation 1.15 the Rabi frequency Ω is given by 

**==> picture [269 x 21] intentionally omitted <==**

and can be complex in general. 

The contributions of _He_ and _Hm_ are easily solved. It is therefore instructive to transform the Hamiltonian into the interaction picture to analyse _Hi_ in more detail. The necessary unitary transformation for this is 

**==> picture [279 x 12] intentionally omitted <==**

and the transformed interaction Hamiltonian _Hint_ is 

**==> picture [399 x 43] intentionally omitted <==**

This Hamiltonian can be simplied further by the rotating wave approximation, which neglects all fast rotating parts of the Hamiltonian. Only the parts which rotate at a frequency ∆= _ω − ω_ 0 , which is the detuning of the laser from the transition frequency of the ion, remain. The result is 

**==> picture [315 x 23] intentionally omitted <==**

The Heisenberg operator for the projection of the wave vector onto the direction of the harmonic oscillator mode _kx_ ( _t_ ) can be rewritten by the rising and lowering Heisenberg operators _a_ ( _t_ ) , _a[†]_ ( _t_ ) of the harmonic oscillator mode. 

**==> picture [269 x 20] intentionally omitted <==**

with the Lamb-Dicke parameter _η_ = _k_ �ℏ _/_ 2 _mωx_ . For Doppler-cooled trapped ions, the variance of the operator _kx_ ( _t_ ) satises 

**==> picture [335 x 28] intentionally omitted <==**

i.e. the wave packet of the motional state is small compared to the wavelength of the light. This allows for a Taylor expansion of the exponent in the Hamiltonian. Expanded to rst order in _η_ and expressed with the Schrödinger operators _a, a[†]_ one gets the Hamiltonian 

**==> picture [345 x 23] intentionally omitted <==**

**==> picture [321 x 11] intentionally omitted <==**

The time dependence _∝_ exp( _±iωxt_ ) comes from the time dependence of the Heisenberg operators in equation 1.21. Rewriting the Heisenberg operators with Schrödinger operators also leads to a Rabi frequency Ω0 = Ω _/_ (1 + _q/_ 2) scaled by the trap parameter _q_ given by equation 1.3. From this Hamiltonian one can see the eect of a light eld on the internal and motional state of a trapped ion. The rst contribution _Hcar ∝_ (Ω0 _σ_ + + h _._ c _._ ) is the carrier transition at zero detuning ∆= 0 and corresponds to excitations and de-excitations of the internal ion state without aecting the motional state. The Rabi frequency is Ω0 . 

Another transition appears for a detuning of ∆= _−ωx_ due to _Hrsb ∝_ (Ω0 _σ_ + _ηa_ + h _._ c _._ ) . It couples states of the form _|_ 0 _⟩⊗|n⟩_ with _|_ 1 _⟩⊗|n −_ 1 _⟩_ with a Rabi frequency Ω0 _√nη_ . This is the so called red sideband. It can be used for cooling, because spontaneous decay of the ion does not change the motional state of the ion for Var ( _kx_ ( _t_ )) _≪_ 1 . One simply has to tune the laser to the red sideband ∆= _−ωx_ , which couples the states _|_ 0 _⟩⊗|n⟩←→|_ 1 _⟩⊗|n −_ 1 _⟩_ . An absorption event combined with one spontaneous emission _|_ 1 _⟩⊗|n−_ 1 _⟩−→|_ 0 _⟩⊗|n−_ 1 _⟩_ will then remove a single phonon. Repeating this cooling cycle many times is called sideband cooling [2]. When the state _|_ 0 _⟩⊗|_ 0 _⟩_ is reached, the ion cannot be excited by the red sideband anymore and stays trapped in this stated. This results in optical pumping to the state _|_ 0 _⟩⊗|_ 0 _⟩_ which is the motional ground state _⟨n⟩_ = 0 . The principle of sideband 

cooling is illustrated in gure 4. The part of the Hamiltonian given by _Hrsb_ has the same form of the Jaynes-Cummings Hamiltonian of cavity and circuit QED [27]. 

The last part of the Hamiltonian given by _Hbsb ∝_ �Ω0 _σ_ + _ηa[†]_ + h _._ c _._ � gives rise to transitions at a detuning ∆= + _ωx_ , that couples _|_ 0 _⟩⊗|n⟩_ with _|_ 1 _⟩⊗|n_ +1 _⟩_ . This is the blue sideband of the spectrum. The respective Rabi frequency is Ω0 _√n_ + 1 _η_ . _Hbsb_ is called anti JaynesCummings Hamiltonian. A coupling of this form does not exist in cavity QED, because there it would violate the conservation of energy. The blue sideband can be used to prepare Fock states of the motional ion state. For this purpose, the ion has to prepared in the motional ground state _nx_ = 0 by sideband cooling rst. Subsequently, starting in _|_ 0 _⟩⊗|_ 0 _⟩_ one applies _nx_ times a _π_ pulse on the blue sideband followed by a _π_ pulse on the carrier to return the internal ion state to _|_ 0 _⟩_ , which leads to the state _|_ 0 _⟩⊗|nx⟩_ . 

**==> picture [423 x 251] intentionally omitted <==**

Figure 4: The action of the 674 nm light eld on the electronic and motional ion state is illustrated. A laser that is not detuned from the internal energy splitting ∆= 0 only changes the internal ion state _|_ 0 _⟩↔|_ 1 _⟩_ without aecting the motional state _|n⟩_ . This is the carrier transition. A laser with blue detuning ∆= _ωx_ can drive the transition of the blue sideband, which adds one phonon _|n⟩→|n_ + 1 _⟩_ while the internal ion state is excited _|_ 0 _⟩→|_ 1 _⟩_ . A light eld tuned to the red sideband ∆= _−ωx_ excites the internal ion state _|_ 0 _⟩→|_ 1 _⟩_ and removes one phonon _|n⟩→|n −_ 1 _⟩_ at the same time. Driving red sideband transitions results in optical pumping to the quantum ground state of motion, because the ion spontaneously decays mainly on the carrier transition and the o-resonant laser cannot excite the ion from state _|_ 0 _⟩⊗|_ 0 _⟩_ anymore, where it remains trapped. 

The Rabi frequencies of the red and blue sideband transitions have an explicit dependence on the number of excitations of the motional state _nx_ . This opens a way of measuring _nx_ by means of measuring the Rabi frequencies of both sidebands. 

## Detection of the Internal Ion State 

The same transition that is used for Doppler cooling is used to read out the internal quantum state of the ion. For this purpose the ion is illuminated by the 422 nm and 

1092 nm lasers. If the ion is in the state 5S1 _/_ 2 the light excites the ion and spontaneously emits photons in all directions. Detection of uorescence light therefore signals population in state 5S1 _/_ 2 or 4D3 _/_ 2 . If the ion is in the metastable state 4D5 _/_ 2 , it does not couple to the light and consequently does not scatter any photons. Absence of uorescence light thus signals population in state 4D5 _/_ 2 . This technique is called electron shelving; it shelves the electron wavefunction of the ion into one of the two states _|_ 0 _⟩, |_ 1 _⟩_ and can be used to measure the qubit state with high delity [28]. 

**==> picture [423 x 212] intentionally omitted <==**

Figure 5: A schematic sketch of the ion trap is shown from the side. One end-cap is not shown for simplicity. The directions for PMT detection and EMCCD detection of uorescence photons are depicted. The 674 nm laser beam, that will be used to address single ions, propagating along 1 _/√_ 2( _−_ 1 _,_ 1 _,_ 0) _[T]_ and the microwave eld for microwave dressing in direction 1 _/√_ 2(1 _, −_ 1 _,_ 0) _[T]_ are shown as well. The sketch also illustrates, from which direction the beam of neutral strontium atoms emerging from the ovens enters the trapping region. 

During state detection, the laser intensity of the 422 nm is approximately 8 _Is_ , with the saturation intensity _Is_ . It is detuned by ∆= _−_ Γ _/_ 2 where Γ is the linewidth of the transition. If the ion couples to the light eld, the steady state population _ρee_ of the excited state 5P1 _/_ 2 resulting from the optical Bloch equation for this set of parameters is given by [29] 

**==> picture [292 x 26] intentionally omitted <==**

The decay rate on the 5S1 _/_ 2 _−_ 5P1 _/_ 2 transition is Γ = 22 MHz [30] which results in a rate _R_ of spontaneously emitted photons given by 

**==> picture [267 x 14] intentionally omitted <==**

The spontaneously emitted photons are collect by an aspheric lens[1] , that covers approximately 2.1% of the full solid angle. Subsequently, the photons are detected by a PMT (photomultiplier tube)[2] . A gated counter[3] is used to read out the number of detection events. A detection time of 500 µ s is enough, to distinguish the internal states 4D5 _/_ 2 from the two states 5S1 _/_ 2 and 4D3 _/_ 2 with a delity of _≈_ 99 _._ 9% [31]. 

For multiple trapped ions the PMT measurement cannot decide which of the ions is in which state. For example, the two two-ion states _|_ 10 _⟩_ and _|_ 01 _⟩_ can not be distinguished in such a measurement. 

**==> picture [423 x 226] intentionally omitted <==**

Figure 6: For 5 _×_ 10[5] images of an ion captured by a EMCCD, the digitalized pixel values are average over 3 _×_ 3 pixels surrounding the known ion position. The resulting histogram of the averaged pixel values is shown. Two clearly separated peaks corresponding to the ion being in state _|_ 1 _⟩_ and in state _|_ 0 _⟩_ are visible. 

Alternatively to the PMT detection, the spontaneously emitted photons are also collected by a homebuilt objective (see section 3.1.1 for details) and focused on an EMCCD (electron-multiplying charge-coupled device) pixel array of a camera[4] . This also provides an image of the ions in the trap. The position of each individual ion can be calibrated prior to a measurement of the internal ion state. During the measurement of the internal states of multiple ions, an image is captured with an exposure time of 3 ms . The square formed by 3 _×_ 3 pixels around each ion position on the camera image are averaged. A histogram of the resulting values for _≈_ 0 _._ 5 _×_ 10[5] images is depicted in gure 6. The histogram shows two well separated peaks, which already indicates that this method can be used to distinguish the internal ion states by comparing the averaged pixel value with a threshold value. 

> 1 Asphericon AFL25-40-S-A, f= 40 mm 

> 2 Hamamatsu Photonics H10682-210 

> 3 National Instruments PCI-6733 

> 4 Andor iXon 3 

For a xed threshold value, there are three possible detection errors. An ion is in the state _|_ 0 _⟩_ , which scatters photons, but the detected photons happen to be below the threshold value, i.e. a miss or type I error. The other error is the detection of photons, that lead to a pixel value above the threshold, even though the ion is in the state _|_ 1 _⟩_ ; this is a false hit or type II error. An additional error source arises as the state 4D5 _/_ 2 is metastable with a lifetime of _≈_ 0 _._ 4 s [32]. This means that _≈_ 0 _._ 7% of the 4D5 _/_ 2 population decays during the 3 ms detection time and leads to additional false hits. The error due to the decay of the metastable state is dominant. It limits the delity, with which an ion can be detected in the state 4D5 _/_ 2 to _≈_ 99 _._ 3% . This error can be reduced for shorter exposure times. 

This analysis shows, that an EMCCD camera can be used to detect the state of a chain of trapped ions with similar delity compared to the PMT. The method requires much longer detection times than the PMT measurement for the state detection of a single ion. For larger ion numbers, it can be faster than the PMT and can even determine which of the ions in the chain is in which state, which is vital to quantum computations and measurements like state tomography of a multi ion state. 

The whole experiment is controlled using the software TrICS (Trapped Ion Control Software), which was developed in the Blatt Group at the University of Innsbruck and the Institute for Quantum Optics and Quantum Information in Innsbruck. The camera software developed within this thesis integrates state detection by the EMCCD camera in an automatized fashion in the experiment software (for details see appendix A). 

## Rydberg Excitation of a Single Trapped Strontium Ion 

In this experiment trapped ions are excited to a Rydberg states by a two photon excitation scheme. The ions are rst initialized in the 4D5 _/_ 2 or 4D3 _/_ 2 state by optical pumping. Subsequently they can be excited to Rydberg state via the intermediate state 6P3 _/_ 2 or 6P1 _/_ 2 . This requires two lasers of wavelength 243 nm and 309 nm [33]. The two laser beams are aligned counterpropagating as depicted in gure 3. This way, the momentum transfer to the ion during a two-photon excitation is kept as small as possible. By keeping the 243 nm laser at a xed blue detuning of 2 _π ×_ 160 MHz and scanning the laser of the second UV laser, a single strontium ion could be excited to Rydberg states nS1 _/_ 2 and nD3 _/_ 2 with n _≈_ 25 [34]. 

It had been predicted, that the electron of a Rydberg state with _j >_ 1 _/_ 2 interact with the oscillating quadrupole eld of the ion trap [13]. This has been observed in the form of Floquet sidebands of the coupled Zeman levels in the manifold of the Rydberg state 24D3 _/_ 2 . [34]. The trapping frequency _ω[′]_ that a Rydberg ion experiences diers from the frequency _ω_ for a ground state ion due to its large polarizability [13], which has been observed as well [34]. 

In the case of the two-photon excitation of a 4D state to a Rydberg states through the intermiediate state 6P one can use STIRAP (stimulated Raman adiabatic passage) for state manipulation. STIRAP is a technique that can transfer population coherently from the 4D state to the Rydberg state. The eigenstate of the system during the adiabatic population transfer is a dark eigenstate without population of the intermediate 6P state. This protects STIRAP from losses due to radiative decay of the intermediate level [35]. To perform STIRAP the 243 nm and 309 nm laser pulses have to be switched slowly. STIRAP is also robust to small uctuations in the experimental parameters, like laser power and pulse shape [35]. The technique enables measurements of Rydberg state lifetimes. Coherent control by STIRAP was also vital for the rst single-qubit phase gate on a trapped Rydberg ion [36]. 

Rydberg states are very sensitive to electric elds. In particular Rydberg states can be ionized by relatively low static or microwave electric elds. The respective electric eld strength for static eld ionization is _E_ = 1 _/_ 9 _n_[4] for atoms and _E_ = _Z_[3] _/_ 16 _n_[4] for ions (in atomic units of electric eld) [37]. This can be seen as a result of the low binding energy. The dierence between ions and atoms stems from the fact, that the Rydberg ion has _Z_ = +2 instead of the neutral Rydberg atom with _Z_ = +1 . This gives rise to a binding energy dierent by a factor of _Z_[2] , i.e. the electron is bound more strongly to the core in an ion than in a atom. The dierent core charge leads to a dierence in orbital size _⟨r⟩_ by a factor of _Z[−]_[1] . It turns out, that the ionization of Rydberg states by microwave radiation is even less demanding and sets a threshold for the electric eld strength of _E_ = 1 _/_ 3 _n_[5] for the case of atoms and _E_ = _Z_[3] _/_ 3 _n_[5] for ions [37]. At suciently strong electric elds, the Stark manifolds of dierent Rydberg states _n_ and _n_ + 1 intersect each other. Coupling between the levels leads to avoided crossings. A microwave eld can drive a number of sequential Landau-Zener transitions of the form _n → n_ +1 , which result in ionization [38]. Rydberg states may even be ionized by black-body radiation [39]. Black-body radiation can also have an negative impact on the lifetime of Rydberg state. 

The ionization and subsequent detection of Rydberg states by static and microwave electric elds has become an important tool for the detection of Rydberg states. The accidental ionization of an Rydberg ion can be disadvantageous for a trapped ion quantum computer however. It turns a previously single charged ion into a doubly charged ion, which has dierent energy levels. It can therefore not be used as qubit any more. It was pointed out by Müller already, that this may not become a problem for the operation of a quantum computer that relies on Rydberg states with principal quantum number up to _n_ = 50 [13]. 

Experiments, exploring Rydberg states of trapped ions suer equally from unintended double-ionization of an ion. It requires the loading of a new singly-charged ion. For this reason, a fast loading technique of the ion trap is desirable. The realization and integration 

of such a technique into the current experiment is the main subject of the thesis. 

## 2. Laser Ablation Loading 

Linear Paul traps oer a deep conning potential up to several eV [40]. This allows for the direct loading of thermal ions, in contrast to experiments with neutral atoms, where one has a shallow potential and therefore, needs to cool the atoms prior to trapping. For loading of ion traps it is sucient, to use an oven, that creates a ux of thermal atoms. Those atoms are ionized by photo-ionization or electron bombardment. Photo-ionization oers a higher eciency whereas the electron beams used for electron impact ionization lead to an accumulation of charges on the insulators around the ion trap. The so-called patch elds created by those charges lead to higher heating rates of the trapped ions [41]. Hence, photo-ionization has been used in combination with a resistively heated oven in the present experiment from the very rst. The atomic beam emerging from the oven is illustrated in gure 5. 

Using an oven for the creation of atomic ux comes with several drawbacks however. It takes a certain amount of time to reach a suciently high temperature for evaporation and subsequent ion loading. In the current experiment it takes typically 15 min from switching on the oven until the rst ion can be loaded at an oven temperature of _≈_ 600 K . In addition to that, the oven remains hot for several minutes after turning it o and also heats its surroundings. It was found that the _π_ time of Rabi oscillations on the 674 nm qubit transition of the ions is slightly shifted in frequency and that the probability of doubly ionizing a Rydberg ion is increased shortly after turning o the oven. Waiting another 15 min after the loading process turns out to solve this issue, but increases the loading time for a single ion to 30 min . 

Pulsed laser ablation loading oers an alternative to loading from a thermal oven. It utilizes ablation from a target by a laser pulse for the creation of atomic ux. This atomic ux is generated almost instantaneously after the laser pulse hits the target surface and can be much larger than the one from an oven. Thus, pulsed laser ablation enables fast loading of trapped ions on demand without a signicant rise in temperature of any parts of the experimental apparatus [42]. The increase in background pressure during ablation loading has been found to vanish several seconds after the loading process in comparison to thermal atom sources, for which it can take minutes until the optimal vacuum pressure is reached again [43]. Pulsed laser ablation can also reduce the amount of deposited material on the trap electrodes [44], because the atomic ux created by laser ablation lasts only for several ns in comparison with the ux from an oven. 

Rydberg ions have a certain probability of getting doubly ionized, which makes it necessary to empty the trap and load a new ion before proceeding with the measurement. The time of at least 30 min for ion loading using an oven was obviously not convenient from an 

experimental point of view, as it limited the possible number of measurements per day. Pulsed laser ablation loading was therefore established within this thesis for the trapped Rydberg ion experiment to exploit all benets of this loading technique in the current experiment. 

In this chapter, the principle of pulsed laser ablation is discussed. The ablation from a strontium target is investigated numerically. The experimental setup is described in detail and the operation of ablation loading in the experiment at hand is explained. 

## 2.1. Pulsed Laser Ablation 

PLA (pulsed laser ablation) refers to the process during which a short laser pulse removes material from the surface of a solid target [45]. For this purpose short or ultra-short laser pulses are used and are focused down to a small spot size. Material is ablated due to sublimation or melting and subsequent evaporation. It is possible to produce atoms, ions or clusters during laser ablation. In the following, laser-solid interaction and the physical process of laser ablation is discussed for metals. Q-switched lasers as light sources for PLA are explained briey. Note, that the following discussion is limited to laser pulses with a low uence below the plasma ignition threshold. In this regime ground state atoms are ablated exclusively and no plasma is produced inside the target. 

## 2.1.1. PLA from a Metal 

A metal target can be described as a composite system of free electrons and a lattice. The energetic excitations of the lattice are dened by phonons. A laser pulse transfers energy to the electrons in the illuminated region of the sample by inverse Bremsstrahlung and photoionization [46]. The laser does not only transfer energy to the outermost electrons in the target surface, but also to electrons in a thin surface layer, whose thickness is the penetration depth _dB_ dened by the Beer-Lambert law of light attenuation. After the light absorption, the electron system is in a non-equilibrium state and subsequently thermalizes on a timescale of tens of femtoseconds due to electron-electron scattering [47]. This can lead to very high temperatures _Te_ for the electron system because of its small heat capacitance _Ce_ . The hot electrons undergo a relaxation process of electron-phonon scattering that can be understood as Cherenkov radiation of phonons emitted by the fast electrons [48]. The emission of those phonons leads to the equilibration of the electron system with the lattice and results in a local rise in the lattice temperature _Tp_ . Heat transport due to heat conductance from the illuminated area into the surrounding bulk leads to equilibration and recovery of the initial situation. 

## 2.1.2. The Two-Temperature Model of PLA 

The so-called two-temperature model is widely used to capture the time evolution of the electron and lattice temperatures _Te_ and _Tp_ by neglecting the electron thermalization on the femtosecond time-scale. It is given by the two coupled dierential equations [48, 49] 

**==> picture [309 x 24] intentionally omitted <==**

**==> picture [264 x 24] intentionally omitted <==**

**==> picture [349 x 14] intentionally omitted <==**

where equation (2.1) describes the coupling of the electron system to the heat ux _Q_ ( _⃗r_ ) inside the electron system and the source term _S_ ( _t_ ) of absorbed laser intensity. _ke_ is the electron heat conductance, _α_ = 1 _/dB_ is the absorption of the metal at the given wavelength, _R_ is its reectivity and _I_ ( _t_ ) is supposed to be the intensity of the laser pulse on the target surface. The part R of the intensity is reected from the surface, whereas the fraction (1-R) enters the target and decays due to absorption according to the BeerLambert law. The z coordinate is the propagation direction of the laser which is assumed to be perpendicular to the metal surface. The dierential equation of the electron system (2.1) and the lattice system (2.2) are connected by the energy exchange rate Γ _ep_ ( _Te − Tp_ ) due to electron phonon scattering with the electron-phonon coupling constant Γ _ep_ . 

The relevant timescales entering the two-temperature model are the electron cooling time _τe_ = _Ce/_ Γ _ep_ , the lattice heating time _τp_ = _Cp/_ Γ _ep_ and the duration of the laser pulse _τL_ . The characteristic behaviour of laser ablation depends on the relative duration of _τL_ in comparison to the time-scales _τe_ , _τp_ [50]. For the case of short laser pulses having a duration _τL_ ≳ 1 ns the relation _τe ≪ τp ≪ τL_ is fullled. This justies the assumption that lattice and electrons have the same temperature, i.e. _Te_ = _Tp_ = _T_ , due to the fast equilibration process. This simplies the dierential equations to 

**==> picture [262 x 26] intentionally omitted <==**

where _C_ and _k_ are the heat capacitance and thermal conductivity. Note that the model has also been reduced to an one dimensional model, which is valid as the length-scale _w_ on which the laser intensity _I_ ( _t,⃗r_ ) changes in directions x and y is assumed to be much larger than the heat diusion length _lT_ = 2 ~~�~~ _kτL/C_ , which is on the order of a micrometer. 

The possibility of a phase transition due to a temperature increase beyond the melting temperature _Tm_ as well as a displacement of the solid surface due to removal of material with an ablation velocity _va_ can be incorporated in this model, which leads to [45, 46]. 

**==> picture [357 x 28] intentionally omitted <==**

with _ρ, cp, Hm_ being the density, specic heat and heat of fusion. z=0 denotes the position 

of the target surface and _δ_ ( _·_ ) is the Dirac delta function. One can assume that the velocity of the evaporation front _va_ ( _T_ ) is given by [45] 

**==> picture [304 x 28] intentionally omitted <==**

based on a atomic ux _J_ following the Hertz-Knudsen equation for the evaporation of particles with mass _M_ from a surface of temperature _T_ . The sticking coecient _s ≈_ 0 _._ 18 accounts for back-ux of ablated atoms. The saturated pressure _ps_ is given by the ClausiusClapeyron relation for a phase transition from liquid to gas at a boiling point _Tb_ and a latent heat of vaporization per particle _Hv_ at _Tb_ . 

**==> picture [291 x 27] intentionally omitted <==**

## 2.1.3. Numerical Calculation 

The non-linear partial dierential equation 2.5 can be solved numerically. In the framework of this thesis, we investigate the process of laser ablation from strontium with Gaussian pulses of 1 _._ 1 ns FWHM duration _τL_ at a wavelength of 515 nm . The equation is therefore solved numerically for a strontium target using Matlab. The target was chosen to be 20 µ m , which is signicantly larger than the penetration depth _dB_ = 1 _/α_ . The boundary condition on the irradiated surface is taken to be 

**==> picture [276 x 66] intentionally omitted <==**

which accounts for energy ux out of the target due to black body radiation and vaporization of atoms. _σT_ and _ϵ_ denote the Stefan-Boltzmann constant and the emissivity respectively. A xed boundary condition 

**==> picture [252 x 12] intentionally omitted <==**

is assumed on the backside of the target with an ambient temperature _Tamb_ . The relevant material parameters are listed in table 1. 

The resulting surface temperature _T_ ( _z_ = 0 _, t_ ) and the ablation velocity _va_ for a laser u- ence of 0 _._ 3 J cm _[−]_[2] is displayed in gure 7. A rise in surface temperature above 3 _×_ 10[3] K following the laser pulse immediately is observable for less than 1 ns . A fast temperature decay is observed down to the temperature of the liquid-solid phase transition at _Tm_ = 1050 K within 14 ns . Further decrease in temperature leads to a surface at ambient temperature _Tamb_ = 300 K . 

|_ρ_|2_._64 g cm_−_3|M|1_._454 96_×_10_−_25 kg|
|---|---|---|---|
|_Tm_|1050 K|_Tb_|1650 K|
|_Tamb_|300 K|_ϵ_|0.3|
|_cp_|301 J_/_kgK|_k_|35 W_/_Km|
|_Hv_|137 kJ mol_−_1|_Hm_|7_._43 kJ mol_−_1|
|_R_|0.75|_α_|5_._7_×_105 cm_−_1|



Table 1: The relevant material parameters for the numerical solution of equation 2.5 in the case of strontium. Data from the Wolfram ElementData function and [51]. 

The ablation velocity peaks 0 _._ 5 ns after the laser pulse reached its maximum in accordance with other numerical studies of equation (2.5) [46]. This underlines the capability of PLA source of atoms for ion trap loading on demand with a short response time. The comparison of the surface temperature and the ablation velocity reveal, that signicant surface evaporation is only expected when the surface temperature exceeds the boiling temperature _Tb_ = 1650 K . This is an evident consequence of the anticipated saturation pressure (2.7) which enters the ablation velocity over the Hertz-Knudsen equation and contains the boiling temperature _Tb_ . 

**==> picture [208 x 208] intentionally omitted <==**

**==> picture [208 x 208] intentionally omitted <==**

Figure 7: On the left, the numerical result for the surface temperature is depicted for ablation from a strontium target by a Gaussian laser pulse of uence 0 _._ 3 J cm _[−]_[2] and pulse length (FWHM) 1 _._ 1 ns . A temperature above the melting temperature _Tm_ is reached for a time interval of 15 ns . After the laser pulse, the temperature decays. The temperature of the liquid to solid phase transition separates two regimes with dierent decays. The corresponding ablation velocity _va_ is shown on the right. The area under the ablation velocity peak corresponds to the ablation depth _h_ given by equation (2.12). In both plots, the dotted red line shows the intensity of the laser pulse in arbitrary units. 

By solving the 1 dimensional model for various laser uences, one can calculate the ablation depth per pulse 

**==> picture [251 x 26] intentionally omitted <==**

dependent on the laser uence. The result is shown in gure 8. The depicted t function for the ablation depth h in dependence on the laser uence _φ_ 

**==> picture [391 x 48] intentionally omitted <==**

is found empirically. It captures nicely the onset of laser ablation at a threshold uence of 0 _._ 179 J cm _[−]_[2] . From the numerical solution of the ablation depth, one can infer the number of ablated atoms. One needs to take into account the spatial dependence of the laser uence in a Gaussian beam with waist _ω_ given by _φ_ ( _x, y_ ) _∝_ exp � _−_ 2( _x_[2] + _y_[2] ) _/w_[2][�] and integrates _h_ ( _φ_ ( _x, y_ )) over the full illuminated target surface. The predicted number of ablated atoms is depicted in gure 8. Note that the thermal heat conductance in _x_ and _y_ direction inside the target is not taken into account, even though the spatial dependence of the laser intensity is accounted for. 

**==> picture [208 x 208] intentionally omitted <==**

**==> picture [208 x 208] intentionally omitted <==**

Figure 8: On the left, numerical results for the ablation depth in dependence on the laser uence in the one dimensional model is depicted. The t is found heuristically. The inferred number of ablated atoms for laser pulses with duration(FWHM) of 1 _._ 1 ns and a Gaussian beam waist 50 µ m are shown on the right. 

The resulting prediction of the number of ablated atoms depending on the pulse energy gives important insight for the operation of ablation loading of strontium ions in a linear Paul trap. The numerical result for the surface temperature and ablation velocity prove that PLA can be used as a source of atoms for the loading of an ion trap with much shorter response time than a thermal oven. 

Note, that the contour, that the laser pulses carve into the target surface for multiple pulses, was not taken into account. This can decrease the eective laser uence on the target and lead to a decrease in the number of ablated atoms. Furthermore, the shielding of the incoming laser pulse by already evaporated material at the Knudsen layer did not enter the model. This eect can limit the ablation of material at high uences. 

## 2.1.4. Q-Switched Lasers for PLA 

Q-switched lasers are widely-used, outstanding sources of laser pulses in the ns regime. Trapped ion groups performing laser ablation loading rely almost exclusively on Q-switched lasers for the creation of short laser pulses for PLA [4244, 52]. 

Like a CW (continuous wave) laser, a Q-switched laser consists of a gain medium inside a cavity. The cavity of a CW laser has a constantly high quality factor, also called Q-factor. During operation, the gain medium of a CW laser is pumped to create a population inversion. This population inversion leads to the desired light amplication due to stimulated emission, which overcomes absorption. In the steady state of the CW laser, the value of the maximally attainable population inversion is limited by gain clamping and does not increase for pump powers above the threshold value necessary for lasing. 

Q-switched lasers are based on a cavity whose Q-factor can be switched rapidly from a low to a high value. A low quality factor can be obtained, by blocking the path inside the cavity by an obscure. This prevents optical feedback to the gain medium and leads to pumping of the gain medium without oscillation. The result is a population inversion, that is not limited by gain clamping and exceeds the inversion reachable in CW mode with the same pump power. Removing the obscure from the optical path on a time scale shorter than the cavity round trip time ( _≈_ 10 ns ) switches to a large Q-factor. The resulting optical feedback and stimulated emission rapidly start up the oscillation of the laser and by that, enable the creation of a giant laser pulse. The whole population inversion is discharged into this single laser pulse, whose length is on the order of the cavity lifetime of the laser [46]. 

There exist dierent techniques to switch from low to high Q-factors. EODs (Electrooptic deectors) and AODs (acousto-optic deectors) are convenient solutions, that allow for fast deection of the light beam inside the cavity, which eectively blocks the cavity. Other methods use mechanical movement of the cavity out-coupling mirror or a saturable absorber inside the laser cavity. 

PLA ablation has many applications. It is used for example in laser machining and pulsed laser deposition of thin lms [45, 46, 50]. PLA is also used to create and load ions into a Fourier-transform ion cyclotron mass spectrometer, which is an ion trap optimized for 

the use as mass spectrometer [53]. The latter application example is very close to pulsed laser ablation loading of linear Paul traps for quantum information experiments. 

## 2.2. Experimental Realization of PLA Loading 

This section describes the realization of pulsed laser ablation loading for the linear Paul trap used in the Trapped Ion Quantum Technologies Group at Stockholm University. The experimental setup for pulsed laser ablation, which was designed, tested and operated as major accomplishment of this thesis, is explained in the following. The capabilities of the system are outlined together with characteristic properties that are important for the experimental application. The problem of ecient photo-ionization and isotope selective loading of strontium-88 is addressed together with the integration of ablation loading in the current experiment. 

## 2.2.1. Requirements on the PLA Setup 

The main purpose of the pulsed laser ablation setup is the creation of a ux of neutral atoms that crosses the trapping axis of the ion trap. There, the atoms can be ionized by photo-ionization and are trapped. 

**==> picture [423 x 238] intentionally omitted <==**

Figure 9: This photograph shows the trap inside the vacuum chamber during the assembly process in 2014 [23]. The trap is embedded in a sapphire holder, which is supported by a mount made from titanium. Above the trap, the cylindrical mount for the aspheric lens can be seen. The resistively heated strontium ovens are located in the bottom of the titanium mount. The red inset shows the ovens mounted in the macor holder before it was mounted inside the titanium holder. In green, the only possible optical path of the ablation laser is outlined. 

Some diculties arise, as laser ablation was not planned from the beginning of the expe- 

riment. The previous loading procedure uses one of two resistively heated ovens, that are located inside the vacuum chamber approximately 45 mm under the ion trap. In between the ovens and the ion trap is a rectangular slit acting as skimmer to prevent atoms that exit the oven at an angle from coating the trap blades. The assembly inside the vacuum chamber is depicted in gure 9. There is a distance of 3 mm between the two ovens and the oven's aperture is 1 _._ 5 mm in radius. Both ovens were mounted in a holder made from macor, which was put inside the bottom of the titanium mount inside the vacuum chamber. Figure 9 shows a photograph of the strontium ovens mounted in the holder. 

The ambitious goal of the work described here was to use one of the two ovens as strontium target for PLA. This avoids opening the vacuum chamber for the installation of an ablation target. Opening the chamber would have interrupted the experiment for several months and would have come with the risk of losing the outstanding vacuum pressure below 10 _[−]_[10] mbar . Using the ovens as ablation target means, however, that there is only one possible path for the ablation laser beam. It enters through the viewport on the top of the vacuum chamber, proceeds through an aspheric lens[1] , passes in between the blade electrodes, transits the skimmer and terminates in one of the ovens. The optical path inside the vacuum chamber is sketched in gure 9. The respective viewport and aspheric lens are also used for PMT detection. The blade electrodes are separated by only 750 µ m . 

The PLA setup should deliver laser pulses, that can be power regulated. The regulation of the pulse power is used to control of the ablation process and thus the amount of ablated atoms. The pulses have to be focused into the strontium ovens taking into account the beam path inside the vacuum chamber. It is important that the laser is not focused too much on the viewport window or the aspheric lense to avoid laser-induced damage. At the same time, the beam diameter at the position of the trap electrodes should be tight enough to avoid any ablation from the blades. This also requires a precise alignment of the laser beam with respect to the trap blades, which has to be maintained on a long term. The gold coating of the trap electrodes may otherwise be damaged by laser ablation. The possibility of monitoring the trap blades during the experiment is therefore necessary. On top of that, monitoring of the ablation laser at the oven position is very helpful for alignment. 

## 2.2.2. Design of the PLA Setup 

In gure 10 the experimental setup is sketched. A Q-switched laser[2] at a wavelength of 515 nm is used. It oers the possibility of continuous pulsing with a pulse repetition rate between 17 Hz and 2 kHz . A single shot mode allows for triggering of single pulses on demand by a TTL (transistor-transistor logic) signal. The laser delivers an outstanding Gaussian beam shape with a beam quality factor _M_[2] = 1 _._ 02 . The laser pulses have a 

> 1 Asphericon AFL25-40-S-A, f= 40 mm 

> 2 Coherent Flare-NX, pulse duration (FWHM) 1 _._ 1 ns 

**==> picture [423 x 295] intentionally omitted <==**

Figure 10: Schematic of the PLA setup. The main parts are the laser, a unit to control the pulse energy, a spatial lter and a unit to capture an image of the blade electrodes. The PLA setup has to include the necessary parts for PMT detection and has to direct the laser pulses into the ovens inside the vacuum chamber. 

maximal energy of 330 µ J . The pulse energy for ablation loading can be regulated using an additional half-wave plate in combination with a polarizing beam splitter[3] . An 0 _._ 75 _[′′]_ aperture beam dump[4] is used to block the unused fraction of laser power. The laser beam is expanded by a plano-concave lens[5] before the beam dump to prevent fast degradation of the beam dump's surface. For a beam waist of 25 µ m inside the strontium oven the available pulse energy suces for pulsed laser ablation from strontium as one can see in comparison with the numerical results in gure 8. 

A Keplerian telescope consisting of two aspheric lenses[6] with _f_ = 25 mm and _f_ = 100 mm is used to expand the Gaussian laser beam. By inserting a 50 µ m pinhole at the focal point of the rst lens, one can use the telescope as spatial lter. This can increase the stability of the alignment and compensate for small displacements of the laser beam, which can consequently protect the trap blades from damage. The radius of the pinhole is chosen to be twice as large as the 1 _/e_[2] radius of the Gaussian beam at the focal point of the rst lens. This result is based on Physical Beam Propagation data simulated in Zemax using the lens data provided by Edmund Optics and the experimentally determined complex 

> 3 Altechna 2-HPCB-B 

> 4 Kentek Trap-It ABD-075 

> 5 Edmund Optics 48-265 PCV 6 _×_ -6 VIS 

> 6 Edmund Optics best form aspheres 89-431 25 _×_ 25 at 532 nm and 89-434 25 _×_ 100 at 532 nm 

beam parameter of the laser. 

As alternative to a spatial lter, one could also couple the laser into an optical ber. Normal photonic crystal bers and step-index bers have been ruled out experimentally due to their low laser induced damage threshold. The only optical ber, that may be able to withstand the enormous peak power density of of the used pulsed laser is a hollow core photonic crystal ber from NKT Photonics. A test and later use of this ber was disregarded due to its high price and high minimum purchase. The stability tests of the setup described in section 2.2.3 showed, that the beam from the Q-switched laser is stable without the necessity of a spatial lter for additional stabilization. 

A _f_ = 200 mm lens[7] is used to focus the laser beam into one of the strontium ovens. Between the spatial lter and the lens a combination of half-wave plate, polarizing beam cube and quarter-wave plate is placed. The half-wave plate is adjusted such, that the beam cube reects maximally. The light passes the quarter-wave plate and is guided into the vacuum chamber to the ovens. Light from the ablation laser that is reected from the blades or the oven is collected by the same optics, that is used to focus it. This reected light passes the quarter wave-plate a second time and can now pass the polarizing beam cube. Focusing this light on the sensor of a webcam provides a monitoring of the trap blades or the ovens. 

The whole optical path including the spatial lter, the 200 mm lens before the vacuum chamber, the glass window of the viewport and the aspheric lens inside the vacuum chamber was simulated using Zemax OpticStudio. The measured complex beam parameter of the Q-switched laser was taken into account as well as lens data from the manufacturers. The lenses on the PLA setup outside the vacuum were chosen such, that one has the possibility of spatial ltering and retains a focal spot size as small as possible at the oven position. At the same time, one would like to reach a rather large beam diameter at the position of the viewport and the aspheric lens to avoid any laser induced damage. Those two optical elements are important as they are used to collect uorescence light from the trapped ions for PMT detection. Enough space was taken into account to insert a dichroic mirror[8] to separate the uorescence light from the optical path of the ablation laser. The mentioned combination of lenses turned out to be a suitable combination. A Gaussian beam waist _w_ 0 (dened as 1/ _e_[2] radius) of 25 µ m and a Rayleigh length _zR_ = 3 _._ 8 mm can be reached at the oven position according to the simulation. The predicted radius _w_ at the viewport _w_ = 284 µ m and at the aspheric lense _w_ = 471 µ m are larger by one order of magnitude. At the position of the trap, the beam has a radius of 169 µ m and should t through the space in between the blades without damaging them. It was also checked in the simulation, that the resolution of 8 mrad per revolution of the used mirror mounts is sucient to align the laser such that it passes in between the blades and terminates in 

> 7 Thorlabs plan convex lens LA1708-A f= 200 mm 

> 8 Thorlabs 2 _′′_ longpass dichroic mirror DMLP490L, 490 nm cuto wavelength 

one of the ovens. 

## 2.2.3. Test and Characterization of the PLA Setup 

The described setup for pulsed laser ablation was implemented and tested prior to its integration and use in the experiment. A description of the out-carried tests and the inferred performance of the experimental equipment is given below. 

**==> picture [208 x 208] intentionally omitted <==**

**==> picture [208 x 208] intentionally omitted <==**

Figure 11: On the left, the laser pulse energy as well as the temperature of the base plate of the laser are depicted. The pulse energies are normalized to the maximal value reached. It can be seen immediately, that the laser needs 100 min to reach its operation temperature and maximum pulse energy. On the right, the dependency of pulse energy on the repetition frequency of the laser in continuous pulse mode is depicted. The energies are normalized to the value at 1 kHz and follow an empirically found quadratic t. 

## Test of the Q-Switched Laser 

The Q-switched laser was characterized with respect to its output power, temperature stability and beam parameter. 

To test the temperature stability of the laser, it was operated in single-shot mode for a period longer than 8 h . Pulses were triggerd by TTL pulses at a low repetition rate of 10 Hz . The temperature of the laser head was measured inside a blind drill hole in the laser head housing using a gauged thermistor. The corresponding measurement is depicted in gure 11. It turned out, that it takes approximately 1 _._ 5 h for the laser to reach its constant operation temperature of 30 _[◦]_ C . An increase of the laser pulse energy by a factor of two during this period was observed, which can be attributed to the change in temperature. During the test, the laser was switched to stand-by for 3 h without disconnecting the power supply. The temperature stayed constant during this time and the pulse energy directly after the standby period was almost unchanged. 

The same test was performed in continuous pulse mode at a repetition frequency of 2 kHz with the only dierence, that a temperature of 37 _[◦]_ C was observed after warm-up. This is 

slightly above the manufacturer-advised base plate temperature of 35 _[◦]_ C and means that the laser should be used with a fan in addition to the already mounted heat sink when used in continuous pulse mode. 

It was checked that a output power of 660 mW can be reached at 2 kHz repetition frequency. This corresponds to pulses of 330 µ J in energy, which equals the value specied by the manufacturer. The pulse energy varies with the repetition frequency by _±_ 5% as one can deduce from the corresponding measurement in gure 11. In single shot mode, one can expect an even smaller pulse energy and large variations from pulse to pulse. 

The complex beam parameter of the laser was determined to be ( _−_ 34 + 393 _i_ )mm , corresponding to a beam waist of (254 _±_ 5) µ m positioned (34 _±_ 17) mm inside the laser head. This measurement was done using a CMOS (complementary metal-oxide-semiconductor) camera sensor and the result deviates from the specied 389 µ m waist located 58 mm inside the laser head. 

## Test Setup 

A test setup was built to test the mechanical stability of the setup and optimize the focus of the ablation laser. A photograph is shown in gure 12. The whole optics was mounted and aligned on an anodized aluminium breadboard, which was custom made in a barbell shape to t on top of the vacuum chamber next to the helical resonator and already existing optics. A hole with diameter 10 cm is cut out in the center of the breadboard, to allow for access to the viewport on top of the vacuum chamber. 

To check the optical path and the focal spot size determined earlier by a Zemax OpticStudio simulation, a viewport as well as an aspheric lens was mounted in the test setup to imitate the optics inside the vacuum chamber. Both optical components are spare parts identical with the ones used in the experiment. The trap blades are mimicked by a variable rectangular slit. A spare oven holder made from macor ceramic is placed behind the slit. A picture of the components corresponding to the optics inside the vacuum is shown in gure 13. The complete beam propagation can be checked and the focal spot size can be optimized using this test setup. It even oers the possibility of measuring the beam waist at positions that would lie inside the vacuum chamber, which would otherwise only be possible by opening the vacuum chamber. 

After optimizing the focal spot size by changing the distances between the lenses, it could be reduced to a size as the one predicted in the Zemax calculation. A waist of _w_ = (25 _._ 1 _±_ 1 _._ 5) µ m and a Rayleigh length _zR_ = (3 _._ 8 _±_ 0 _._ 5) mm was measured in very good agreement with the simulations, even though the distances between the optical components had to be altered from the ones in the simulation to obtain the result. Compared to the focus, a beam diameter larger by a factor of 30 on the aspheric lens and larger by at least 

**==> picture [423 x 281] intentionally omitted <==**

Figure 12: The test setup to characterize the PLA is shown. Most of the parts on the black anodized breadboard are used in the experiment. The optical components on top of the picture mounted on the table imitate the viewport and the components in the vacuum chamber for testing purposes. A hole in the center of the breadboard in combination with a mirror mounted at azimuth angle of 45 ° allow guiding the laser beam into the vacuum chamber in the real experiment. A ber coupled HeNe Laser is used in the upper left corner of the breadboard to pre-align the optical path, which is used for uorescences detection by a PMT in the experiment. 

a factor of 6 on the viewport could be observed. They should thus be protected from laser induced damage. It could also be veried experimentally based on the test setup, that the beam can be aligned to t through the trap blades. The laser spot could be positioned with a precision of _±_ 18 µ m on the oven holder, even though there is a long optical path of almost 1 m between the mirror, that can be used for this alignment, and the oven position. 

The optical power, that can potentially reach the target was measured. The half-wave plate position was varied, to test the capability of power regulation. The result is depicted in gure 14 and shows, that the pulse energy can be tuned with the manual translation mount with a resolution of _±_ 2 µ J . One can also see from the measurement, that 40% of the pulse energy are lost due to reections on the surface of optical components. 

To test the stability of the design, the laser was set to single-shot mode and TTL pulses at a repetition rate of 10 Hz triggered laser pulses over a period longer than 5 h . The intensity prole of the laser pulses was recorded by a CMOS camera sensor, which was placed at the image plane where the strontium target would be positioned in the real experiment. The absolute change of position was obtained by tting the measured intensity proles by two dimensional Gaussian distributions. The result is depicted in gure 14. It shows, 

**==> picture [423 x 281] intentionally omitted <==**

Figure 13: A close-up view of the components imitating the vacuum chamber and the components inside it are shown. Used parts are a viewport, an aspheric lense, a variable rectangular aperture and an oven holder. The estimated beam propagation can be measured in this conguration. 

that the laser spot moved by less than 3 µ m . This conrms the high mechanical stability of the setup and the laser. In particular, the measured change in beam position is smaller than the beam waist by an order of magnitude and thus, can be neglected. The change in laser beam position in the image plane cannot be fully explained by a change in laser temperature, which can also be seen from gure 14. This test was performed without using the spatial lter and indicates, that the spatial lter is not necessary. Note, that the maximal displacement of the laser beam in the image plane of 3 µ m has a rather large systematic uncertainty _±_ 2 _._ 65 µ m stemming from the pixel size of the used CMOS chip. During this test, the laser was set into stand-by for approximately 1 h , which did not lead to a noticeable change in the measured beam position. In a separate test, the laser was turned o completely for several days. No changes in laser beam position larger than the ones in the test described before could be observed. 

For the application of pulsed laser ablation for creating of a ux of atoms, small changes in the laser position on the target can even be helpful. If the laser beam remains on the exact same position for all times, a groove will arise on the target surface. This alters the angle of incident dependent on the distance from the center, the absorption, the thermal conductivity of the target and the shielding of incoming light. This can have a long-term impact on the ablation rate [45]. For this reason, some trapped ion groups using ablation loading from a target utilize a mirror that can be moved by piezoelectric actuators. This 

**==> picture [208 x 208] intentionally omitted <==**

**==> picture [208 x 208] intentionally omitted <==**

Figure 14: On the left, measured pulse energies (dots) are plotted against the position of the half-wave plate, which is positioned before the rst polarizing beam splitter. The ability of adjusting the pulse energy becomes obvious and a good agreement with the theoretically expected t curve can be seen. On the right, the change of laser beam position during a medium-term test is depicted in blue. Large error bars result from the resolution of the CMOS chip, that recorded the laser beam position. The changes in position are smaller than the beam waist by an order of magnitude and can in no way worsen the performance of the PLA setup in the experiment. The changes in temperature upon start-up (red) does not signicantly aect the beam position. 

way, one can introduce a small jitter of the laser beam position on the target, which helps retaining a constant atomic ux over long periods of time [43]. A mirror with piezo actuators was not considered in the design, but can be kept in mind. Should it turn out, that the ablation rate from the strontium target decreases in the daily application of PLA due to a constant beam position, this can still be implemented later. 

## Laser Ablation from a Test Target 

It had not been clear during the design and test period of the PLA setup, if it would be feasible to ablate atoms from the strontium inside the ovens. That is, why an alternative solution, which would include opening the vacuum chamber and mounting an ablation target inside of it, was always kept in mind. As target SrTiO3[9] was choosen, as it turned out to be a suitable target for loading of strontium ions into a trap in a comparative test [44]. SrTiO3 provides a constant atomic yield during PLA on a long-term and does not oxidize, which can decrease the atomic ux obtained from PLA. An aluminium mount was manufactured in the mechanical workshop of Albanova that can be used to mount the target in the vacuum chamber. 

To make sure that material can be ablated from the target and to test the capability of the PLA setup for laser ablation, the target was placed in the test setup at the corresponding position, where it would be mounted in the experiment. This coincidences with the position, where the entrance of the strontium ovens is in the real experiment. The SrTiO3 

> 9 MTI cooperation, SrTiO3 (100) polished single crystal of size 10 _×_ 5 _×_ 0 _._ 5 mm 

**==> picture [423 x 245] intentionally omitted <==**

Figure 15: A microscope capture of a SrTiO3 target after exposure to 1 _._ 2 _×_ 10[6] pulses of approximately 100 µ J pulse energy is shown. A small crater is clearly visible as a result of laser ablation. The shown grid has a spacing size of 100 µ m . 

target was exposed to approximately 1 _._ 2 _×_ 10[6] pulses with an energy of 100 µ J . The number and energy of the laser pulses was chosen large in comparison with various publications about PLA loading of ion traps. This way, a large amount of material was ablated from the target surface. The microscopic crater resulting from pulsed laser ablation was even visible on a microscope picture, which is shown in gure 15. The edges of the crater are not sharp and are bordered by a tiny bright corona. This is an indication, that material was molten during the ablation process, which is typical for laser ablation by ns laser pulses in contrast to ablation by ultra-short ( ps to fs ) pulses [50]. The size of the crater is approximately 75 µ m _×_ 50 µ m which ts very well to the value of the measured beam waist. 

## Test of the Imaging 

A similar test was performed, during which a piece of gold plated at glass was placed at the position where the trap blades are located in the real experiment. This way, the possible danger of ablating gold from the trap blades was ruled out. There was ablation of material visible only for laser pulses with an energy _>_ 100 µ J , which is far above the energy range were the onset of laser ablation is expected. The area in which laser ablation was visible was smaller than 400 µ m _×_ 500 µ m . This means, if the ablation laser beam is aligned precisely, the trap blades are not endangered as they are 750 µ m apart from each other. The gold surface of the trap blades is also free from any dirt as well as scratches in contrast to the used gold surface in this test. This makes the trap blades even more resistant to PLA than one may expect from this test. 

The imaging of the trap blades for monitoring purposes was tried out in the test setup as well. For this, a vernier calliper was almost closed to form a slit of size 300 µ m . It was placed exactly at the position, where the trap blades would be in the real experiment. It turned out, that a lens with focal length 75 mm is suitable to obtain a nice image of the calliper slit. From this, it was inferred, that the imaging design would also be capable of capturing an image of the trap blades in the real experiment. It was already very dicult in the test setup, to take an image of the plane, where the ovens would be located. To test this, a piece of graph paper was placed at the oven position and the camera sensor was moved slightly for focusing. Only when illuminating the graph paper with a 300 lumen torch, an image could be recorded using the camera. As there is no proper way of illuminating the ovens inside the vacuum chamber, it is clear, that the imaging unit cannot be used to take an image of the strontium ovens. To resolve this, a webcam was mounted next to one of the viewports on the side of the vacuum chamber, when ablation loading was integrated into the experiment later. This way, one can take an image of the oven for alignment of the ablation laser position and in parallel an image of the trap blades using the imaging on the PLA setup. 

## 2.2.4. Integration into Current Experiment 

After the PLA setup was tested successfully, the mirror in the center of the breadboard ° was replaced by a mirror at an azimuthal angle of 45 . It guides the optical path in a direction perpendicular to the plane of the breadboard through the hole in the center of the breadboard. The backreection from a mirror lying on the optical table below the mirror was used to make the alignment of the inclined mirror as precise as possible. This assures, that the ablation laser will be directed through the center of the vacuum chamber at the correct angle without the need of considerable alignment. The optical path which would be used for PMT detection of uorescence light was pre-adjusted by using a ber coupled HeNe laser. The PLA setup was then ready to be transferred and integrated into the main experiment. The whole PLA setup was moved carefully above the vacuum chamber and mounted on four 1 _._ 5 _[′′]_ thick, 31 cm long posts. There is no mechanical connection with the PLA setup except from the posts. In particular, there is no direct contact between the vacuum chamber and the breadboard of the PLA setup apart from the fact that they are mounted on the same optical table. 

Subsequently, the PMT was mounted on the breadboard. A _f_ = 250 mm lens was placed in front of it, to direct the uorescence light from the trapped ions onto the sensitive area of the detector. In front of the PMT there is an adjustable rectangular aperture, that is placed at the image plane of the ions to reduce the detection of stray light not emerging from the ions. In addition, four lters block photons of undesired frequency from entering the PMT. The signal to noise ratio of the detected uorescence signal from a cloud of trapped ions was optimized by changing the direction of the optical path with the dielectric and the dichroic mirror in front of the PMT. The size and position of 

the aperture were optimized in addition. Prior to the realization of PLA loading, the PMT had been mounted at the end of an approximately 25 cm long lens tube, which was mounted vertically on top of the vacuum chamber. Thus, the adjustment had been rather inconvenient and the stability had been very poor. Mounting the PMT on the breadboard and introducing two mirrors for alignment improved the situation. 

Subsequently, the webcam on the PLA breadboard was mounted and adjusted, to enable live imaging of the blade electrodes. An additional camera was mounted above the side window of the vacuum chamber with free sight to the strontium ovens. The ablation laser could be aligned after that. It was set in continuous pulse mode at the lowest possible pulse energy. The adjustment using the two mirrors before the dichroic mirror turned out to be convenient without altering the alignment of the PMT. The live image from the two webcams eased the adjustment of the ablation laser beam. During the process of alignment at minimum pulse energy at 100 Hz repetition frequency some ions were already loaded unexpectedly by laser ablation and photo-ionization. 

For further integration of PLA loading into the established experimental setup, a software and user interface for the used EMCCD camera was programmed. It oers convenient access to the camera's features that are used in the experiment. In particular, it oers a TCP (transmission control protocol) camera server client communication. This is especially useful as the camera and the rest of the experiment are operated by dierent computers. Communication of the experiment PC with the camera software on a dierent computer becomes essential when it comes to automatic PLA loading and experiments including the read-out of camera images. Additional features of the newly created software are an user friendly GUI (graphical user interface) and a software that can detect the number of ions and the presence of dark ions in a camera image with very high delity. More details about the camera software can be found in the appendix A. 

For ideal and automatic control of the loading process two optical shutters moved by servomotors[10] were introduced. One is used to switch the photo-ionization laser on and o. The other shutter blocks and unblocks the 0[th] order of 422 nm cooling light at an AOM (acousto-optic modulator). The light passes this AOM in double-pass conguration. The 0[th] and 1[st] order dier in frequency by 220 MHz . The 0[th] order beam has more power and is farther red detuned compared to the 1[st] order beam. Thus, it is used for the fast and ecient cooling of hot ions during loading. In addition, a switch[11] that turns o the ion trap when receiving a TTL signal was installed after the RF driver[12] . It makes it possible to empty the trap remotely. 

In some situations, the experimentalist wants to reduce the number of ions in the trap. 

> 10 SAVÖX SAVSH0264MG 

> 11 Mini-Circuits, switch ZASWA-2-50-DR+ 

> 12 Rhode & Schwarz SML02 9 kHz 2 _._ 2 GHz 

For this purpose, a relay was installed that switches the voltage of one opposite blade electrode pair from 1 _._ 5 V provided by a battery to 55 V provided by a power supply. A bistable latching mechanical relay[13] was chosen for this purpose as it creates a magnetic eld only during the switching process and isolates the trap blades from the noise of the power supply when the battery voltage is applied. The latter is also the reason, why an earlier version with a solid-state relay was discarded. Applying 55 V to the trap blades pushes the ions out of the trap and is a convenient way to reduce the number of ions on a time-scale below one minute. When the desired number of ions is loaded and formed a Coulomb crystal, there are often additional hot ions that orbit around the center of the trap and are not cooled eciently by Doppler and sympathetic cooling. Applying a higher voltage instead of the battery voltage to the trap blades for a short time can remove those hot ions without losing any of the ions that are already suciently cold. 

## 2.2.5. Photo-Ionization 

The neutral atoms created by PLA or an oven are photo-ionized. This process is much more ecient than ionization by electron-bombardment [41]. It also creates no patch electric elds emerging from stray charges, which would contribute considerably to the heating rates of the trapped ions [24]. 

Neutral strontium has two valence electrons and its ground state conguration is (5s[2] )[1] S0 . It can be auto-ionized, i.e. strontium can be excited in a two-photon excitation rst to the state (5s5p)[1] P1 and subsequentally to an auto-ionizing state (5p[2] )[1] D2 [54, 55]. This state is short lived and decays by auto-ionization with high probability. During this process, one of the excited electron transfers its energy due to Coulomb interaction to the other excited electron which has as consequence an energy above the ionization energy [56]. Auto-ionization is thus accompanied by the emission of an electron, leaving a strontium ion behind. 

The two step photo-ionization has been proven to be suitable for quantum information experiments with trapped strontium ions [26, 57]. For the rst step of the excitation, a grating stabilized 461 nm laser[14] is used in the experiment at hand. A pigtailed single mode laser[15] at 405 nm is used for the second excitation step. It delivers a Gaussian intensity prole, which enables much better ber coupling eciency compared to an earlier used blu-ray laser diode[16] . To allow for small wavelength adjustments of the 405 nm laser diode, a copper mount was designed on top of which a Peltier element and a heat sink can be mounted. A picture is shown in gure 16. Wavelength adjustment over a range of 1 nm is attainable, as one can see in gure 16. Both photo-ionization lasers are overlapped with the 243 nm laser and guided to the trap through a photonic crystal ber. All three lasers 

> 13 AXICOM V23079-B1201-B301, bistable, 2 coils, coil voltage 5V 

> 14 Toptica DL pro 

> 15 Laser diode: Thorlabs L405-SF10; Driver: Thorlabs IP250-BV 

> 16 InsaneWare blu-ray 

are focused onto the center of the trap through one of the end-cap electrodes. 

**==> picture [229 x 229] intentionally omitted <==**

**==> picture [191 x 199] intentionally omitted <==**

Figure 16: On the right, the temperature controlled mount made from copper can be seen. It has a Peltier element and a heat sink on top. A small hole withouth thread can be used to position a temperature sensor in close proximity to the laser diode. On the left, the change in wavelength with respect to the laser diode temperature is plotted. It can be tuned over a range of almost 1 nm . 

The wavelength of the rst excitation step had been determined to be 460 _._ 8620 nm by measuring the uorescence of neutral strontium atoms emerging from one of the ovens and passing the trap center. This is in agreement with precision spectroscopy measurements of strontium optical clocks [58] and earlier spectroscopy experiments of strontium [54, 55]. 

## 2.2.6. Isotope Selective Loading 

In several trapped ion experiments photo-ionization enables isotope selective loading [59]. This works especially well for calcium, where a two step photo-ionization as explained for strontium can be applied. The transition for the rst excitation step dier by more than 300 MHz for dierent calcium isotopes. Tuning the laser that drives the rst excitation step to the wavelength of the desired isotope can enable almost exclusive ionization and thus, loading of the desired isotope. Using sources with an enriched amount of the desired isotope can help loading only the desired isotope with very high probability. 

For strontium, the situation is dierent. Strontium has four stable isotopes. The desired isotope for this experiment is[88] Sr which has the highest natural abundance of all four isotopes, that are listed in table 2. The isotope shift of the 461 nm transitions in the dierent strontium isotopes is on the order of the spectral linewidth of the transitions. Thus, the transition lines of the four isotopes overlap in the spectrum [61]. This makes photo-ionization using the 461 nm and 405 nm transitions less isotope selective. As a consequence of the almost identical 461 nm transition in dierent isotopes, not even blue magneto optical traps for neutral atoms based on the 461 nm transition are isotope 

|Isotope|Abundance in %|Nuclear spin|
|---|---|---|
|88Sr<br>87Sr<br>86Sr<br>84Sr|82.58<br>7.00<br>9.86<br>0.56|0<br>9/2<br>0<br>0|



Table 2: Abundance of natural strontium isotopes and their nuclear spin. Values from [60]. 

selective [58, 62]. In experiments with cold neutral strontium atoms, one uses the blue MOT to cool down to mK and then switches to a red MOT that uses the narrow 689 nm clock transition from state[1] S0 to[3] P1 to cool down to µ K [58]. This transition is much narrower with a width of 7 _._ 4 kHz and the dierence in frequency for the dierent isotopes is larger for this transition. Using the 689 nm transition for isotope selective ionization or even trapping and cooling prior to ionization would require additional laser sources like a narrowband laser at 689 nm . 

Deecting the beam of the undesired isotope[87] Sr on its path from the oven to the ion trap may avoid the loading of this isotope. This may be done by deection in an inhomogeneous magnetic eld as in a usual Stern-Gerlach apparatus or by deection in a light eld in the fashion of an optical Stern-Gerlach experiment [63]. This can only work for the isotope 87Sr because it is the only strontium isotope with a spin. As the atoms ablated from a target by PLA have a velocity on the order of km s _[−]_[1] [64] and as the distance between ablation target and ion trap is short ( _<_ 5 cm ) in our experiment, the time during which the ions experience a force is short. It would take a magnetic eld gradient on the order of 10[4] T cm _[−]_[1] to deect the atomic beam such that it does not enter the trap. Thus, a deection of the[87] Sr atomic beam stemming from a light eld or a inhomogeneous magnetic eld, that would be sucient to avoid loading of this isotope is not feasible. 

Some other techniques exist, that can be used to eliminate ions of the unwanted isotopes from the RF trap, if they have been ionized and loaded into the trap already [65]. A simple way is to use the mass selectivity of the RF trap. The motion of the ions in a trap follow a Mathieu equation. If the trapping parameters _q_ = 2 _eV/mr_ 0[2][Ω][2] _RF_[and] _[a]_[ = 4] _[eU/mr]_ 0[2][Ω][2] _RF_ lead to stable solutions of this equation, one can expect trapping of ions. For other values of _q_ and _a_ , the solution may be unstable and trapping of ions becomes impossible [40]. The parameters _q_ and _a_ depend on the isotope mass of the particles and the voltages applied to the trap blades. This makes it possible, to apply a voltage to the trap blades, that allows for the trapping of particles with the mass of the desired isotope only. Another possibility is direct cooling of only the desired target isotope combined with a shallow trap depth and selective heating of the undesired isotopes [66]. Non-linear resonance in a Paul trap can emerge as real ion traps cannot create an ideal RF quadrupole potential. This 

leads to instabilities for certain values of _q_ and _a_ , which has been exploited as well to select certain isotopes in ion traps [67]. 

It is also possible to realize deterministic loading of the desired isotope by changing the trap type. In the current linear Paul trap, the zones where ions are loaded and were experiments are performed with the ions are identical. It is possible, to manufacture linear Paul traps with segmented blade electrodes [68]. In such a trap, one can have a zone that is exclusively used for loading. If the correct isotope was loaded, one shuttles the ion from the loading zone into the zone, where experiments are performed with the ions. This is done by changing the voltage on the trap electrodes. 

## 2.3. Pulsed Laser Ablation Loading 

Several tests and experiments have been carried in order to test PLA loading of trapped ions in the current experiment. The results and a description of the optimal operation mode are described in the following. 

## 2.3.1. Cooling Time of PLA Loaded Ions 

Already the rst attempts of loading ions by single laser pulses were successful and showed, that loading of ions by single pulses is feasible. It was recognized, however, that the time between the ablation pulse and the ion being crystallized and detected in the center of the trap can be fairly long. To investigate this more quantitatively, the probabilities of detecting zero, one and more than one ions in dependence of the time _t_ after an ablation pulse was determined. 

For this purpose, the ablation pulse is triggered a single time and images of the center of the trap are taken by the EMCCD camera for 50 s . During the whole procedure, the 422 nm Doppler cooling laser and the 1092 nm repump laser were used for laser cooling. Both lasers were controlled via a double-pass AOM setup and both, 0[th] and 1[st] order of the 422 nm , were sent to the ion. Thus, the 422 nm light had two components with detunings ∆1 _≈−_ Γ _/_ 2 = _−_ 2 _π ×_ 11 MHz and ∆2 _≈−_ 2 _π ×_ 231 MHz . The far detuned beam served to cool hot ions in the trap. The whole procedure was repeated 100 times. From the images taken after a delay _t_ after the ablation pulse, the probabilities of nding a certain number of ions at this delay time were deduced. The result can be seen in gure 17. One can see clearly, that the probability to nd one ion peaks 3 s after the ablation pulse was triggered. In contrast, the probability of nding more than one ion increases monotonically. This suggests, that ions are already trapped but stay at high temperature for a long time despite of Doppler cooling. 

**==> picture [423 x 226] intentionally omitted <==**

Figure 17: The probability of detecting no ion, one ion and more than one ion at delay time _t_ after a ablation pulse at _t_ = 0 is depicted. The pulse energy was 50 µ J . 

The single Doppler cooling beam in the given experiment adds a friction force to the force of the harmonic potential. This beam is red-detuned, such that the ions are only cooled when moving towards the light source. Only then, they are resonant due to the Doppler shift and can scatter photons, that carry away their energy. For ions that are already cold and therefore, have a small velocity that suces _[⃗] k · ⃗v_ ≲ Γ _/_ 2 Doppler cooling is optimized for a detuning ∆1 = _−_ Γ _/_ 2 . The constraint on the velocity corresponds to a kinetic energy _Ekin_ = 8 µ eV and corresponding temperature _T_ = 0 _._ 1 K . The energy of an ion directly after ionization in the trapping region depends on its velocity and the position, where it is ionized. The velocity determines its initial kinetic energy whilst the position xes the initial potential energy. The kinetic energy of atoms from PLA has been found to be up to 350 meV [42]. The used trap has a potential depth of _≈_ 14 eV . Ions generated by PLA can have a high energy and velocity that does not full _[⃗] k · ⃗v_ ≲ Γ _/_ 2 . The single Doppler cooling beam with detuning ∆1 can cool a fast ion only on a very short path of its trajectory in phase space, where the ion velocity is close to zero. Small velocities occur only at large distances from the potential minimum. The Doppler cooling beam is focused on the trap center, such that the ion is at a position of small intensity, when the resonance condition is fullled. This means, that the single light eld with detuning ∆1 = _−_ Γ _/_ 2 is not sucient, to cool an ion generated by PLA. 

To be able to cool even hot ions, an additional Doppler cooling component with a detuning ∆2 = _−_ 2 _π ×_ 231 MHz is introduced. The larger detuning means, that the ion can be resonant at higher velocity and smaller distance from the trap center. This is depicted in gure 18. It shows the trajectory of a trapped ion of energy 50 meV . Also shown are the regions in phase space, where the Doppler cooling laser actually exhibits a dissipative friction force on the ion. The additional cooling beam with detuning ∆2 increases the 

space of eective cooling in the phase space. The time, that it takes for an ion to be cooled, such that it enters the crystal phase in the trapping potential can still be on the order of minutes as one can see from the measurement result in gure 17. 

**==> picture [339 x 339] intentionally omitted <==**

Figure 18: The one dimensional phase space of an ion in a harmonic potential with _ω_ = 2 _π ×_ 1 MHz is shown. The regions, in which the ion experiences a friction force and gets eectively cooled due to the Doppler cooling beams are shown as blue ellipses. Their widths is given by the region, in which the uorescence of an ion reaches more than half of its maximum value. This is the region that is eectively cooled by the 422 nm and 1092 nm beam. The height of the beam is determined by the width Γ of the transition, that is used for Doppler cooling. The trajectory of a trapped ion with energy 50 meV is plotted exemplary. It never enters the region of eective Doppler cooling and can therefore orbit a long time around the center of the trap. 

In practice, one can load ions fast, by triggering multiple laser pulses for PLA. The time until all ions in the trap condense into the crystal phase may take several minutes. The desired number of ions is reached much earlier, however. The additional ions, that are not yet crystallized can be expelled from the ion trap, by applying a DC voltage _U_ = 55 V instead of the usual _U_ = 1 _._ 5 V on the trap electrodes. This makes the trajectory of the ions unstable, as the trapping parameter _a_ is moved out of the stability region in the _a − q_ plane. Applying the voltage for only some seconds, removes all hot ions, but the ions that are already condensed into the crystal phase stay in the trap. 

To improve the cooling, during loading, we performed the following test. The 405 nm laser was overlapped with the 422 nm Doppler cooling laser, such that only ions at the 

focus of the cooling lasers can be ionized. This may prevent ions from being ionized at a large radius from the trap center, where the intensity of the 422 nm light is low and where they would obtain a large potential energy and thus, would orbit around the trap center without cooling for a time on the order of minutes. With this congurations, no ions could be loaded at all. The reason for that may be that the two photo-ionization lasers did not overlap or that the intensity of the 405 nm laser was too small at the trap center. 

One may also improve Doppler cooling by increasing the region that is illuminated by the Doppler cooling beam. The size of the area that is cooled eectively was found to measure 66 µ m in axial direction of the trap. It was determined by moving a single trapped ion in the trap by changing the voltage on the end-cap electrodes. The uorescence intensity measured by the EMCCD camera is proportional to the laser intensity. The resulting spatial intensity prole suggested, that the 422 nm and 1092 nm beam have only a small overlap at the trap center. The measurement does not reect the intensity prole of the 422 nm beam but rather the overlap of the two lasers. Increasing the overlap of the two beams by changing the optics will improve the eciency of Doppler cooling of ions, that have a trajectory with a large distance from the trap center. 

## 2.3.2. Number of Loaded Ions per Ablation Pulse 

**==> picture [208 x 208] intentionally omitted <==**

**==> picture [208 x 208] intentionally omitted <==**

Figure 19: The probability to nd a certain number of ions after one ablation pulse and 5 s cooling time is shown on the left. The probability to load more than one ion did not surpass the probability to load one ion in this measurement. The average number of ions loaded by a single pulse dependent on the pulse energy is inferred from the measurement and plotted on the right. 

In order to determine the optimal pulse energy, the number of ions trapped during PLA loading was measured. During this measurement, the laser pulse was triggered and the ions were Doppler cooled for 5 s . Hot ions were removed from the trap by applying _U_ = 55 V to the blade electrodes for 1 s . The number of ions can be easily retrieved from an image captured by the EMCCD camera. Hot ions have to be removed from the trap before taking 

a picture, otherwise, the ion crystal may be distorted due to an additional ion entering the crystal, which then changes to a cloud instead of an ion crystal on the image. The procedure was repeated 100 times at dierent pulse energies. 

The resulting probability to load a certain number of ions dependent on the pulse energy is shown in gure 19. The probability to load no ion can be decreased to 65% by increasing the pulse energy. The probability of loading one ion increased from 10% for a pulse energy 55 µ J to 35% for pulses 110 µ J . The probability to load more than one ion did neither increase signicantly in this measurement, nor did it surpass the probability to load one ion. From the measured probability, one can determine the average ion number _⟨n⟩_ , which is also plotted in gure 19. If one assumes the expected ion number _⟨n⟩_ to scale linearly with the ablated atom number calculated in section 2.1.3, one would expect a much steeper increase of _⟨n⟩_ than found from this measurement. The number of loaded ions in this measurement is of course aected by the poor Doppler cooling eciency. This measurement can serve as a quantitative test to characterize Doppler cooling after the necessary steps for improvements have been carried out. 

## 2.3.3. Time-of-Flight Measurements 

In order to characterize the ux of neutral atoms by PLA it was attempted to perform time-of-ight measurements. They can give information about the velocity distribution of the atoms, which is connected to their average energy. The cooling might be optimized according to the measured velocity distribution. A similar experiment of this kind was performed by Guggemos et al. and is explained in [64]. 

For time of ight measurements, one ablation pulse is triggered. To detect a signal, that is proportional to the number of atoms passing the trap center, only the laser at 461 nm passes the trap along its symmetry axis. The laser is tuned to the resonance frequency of the strontium atoms, which should lead to uorescence light, if a sucient number of atoms passes the trap center. The atoms, that pass the trap center have only a negligible velocity component in the direction of the 461 nm laser since atomic and laser beams are perpendicular to each other. The uorescence should therefore not be altered by a Doppler shift. The PMT detects photons that are collected from the trap center. The counter of the National Instruments card PCI-6733 is used to count the measurement events of the PMT. The counter is gated by pulses of the required length of 10 ns . The time between two gate pulses can be made as short as 0 _._ 6 µ s limited by the FPGA that is used to create the pulses. The experimental setup should therefore be able to measure the PMT counts in time bins of size 0 _._ 6 µ s . 

Unfortunately, no uorescence photons could be detected this way. The used pulse energy was as high as 150 µ J and was not increased further to avoid possible laser induced damage of the optical components. It was also tried to illuminate the trap center from the diagonal 

direction instead of the axial direction. This leads to a much larger beam waist at the center and possibly larger overlap of the laser beam with the atomic particle current. With this conguration, no uorescence could be detected either. In both cases, the laser frequency was changed in the range of a GHz to avoid a wrong laser frequency as error source. 

Possible reasons, for the absence of any uorescence photons may be a too small atom number or a insucient overlap between the laser beam and the atomic beam. In the experiment by Guggemos et al ablation from a calcium and aluminium target were investigated. Laser pulses of similar energy were used. The targets were much closer to the trap center, however, and thus possibly lead to a higher atomic ux. The collection eciency of photons in this experiment and the one of Guggemos et al are similar. 

## 2.3.4. Experimental Sequence for Automatic PLA Loading 

This section describes the experimental sequence that is used in the experiment to load _n_ ions automatically. 

In preparation for the automatic loading, _m_ = 1 _,_ 2 _, ..., n_ ions have to be loaded manually and the positions have to be calibrated, by pressing the button Auto calibrate in the camera GUI and saving the successful calibration by clicking Save as reference. 

After this is done, the desired number of ions _n_ can be loaded, by just pressing the respective button in gTrICS. This will start the following loading procedure: 

1. Open the shutter for the 422 nm cooling laser, the 1092 nm repump lasers and the photo-ionization lasers for loading. 

2. Shorten the trap circuit for 50 ms to make sure the trap is empty. 

3. Trigger an ablation pulse. 

4. Wait for 1 s . 

5. Check the number and positions of the ions by analyzing two subsequent camera images. If the positions of the uorescing ions do not agree with the calibrations, go back to step 2. If the ion number is larger than _n_ go back to step 2. If the ion number is too small, go back to step 3. Else, pass on to the next step. 

6. Switch from _U_ = 1 _._ 5 V on the trap electrodes to _U_ = 55 V for 3 s . Wait 2 s . 

7. Repeat the procedure of step 5. For pass nally go to step 8. 

8. Reset the 422 nm cooling laser and the 1092 nm repump lasers to the settings before loading. Close the shutters of the photo-ionization lasers. 

This procedure can be used to load one ion with an average time of 36 s . The minimal time necessary to load one ion is 9 s and is achieved if every step has to be executed only once. In step 5, the position and number of ions are determined by the method described in A.3. 

Note that only in step 1 and 8 a sequence is loaded and run in the TrICS control software. This assures that the right lasers are sent to the trap center without undesired attenuation by an AOM or shutter. The steps 2-7 are not carried out by loading and running a sequence, but by a Python script that can access the GUI eld values in gTrICS. This is much faster, as loading and running a sequence would take additional 1 _._ 5 s for every step. The current loading procedure is fast enough. The bottleneck that limits the loading time at the moment is the time to Doppler cool ions into the crystalline phase. 

## 3. Single-Ion Addressing 

If a linear chain of trapped ions is used as the register of a quantum computer, one wants to perform single-qubit gates on selected, individual ions. In addition, some proposed two qubit gates like the Cirac-Zoller C-NOT gate [11] demand that one can manipulate the internal state of a single trapped ion coherently. Another frequently used technique in trapped ion experiments is to induce an ac-Stark shift on an individual ion [69, 70]. 

In order to be able to change the internal quantum state of an individual ion, it is necessary to address it by a tightly focused laser beam. At the same time, one wants to prevent the internal state of neighbouring ions to be altered by the operation, which would correspond to so-called addressing errors. In the experimental realisation one wants the Rabi frequency Ω _i ∝ √I_ of the addressed ion _i_ to be much larger than the Rabi frequency Ω _j_ of the neighbouring ions. When driving a resonant _π_ = _t_ Ω _i_ pulse on the addressed ion _i_ , it's initial internal state is rotated by the operator given by 

**==> picture [267 x 13] intentionally omitted <==**

around the axis _σφ_ on the equator of the Bloch sphere depending on the laser phase _φ_ 

**==> picture [261 x 12] intentionally omitted <==**

Due to the dierence in Rabi frequency for the neighbouring ion _j_ , this operation does not correspond to a _π_ pulse, but to a rotation 

**==> picture [266 x 13] intentionally omitted <==**

by an angle 

**==> picture [248 x 25] intentionally omitted <==**

The error in form of a rotation on qubit _j_ , when performing a _π_ pulse on ion _i_ is therefore proportional to the ratio of the Rabi frequencies Ω _j/_ Ω _i_ . 

When a o-resonant light eld with Rabi frequency Ω _i_ and detuning ∆ is applied for a time _t_ to the ion, an ac-Stark shift _δi_ = _−_ Ω[2] _i[/]_[2∆][is][induced][on][the][qubit][transition][of][ion] _i_ . This changes the qubit state of ion _i_ according to the operation [69] 

where _θ_ = _tδi_ . For a light pulse of length _t_ = _π/δi_ a _π_ rotation results for ion _i_ . Due to the dierence in Rabi frequency, ion _j_ is subjected to a rotation by an angle 

**==> picture [263 x 30] intentionally omitted <==**

The unintended rotation on ion _j_ scales like Ω[2] _j[/]_[Ω] _i_[2][, which is the ratio of light intensity on] the ions _j_ and _i_ . This diers from the resonant operation, where the error scaled with the electric eld strength according to Ω _j/_ Ω _i_ . The ions in a chain are typically separated by a distance of 5 µ m . If one assumes the addressing beam to have a perfect Gaussian shape with 1 _/e_[2] waist 3 µ m , the angle of the unintended rotation on ion _j_ during a resonant _π_ pulse on its next neighbour ion _i_ would be _θ_ = _π ×_ 6% whereas an o-resonant pulse on ion _i_ with _θ_ = _π_ leads to _θ_ = _π ×_ 0 _._ 4% . 

It is therefore benecial to perform single-qubit operations on single ions by inducing acStark shifts only, due to the smaller error. To be able to do any arbitrary rotation on the Bloch sphere, one combines the ac-Stark shift on single qubits with a beam that drives Rabi oscillations of all ions simultaneously with identical Rabi frequency. 

In the experiment at hand, the Rydberg excitation of a single trapped ion has been investigated thoroughly. To be able, to study the interaction between two Rydberg ions more closely and perform a two-ion Rydberg gate, addressing of a single trapped ion in a string of multiple ions is essential. The necessary optical setup for the addressing of single ions in the trapped Rydberg ion experiment was therefore designed and tests to evaluate its performance were prepared. 

## 3.1. Key components 

This section summarizes the design of the addressing setup. The necessary requirements on the optical system are outlined and each technical key component is described in detail. 

The addressing beam will be used to manipulate the qubit transition of the strontium ions at 674 nm . The objective, that is used to collect uorescence photons at 422 nm for the detection with the EMCCD camera, is also employed to focus the laser beam for single-ion addressing. The respective beam is shown in gure 5. In order to achieve a focal spot size of the laser beam, the objective's full aperture needs to be illuminated. An achromatic doublet lens with short focal length is positioned in front of the objective for this purpose. 

It is mounted on a _xyz_ translation stage to be able to optimize the focus and position of the laser beam on the ion. 

In order to select an individual ion and address it with the laser beam, two solutions exist [71]. In one approach, the ions are shuttled in the ion trap to move the correct ion into the focus of the laser beam. In a second approach, the laser beam is deected such that it is focused on the selected ion. For the trapped Rydberg experiment the latter approach is chosen. The only way to shuttle the ions would be to change the voltage on the end-cap electrodes. They are protected from noise by low-pass RC lters, which would limit the speed at which ions can be moved into and out of the focus of the addressing beam. The laser beam can be deected much faster by an AOD (acousto-optic deector). 

**==> picture [423 x 200] intentionally omitted <==**

Figure 20: The four lenses of the objective are shown together with the aluminium spacers. Everything is mounted in the shown lens tube by stress-free retaining rings. 

## 3.1.1. Objective 

The objective for imaging and addressing was designed by Markus Hennrich. It consists of four lenses; one planoconcave, one meniscus and two planoconvex lenses. The layout is shown in gure 21. It has a numerical aperture NA = 0 _._ 24 and is outside the vacuum chamber. It images the ions through the viewport. All lenses are standard 2" fused silica catalog lenses. The approach to select 4 lenses with dierent curvatures has been used for similar objectives for imaging of single trapped particles [72, 73]. The idea of the design is that the spherical aberrations of the lenses and the spherical aberrations of the viewport cancel each other. The objective should perform close to the diraction limit for all relevant wavelengths 243 _,_ 308 _,_ 422 and 674 nm with dierent focal lengths. The lenses are kept at the right distance by three aluminium spacers, that have been manufactured by the mechanical workshop at the University of Innsbruck. The lenses are mounted in a 2" lens tube by two stress-free retaining rings. All parts of the objective are shown in gure 20. 

**==> picture [208 x 374] intentionally omitted <==**

**==> picture [208 x 314] intentionally omitted <==**

Figure 21: On the left, the layout of the objective from Zemax OpticStudio is shown. The objective consists of one planoconcave, two planoconvex and one meniscus lens. It can focus through a 3 mm window. On the right, the objective is shown during the assembly process. 

To test the size and deection of the addressing beam, that can be expected in the experiment, a second objective identical to the one already in use was assembled. The layout of the lenses and the stacked lenses and spacers can be seen in gure 21. 

## Modulation Transfer Function 

An optical system images objects from the object plane to the image plane. The performance of the optical system is characterized by its ability to resolve two close-lying objects in the image. The MTF (modulation transfer function) gives a quantitative measure at which distance a structure can still be resolved. It is given by the Michelson contrast [74] of the image, also known as visibility, 

**==> picture [261 x 25] intentionally omitted <==**

with which a line structure can be resolved in the image plane. The MTF is measured for line structures of dierent spatial modulation frequency. 

In the given experiment, the performance of the objective with viewport is to be characterized. A negative 1951 USAF test target[1] was placed 72 mm in front of the objective with a view port of the used type in between. This corresponds to the position, where the ions would be in the real experiment. A CMOS sensor was positioned at the image plane 45 cm behind the objective. The distances agreed with the ones in the Zemax OpticsStudio simulation for the wavelength of 674 nm . The test target was illuminated from the back by a laser beam of the correct wavelength. The laser beam passed a 25 mm lens, i.e. the target was illuminated by rays with large and small angles which guarantees that even light from the smallest structures can be collected suciently. Illuminating the small line structures on the target with a coherent source leads to unwanted diraction patterns, however. To remove those, a rotating lter made from a single layer of opaque scotch tape was placed in the laser beam shortly before the lens. This destroys the spatial coherence of the laser beam. Taking an image at sucient long exposure time produced an image that is free of diraction patterns. The picture is shown in gure 22. Even the smallest structure available on the test target at hand (group 7, item 6) was resolved and free of diraction artefacts. Due to the rotating scotch tape in the laser beam, the illumination is not perfectly homogeneous but acquires a striped modulation. 

**==> picture [339 x 271] intentionally omitted <==**

Figure 22: The real image of the 1951 USAF test target is shown. It was produced by the objective and measured with a CMOS sensor. This image was used to determine the MTF of the objective with the viewport. The white spot above group number six is a small island of dead pixels on the used CMOS sensor. Due to the rotating scotch tape the image is free of diraction patterns even for the small structures of group seven. 

The MTF was determined from the measured image 22. The result is shown in gure 23 

> 1 Thorlabs, Negative 1951 USAF Test Target, R1DS1N 

together with the expected diraction limited performance of the objective calculated with Zemax OpticStudio. The uncertainties in the measurement result from the inhomogeneous illumination. Inferred from the MTF, the objective is close to the diraction-limit for 674 nm . 

**==> picture [339 x 226] intentionally omitted <==**

Figure 23: The measured MTF is plotted in comparison to the diraction limited MTF for the objective at the respective wavelength 674 nm , which was calculated with Zemax OpticStudio. The objective is close to being diraction limited. 

## Focusing of the 674 nm Beam 

For the application of single-ion addressing, it is more important to focus down a Gaussian laser beam with wavelength 674 nm . A test that characterizes the objective with respect to this aspect was carried out. It is outlined in the following. 

To achieve the smallest focal spot size possible, the whole aperture of the objective has to be illuminated. For this reason, an achromatic lens[2] with focal length f = 16 mm was positioned 47 cm before the objective. Congurations with dierent achromatic lenses were compared in Zemax OpticStudio and the chosen one matches the diameter of the used collimated laser beam, which has an 1 _/e_[2] radius _w_ = 0 _._ 4 mm . The distance between the achromat and the objective was optimized using Zemax OpticStudio. According to the physical optics propagation in Zemax, the optimized conguration is supposed to deliver a waist _w_ 0 = 2 _._ 12 µ m and a Rayleigh length _zR_ = 9 _._ 0 µ m . 

To check the result from Zemax experimentally, one has to measure the beam propagation around the focal plane of the objective. Routinely, a scientic CMOS camera sensor[3] with a pixel size of 5 _._ 3 µ m is used for this purpose. The camera resolution given by the pixel size, however, would not be enough for the characterization of the expected focused laser beam. As a remedy, a beam proler based on the Raspberry Pi camera module V2 NoIR 

> 2 Thorlabs AC080-016-B 

> 3 uEye UI-3240ML-NIR-GL 

was developed. The Raspberry Pi CMOS camera chip has a pixel size of 1 _._ 12 µ m which allows for the characterization of tightly focused laser beams. Details about the beam proler can be found in appendix B. The beam proler may become a helpful tool in the laboratory for the future. 

**==> picture [339 x 226] intentionally omitted <==**

Figure 24: The Gaussian beam propagation for a 674 nm laser beam performed with a home-built beam proler is shown. A minimal waist of 2 _._ 1 µ m can be reached at the focus. The lines show a t with the beam waist constrained to the minimum value measured. The two main axes of the beam have their focus at dierent positions, which indicates astigmatism. 

The CMOS sensor of the beam proler was mounted on a micrometer stage, which allowed analyzing the beam prole at dierent positions. The beam prole was tted by a 2D Gaussian distribution to obtain the 1 _/e_[2] waists in the direction of the two main axes of the prole. The result is plotted in gure 24. The measurement values were tted by a Gaussian beam propagation, corrected by the beam quality factor _M_[2] 

**==> picture [293 x 33] intentionally omitted <==**

The waist was restricted to the minimal measured value, whereas _z_ 0 and _M_[2] were used as free t parameters. The resulting values are summarized in table 3 together with the inferred Rayleigh length _zR_ = _πw_ 0[2] _[/λM]_[2][.] For both axes, the minimal waist size _w_ 0 = (2 _._ 1 _±_ 0 _._ 5) µ m agrees with the expected value from the Zemax calculations. The _M_[2] parameters around 2.0 suggest, that there exist aberrations. The resulting beam waists are small enough that addressing of a single ion with small addressing errors of its neighbours during an o-resonant ac-Stark operation may be feasible. Note, that the measured beam waist is already on the order of the resolution 2 _._ 24 µ m of the CMOS sensor given by twice the pixel size due to averaging over the Bayer lter array. 

|axis|_w_0 / µm|_M_2|_z_0 / µm|_zR_ / µm|
|---|---|---|---|---|
|1<br>2|2_._4_±_0_._6<br>2_._1_±_0_._5|2_._1_±_0_._5<br>1_._9_±_0_._4|_−_9_±_1<br>9_._3_±_0_._8|12_±_6<br>11_±_5|
|Zemax Result|2.12|1.0|0|9.0|



Table 3: Parameters of the measured beam propagation of the 674 nm beam that was focused by the objective are displayed. _w_ 0 is the minimum value of beam waist, that was measured. The beam quality factor _M_[2] and the position of the waist _z_ 0 were determined by a t. The Rayleigh length _zR_ was inferred from the other values. The measured beam was elliptical at the focus compared to the Zemax result; the attained waists _w_ 0 agrees with the expected values from Zemax within the uncertainty. 

Rather dissatisfying is the discrepancy in _z_ 0 for the two laser beams. The beam prole was not spherical but elliptical. This means, that the laser beam is aected by astigmatic aberrations. Axis 1 and 2 are perpendicular to each other and appeared rotated by an angle of 45 _[◦]_ with respect to the sagittal and tangential directions. The astigmatism could not be removed by adjusting the tilt angle of the objective. This leaves as only possible cause, that one lens in the objective is tilted by a small angle. This was veried by rotating the objective, which also rotated the axis 1 and 2 of the elliptical beam prole. The astigmatism probably occurs due to a slightly tilted lens in the objective, caused by an decentered spacer between the lenses. Especially the smallest aluminium spacer is prone to this error, as it can move and decentered easily during the objective assembly. So far, no way was found to correct the objective for this aberration. For the application in single-ion addressing in a 1D ion chain, one may just rotate the objective so that axis 1 of the beam prole is parallel to the ion chain. The focus is adjusted so that the ions are at the focus of the beam prole of axis 1. 

## 3.1.2. Acousto-Optic Deector 

To deect the laser beam and address dierent ions in a chain, an acousto-optic deector (AOD) is used. In an AOD, the laser beam passes through a crystal. A piezoelectric transducer is used to excite a sound wave with frequency _f_ , velocity _va_ and wave vector _⃗q_ in the crystal. This creates a refractive index grating in the crystal. Light can be diracted from the grating when passing the crystal which produces multiple diracted beams of order _m_ behind the AOD. The wave vector _[⃗] k_ of the light eld changes to _[⃗] k_ + _m⃗q_ under _m_[th] order diraction. This is equivalent to a deection of the beam by an angle Θ . The diraction angle can be changed, by changing the frequency _f_ of the sound wave in the crystal. AODs use the 1[st] order diracted beam and work within a frequency bandwidth ∆ _f_ around a center frequency _fc_ . The attainable change in diraction angle ∆Θ is given by 

where _λ_ is the wavelength of the light. If the frequency is changed, it takes a time interval of 

**==> picture [238 x 12] intentionally omitted <==**

until the sound wave with new frequeny crosses the diameter _D_ of the laser beam in the AOD crystal. This time physically limits the speed, by which one can change between two deection angles. For an incoming Gaussian laser beam with, the number of resolved spots _N_ , that are attained after focusing down the output of the AOD is given by 

**==> picture [239 x 11] intentionally omitted <==**

which is called time-bandwidth product. It is a useful gure of merit for a specic AOD. Note, that the maximal number of spots is achieved when the laser beam lls the whole aperture of the device. Resolved spots means in this case, that the peak of one focused spot is positioned at the rst minimum of the Airy diraction pattern of its neighbouring spot. 

For the given application Brimrose's model TED-320-200-674 was chosen. It can operate in the wavelength range (674 _±_ 50) nm and is based on a TeO2 crystal. The center frequency is _fc_ = 320 MHz with bandwidth ∆ _f_ = 200 MHz . This allows for an overall deection ° angle of ∆Θ = 32 mrad = 1 _._ 8 . The rectangular aperture of the AOD measures _D × h_ = 2 _._ 1 mm _×_ 0 _._ 3 mm , i.e. it takes a sound wave ∆ _t_ = 0 _._ 5 µ s to pass the whole aperture. This leads to a time bandwidth product ∆ _f_ ∆ _t_ = 99 . A TeO2 crystal with longitudinal acoustic wave was chosen for this application as it results in a sound wave with larger velocity and thus addressing times _<_ 1 µ s . 

The AOD is powered by a direct digital synthesizer (DDS), whose signal is amplied by an RF amplier. The peak eciency of the AOD is at an input power of 2 W . This power should not be exceeded. 

Applying a sinusoidal signal with a single frequency at a time to the AOD generates one deected beam and one undeected beam after the AOD. In a later stage of the experiment, one may want several addressing beams simultaneously. This can be accomplished by driving the AOD with a signal that has multiple frequency components. At high RF power, this leads to non-linear frequency mixing in the crystal. The frequencies of the various signal components will be sum and dierence of the input signal frequencies in the crystal [75]. The AOD then produces multiple output beams under dierent deection angles. By changing the phases of the input signal components, on can make certain frequency components in the crystal vanish due to destructive interferences. 

In the rst order deected beam in an AOD driven with frequency _f_ , the frequency _ω_ of 

the laser is shifted by 

**==> picture [49 x 11] intentionally omitted <==**

**==> picture [28 x 12] intentionally omitted <==**

due to energy conservation during the scattering process. Thus, the laser frequency will vary for the dierent ion positions. For a single addressed ion, this detuning can be cancelled by an additional double-pass AOM. In the experiment, the laser will be guided towards the single-ion addressing setup by an optical ber. The standard technique to switch a laser fast is to use an AOM in double-pass conguration before the ber. In this conguration, the laser is diracted every time it passes the AOM leading to twice the frequency shift. This frequency shift can be used to cancel the shift caused by the AOD. 

## 3.2. Zemax OpticStudio Simulations 

The combination of the components has to meet certain requirements for the addressing of single ions. The AOD is placed before the achromatic lens. They should produce a sucient displacement of the focused beam at the ions' position. At the same time, the achromat should illuminate the objective's aperture as much as possible with the restriction, that the beam does not get clipped at the maximal and minimal deection angle. This requires that the output of the optical ber, that serves as incoming beam, is shaped to the ideal beam diameter. The active aperture of the AOD has a rectangular shape of size 2 _._ 1 mm _×_ 0 _._ 3 mm which gives rise to another restriction on laser beam. It means, that the beam has to be made elliptical before the AOD. 

In order to determine suitable optics for the single-ion addressing setup, the optical system design software Zemax OpticStudio was used. The main steps in the design process and the nal design, which is shown in gure 25, are outlined in the following. 

## 3.2.1. A Suitable Combination of Achromat and AOD 

To obtain a diraction-limited focal spot size at the position of the ions, the 674 nm laser beam has to be expanded in front of the objective, to ll the whole aperture of the objective. An achromatic doublet lens with focal length _f_ is used for this purpose, as it corrects spherical and chromatic aberrations and is therefore superior to a simple singlet lens. 

Several achromatic doublet lenses from Thorlabs were compared in the rst step of the design process. Three light elds with angles _−_ 0 _._ 9 _[◦] ,_ 0 _[◦] ,_ 0 _._ 9 _[◦]_ were used in the simulation. This corresponds to the range of deection that can be attained with the desired AOD. 

|Achromat|_f_/mm|_a_/mm|_rA_/µm|displacement range/µm|
|---|---|---|---|---|
|AC080-010-B<br>AC080-016-B<br>AC127-019-B<br>AC127-025-B|10<br>16<br>19<br>25|0.4<br>0.8<br>1.0<br>1.5|2.5<br>2.6<br>2.5<br>2.2|_±_19<br>_±_40<br>_±_48<br>_±_63|



Table 4: For each achromatic lens doublet with focal length _f_ manufactured by Thorlabs, the optimal aperture diameter _a_ was determined. The resulting Airy radius _rA_ and Gaussian waist _w_ 0 of the resulting spot in the image plane is listed for the optimized conguration. The range of displacement in the image plane resulting from a deection by _±_ 0 _._ 9 _[◦]_ of the incident light eld is given as well. 

The entrance aperture of the light eld was increased, such that the focal spot size was minimized with the constraint that no light got clipped at the objective. For all congurations, the distance between the entrance pupil and the achromatic lens as well as the distance between the achromatic lens and the objective were optimized. The performance of the system was diraction limited for every case, i.e. for a given eld all traced rays were within the Airy disk of the respective light spot. The angle of the incident light elds leads to a displacement _d_ of the light spot in the focal plane. In table 4 the results of the simulation are presented for dierent achromatic doublets. The optimal aperture _a_ of the incident light is given together with the respective spot size in form of the Airy radius _rA_ , i.e. the rst null of the diraction pattern for an uniformly illuminated entrance pupil. 

**==> picture [423 x 265] intentionally omitted <==**

Figure 25: A sketch of the single-ion addressing setup is shown. A home-built objective is used to focus on the ions. An achromat expands the beam before the objective. An AOD is used to deect the beam and direct the laser to the selected ion. The laser is guided to the setup by an optical ber. A Keplerian telescope expands the laser beam after the ber and a cylindrical Galilean telescope matches the beam to the active aperture of the AOD. 

From the resulting values, the achromatic doublet AC127-025-B from Thorlabs with focal length _f_ = 25 mm was chosen as optimal solution. It oers the largest range of displacement _±_ 63 µ m of the focused spot in the image plane. At a typical inter ion distance of 5 µ m this is enough to address up to 25 ions. The optimal aperture for this achromatic doublet lens matches the active aperture of the AOD. The resulting spot size in the image plane given by the Airy radius _rA_ = 2 _._ 2 µ m and the Gaussian waist _w_ 0 = 2 _._ 3 µ m should be suciently tight to address single ions. 

## 3.2.2. The Complete Optical Design 

Based on the chosen achromatic doublet lens, a more detailed optical design was developed. The restriction arising from the nite active aperture of the AOD given by 2 _._ 1 mm _×_ 0 _._ 3 mm was taken into account. The laser light is rst guided to the single-ion addressing setup by an optical ber, whose output is a Gaussian beam with waist 350 µ m . 

**==> picture [423 x 159] intentionally omitted <==**

Figure 26: The expected intensity prole on the entrance of the AOD found with the physical beam propagation option in Zemax is depicted. The active aperture of the AOD is depicted and the beam should match the aperture nicely. 

A single light eld at wavelength 674 nm with aperture diameter 0 _._ 8 mm was assumed for this simulation with Gaussian apodization type, to resemble the physical beam. To match the output of the optical ber to the ideal aperture diameter _a_ = 1 _._ 5 µ m , that was determined in the prior design step, a Kepler telescope composed of two achromatic doublet lenses[4] with focal length 10 mm and 19 mm is used to expand the beam. The optimal distance 25 _._ 7 mm between the lenses was found by optimization with Zemax OpticStudio. To match the beam to the active aperture of the AOD, a Galilean telescope with two cylindrical lenses[5] is placed 50 mm after the Kepler telescope. The distance between the two cylindrical lenses was optimized to 76 mm . The TeO2 crystal of the AOD with thickness 10 mm was taken into account in the simulation and was placed 67 mm behind the Galilean telescope and 20 mm before the achromatic doublet lens. This way, the point of deection will be at the focal plane of the _f_ = 25 mm achromatic doublet, as in the prior simulation. 

> 4 Thorlabs AC080-010-B and AC127-019-B 

> 5 Thorlabs LJ1567L1-B and LK1283L1-B 

The simulated radius of the Airy ellipse in the sagittal plane, this is the plane in which the ion chain resides, is 2 _._ 2 µ m . In the tangential direction, the Airy ellipse radius is 39 µ m due to the cylindrical Galilean telescope. The system is diraction limited in the sense, that all traced rays lie within the Airy ellipse. The modulation transfer function of the system for the sagittal plane diered by less than 5% from the diraction limited modulation transfer function for the given system. 

The physical optics propagation in Zemax was used to analyze the resulting focal spot for the incoming Gaussian beam with 1 _/e_[2] waist 350 µ m . The expected intensity prole at the entrance of the AOD is shown in gure 26. The beam prole matches the active aperture and has 1 _/e_[2] waists _wt_ = 0 _._ 7 mm in the tangential plane and _ws_ = 0 _._ 1 mm in the sagittal plane. The maximum optical power density of the AOD is specied to 5 W mm _[−]_[2] . One would be able to use a beam of 550 mW optical power without damaging the crystal of the AOD. This value already exceeds the available laser power by a factor of two. 

The expected intensity prole in the image plane is shown in gure 27. The intensity has a 1 _/e_[2] waist of 9 µ m in tangential direction and 2 µ m in sagittal direction, where the latter is the important gure of merit for the addressing of single ions. In the sagittal plane, the intensity prole has a diraction pattern, that has a peak 4 µ m from the central peak with 4% of the peak intensity. This diraction pattern will result in a lower bound for the addressing errors. Those errors may be decreased, by going to a conguration, where the neighbouring ions reside in the minima of the diraction pattern, i.e. at distances _±_ 2 _._ 8 µ m , _±_ 5 _._ 9 µ m , etc. 

**==> picture [221 x 218] intentionally omitted <==**

**==> picture [195 x 221] intentionally omitted <==**

Figure 27: The intensity prole at the position of the trapped ion chain was calculated using Zemax's physical beam propagation. The central peak of the normalized intensity on the left shows a narrow waist in the sagittal direction of 2 µ m . At larger distances, one nds a diraction pattern. The diraction pattern can be seen clearly in the plot of the cross section along the sagittal plane on the right. The intensity maxima of the diraction pattern are 4% of the peak intensity. 

## 3.3. Next Steps 

The described tests and the design study showed that addressing of single ions is feasible with the home-built objective. The next step towards the addressing of single ions will be a test of the optical design. One just has to insert the selected lenses in the setup that was used to characterize the objective. The resulting focused laser beam can be easily characterized with the newly developed beam proler. A suitable non-magnetic piezodriven xyz translation stage, on which the last achromatic doublet lens can be mounted, was purchased already. The translation stage together with the AOD can be tested in the test setup to evaluate their performance. It is to be checked if the deection of the beam is sucient to address several ions in a string without distorting the quality of the focus. It is also important for the application how precisely the laser beam can be aligned with the lens on the translation stage. If the performance of the system turns out to be as expected from the presented design, it can be integrated in the main experiment. 

## 4. Summary and Outlook 

The pulsed laser ablation setup that was designed, characterized and built within this thesis meets the experimental requirements for ablation loading. The newly established loading technique is fully automatic, and decreased the overall loading time from 30 min to 36 s . This is an improvement by a factor of 50. The experimental parameters that can be used to optimize the loading further have been determined. In particular, improving the Doppler cooling eciency in the current experiment will further decrease the loading time. In the course of the automation of ablation loading, the EMCCD camera was integrated into the current experiment. This is a necessary prerequisite for fully automatic measurements. 

In the future, the loading time has to be decreased signicantly and loading of strontium ions has to be fully isotope selective. This will be important for a quantum computer based on trapped Rydberg ions, whose speed is not limited by the time to load an ion after unintended double-ionization of a Rydberg ion. The most promising technology for this purpose are segmented ion traps. Traps of this type oer separate zones for loading, storing and experiments with ions respectively. The loading zone is exclusively used for ablation loading of ions. Ions of the right isotope are shuttled into the storing zone, where one has a reservoir of[88] Sr[+] . In the experimental zone one can hold a chain of ions used for quantum computation. If an ion is doubly-ionized, a new ion or a whole crystal of ions can be shuttled from the reservoir into the experimental zone. 

Due to the fast loading Technique established within this thesis, experiments with Rydberg ions are no longer limited by the long time necessary for ion loading. This will enable ecient measurements with multiple trapped Rydberg ions. 

The design of the single-ion addressing setup and the rst out-carried tests showed that single-ion addressing is possible in the experiment. The proposed optical design can be realized and tested with the developed beam proler. After integration into the experiment, the single-ion addressing enables full control over the internal quantum state of all ions in a chain. In other words, it enables arbitrary single qubit gates. This is a important ingredients for the universal set of quantum gates of a quantum computer [76]. 

If two trapped ions are excited to the Rydberg state they interact strongly with each other. The interaction between Rydberg ions is currently under investigation by the PhD students Chi Zhang and Fabian Pokorny. According to theoretical predictions [13, 77], it is possible to tune the interaction by coupling two Rydberg states by microwave radiation, which leads to microwave-dressed Rydberg states with oscillating dipole moments. The 

latest experimental results showed Rydberg blockade interaction between two microwavedressed Rydberg ions. Interaction of trapped Rydberg ions is a necessary prerequisite for a two-qubit gate between Rydberg ions. An important step towards quantum computation with trapped Rydberg ions in the current experiment is the addressing of single ions. The basic requirements for single ion addressing were demonstrated within this work. A combination of Rydberg interaction and addressed qubit operations will allow the control of universal quantum operations. Thus, the experimental system is getting closer to realizing the concept of a universal trapped Rydberg ion quantum computer. 

## Bibliography 

- [1] W. Paul, Electromagnetic traps for charged and neutral particles, Reviews of Modern Physics 62, 531 (1990). 

- [2] J. Eschner, G. Morigi, F. Schmidt-Kaler, and R. Blatt, Laser cooling of trapped ions, Journal of the Optical Society of America B 20, 1003 (2003). 

- [3] N. Huntemann, C. Sanner, B. Lipphardt, C. Tamm, and E. Peik, Single-ion atomic clock with 3 _×_ 10 _[−]_[18] systematic uncertainty, Physical Review Letters 116, 063001 (2016). 

- [4] D. Leibfried, R. Blatt, C. Monroe, and D. Wineland, Quantum dynamics of single trapped ions, Reviews of Modern Physics 75, 281 (2003). 

- [5] J. Zhang, P. W. Hess, A. Kyprianidis, P. Becker, A. Lee, J. Smith, G. Pagano, I.-D. Potirniche, A. C. Potter, A. Vishwanath, N. Y. Yao, and C. Monroe, Observation of a discrete time crystal, Nature 543, 217 (2017). 

- [6] P. W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Review 41, 303 (1999). 

- [7] L. K. Grover, A fast quantum mechanical algorithm for database search, in Annual ACM symposium on Theory of computing (1996). 

- [8] S. Lloyd, Universal quantum simulators, Science 273, 1073 (1996). 

- [9] R. Blatt and C. F. Roos, Quantum simulations with trapped ions, Nature Physics 8, 277 (2012). 

- [10] Y. Wang, M. Um, J. Zhang, S. An, M. Lyu, J.-N. Zhang, L.-M. Duan, D. Yum, and K. Kim, Single-qubit quantum memory exceeding ten-minute coherence time, Nature Photonics 11, 646 (2017). 

- [11] J. I. Cirac and P. Zoller, Quantum computations with cold trapped ions, Physical Review Letters 74, 4091 (1995). 

- [12] F. Schmidt-Kaler, H. Häner, M. Riebe, S. Gulde, G. P. T. Lancaster, T. Deuschle, C. Becher, C. F. Roos, J. Eschner, and R. Blatt, Realization of the Cirac-Zoller controlled-NOT quantum gate, Nature 422, 408 (2003). 

- [13] M. Müller, L. Liang, I. Lesanovsky, and P. Zoller, Trapped Rydberg ions: from spin chains to fast quantum gates, New Journal of Physics 10, 093009 (2008). 

- [14] K. R. Brown, J. Kim, and C. Monroe, Co-designing a scalable quantum computer with trapped atomic ions, npj Quantum Information 2, 16034 (2016). 

- [15] D. Comparat and P. Pillet, Dipole blockade in a cold Rydberg atomic sample [invited], Journal of the Optical Society of America B 27, A208 (2010). 

- [16] I. Mourachko, W. Li, and T. F. Gallagher, Controlled many-body interactions in a frozen Rydberg gas, Physical Review A 70, 031401 (2004). 

- [17] D. Petrosyan and K. Mølmer, Binding potentials and interaction gates between microwave-dressed Rydberg atoms, Physical Review Letters 113, 123003 (2014). 

- [18] M. Weidemüller, There can be only one, Nature Physics 5, 91 (2009). 

- [19] M. Saman, T. G. Walker, and K. Mølmer, Quantum information with Rydberg atoms, Reviews of Modern Physics 82, 2313 (2010). 

- [20] M. Saman, Quantum computing with atomic qubits and Rydberg interactions: progress and challenges, Journal of Physics B: Atomic, Molecular and Optical Physics 49, 202001 (2016). 

- [21] D. Jaksch, J. I. Cirac, P. Zoller, S. L. Rolston, R. Côté, and M. D. Lukin, Fast quantum gates for neutral atoms, Physical Review Letters 85, 2208 (2000). 

- [22] F. Kress, Frequenzstabilisierung eines 674 nm Diodenlasers zur Detektion der Rydberganregung von Strontiumionen, MA thesis (University of Innsbruck, Nov. 1, 2015). 

- [23] F. Pokorny, Experimental setup for trapping strontium Rydberg ions, MA thesis (University of Innsbruck, Mar. 1, 2014). 

- [24] Q. A. Turchette, Kielpinski, B. E. King, D. Leibfried, D. M. Meekhof, C. J. Myatt, M. A. Rowe, C. A. Sackett, C. S. Wood, W. M. Itano, C. Monroe, and D. J. Wineland, Heating of trapped ions from the quantum ground state, Physical Review A 61, 063418 (2000). 

- [25] W. Sachtler, G. Dorgelo, and A. Holscher, The work function of gold, Surface Science 5, 221 (1966). 

- [26] M. Brownnutt,[88] Sr[+] ion trapping techniques and technologies for quantum information processing, PhD thesis (Imperial College London, Sept. 21, 2007). 

- [27] B. M. Rodríguez-Lara, H. Moya-Cessa, and A. B. Klimov, Combining jaynes-cummings and anti-jaynes-cummings dynamics in a trapped-ion system driven by a laser, Physical Review A 71, 023811 (2005). 

- [28] A. H. Myerson, D. J. Szwer, S. C. Webster, D. T. C. Allcock, M. J. Curtis, G. Imreh, J. A. Sherman, D. N. Stacey, A. M. Steane, and D. M. Lucas, High-delity readout of trapped-ion qubits, Physical Review Letters 100, 200502 (2008). 

- [29] H. J. Metcalf, P. van der Straten, and P. van der Straten, Laser cooling and trapping (graduate texts in contemporary physics) (Springer Berlin Heidelberg, 2001). 

- [30] E. H. Pinnington, R. W. Berends, and M. Lumsden, Studies of laser-induced uorescence in fast beams of Sr[+] and Ba[+] ions, Journal of Physics B: Atomic, Molecular and Optical Physics 28, 2095 (1995). 

- [31] G. Higgins, A single trapped Rydberg ion, PhD thesis (Stockholm University, Apr. 1, 2018). 

- [32] E. Biémont, J. Lidberg, S. Mannervik, L.-O. Norlin, P. Royen, A. Schmitt, W. Shi, and X. Tordoir, Lifetimes of metastable states in Sr II, The European Physical Journal D 11, 355 (2000). 

- [33] C. Maier, Laser system for the Rydberg excitation of strontium ions, MA thesis (University of Innsbruck, Nov. 1, 2013). 

- [34] G. Higgins, W. Li, F. Pokorny, C. Zhang, F. Kress, C. Maier, J. Haag, Q. Bodart, I. Lesanovsky, and M. Hennrich, Single strontium Rydberg ion conned in a Paul trap, Physical Review X 7, 021038 (2017). 

- [35] N. V. Vitanov, A. A. Rangelov, B. W. Shore, and K. Bergmann, Stimulated Raman adiabatic passage in physics, chemistry, and beyond, Reviews of Modern Physics 89, 015006 (2017). 

- [36] G. Higgins, F. Pokorny, C. Zhang, Q. Bodart, and M. Hennrich, Coherent control of a single trapped Rydberg ion, Physical Review Letters 119, 220501 (2017). 

- [37] M. Seng, U. Eichmann, V. Lange, T. Gallagher, and W. Sandner, Microwave ionization of Rydberg states of the barium ion, The European Physical Journal D 3, 21 (1998). 

- [38] P. Pillet, W. W. Smith, R. Kachru, N. H. Tran, and T. F. Gallagher, Microwave ionization of Na Rydberg levels, Physical Review Letters 50, 1042 (1983). 

- [39] I. I. Beterov, D. B. Tretyakov, I. I. Ryabtsev, A. Ekers, and N. N. Bezuglov, Ionization of sodium and rubidium S _,_ nP _,_ and nD Rydberg atoms by blackbody radiation, Physical Review A 75, 052720 (2007). 

- [40] C. F. Roos, Controlling the quantum state of trapped ions, PhD thesis (University of Innsbruck, Feb. 1, 2000). 

- [41] S. Gulde, D. Rotter, P. Barton, F. Schmidt-Kaler, R. Blatt, and W. Hogervorst, Simple and ecient photo-ionization loading of ions for precision ion-trapping experiments, Applied Physics B 73, 861 (2001). 

- [42] K. Sheridan, W. Lange, and M. Keller, All-optical ion generation for ion trap loading, Applied Physics B 104, 755 (2011). 

- [43] R. Hendricks, D. Grant, P. Herskind, A. Dantan, and M. Drewsen, An all-optical ion-loading technique for scalable microtrap architectures, Applied Physics B 88, 507 (2007). 

- [44] D. R. Leibrandt, R. J. Clark, J. Labaziewicz, P. Antohi, W. Bakr, K. R. Brown, and I. L. Chuang, Laser ablation loading of a surface-electrode ion trap, Physical Review A 76, 055403 (2007). 

- [45] D. W. Bäuerle, Laser processing and chemistry (Springer Berlin Heidelberg, Sept. 2, 2011). 

- [46] M. Stafe, A. Marcu, and N. Puscas, Pulsed laser ablation of solids (Springer Berlin Heidelberg, Nov. 9, 2013), 233 pp. 

- [47] E. Carpene, Ultrafast laser irradiation of metals: beyond the two-temperature model, Physical Review B 74, 024301 (2006). 

- [48] L. T. M. I. Kaganov I. M. Lifshitz, Relaxation between electrons and the crystalline lattice, Soviet Physis JETP (1956). 

- [49] T. P. S.I. Anisimov B.L. Kapeliovich, Electron emission from metal surfaces exposed to ultrashort laser pulses, Soviet Physis JETP (1974). 

- [50] B. N. Chichkov, C. Momma, S. Nolte, F. von Alvensleben, and A. Tünnermann, Femtosecond, picosecond and nanosecond laser ablation of solids, Applied Physics A 63, 109 (1996). 

- [51] J. G. Endriz and W. E. Spicer, Reectance studies of Ba _,_ Sr _,_ Eu _,_ and Yb , Physical Review B 2, 1466 (1970). 

- [52] K. Zimmermann, M. V. Okhapkin, O. A. Herrera-Sancho, and E. Peik, Laser ablation loading of a radiofrequency ion trap, Applied Physics B 107, 883 (2012). 

- [53] J. C. Miller, Laser ablation (Springer Berlin Heidelberg, Dec. 8, 2011), 204 pp. 

- [54] C. Dai, S. Hu, and J. Lu, Multistep excitation of autoionizing states of neutral strontium, Journal of Quantitative Spectroscopy and Radiative Transfer 56, 255 (1996). 

- [55] W. Mende, K. Bartschat, and M. Kock, Near-threshold photoionization from the Sr I (5s5p)[1] P[1] 0[state,][Journal][of][Physics][B:][Atomic,][Molecular][and][Optical][Physics] 28, 2385 (1995). 

- [56] W. Demtröder, Experimentalphysik 3: Atome, Moleküle und Festkörper (SpringerLehrbuch) (German Edition) (Springer Berlin Heidelberg, 2004). 

- [57] K. Vant, J. Chiaverini, W. Lybarger, and D. J. Berkeland, Photoionization of strontium for trapped-ion quantum information processing, (2006), arXiv:quantph/0607055v1 [quant-ph]. 

- [58] M. Boyd, High precision spectroscopy of strontium in an optical lattice: towards a new standard for frequency and time, PhD thesis (University of Colorado Boulder, 2002, Oct. 1, 2007). 

- [59] D. M. Lucas, A. Ramos, J. P. Home, M. J. McDonnell, S. Nakayama, J.-P. Stacey, S. C. Webster, D. N. Stacey, and A. M. Steane, Isotope-selective photoionization for calcium ion trapping, Physical Review A 69, 012711 (2004). 

- [60] J. Emsley, The elements (oxford chemistry guides) (Oxford University Press, 1998). 

- [61] M. Schioppo, N. Poli, M. Prevedelli, S. Falke, C. Lisdat, U. Sterr, and G. M. Tino, A compact and ecient strontium oven for laser-cooling experiments, Review of Scientic Instruments 83, 103101 (2012). 

- [62] M. Bober, J. Zachorowski, W. Gawlik, P. Morzy«ski, M. Zawada, D. Lisak, A. Cygan, K. Bielska, M. Piwi«ski, R. S. Trawi«ski, R. Ciuryªo, F. Ozimek, and C. Radzewicz, Precision spectroscopy of cold strontium atoms, towards optical atomic clock, 2013. 

- [63] R. J. Cook, Optical Stern-Gerlach eect, Physical Review A 35, 3844 (1987). 

- [64] M. Guggemos, D. Heinrich, O. A. Herrera-Sancho, R. Blatt, and C. F. Roos, Sympathetic cooling and detection of a hot trapped ion by a cold one, New Journal of Physics 17, 103001 (2015). 

- [65] K. Toyoda, H. Kataoka, Y. Kai, A. Miura, M. Watanabe, and S. Urabe, Separation of laser-cooled[42] Ca[+] and[44] Ca[+] in a linear Paul trap, Applied Physics B 72, 327 (2001). 

- [66] U. Tanaka, H. Imajo, K. Hayasaka, R. Ohmukai, M. Watanabe, and S. Urabe, Laser cooling and isotope separation of Cd[+] ions conned in a linear Paul trap, Optics Letters 22, 1353 (1997). 

- [67] R. Alheit, K. Enders, and G. Werth, Isotope separation by nonlinear resonances in a Paul trap, Applied Physics B Laser and Optics 62, 511 (1996). 

- [68] G. Huber, T. Deuschle, W. Schnitzler, R. Reichle, K. Singer, and F. Schmidt-Kaler, Transport of ions in a segmented linear Paul trap in printed-circuit-board technology, New Journal of Physics 10, 013004 (2008). 

- [69] P. Schindler, D. Nigg, T. Monz, J. T. Barreiro, E. Martinez, S. X. Wang, S. Quint, M. F. Brandl, V. Nebendahl, C. F. Roos, M. Chwalla, M. Hennrich, and R. Blatt, A quantum information processor with trapped ions, New Journal of Physics 15, 123012 (2013). 

- [70] H. Häner, S. Gulde, M. Riebe, G. Lancaster, C. Becher, J. Eschner, F. SchmidtKaler, and R. Blatt, Precision measurement and compensation of optical Stark shifts for an ion-trap quantum processor, Physical Review Letters 90, 143602 (2003). 

- [71] H. C. Nägerl, D. Leibfried, H. Rohde, G. Thalhammer, J. Eschner, F. Schmidt-Kaler, and R. Blatt, Laser addressing of individual ions in a linear ion trap, Physical Review A 60, 145 (1999). 

- [72] W. Alt, An objective lens for ecient uorescence detection of single atoms, Optik - International Journal for Light and Electron Optics 113, 142 (2002). 

- [73] L. M. Bennie, P. T. Starkey, M. Jasperse, C. J. Billington, R. P. Anderson, and L. D. Turner, A versatile high resolution objective for imaging quantum gases, Optics Express 21, 9011 (2013). 

- [74] A. A. Michelson, Studies in optics (phoenix science) (Univ of Chicago Pr, 1927). 

- [75] AWG precise enough for quantum research, (Sept. 12, 2017) https://spectruminstrumentation.com/en/awg-precise-enough-quantum-research. 

- [76] M. A. Nielsen and I. L. Chuang, Quantum computation and quantum information: 10th anniversary edition (Cambridge University Press, 2011). 

- [77] W. Li and I. Lesanovsky, Entangling quantum gate in trapped ions via Rydberg blockade, Applied Physics B 114, 37 (2014). 

- [78] H. R. Miller, Color lter array for CCD and CMOS image sensors using a chemically amplied thermally cured pre-dyed positive-tone photoresist for 365-nm lithography, in Advances in resist technology and processing XVI, edited by W. Conley (Jan. 1999). 

- [79] T. Wilkes, A. McGonigle, T. Pering, A. Taggart, B. White, R. Bryant, and J. Willmott, Ultraviolet imaging with low cost smartphone sensors: development and application of a Raspberry Pi-based UV camera, Sensors 16, 1649 (2016). 

## Appendices 

## A. Camera Software 

In the experimental setup, an electron multiplying charged coupled device (EMCCD) camera[1] is used to take images of the ions. The ions' uorescence light is collected with a home-built objective (see section 3.1.1 for details) and focused by two achromatic doublets[2] onto the camera sensor. This makes the image of the ions appear magnied by a factor of 19.4 on the camera chip. The EMCCD sensor has a resolution of 512 _×_ 512 with pixel size 16 µ m _×_ 16 µ m and full detector coverage. The camera is connected via a PCI (peripheral component interconnect) card with a computer. This computer is used almost exclusively to control the camera and thus, is referred to as camera PC in the following. One way to access the camera is the GUI software called SOLIS provided by the manufacturer of the camera. Even though SOLIS oers one to access all possible settings and operation modi of the camera, it is not possible to access the camera remotely or set up a camera server. Requiring images remotely in an automatic fashion from a dierent computer is simply impossible like this. However, many experimental situations require that one can access the camera from the TrICS PC, which controls the experiment by TrICS (Trapped Ion Control Software). 

As a remedy, a new GUI was implemented for the camera in use. It is based on the Python module qCamera[3] by Michael DePalatis. The nal software solution makes automated data processing synchronized with the rest of the experiment possible. It oers sucient control of the camera parameters in combination with high usability. On top of that, the experimentalist can enjoy the live image of single Sr ions provided by the GUI on the camera PC, while accessing the camera from the TrICS PC during the experiment. 

The basic structure of the new camera software is outlined below. Explanations and documentation are given for all main parts. In addition to that, one nds plenty of comments in the Python code of the program. Specic information for the used Andor camera can be found in the Andor software guide, Andor hardware guide and the user's guide to Andor SDK. The following descriptions can be seen as user manual. It was not written by a software engineer and is not meant for software engineers. The reader is not expected to have any prerequisites in C++. Only knowledge in Python and object oriented programming is expected. 

## A.1. qCamera 

The qCamera module is the basis of the new camera software that is used. It is a wrapper of the Andor SDK (software development kit) and allows one to access all functions in 

> 1 Andor iXon 3 

> 2 Thorlabs AC254-050-A and AC254-250-A 

> 3 qCamera, version 1.0.0b2 from https://bitbucket.org/iontrapgroup/qcamera 

the DLL (dynamic link library) of the original Andor driver. In addition, qCamera oers implementations of a ring buer and a RPC (remote procedure call) for a camera server to client communication. It also includes the possibility of event logging in the respective Python console. 

Large parts of the original qCamera distribution were not fully developed and contained bugs, which had to be eliminated prior to use. The currently used software solution is free from any known bugs originating from the qCamera module. 

The structure of the qCamera module is depicted in a UML class diagram in gure 28. The heart of the software is the class Camera. It models the state of a camera with instance variables roi, t-ms, gain, shape, bins, shutter_open, etc. The behaviour of a Camera object is governed by the dierent member functions like open_shutter(self), set_exposure_time(self,*args), start(self), GetMostRecentImage(self), set_roi(self,*args), etc. 

Most of these functions are supposed to be overridden by child classes. Thus, the Camera class can be seen as abstract generalization of a camera. For the use with a camera of a specic type, a child class of Camera has to be introduced. qCamera contains for example an AndorCamera class, which is tailored for cameras from the manufacturer Andor, like the one used in the experiment. Most of the functionality and hardware specic behaviour is implemented in the AndorCamera class. 

An important attribute of any camera is the clib object of ctypes.windll library type, which holds the Andor DLL. It acts as interface between the driver of the Andor PCI card and the Python programme. Any arbitrary function foo(*args) from the driver DLL[4] can be called as attribute of the clib object, i.e. clib.foo(*args). As the DLL is based on the programming language C, one has to pay attention to the arguments of the DLL functions and pass variables/ pointers/ referenses of appropriate type by using the Python module CPython. Most of the functions in the Andor DLL return an integer, that gives detailed information about the result of the function call and the status of the camera hardware and driver. After a successful function call 20002 is returned, for example. If an acquisition is still in progress 20013 is returned. The member function _chk(self, status) of the AndorCamera class exploits this and gives logger warnings, if function calls fail for some reason. Hence, a save way to call the DLL function foo(int a, float* b) with the value a=3 would be 

a=3 b=ctypes.c_float() _chk(a,ctypes.pointer(b)) 

> 4 detailed descriptions of all functions in the driver DLL can be found in the User's Guide to Andor SDK 

Note that we are able to pass an integer in the usual Python style. As the function expects a pointer of type oat as second argument, we have to dene a variable of type oat and pass a pointer to this variable to the function. Another important member function of the AndorCamera class is its constructor, as it congures many default hardware settings. At construction time, it sets the acquisition mode to continuous, the trigger mode to software, the A/D channels to 1 with an A/D channel bit depth of 14. The pre-amplifying gain is set to 5 and the temperature setpoint is updated to -60 _[◦]_ C. This behaviour can be altered by implementing additional member functions of AndorCamera or changing the constructor. The function that opens and closes the shutter of the Andor camera opens and closes both, the internal and external shutter, at the same time. No shutter is used in automatic mode with the current settings. 

Any Camera object holds an instance of the class RingBuffer as ringbuffer attribute. This buer can be used to save a nite number of images during acquisitions in the hierarchical data le (HDF5). This software buer is not used in any way at the moment, but may become a helpful tool in the future. 

qCamer contains the two important classes RemoteCameraServer and RemoteCameraClient. Any object of the class RemoteCameraClient holds an instance of RemoteCameraServer as server and can call functions on it via remote call procedure (RPC). This means, one can initialize an AndorCamera object and pass it to the constructor of a RemoteCameraServer within a Python program that runs on the camera PC. A RemoteCameraClient can then be initialized on a separate computer (e.g. TrICS PC) and connect to the server on the camera PC. This way, the user gains remote control over the camera, which can be expanded or restricted by adding or removing functions in the classes RemoteCameraClient and RemoteCameraServer. This feature becomes especially important for the integration of the camera, that is controlled by the camera PC, into the rest of the experiment, that is controlled by the TrICS PC. 

## A.2. GUI 

To allow for convenient and fast operation of the camera as well as a live image of the trapped stronium ions, a GUI was programmed for the camera software. It is implemented as CamView class, which is a child class of the PyQt4.QtGui.QMainWindow class, and acts as main thread during camera operation, i.e. it manages the access of the server and the user interface to the camera hardware by the use of threads and signals. The dependencies on classes of qCamera and other Python modules are shown in the UML class diagram in gure 30. 

The GUI allows the user specifying a ROI (region of interest), toggling the shutter, and starting acquisitions. Setting the ROI will not only reduce the image area shown in the GUI, but will also decrease the area on the detector, that is read-out eectively. Setting a small ROI allows for shorter read-out times of the detector and thus, enables higher frame rates. For certain actions, like toggling the shutter or changing the ROI, it is necessary to stop the acquisition of the camera on the hardware level. The software will do this in the background for the user, s.t. errors from the camera driver are avoided. The same holds true for the range of values allowed for the ROI, exposure time and gain, which can also be changed in the GUI. The value for the gain in the GUI can be understand as the EM RealGain with a linear scale specied by Andor. The value for the exposure time is in millisecond and is restricted by the software to the interval [1 _,_ 150] . 

Another feature is the auto calibration of cursors. The software estimates the positions of _n_ ions by tting a sum of _n_ Gaussian distributions to a camera image. The resulting positions are shown in the image afterwards as red crosses, each surrounded by circles with a radius of 2 standard deviations of the respective Gaussian t. The positions and standard deviations shown in the GUI on the live image of the ions are saved as list of Numpy arrays in the variable centers and sigmas of the CamView class. The user has the possibility of saving the positions as reference positions in the variable reference of the RemoteCameraServer object, by pressing the button save as reference in the GUI. The CamView object has access to the RemoteCameraServer, which is passed to the constructor of the CamView class and saved as instance variable server. The saved reference positions are used in the automated ablation loading process to detect ions from the wrong isotope. 

During the experiment, one wants to acquire images with the RemoteCameraServer before passing them to the RemoteCameraClient. At the same time, a live image shown by the camera GUI of the ion in the trap is very benecial to notice for example the loss or double ionization of an ion. To allow both, the camera GUI and the RemoteCameraServer to access the camera hardware almost at the same time, the program uses multiple threads. The CamView object acts as main thread and starts for continuous acquisitions a seperate thread of the class AcquisitionThread, which inherits from the QtCore.QThread class. The RemoteCameraServer is implemented as QtCore.QThread as well. Threads can be run in parallel, share the same memory and communicate with each other, which makes them the ideal solution for controlling the access to the camera hardware, so that no error is thrown by the driver. In the following, the operation of the camera with attention to the software level and the working principle of the dierent threads is discussed based on two examples. 

## A.2.1. Checking the Ions' Position During an Ongoing Acquisition 

The rst example explains, how the camera server can interrupt an ongoing acquisition process of the GUI when the client asks to check the position of the ions. 

As initial situation, we assume, that the user has set a ROI, a suitable exposure time and an EM gain in the GUI. The shutter has been opened and the acquisition has already been started by pressing the button in the GUI. The camera is now in the continuous acquisition mode and listens for software triggers. Those are continuously sent by the AcquisitionThread of the CamView object. After every trigger, the software waits until the acquisition has been nished[5] and acquires the most recent image from the driver, before sending the next software trigger. Suppose, that the RemoteCameraClient calls the function checkPositions at an arbitrary moment of time to take a camera image and check the number and position of the ions. This will lead to the function call of checkPositions of the RemoteCameraServer. The RemoteCameraServer will immediately emit the QtCore.SIGNAL("interruptAcq()"). The CamView object is connected to this signal upon construction. Subsequently the member function interruptAcq(self) of the CamView object is executed, which stops the current AcquisitionThread. The server thread waited in the mean time and is woken up by the CamView object. This is possible, because the two of them share a Qt.Qmutex as well as a QtCore.QWaitCondition object. Waked up again, the server can now start to take an image by starting the camera, sending a software trigger and reading out the acquired data. After doing so, it stops the camera and emits the signal "done()", which is again received by the CamView object. This shows the CamView object, that the server is nished with accessing the camera hardware and restarts the acquisition. From this moment, the user will be able to see continuously taken live images again. The server will proceed with analysing the image data. The data is rst converted to a grey scale image. After that, the ions are detected and their positions are cross-checked with the reference positions saved on the server in the variable reference. The processing of the data relies on functions from the countIons module. A boolean value, that shows if the positions of the ions t to the reference and the number of detected ions is returned by the server. Subsequently, the RemoteCameraClient can work with this information. 

Note, how the signals between the threads are used to stop a running acquisition and restart the acquisition again, after the server is nished. This prevents, that the server tries to start the camera or send a software trigger, before the prior acquisition has been nished. If the server tried to send software triggers while another acquisition is still in progress a driver error would occur. 

## A.2.2. Integration of the EMCCD into Measurements 

For some measurements, it is useful to take images while scanning a sequence in TrICS, e.g. in the case of state tomography of more than one ion or for the read-out of the state of an ion chain as quantum register. In the following, the role of the software during such a measurement is outlined. 

> 5 A separate thread tries to call the function WaitForAcquisition(void) of the DLL, while the original AcquisitionThread waits for 2 _._ 5 exposure times. The rst of those to events determines, when the acquisition is nished. 

As starting point, we assume similar to the prior example, that the user has selected a ROI, has set the exposure time to 100 ms and the em gain to 300 . The continuous acquisition of images is already in progress and the user has set the calibrated positions of the ions and saved them as reference. The camera is in the acquisition mode continuous and trigger mode software. To use the camera in the sequence, the RemoteCameraClient has to call the function startExternalTriggerMode(exposure_t_ms=10), which will lead to the call of the member function with the same name on the RemoteCameraServer object. First, the server will emit the QtCore.Signal "interruptAcq()" to stop the current acquisition. It waits for the CamView object to wake it up again, which is possible because they share a Qt.Qmutex and a QtCore.QWaitCondition object. After CamView has interrupted the acquisition, it calls the function self.cond.wakeAll(), which wakes up the server. The server continues by setting the exposure time to exposure_t_ms ms and setting the trigger mode to external. This enables, that camera acquisitions are triggered by TTL pulses. The function startExternalTriggerMode(**kwargs) subsequently starts the camera and returns the old exposure time in milliseconds, i.e. 100 in this example. 

For an unlimited time, the camera will now listen for external trigger signals, which are TTL pulses raised by an external source. During this time, the image shown in the GUI will be frozen. Each captured image is read from the camera sensor and the data is stored in the memory of the driver card. The memory is large enough to hold 96 full size images. If the user has selected a ROI, the read-out from the sensor will be much faster and the storage will be able to hold accordingly more images (e.g. for a ROI of 255 _×_ 255 the memory is enough for 384 images). It is also important, to give the camera enough time for exposure and read-out after triggering the capture of an image. This can be done, by assuring, that the time between two trigger events is at least the kinetic cycle time, which is always shown in the Python console, when changing the exposure time. If a trigger event happens before the previous exposure and readout has been nished, the trigger event will be ignored. 

After the desired number of images has been taken, the function stopExternalTriggerMode(old_t_ms=100, max_ion_number=3) has to be called on the server. This will reset the exposure time back to the value given by old_t_ms and the trigger mode software is restored. After that, all images that have been triggered by a TTL pulse and that are saved on the memory of the PCI card are read-out. The server emits the signal "done()" to show the CamView object, that it can restart the acquisition again. The server returns information containing exposure time, number of taken images, the selected ROI and the references of up to 3 ions (if not specied dierently in the max_ion_number argument) together with all images. 

To allow this procedure of starting and stopping the external trigger mode to work automatically, a small Python script called camera_trigger_mode.py has to run on the same computer as TrICS. This Python script connects to the channel camera_trigger_mode of 

gTrICS. When this box is selected, the Python script starts the external trigger mode. It stops the external trigger mode and saves the images, as soon as the box is unchecked. To avoid the must of checking and unchecking the box in gTrICS before and after every scan, one can run the small script camera_control.py in the gTrICS Python API, that does the job automatically when scanning a sequence. 

## A.3. Ion Recognition Software 

For automatic loading of the ion trap and analysis of a large number of camera images, a software, that recognizes ions automatically, is implemented. It can be found in the countIons module, that is also used by the camera software. It relies on functions of the Python package OpenCV. 

The rst step, when recognizing ions, is to convert the raw data consisting of count rates from the EMCCD sensor to a gray scale image with the function data2Gray(array). In the next step, the function findIonsInRoi(gray,colMin,rowMin,roiSelected, gaussianFilter=False) creates a thresholded image using Otsu's binarization method. Based on the image histogram, Otsu's technique automatically calculates a threshold value, according to which the image will be binarized. This works out very well for images of ions, as they are bimodal, i.e. they have a histogram with two peaks. The only requirement for is, that the ROI is set appropriately. Next, the function cv2.findContours( binarized_image,1,2) is used to nd the contours of the ions on the binarized image. After disregarding any contour that consists of only one pixel, cv2.minEnclosingCircle( contour) is used to nd the minimal enclosing circle and its centre for every found contour. The centres of those circles are a very reliable estimation for the position of the ions. The explained way is much faster than applying a t of a sum of multiple two dimensional Gaussian distributions to the raw data. 

For automatic loading, it is necessary that the software recognizes the number of ions in the trap and compares their position to the calibrated reference position of multiple 88Sr+ ions. This not only tells whether the desired ion number has been reached but also helps to detect if there are any so-called dark ions in the trap. Those are most likely doubly ionized or ions from a wrong strontium isotope. As those dark ions do not show any uorescence at the wavelength 422 nm , they are not visible on the camera image. In the presence of a dark ion, the visible[88] Sr[+] ions appear at a dierent position, however, because of the Coulomb repulsion from the dark ion. 

To check, if there is a certain number of[88] Sr , one acquires two successive camera images and counter checks the positions found by findIonsInRoi(*args) with the reference 

|_P_(_n|m_)|_P_(_n|m_)|_m_|_m_|_m_|
|---|---|---|---|---|
|||1|2|3|
|_n_|1|1|0|0|
||2|0|1|0.006|
||3|0|0|0.994|



Table 5: The probability _P_ ( _n | m_ ) of recognizing _n_ ions, if the image actually showed _m_ ions. 

positions saved on the server. If at least one of the two checks yields, that the ions' positions are correct, this result is accepted. By doing the test twice, one avoids, that an ion is not recognized at all or recognized as two ions, which happens in few cases and results in the wrong number of ions at the wrong position of course. In the table 5 the probability _P_ ( _n|m_ ) of nding _n_ ions if there were actually _m_ ions in the trap are listed. For each case _m_ = 1 _,_ 2 _,_ 3 the software was tested on 1000 images with a exposure time of 100 ms . The values in the table 5 show, that this is a reliable method to detect the number of ions during the automatic loading process. 

**==> picture [366 x 487] intentionally omitted <==**

**----- Start of picture text -----**<br>
RemoteCameraServer RPCServer<br>mutex<br>cond<br>reference RPCDispatcher RingBuffer<br>cam<br>dispatcher<br>context<br>transport<br>server Camera AndorCamera<br>redis clib _acq_modes<br>__init__ roi _trigger_modescond<br>run roi_selected lock<br>serve t_ms thread<br>get_camera_properties gain clib<br>close shape<br>set_acquisition_mode bins shape<br>use_noise_filter<br>get_image crop<br>wait_for_temp<br>save_image shutter_open<br>checkPositions cooler_active temperature_set_point<br>checkPositionsTwice temperature_set_point temp_stabilizedroi<br>getPositionsServer acq_mode<br>roi_selected<br>startExternalTriggerMode trigger_mode<br>stopExternalTriggerMode rbuffer acq_mode<br>start props trigger_mode<br>t_ms<br>stop<br>SendSoftwareTrigger __init__ gain<br>GetMostRecentImage initialize cooler_activebins<br>... get_camera_properties<br>__enter__<br>_chk<br>__exit__ initialize<br>close<br>get_camera_properties<br>zmq.Context RPCClient set_acquisition_modeget_image close<br>set_roi<br>acquire_image_data<br>reset_roi<br>get_trigger_mode<br>set_acquisition_mode<br>set_trigger_mode<br>start read_out_full_image<br>RemoteCameraClient stop read_out_roi<br>SendSoftwareTrigger<br>SendSoftwareTrigger<br>contextclient open_shutter GetMostRecentFullGetMostRecentROI<br>close_shutter<br>server GetMostRecentImage<br>set_shutter<br>acquire_image_data<br>initialize toggle_shutter get_trigger_mode<br>get_exposure_time<br>get_camera_properties set_trigger_mode<br>close set_exposure_time start<br>update_exposure_time<br>set_acquisition_mode stop<br>acquire_image_data GetMostRecentImage set_shutter<br>start get_gain update_exposure_time<br>stop set_gain get_gain<br>SendSoftwareTrigger cooler_on set_gain<br>checkPositions cooler_off cooler_on<br>checkPositionsTwice set_cooler cooler_off<br>startExternalTriggerMode get_cooler_temperature get_cooler_temperature<br>stopExternalTriggerMode set_cooler_temperature set_cooler_temperature<br>... set_roireset_roi<br>**----- End of picture text -----**<br>


Figure 28: UML class diagram of the qCamera module for Python. 

**==> picture [423 x 450] intentionally omitted <==**

Figure 29: A screenshot of the new camera software is shown. It oers access to all necessary parameters at rst sight. 

**==> picture [361 x 493] intentionally omitted <==**

**----- Start of picture text -----**<br>
QtGui.QMainWindow QtCore.QThread<br>AcquisitionThread<br>cam<br>mutex<br>CamView active<br>cam __init__<br>data __del__<br>center acquireNextImage<br>sigmas run RemoteCameraServer<br>cond<br>mutex<br>mutex<br>cond<br>server SingleThread reference<br>serverStoppedAcq cam<br>acqThread cam dispatcher<br>__init__initUI mutexactive contexttransport<br>toggleAcq __init__ serverredis<br>singleAcq __del__<br>interruptAcq acquireNextImage __init__<br>restartAcq run run<br>RefreshImage serve<br>setGain<br>get_camera_properties<br>setExpTimepaintEvent QtCore.QWaitCondition close<br>setCenter set_acquisition_mode<br>resetCenter get_image<br>setROI save_image<br>printSomething<br>resetROI<br>checkPositions<br>ShutterButtonClicked<br>checkPositionsTwice<br>CalibratePositions<br>closeEvent set_roi<br>reset_roi<br>get_trigger_mode<br>QMutex set_trigger_mode<br>start<br>RemoteCameraClient stop<br>SendSoftwareTrigger<br>context GetMostRecentImage<br>client checkPositions<br>server Camera checkPositionsTwice<br>initialize clib startExternalTriggerMode<br>stopExternalTriggerMode<br>get_trigger_mode roi<br>update_exposure_time<br>set_trigger_mode t_ms<br>start ... get_gainset_gain<br>stop<br>get_cooler_temperature<br>SendSoftwareTrigger __init__<br>set_cooler_temperature<br>GetMostRecentImage set_acquisition_mode<br>checkPositions ...<br>checkPositionsTwice<br>startExternalTriggerMode<br>stopExternalTriggerMode<br>update_exposure_time<br>get_gain<br>set_gain<br>get_cooler_temperature<br>set_cooler_temperature zmq.Context<br>**----- End of picture text -----**<br>


Figure 30: UML class diagram of the CamView class, that implements the camera GUI. Important dependencies on classes from other Python modules are considered as well. 

## B. Raspberry Pi Beam Proler 

For the addressing of single ions, a tightly focused laser beam with a waist smaller than 5 µ m is used. In order to test the planned optics and setup prior to its integration into the experiment, it is necessary to characterize the focused laser beam with respect to its waist _w_ and _M_[2] parameter. For this purpose, one can measure the spatial intensity prole of a laser beam directly with a camera chip. By measuring the intensity prole with a camera sensor, one can inspect the focused laser beam directly for aberrations. A scientic camera was used for this purpose routinely in our lab. The camera is a CMOS sensor with a pixel size of 5 _._ 3 µ m . The resolution is therefore too low to characterize the expected intensity prole at the focus of the laser beam. 

For the characterization of the addressing beam, a camera sensor with higher resolution, i.e. smaller pixel size, is desirable. A low cost camera chip, with small pixel size is the Raspberry Pi camera module V2. A Raspberry Pi beam proler, that is able to characterize tightly focused laser beams, was developed as tool for the characterization of the single ion addressing beam and future beam prole measurements in the lab. The details of this beam proler are outlined in the following. A software that is easy to use and allows to control the newly developed beam proler remotely was programmed. A short software manual for the users is given in the following. The beam proler is in particular interesting, as commercial beam prolers do not oer the characterization of laser beams with a small focus and come with a high price. 

## B.1. Raspberry Pi Camera Module V2 

The Raspberry Pi camera module V2 works with a Sony IMX219PQ image sonsor, which is a CMOS sensor with a pixel size as small as 1 _._ 12 µ m . It has 3280 _×_ 2464 active pixels and the sensor measures a diagonal size of 4 _._ 6 mm . It is available as a NoIR version without infrared lter. The camera can be used in combination with a Raspberry Pi and due to the open source Python module picamera, one can access nearly all hardware settings of the camera sensor in a Python program. It is possible, to read out the raw Bayer data, that corresponds to the directly measured light intensity on the sensor, which has not undergone any GPU processing. The full hardware control and the capturing of raw Bayer data distinguishes the Raspberry Pi camera sensor from other low cost webcams. 

## B.1.1. De-Bayering of the CMOS Sensor 

On top of the Raspberry Pi camera module is a plastic housing holding an objective and a glass window. The objective can simply be unscrewed with a small tool, that is included 

in the delivery of the camera. The glass window is glued to the plastic housing. One can remove the plastic housing and the glass window, to avoid ghosting and aberrations caused by the window. For this, one can unplug the actual camera chip from the PCB board. The plastic housing is glued to the PCB board of the camera chip. The best way to remove it is to cut gently with a razor blade or scalpel between the PCB (printed circuit board) board and the plastic housing. One should do this very carefully as there are ve tiny SMD (surface-mounted device) components 1 mm away from the edges of the PCB board. There can be found many instructions on the internet, how to remove the plastic housing from the sensor. The camera sensor after successful removal of the plastic housing can be seen in gure 31. The glass window is glued to the plastic housing. By heating the glass window with a heat gun or soldering iron, the glue may soften slightly, which makes removing the window easier. In some cases, the glass window breaks, when it is removed, which is less of a problem. 

**==> picture [423 x 242] intentionally omitted <==**

Figure 31: The Raspberry Pi CMOS sensor after the removal of the plastic housing is shown. The plastic housing is on the right. The ve SMD components in close proximity to where the plastic housing is glued are clearly visible. One has to be careful not to rip them o when removing the plastic housing. The sensor should not be touched as it surrounded by tiny gold contacts. 

On top of the camera sensor is a so-called Bayer lter or CFA (color lter array). A Bayer lter consists of a mosaic structure of photoresist like Diazonaphthoquinone-novolak [78]. This array is lled with dierent pigment or dye molecules, which transmit only certain parts of the visible spectrum, for instance green, red or blue. A Bayer lter turns a monochrome sensor array into a color resolving imaging sensor. The Bayer lter on the Raspberry Pi camera sensor is GBRG, i.e. for any square of 2 _×_ 2 neighbouring pixels two pixels on the diagonal are covered by a green permeable lter, whereas the two pixels on the other diagonal are covered by a blue and red permeable lter respectively. The Bayer 

lter is necessary for color photography with the CMOS sensor. For the use as a beam proler, it would be benecial to remove the Bayer lter array from the camera sensor. This turns the sensor into a monochrome imaging sensor, that is sensitive to radiation ranging from UV to IR. Chemical removal of the Bayer lter from this type of chip by a photoresist remover has been demonstrated for the development of a low-cost UV camera in [79]. Such a chemical removal has to remove not only the Bayer lter, but also the microlens array on top of that. 

In order to remove the color lter and micro lens array, the sensor was immersed in a ultrasonic bath with a photoresist remover[1] , that was available in the clean room of Albanova. This was repeated twice for 30 min at 58 _[◦]_ C . Subsequently, the sensor was cleaned in an acetone bath followed by a isopropanol bath for 1 min respectively. 

The rst trial was done with a camera chip, whose bondigs got damaged during the removal of the plastic housing. The CMOS sensor was also slightly scratcehd in this case. Inspection under the microscope after the chemical procedure showed a partial removal of the Bayer lter. In a second try, a functioning camera chip was used. After the removal attempt, the Bayer lter looked intact, however. When connecting the camera chip to the PCB board of the camera module, the Raspberry Pi was unable to read images from the sensor; i.e. the bondings on the chip or the cables to the connector got damaged due to the removal process. No further attempt was made to remove the Bayer lter array chemically. It was concluded instead, that the photoresist remover at hand is not able to remover the photoresist, that builds up the color lter and microlens array. 

It is common in the community of astrophotography, to remove the color lter array from the sensor of a DSLR camera to gain higher light sensitivity. For this purpose, the Bayer lter is just scratched o mechanically from the camera sensor by a wooden tool. This was also tried with the two broken Raspberry PI camera sensors after the attempt of chemical removing the Bayer lter. The mechanical removal is in this case much harder, because there is a microlens array on top of the Bayer lter and because the CMOS sensor is much smaller than the sensor of a DSLR camera. 

To get a monochrome performance of the sensor, the raw Bayer data, which is the direct read out of the pixel values from the sensor, is post-processed. For the intensity of a monochrome laser beam, the raw Bayer data _P_ ( _i, j_ ) corresponds to the intensity _I_ ( _i, j_ ) , that hits the camera sensor modulated by the eciency of the Bayer lter array at every given pixel _b_ ( _i, j_ ) . 

**==> picture [262 x 12] intentionally omitted <==**

> 1 Micro Resist Technology, mr-Rem 700 

In order to undo the action of the Bayer lter, one can substitute every pixel value by the average over the pixel values within a 2 _×_ 2 square of neighbouring pixel. This will always include two green pixels, one red and one blue pixel. The new pixel values _P[′]_ ( _i, j_ ) are nothing else than a convolution of the old values with a 2 _×_ 2 matrix _M_ with all entries 1/4. 

**==> picture [321 x 33] intentionally omitted <==**

Alternatively, one can also take capture the raw data, when the whole sensor is illuminated with constant intensity _I_ ( _i, j_ ) = _I_ 0 at the wavelength of interest. The measured pixel values 

**==> picture [254 x 12] intentionally omitted <==**

serve as calibration and one can either gain the eciency of each pixel _i, j_ or the average pixel eciency for pixels of a given color from it. In the rst case, the corrected pixel values _P[′]_ ( _i, j_ ) are simply 

**==> picture [276 x 27] intentionally omitted <==**

which is the normalized intensity. 

## B.2. Beam Proler Software 

The software of the beam proler can be divided into three parts. One is the remote procedure control that is established between the Raspberry Pi and another computer. The second part is the communication between the Raspberry Pi and the computer via a network socket, that is used to transmit images from the Raspberry to the computer. The third part is the GUI, that is run on the computer, to control the camera and perform beam proling and measurements of the q-parameter. 

Necessary Python modules for the beam proler are picamera (only on the Raspberry Pi), PyQtGraph (only on the computer), PyQt4, tinyrpc and zmq. 

## Remote Procedure Control 

A remote RPC (remote procedure call) is established between the computer (client) and the Raspberry Pi (server). This behaviour is modelled by two classes BeamProfilerClient 

and BeamProfilerServer. An instance of the respective class has to be initialized on the computer and the Raspberry respectively. The member function serve_forever() of the BeamProfilerServer object on the Raspberry Pi has to be executed, before the client can connect to the server. The two computers must be connected to the same local network and the local IP address of the RaspberryPi has to be passed to the BeamProfilerClient instance on the computer upon its construction. 

After the RPC has been set up, the client can control all hardware settings of the camera via its own member functions. The only setting, that is not accessible is the sensor mode, which is set to be 2 by default, as it allows for the use of the full sensor area. 

## Socket Network Interface 

Sending captured images from the Raspberry Pi and receiving them on the computer is handled by the two classes Network_Sender and Network_Receiver. Both classes are implemented as child classes of the QtCore.QThread class. 

The Network_Sender is an attribute of the BeamProfilerServer. The BeamProfilerClient initalizes its Network_Receiver, which has its own network socket on the port 8000 based on the Python module socket. The socket starts listening for a connection from the Raspberry Pi. The BeamProfilerClient on the computer issues the initialization of a Network_Sender on the BeamProfilerServer object. The Network_Sender instance tries to connect to the socket of the Network_Receiver. It needs the IP address of the computer upon construction for this purpose. The Network_Sender on the Raspberry Pi can then take one image after another and send it to the Network_Receiver on the computer via the socket interface. It is possible to send and receive the raw Bayer data or images in the YUV format. In the latter case, only the Y array is sent. 

Transmitting images from the Raspberry Pi to the computer was found to be rather slow; frame rate _≈_ 0 _._ 2 Hz for a full size raw Bayer image. If one selects a ROI only the data of the selected part is sent, which increases the frame rate correspondingly. Hooking up the Raspberry Pi to the network via Ethernet comes with an additional speed-up. The frame rate at which images an be transferred from the Raspberry to the computer is certainly a feature of the beam proler, that deserves improvement in the future. This may be done, by communication via a USB connection between the Raspberry Pi and the computer. 

## Beam Proler GUI 

The GUI of the beam proler, that runs on the computer, is implemented as child class of the QtGui.QMainWindow class. In the background, it manages the RPC and the socket network interface during image acquisitions, that have just been described. Processes, that are supposed to happen in parallel or successively are implemented as QtCore.QThreads 

communicating via QtCore.SIGNALS. The GUI opens the user the possibility to change all hardware settings of the camera, start the acquisition of camera images and analyze the intensity prole. Version 4 of the Python module PyQt, which is not compatible with version 5, was used to implement the GUI. 

The next section is dedicated exclusively to the use of the beam proler and the GUI for the end user. 

## B.3. User Guide 

The following user guide can be seen as a brief manual of the beam proler. Users, that want to apply the beam proler in the daily lab routine without the necessity of understanding the whole code and underlying application software may nd this section most useful. 

## Starting the Beam Proler and Establishing a Connection 

In order to use the beam proler, one has to plug in the Raspberry Pi Camera Module V2 to the Raspberry Pi via the ribbon cable. Afterwards, one can power up the Raspberry Pi. In case, you are using a brand new Raspberry Pi, go into the raspi-cong and make sure, that the camera is enabled and that the GPU memory is set to 512 Mb. 

Then, the le called RPC_ script has to be run and an instance of the BeamProfilerServer has to be initialized and started with the following code snippet 

server=BeamProfilerServer() 

server.serve() 

The instance of the BeamProfilerServer class is now running on the Raspberry Pi and ready to receive commands from a client on the computer. From this point, we will not have to deal with the Raspberry Pi anymore, but can do everything from the GUI on the computer. 

On the computer we run the le ProlerGUI in Python, which should contain a statement like 

if __name__ == "__main__": app = QtGui.QApplication(sys.argv) GUI=BeamProfiler(None) 

sys.exit(app.exec_()) 

This starts the beam proler GUI. If the BeamProfilerServer has been started on the Raspberry Pi already, one can enter the local IP address of the Raspberry Pi in the respective eld of the GUI and click on the button that says connect to raspberry pi. 

The RPC is now established and we can take images and change the camera settings in the GUI. 

## Starting Acquisitions and Camera Settings 

The beam proler GUI must know the local IP address of the computer, to guarantee for smooth communication via the socket network interface. The GUI tries to determine this IP address by itself and shows the respective result in the eld that reads Your IP. If the shown value is not your IP address, you have to change it to your actual local IP address and save the change by pressing the button set own IP manually. 

We are now ready to start an acquisition. For this, just press the button start RAW acquisition or start YUV acquisition depending on the kind of images you want to read out. For the proling of laser beams it is highly recommended to use the raw format, as it was not subjected to any post-processing. The GUI has a tab on the right side which reads camera. Here, all camera settings can be accessed and manipulated. After starting the acquisition, the resulting image is plotted in the GUI. To increase the frame rate, it is advisable to set a ROI, because less data has to be sent from the Raspberry Pi to the computer in this case. It is recommendable, to let the camera take several images with exposure mode in auto before one switches to o, such that one can change the exposure time by hand. This enables the camera to stabilize the analog and digital gain, which can not be manipulated by the software for technical reasons. The tab with the camera settings also includes a button refresh values, which updates the values for all shown settings of the camera. The camera settings can be changed while an acquisition is in progress. 

## Analyzing the Intensity Prole 

The GUI oers two ways to investigate the beam prole of a elliptical Gaussian beam. For this, one has to go to the tab, that reads t. Here one can analyze the intensity prole according to the _D_ 4 _σ_ method, which is also conform with the ISO 11146-1 standard for stigmatic and simple astigmatic beams. The user just has to press the button ISO 11146 D4 _σ_ for this purpose. The resulting values are displayed for every captured image and a Gaussian prole according to the results is displayed next to the measured intensity prole. 

In the _D_ 4 _σ_ the center coordinates _⟨i⟩, ⟨j⟩_ of the beam is determined by calculating the rst moments of the measured intensity distribution _I_ ( _i, j_ ) . 

**==> picture [257 x 30] intentionally omitted <==**

**==> picture [258 x 30] intentionally omitted <==**

_i_ and _j_ label the pixel position on the detector. _P_ is the power of the measured intensity given by 

**==> picture [246 x 26] intentionally omitted <==**

To arrive at the actual beam diameter, one also has to calculate the second moments 

**==> picture [296 x 64] intentionally omitted <==**

**==> picture [296 x 30] intentionally omitted <==**

From this one can calculate the _D_ 4 _σ_ beam diameters 

**==> picture [348 x 63] intentionally omitted <==**

where _γ_ = sgn( _⟨i_[2] _⟩−⟨j_[2] _⟩_ ) . The _D_ 4 _σ_ 1 _,_ 2 beam diameters correspond to four times the standard deviations _σ_ 1 _,_ 2 of the intensity distribution along the respective main axis of the Gaussian beam prole. This also accounts for the case, in which those axes are rotated with respect to the _x, y_ axes. The angle of rotation is given by 

**==> picture [277 x 28] intentionally omitted <==**

For a Gaussian beam, _D_ 4 _σ_ 1 _,_ 2 is equal to 2 _w_ 1 _,_ 2 with the 1 _/e_[2] waists _w_ 1 _,_ 2 of the intensity prole. The values, that have been described so far are of course in units of pixel size. In order to get physical meaningful results, one has to multiply with the right power of the pixel size 1 _._ 12 µ m . 

The _D_ 4 _σ_ method is aected by a non-zero baseline value. It is therefore advisable, to take an image while the laser beam is blocked and save it as baseline value by pressing the button baseline correction. The saved values will be subtracted from every image prior to the _D_ 4 _σ_ analysis. 

As an alternative to the _D_ 4 _σ_ method, a two dimensional Gaussian least square t is implemented as well. It is started by pressing the button t 2D Gaussian. This method attempts to determine the second moments of the Gaussian beam prole by the _D_ 4 _σ_ analysis, whose result is used as initial guess for the t. The least square t is less prone to the baseline value. After a successful t, the result is displayed next to the measured intensity prole. 

## Measuring the Complex Beam Parameter 

One is often interested in the complex beam parameter _q_ , which characterizes the propagation of a laser beam with respect to its Rayleigh length _zR_ and the position _z_ 0 of its minimum 1 _/e_[2] waist. 

**==> picture [241 x 12] intentionally omitted <==**

with the usual Rayleigh length expressed by the 1 _/e_[2] beam waist _w_ 0 at _z_ 0 

**==> picture [236 x 25] intentionally omitted <==**

The _q_ parameter fully determines the propagation of a Gaussian beam according to 

**==> picture [277 x 34] intentionally omitted <==**

To determine the _q_ parameter, one has to take several measurements of the intensity prole and analyze it with respect to its diameter according to either the _D_ 4 _σ_ method or the 2D Gaussian t. After that, one can save the resulting diameter of the last measure- 

ment together with the value _z_ of the detector position in the lab frame. The respective value of _z_ is entered in mm and the button add to q measurement has to be pressed. One can delete the last added value or all values by pressing the buttons remove last or reset. One also has to enter the wavelength in nm once and save it with the button set. The ISO 11146 standard recommends, to determine the beam diameter ve times at each value of _z_ . Concerning the distribution of _z_ values, half of the data points should be within _|z| < zR_ whereas the other half of data points should be within _|z| >_ 2 _zR_ . As soon as suciently much data points are taken, the resulting propagation can be plotted and tted according to equation B.16. The resulting data points and t curve are shown in the tab labeled beam parameter q. The resulting _q_ values for the two axis are shown in the legend. The angle of the beam axis with the lab frame _x, y_ is also plotted. 

## B.4. Conclusion 

The designed beam proler based on the Raspberry Pi camera module was applied in section 3.1.1 for the characterization of the highly focused 674 nm laser beam, that will be used to address single ions. As soon as the single-ion addressing setup is completed according to the design proposal in section 3.2, the beam proler can be used to measure the obtained focus in a test run. This can help to evaluate the expected performance of the optical setup. Hopefully, the beam proler will be considered a useful tool in the Trapped Ion Quantum Technologies Group and will be developed further. The frame-rate, which is restricted by the speed of data transfer from the Raspberry Pi to the computer, may be improved for example. Another great achievement would be the successful removal of the Bayer lter array, which enables the full resolution of 1 _._ 12 µ m pixels. It also increase the sensitivity of the sensor for UV lasers. 

TRITA-SCI-GRU 2018:049 

**==> picture [596 x 133] intentionally omitted <==**

**----- Start of picture text -----**<br>
www.kth.se<br>www.tum.de<br>**----- End of picture text -----**<br>


