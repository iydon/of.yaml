<!-- Template from https://github.com/othneildrew/Best-README-Template -->
<div id="top"></div>



<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL-3.0 License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/iydon/of.yaml">
    🟢⬜🟩⬜🟩<br />
    ⬜⬜⬜⬜⬜<br />
    🟩⬜🟩⬜🟩<br />
    ⬜⬜⬜⬜⬜<br />
    🟩⬜🟩⬜🟩<br />
  </a>

  <h3 align="center">OpenFOAM.YAML</h3>

  <p align="center">
    Python Interface to OpenFOAM Using YAML Configuration
    <br />
    <a href="https://github.com/iydon/of.yaml"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/iydon/of.yaml">View Demo</a>
    ·
    <a href="https://github.com/iydon/of.yaml/issues">Report Bug</a>
    ·
    <a href="https://github.com/iydon/of.yaml/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#demo">Demo</a></li>
        <li><a href="#tutorials">Tutorials</a></li>
        <li><a href="#task-list">Task List</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This repository was originally designed to solve the problem of complex OpenFOAM case structure, and the solution was to re-present the original cases using the common configuration file format YAML. Later, since there is a corresponding package for the YAML format in Python, I wrote this Python interface package for OpenFOAM, and then I added progress bars to most OpenFOAM solvers by analyzing log files in real time. Although there are still many details to be specified in this repository, its function of generating cases and calling solvers is ready for preliminary use, for example, I used this package to generate cases in batch in my own project. In the future I would like to integrate the post-processing steps into this interface package as well.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Poetry](https://github.com/python-poetry/poetry)
* [PyYAML](https://github.com/yaml/pyyaml)
* [py7zr](https://github.com/miurahr/py7zr)
* [packaging](https://github.com/pypa/packaging)
* [click](https://github.com/pallets/click)
* [tqdm](https://github.com/tqdm/tqdm)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This project currently uses Poetry to manage Python dependencies. I've heard good things about [PDM](https://github.com/pdm-project/pdm) so far, and may provide PDM support subsequently. If Poetry is not installed, you can refer to [official installation guide](https://github.com/python-poetry/poetry#installation).

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/iydon/of.yaml.git
   ```
2. Install Python dependencies
   ```sh
   poetry install
   ```
3. Activate the virtual environment
   ```sh
   poetry shell
   ```
4. (Optional) Convert Python package into a single file
   ```sh
   make standalone
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Demo

Save the following demo code as a separate file (e.g. `demo.py`).

```python
from foam import Foam

foam = Foam.from_file('tutorials/incompressible/simpleFoam/airFoil2D.yaml')
foam.save('airFoil2D')
foam.cmd.all_run()
```

Running the demo code in the virtual environment results in the following output.

```sh
$ poetry run python demo.py
Running simpleFoam on .../of.yaml/airFoil2D
 63%|██████████████████████████████████████▏                      | 313.0/500.0 [00:06<00:04, 46.66it/s]
```

### Tutorials

The following table shows the OpenFOAM cases that have been converted to YAML format. You can find the corresponding rules by comparing the YAML format with its original format, and I don't have the time or interest to organize the corresponding documentation for the time being.

<details>
  <summary>The existing OpenFOAM tutorials in YAML format</summary>

  | YAML | OpenFOAM | Version | Solver |
  | --- | --- | --- | --- |
  | [airFoil2D.yaml](tutorials/incompressible/simpleFoam/airFoil2D.yaml) | [airFoil2D](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/incompressible/simpleFoam/airFoil2D) | 7 | [incompressible/simpleFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/incompressible/simpleFoam) |
  | [beamEndLoad.yaml](tutorials/stressAnalysis/solidEquilibriumDisplacementFoam/beamEndLoad.yaml) | [beamEndLoad](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/stressAnalysis/solidEquilibriumDisplacementFoam/beamEndLoad) | 7 | [stressAnalysis/solidEquilibriumDisplacementFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/stressAnalysis/solidEquilibriumDisplacementFoam) |
  | [boxTurb16.yaml](tutorials/DNS/dnsFoam/boxTurb16.yaml) | [boxTurb16](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/DNS/dnsFoam/boxTurb16) | 7 | [DNS/dnsFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/DNS/dnsFoam) |
  | [cylinder.yaml](tutorials/basic/potentialFoam/cylinder.yaml) | [cylinder](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/basic/potentialFoam/cylinder) | 7 | [basic/potentialFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/basic/potentialFoam) |
  | [damBreak.yaml](tutorials/multiphase/interMixingFoam/laminar/damBreak.yaml) | [damBreak](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interMixingFoam/laminar/damBreak) | 7 | [multiphase/interMixingFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interFoam/interMixingFoam) |
  | [damBreak4phase.yaml](tutorials/multiphase/multiphaseInterFoam/laminar/damBreak4phase.yaml) | [damBreak4phase](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/multiphaseInterFoam/laminar/damBreak4phase) | 7 | [multiphase/multiphaseInterFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/multiphaseInterFoam) |
  | [damBreak4phaseFine.yaml](tutorials/multiphase/multiphaseInterFoam/laminar/damBreak4phaseFine.yaml) | [damBreak4phaseFine](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/multiphaseInterFoam/laminar/damBreak4phaseFine) | 7 | [multiphase/multiphaseInterFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/multiphaseInterFoam) |
  | [damBreakWithObstacle.yaml](tutorials/multiphase/interFoam/laminar/damBreakWithObstacle.yaml) | [damBreakWithObstacle](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interFoam/laminar/damBreakWithObstacle) | 7 | [multiphase/interFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interFoam) |
  | [DTCHull.yaml](tutorials/multiphase/interFoam/RAS/DTCHull.yaml) | [DTCHull](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interFoam/RAS/DTCHull) | 7 | [multiphase/interFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interFoam) |
  | [elbow.yaml](tutorials/incompressible/icoFoam/elbow.yaml) | [elbow](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/incompressible/icoFoam/elbow) | 7 | [incompressible/icoFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/incompressible/icoFoam) |
  | [europeanCall.yaml](tutorials/financial/financialFoam/europeanCall.yaml) | [europeanCall](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/financial/financialFoam/europeanCall) | 7 | [financial/financialFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/financial/financialFoam) |
  | [fileHandler.yaml](tutorials/IO/fileHandler.yaml) | [fileHandler](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/IO/fileHandler) | 7 | [lagrangian/icoUncoupledKinematicParcelFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/lagrangian/icoUncoupledKinematicParcelFoam) |
  | [flange.yaml](tutorials/basic/laplacianFoam/flange.yaml) | [flange](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/basic/laplacianFoam/flange) | 7 | [basic/laplacianFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/basic/laplacianFoam) |
  | [mixerVessel2D.yaml](tutorials/multiphase/multiphaseInterFoam/laminar/mixerVessel2D.yaml) | [mixerVessel2D](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/multiphaseInterFoam/laminar/mixerVessel2D) | 7 | [multiphase/multiphaseInterFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/multiphaseInterFoam) |
  | [nozzleFlow2D.yaml](tutorials/multiphase/interFoam/LES/nozzleFlow2D.yaml) | [nozzleFlow2D](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interFoam/LES/nozzleFlow2D) | 7 | [multiphase/interFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interFoam) |
  | [pipeCyclic.yaml](tutorials/incompressible/simpleFoam/pipeCyclic.yaml) | [pipeCyclic](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/incompressible/simpleFoam/pipeCyclic) | 7 | [incompressible/simpleFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/incompressible/simpleFoam) |
  | [pitzDaily.yaml](tutorials/basic/potentialFoam/pitzDaily.yaml) | [pitzDaily](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/basic/potentialFoam/pitzDaily) | 7 | [basic/potentialFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/basic/potentialFoam) |
  | [pitzDaily.yaml](tutorials/basic/scalarTransportFoam/pitzDaily.yaml) | [pitzDaily](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/basic/scalarTransportFoam/pitzDaily) | 7 | [basic/scalarTransportFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/basic/scalarTransportFoam) |
  | [plateHole.yaml](tutorials/stressAnalysis/solidDisplacementFoam/plateHole.yaml) | [plateHole](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/stressAnalysis/solidDisplacementFoam/plateHole) | 7 | [stressAnalysis/solidDisplacementFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/stressAnalysis/solidDisplacementFoam) |
  | [sloshingTank3D6DoF.yaml](tutorials/multiphase/interFoam/laminar/sloshingTank3D6DoF.yaml) | [sloshingTank3D6DoF](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interFoam/laminar/sloshingTank3D6DoF) | 7 | [multiphase/interFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interFoam) |
  | [propeller.yaml](tutorials/multiphase/interPhaseChangeFoam/propeller.yaml) | [propeller](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interPhaseChangeFoam/propeller) | 7 | [multiphase/interPhaseChangeFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interPhaseChangeFoam) |
  | [mixerVesselAMI.yaml](tutorials/multiphase/interFoam/RAS/mixerVesselAMI.yaml) | [mixerVesselAMI](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interFoam/RAS/mixerVesselAMI) | 7 | [multiphase/interFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interFoam) |
  | [sloshingTank2D.yaml](tutorials/multiphase/compressibleInterFoam/laminar/sloshingTank2D.yaml) | [sloshingTank2D](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/compressibleInterFoam/laminar/sloshingTank2D) | 7 | [multiphase/compressibleInterFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/compressibleInterFoam) |
  | [damBreak4phase.yaml](tutorials/multiphase/compressibleMultiphaseInterFoam/laminar/damBreak4phase.yaml) | [damBreak4phase](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/compressibleMultiphaseInterFoam/laminar/damBreak4phase) | 7 | [multiphase/compressibleMultiphaseInterFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/compressibleMultiphaseInterFoam) |
  | [flamePropagationWithObstacles.yaml](tutorials/combustion/PDRFoam/flamePropagationWithObstacles.yaml) | [flamePropagationWithObstacles](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/combustion/PDRFoam/flamePropagationWithObstacles) | 7 | [combustion/PDRFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/combustion/PDRFoam) |
  | [kivaTest.yaml](tutorials/combustion/XiEngineFoam/kivaTest.yaml) | [kivaTest](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/combustion/XiEngineFoam/kivaTest) | 7 | [combustion/XiEngineFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/combustion/XiFoam/XiEngineFoam) |
  | [moriyoshiHomogeneous.yaml](tutorials/combustion/XiFoam/RAS/moriyoshiHomogeneous.yaml) | [moriyoshiHomogeneous](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/combustion/XiFoam/RAS/moriyoshiHomogeneous) | 7 | [combustion/XiFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/combustion/XiFoam) |
  | [throttle.yaml](tutorials/multiphase/cavitatingFoam/LES/throttle.yaml) | [throttle](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/cavitatingFoam/LES/throttle) | 7 | [multiphase/cavitatingFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/cavitatingFoam) |
  | [throttle3D.yaml](tutorials/multiphase/cavitatingFoam/LES/throttle3D.yaml) | [throttle3D](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/cavitatingFoam/LES/throttle3D) | 7 | [multiphase/cavitatingFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/cavitatingFoam) |
  | [throttle.yaml](tutorials/multiphase/cavitatingFoam/RAS/throttle.yaml) | [throttle](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/cavitatingFoam/RAS/throttle) | 7 | [multiphase/cavitatingFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/cavitatingFoam) |
</details>

### Task List

The following is a task list to convert [OpenFOAM-7](https://github.com/OpenFOAM/OpenFOAM-7) to the corresponding YAML format. The corresponding rules for conversion are not currently organized because some of them are still unstable. I will first try to convert as many tutorials as possible, and then organize the rules afterwards.

<details>
  <summary>Conversion task list</summary>

  - [x] DNS
      - [x] dnsFoam
          - [x] boxTurb16
  - [x] IO
      - [x] fileHandler
  - [x] basic
      - [x] laplacianFoam
          - [x] flange
      - [x] potentialFoam
          - [x] cylinder
          - [x] pitzDaily
      - [x] scalarTransportFoam
          - [x] pitzDaily
  - [ ] combustion
      - [x] PDRFoam
          - [x] flamePropagationWithObstacles
      - [x] XiEngineFoam
          - [x] kivaTest
      - [x] XiFoam
          - [x] RAS
              - [x] moriyoshiHomogeneous
      - [ ] chemFoam
          - [ ] gri
          - [ ] h2
          - [ ] ic8h18
          - [ ] ic8h18_TDAC
          - [ ] nc7h16
      - [ ] coldEngineFoam
          - [ ] freePiston
      - [ ] fireFoam
          - [ ] LES
              - [ ] flameSpreadWaterSuppressionPanel
              - [ ] oppositeBurningPanels
              - [ ] smallPoolFire2D
              - [ ] smallPoolFire3D
      - [ ] reactingFoam
          - [ ] RAS
              - [ ] DLR_A_LTS
              - [ ] SandiaD_LTS
              - [ ] membrane
          - [ ] laminar
              - [ ] counterFlowFlame2D
              - [ ] counterFlowFlame2DLTS
              - [ ] counterFlowFlame2DLTS_GRI_TDAC
              - [ ] counterFlowFlame2D_GRI
              - [ ] counterFlowFlame2D_GRI_TDAC
  - [ ] compressible
      - [ ] rhoCentralFoam
          - [ ] LadenburgJet60psi
          - [ ] biconic25-55Run35
          - [ ] forwardStep
          - [ ] movingCone
          - [ ] obliqueShock
          - [ ] shockTube
          - [ ] wedge15Ma5
      - [ ] rhoPimpleFoam
          - [ ] LES
              - [ ] pitzDaily
          - [ ] RAS
              - [ ] aerofoilNACA0012
              - [ ] angledDuct
              - [ ] angledDuctLTS
              - [ ] annularThermalMixer
              - [ ] cavity
              - [ ] mixerVessel2D
              - [ ] nacaAirfoil
              - [ ] prism
              - [ ] squareBendLiq
          - [ ] laminar
              - [ ] blockedChannel
              - [ ] decompressionTank
              - [ ] forwardStep
              - [ ] helmholtzResonance
              - [ ] shockTube
      - [ ] rhoPorousSimpleFoam
          - [ ] angledDuctExplicit
          - [ ] angledDuctImplicit
      - [ ] rhoSimpleFoam
          - [ ] aerofoilNACA0012
          - [ ] angledDuctExplicitFixedCoeff
          - [ ] squareBend
          - [ ] squareBendLiq
  - [ ] discreteMethods
      - [ ] dsmcFoam
          - [ ] freeSpacePeriodic
          - [ ] freeSpaceStream
          - [ ] supersonicCorner
          - [ ] wedge15Ma5
      - [ ] molecularDynamics
          - [ ] mdEquilibrationFoam
              - [ ] periodicCubeArgon
              - [ ] periodicCubeWater
          - [ ] mdFoam
              - [ ] nanoNozzle
  - [ ] electromagnetics
      - [ ] electrostaticFoam
          - [ ] chargedWire
      - [ ] mhdFoam
          - [ ] hartmann
  - [x] financial
      - [x] financialFoam
          - [x] europeanCall
  - [ ] heatTransfer
      - [ ] buoyantPimpleFoam
          - [ ] BernardCells
          - [ ] hotRoom
          - [ ] hotRoomBoussinesq
      - [ ] buoyantSimpleFoam
          - [ ] buoyantCavity
          - [ ] circuitBoardCooling
          - [ ] externalCoupledCavity
          - [ ] hotRadiationRoom
          - [ ] hotRadiationRoomFvDOM
          - [ ] hotRoomBoussinesq
          - [ ] iglooWithFridges
      - [ ] chtMultiRegionFoam
          - [ ] coolingSphere
          - [ ] heatExchanger
          - [ ] heatedDuct
          - [ ] reverseBurner
          - [ ] shellAndTubeHeatExchanger
  - [ ] incompressible
      - [ ] SRFPimpleFoam
          - [ ] rotor2D
      - [ ] SRFSimpleFoam
          - [ ] mixer
      - [ ] adjointShapeOptimizationFoam
          - [ ] pitzDaily
      - [ ] boundaryFoam
          - [ ] boundaryLaunderSharma
          - [ ] boundaryWallFunctions
          - [ ] boundaryWallFunctionsProfile
      - [ ] icoFoam
          - [ ] cavity
              - [ ] cavity
              - [ ] cavityClipped
              - [ ] cavityGrade
          - [x] elbow
      - [ ] nonNewtonianIcoFoam
          - [ ] offsetCylinder
      - [ ] pimpleFoam
          - [ ] LES
              - [ ] channel395
          - [ ] RAS
              - [ ] TJunction
              - [ ] TJunctionFan
              - [ ] elipsekkLOmega
              - [ ] impeller
              - [ ] oscillatingInletACMI2D
              - [ ] pitzDaily
              - [ ] pitzDailyLTS
              - [ ] propeller
              - [ ] wingMotion
          - [ ] laminar
              - [ ] blockedChannel
              - [ ] mixerVesselAMI2D
              - [ ] movingCone
              - [ ] offsetCylinder
              - [ ] planarContraction
              - [ ] planarCouette
              - [ ] planarPoiseuille
      - [ ] pisoFoam
          - [ ] LES
              - [ ] motorBike
              - [ ] pitzDaily
              - [ ] pitzDailyMapped
          - [ ] RAS
              - [ ] cavity
              - [ ] cavityCoupledU
          - [ ] laminar
              - [ ] porousBlockage
      - [ ] porousSimpleFoam
          - [ ] angledDuctExplicit
          - [ ] angledDuctImplicit
          - [ ] straightDuctImplicit
      - [ ] shallowWaterFoam
          - [ ] squareBump
      - [ ] simpleFoam
          - [ ] T3A
          - [x] airFoil2D
          - [ ] mixerVessel2D
          - [ ] motorBike
          - [x] pipeCyclic
          - [ ] pitzDaily
          - [ ] pitzDailyExptInlet
          - [ ] rotorDisk
          - [ ] turbineSiting
          - [ ] windAroundBuildings
  - [ ] lagrangian
      - [ ] DPMFoam
          - [ ] Goldschmidt
      - [ ] MPPICFoam
          - [ ] Goldschmidt
          - [ ] column
          - [ ] cyclone
          - [ ] injectionChannel
      - [ ] coalChemistryFoam
          - [ ] simplifiedSiwek
      - [ ] icoUncoupledKinematicParcelFoam
          - [ ] hopper
              - [ ] hopperEmptying
              - [ ] hopperInitialState
          - [ ] mixerVesselAMI2D
      - [ ] reactingParcelFoam
          - [ ] counterFlowFlame2DLTS
          - [ ] cylinder
          - [ ] filter
          - [ ] hotBoxes
          - [ ] parcelInBox
          - [ ] rivuletPanel
          - [ ] splashPanel
          - [ ] verticalChannel
          - [ ] verticalChannelLTS
      - [ ] simpleReactingParcelFoam
          - [ ] verticalChannel
      - [ ] sprayFoam
          - [ ] aachenBomb
  - [ ] mesh
      - [ ] blockMesh
          - [ ] pipe
          - [ ] sphere
          - [ ] sphere7
          - [ ] sphere7ProjectedEdges
      - [ ] foamyHexMesh
          - [ ] blob
          - [ ] flange
          - [ ] mixerVessel
          - [ ] simpleShapes
          - [ ] straightDuctImplicit → ../../incompressible/porousSimpleFoam/straightDuctImplicit
      - [ ] foamyQuadMesh
          - [ ] jaggedBoundary
          - [ ] square
      - [ ] moveDynamicMesh
          - [ ] SnakeRiverCanyon
      - [ ] refineMesh
          - [ ] refineFieldDirs
      - [ ] snappyHexMesh
          - [ ] flange
          - [ ] iglooWithFridges → ../../heatTransfer/buoyantSimpleFoam/iglooWithFridges
          - [ ] motorBike → ../../incompressible/simpleFoam/motorBike
  - [ ] multiphase
      - [x] cavitatingFoam
          - [x] LES
              - [x] throttle
              - [x] throttle3D
          - [x] RAS
              - [x] throttle
      - [ ] compressibleInterFoam
          - [ ] laminar
              - [ ] climbingRod
              - [ ] depthCharge2D
              - [ ] depthCharge3D
              - [x] sloshingTank2D
      - [x] compressibleMultiphaseInterFoam
          - [x] laminar
              - [x] damBreak4phase
      - [ ] driftFluxFoam
          - [ ] RAS
              - [ ] dahl
              - [ ] mixerVessel2D
              - [ ] tank3D
      - [ ] interFoam
          - [x] LES
              - [x] nozzleFlow2D
          - [ ] RAS
              - [x] DTCHull
              - [ ] DTCHullMoving
              - [ ] DTCHullWave
              - [ ] angledDuct
              - [ ] damBreak
              - [ ] damBreakPorousBaffle
              - [ ] floatingObject
              - [x] mixerVesselAMI
              - [ ] waterChannel
              - [ ] weirOverflow
          - [ ] laminar
              - [ ] capillaryRise
              - [ ] damBreak
              - [x] damBreakWithObstacle
              - [ ] mixerVessel2D
              - [ ] sloshingCylinder
              - [ ] sloshingTank2D
              - [ ] sloshingTank2D3DoF
              - [ ] sloshingTank3D
              - [ ] sloshingTank3D3DoF
              - [x] sloshingTank3D6DoF
              - [ ] testTubeMixer
              - [ ] wave
      - [x] interMixingFoam
          - [x] laminar
              - [x] damBreak
      - [ ] interPhaseChangeFoam
          - [ ] cavitatingBullet
          - [x] propeller
      - [ ] multiphaseEulerFoam
          - [ ] bubbleColumn
          - [ ] damBreak4phase
          - [ ] damBreak4phaseFine
          - [ ] mixerVessel2D
      - [x] multiphaseInterFoam
          - [x] laminar
              - [x] damBreak4phase
              - [x] damBreak4phaseFine
              - [x] mixerVessel2D
      - [ ] potentialFreeSurfaceFoam
          - [ ] movingOscillatingBox
          - [ ] oscillatingBox
      - [ ] reactingMultiphaseEulerFoam
          - [ ] RAS
              - [ ] wallBoiling1D_2phase
              - [ ] wallBoiling1D_3phase
          - [ ] laminar
              - [ ] bed
              - [ ] bubbleColumn
              - [ ] bubbleColumnFixedPolydisperse
              - [ ] bubbleColumnPolydisperse
              - [ ] mixerVessel2D
              - [ ] trickleBed
      - [ ] reactingTwoPhaseEulerFoam
          - [ ] LES
              - [ ] bubbleColumn
          - [ ] RAS
              - [ ] LBend
              - [ ] bubbleColumn
              - [ ] bubbleColumnEvaporatingReacting
              - [ ] bubbleColumnPolydisperse
              - [ ] fluidisedBed
              - [ ] wallBoiling
              - [ ] wallBoiling1D
              - [ ] wallBoilingIATE
              - [ ] wallBoilingPolyDisperse
          - [ ] laminar
              - [ ] bubbleColumn
              - [ ] bubbleColumnEvaporating
              - [ ] bubbleColumnEvaporatingDissolving
              - [ ] bubbleColumnIATE
              - [ ] fluidisedBed
              - [ ] injection
              - [ ] mixerVessel2D
              - [ ] steamInjection
      - [ ] twoLiquidMixingFoam
          - [ ] lockExchange
      - [ ] twoPhaseEulerFoam
          - [ ] LES
              - [ ] bubbleColumn
          - [ ] RAS
              - [ ] bubbleColumn
              - [ ] fluidisedBed
          - [ ] laminar
              - [ ] bubbleColumn
              - [ ] bubbleColumnIATE
              - [ ] fluidisedBed
              - [ ] injection
              - [ ] mixerVessel2D
  - [ ] resources
      - [ ] geometry
  - [x] stressAnalysis
      - [x] solidDisplacementFoam
          - [x] plateHole
      - [x] solidEquilibriumDisplacementFoam
          - [x] beamEndLoad
</details>

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repository and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Iydon Liang - [@iydon](https://github.com/iydon) - liangiydon@gmail.com

Project Link: [https://github.com/iydon/of.yaml](https://github.com/iydon/of.yaml)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/iydon/of.yaml.svg?style=for-the-badge
[contributors-url]: https://github.com/iydon/of.yaml/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/iydon/of.yaml.svg?style=for-the-badge
[forks-url]: https://github.com/iydon/of.yaml/network/members
[stars-shield]: https://img.shields.io/github/stars/iydon/of.yaml.svg?style=for-the-badge
[stars-url]: https://github.com/iydon/of.yaml/stargazers
[issues-shield]: https://img.shields.io/github/issues/iydon/of.yaml.svg?style=for-the-badge
[issues-url]: https://github.com/iydon/of.yaml/issues
[license-shield]: https://img.shields.io/github/license/iydon/of.yaml.svg?style=for-the-badge
[license-url]: https://github.com/iydon/of.yaml/blob/master/LICENSE.txt
