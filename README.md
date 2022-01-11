# OpenFOAM Tutorials in YAML Format

| YAML | OpenFOAM | Version | Solver |
| --- | --- | --- | --- |
| [airFoil2D.yaml](tutorials/incompressible/simpleFoam/airFoil2D.yaml) | [airFoil2D](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/incompressible/simpleFoam/airFoil2D) | 7 | [incompressible/simpleFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/incompressible/simpleFoam) |
| [beamEndLoad.yaml](tutorials/stressAnalysis/solidEquilibriumDisplacementFoam/beamEndLoad.yaml) | [beamEndLoad](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/stressAnalysis/solidEquilibriumDisplacementFoam/beamEndLoad) | 7 | [stressAnalysis/solidEquilibriumDisplacementFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/stressAnalysis/solidEquilibriumDisplacementFoam) |
| [boxTurb16.yaml](tutorials/DNS/dnsFoam/boxTurb16.yaml) | [boxTurb16](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/DNS/dnsFoam/boxTurb16) | 7 | [DNS/dnsFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/DNS/dnsFoam) |
| [cylinder.yaml](tutorials/basic/potentialFoam/cylinder.yaml) | [cylinder](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/basic/potentialFoam/cylinder) | 7 | [basic/potentialFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/basic/potentialFoam) |
| [damBreak.yaml](tutorials/multiphase/interMixingFoam/laminar/damBreak.yaml) | [damBreak](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interMixingFoam/laminar/damBreak) | 7 | [multiphase/interMixingFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interFoam/interMixingFoam) |
| [damBreakWithObstacle.yaml](tutorials/multiphase/interFoam/laminar/damBreakWithObstacle.yaml) | [damBreakWithObstacle](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interFoam/laminar/damBreakWithObstacle) | 7 | [multiphase/interFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interFoam) |
| [elbow.yaml](tutorials/incompressible/icoFoam/elbow.yaml) | [elbow](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/incompressible/icoFoam/elbow) | 7 | [incompressible/icoFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/incompressible/icoFoam) |
| [fileHandler.yaml](tutorials/IO/fileHandler.yaml) | [fileHandler](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/IO/fileHandler) | 7 | [lagrangian/icoUncoupledKinematicParcelFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/lagrangian/icoUncoupledKinematicParcelFoam) |
| [flange.yaml](tutorials/basic/laplacianFoam/flange.yaml) | [flange](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/basic/laplacianFoam/flange) | 7 | [basic/laplacianFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/basic/laplacianFoam) |
| [pipeCyclic.yaml](tutorials/incompressible/simpleFoam/pipeCyclic.yaml) | [pipeCyclic](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/incompressible/simpleFoam/pipeCyclic) | 7 | [incompressible/simpleFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/incompressible/simpleFoam) |
| [pitzDaily.yaml](tutorials/basic/potentialFoam/pitzDaily.yaml) | [pitzDaily](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/basic/potentialFoam/pitzDaily) | 7 | [basic/potentialFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/basic/potentialFoam) |
| [plateHole.yaml](tutorials/stressAnalysis/solidDisplacementFoam/plateHole.yaml) | [plateHole](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/stressAnalysis/solidDisplacementFoam/plateHole) | 7 | [stressAnalysis/solidDisplacementFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/stressAnalysis/solidDisplacementFoam) |
| [sloshingTank3D6DoF.yaml](tutorials/multiphase/interFoam/laminar/sloshingTank3D6DoF.yaml) | [sloshingTank3D6DoF](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interFoam/laminar/sloshingTank3D6DoF) | 7 | [multiphase/interFoam](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/applications/solvers/multiphase/interFoam) |



# To-Do List

- [x] DNS
    - [x] dnsFoam
        - [x] boxTurb16
- [x] IO
    - [x] fileHandler
- [ ] basic
    - [x] laplacianFoam
        - [x] flange
    - [x] potentialFoam
        - [x] cylinder
        - [x] pitzDaily
    - [ ] scalarTransportFoam
        - [ ] pitzDaily
- [ ] combustion
    - [ ] PDRFoam
        - [ ] flamePropagationWithObstacles
    - [ ] XiEngineFoam
        - [ ] kivaTest
    - [ ] XiFoam
        - [ ] RAS
            - [ ] moriyoshiHomogeneous
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
- [ ] financial
    - [ ] financialFoam
        - [ ] europeanCall
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
    - [ ] cavitatingFoam
        - [ ] LES
            - [ ] throttle
            - [ ] throttle3D
        - [ ] RAS
            - [ ] throttle
    - [ ] compressibleInterFoam
        - [ ] laminar
            - [ ] climbingRod
            - [ ] depthCharge2D
            - [ ] depthCharge3D
            - [ ] sloshingTank2D
    - [ ] compressibleMultiphaseInterFoam
        - [ ] laminar
            - [ ] damBreak4phase
    - [ ] driftFluxFoam
        - [ ] RAS
            - [ ] dahl
            - [ ] mixerVessel2D
            - [ ] tank3D
    - [ ] interFoam
        - [ ] LES
            - [ ] nozzleFlow2D
        - [ ] RAS
            - [ ] DTCHull
            - [ ] DTCHullMoving
            - [ ] DTCHullWave
            - [ ] angledDuct
            - [ ] damBreak
            - [ ] damBreakPorousBaffle
            - [ ] floatingObject
            - [ ] mixerVesselAMI
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
        - [ ] propeller
    - [ ] multiphaseEulerFoam
        - [ ] bubbleColumn
        - [ ] damBreak4phase
        - [ ] damBreak4phaseFine
        - [ ] mixerVessel2D
    - [ ] multiphaseInterFoam
        - [ ] laminar
            - [ ] damBreak4phase
            - [ ] damBreak4phaseFine
            - [ ] mixerVessel2D
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
