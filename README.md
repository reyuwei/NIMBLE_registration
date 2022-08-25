# nr-reg
Repo for non-rigid registration in **PIANO: A Parametric Hand Bone Model from Magnetic Resonance Imaging, IJCAI' 21** and **NIMBLE: A Non-rigid Hand Model with Bones and Muscles, SIG' 22**

# Usage
- Embedded non-rigid registration (PIANO)

    `reg_embedded.py`

- Tetrahedral-based non-rigid deformation (NIMBLE)

    `reg_tet.py` (not ready yet)

## Acknowledgment
- Algorithm reference
  - [[TOG20] Constraining Dense Hand Surface Tracking with Elasticity](https://research.facebook.com/publications/constraining-dense-hand-surface-tracking-with-elasticity/)
  - [[SIG12 Course] FEM Simulation of 3D Deformable Solids: A practitioner's guide to theory, discretization and model reduction](http://viterbi-web.usc.edu/~jbarbic/femdefo/)
  - [[TVCG19] FlyFusion: Realtime Dynamic Scene Reconstruction Using a Flying Depth Camera](https://ieeexplore.ieee.org/document/8778689)
  - [[SIG18] MonoPerfCap: Human Performance Capture from Monocular Video](https://vcai.mpi-inf.mpg.de/projects/wxu/MonoPerfCap/)
  - [[SIG07] Embedded Deformation for Shape Manipulation](https://people.inf.ethz.ch/~sumnerb/research/embdef/Sumner2007EDF.pdf)


- Code reference
  - [manopth](https://github.com/hassony2/manopth/blob/master/manopth) by [Yana Hasson](https://hassony2.github.io/)
  - [pytorch_HMR](https://github.com/MandyMo/pytorch_HMR) by [Zhang Xiong](https://github.com/MandyMo)
  - [SMPLX](https://github.com/vchoutas/smplx) by [Vassilis Choutas](https://github.com/vchoutas)
  - [LoopReg](https://github.com/bharat-b7/LoopReg) by [Bharat Bhatnagar](https://github.com/bharat-b7)
  - [GAMES201-elasticity demo](https://github.com/taichi-dev/games201/releases/download/lec3/demos.zip) by [Yuanming Hu](https://yuanming.taichi.graphics/)
