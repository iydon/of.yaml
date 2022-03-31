__all__ = ['Default', 'Apps']


import re
import typing as t

import tqdm

if t.TYPE_CHECKING:
    from ..core import Foam


class Default:
    def __init__(self, foam: 'Foam') -> None:
        pass

    def __enter__(self) -> 'Default':
        return self

    def __exit__(self, type, value, traceback) -> None:
        pass

    def step(self, line: bytes) -> None:
        pass

    def close(self) -> None:
        pass

class FoamBase(Default):
    def __init__(self, foam: 'Foam') -> None:
        self._foam = foam
        start = float(foam['foam']['system', 'controlDict', 'startTime'])
        end = float(foam['foam']['system', 'controlDict', 'endTime'])
        self.pbar = tqdm.tqdm(total=end-start)
        self._new = self._old = start

    def __exit__(self, type, value, traceback) -> None:
        self.pbar.close()

    def step(self, line: bytes) -> None:
        now = self.now(line) or self._new
        self._new, self._old = now, self._new
        self.pbar.update(self._new-self._old)

    def now(self, line: bytes) -> t.Optional[float]:
        raise NotImplementedError

class FoamByTime(FoamBase):
    '''
    - multiphase:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/cavitatingFoam/cavitatingFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/driftFluxFoam/driftFluxFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/compressibleMultiphaseInterFoam/compressibleMultiphaseInterFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/interPhaseChangeFoam/interPhaseChangeFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/potentialFreeSurfaceFoam/potentialFreeSurfaceFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/reactingEulerFoam/reactingMultiphaseEulerFoam/reactingMultiphaseEulerFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/reactingEulerFoam/reactingTwoPhaseEulerFoam/reactingTwoPhaseEulerFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/twoLiquidMixingFoam/twoLiquidMixingFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/compressibleInterFoam/compressibleInterFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/compressibleInterFoam/compressibleInterFilmFoam/compressibleInterFilmFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/interFoam/interFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/interFoam/interMixingFoam/interMixingFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/multiphaseEulerFoam/multiphaseEulerFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/twoPhaseEulerFoam/twoPhaseEulerFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/multiphase/multiphaseInterFoam/multiphaseInterFoam.C
    - discreteMethods:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/discreteMethods/molecularDynamics/mdFoam/mdFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/discreteMethods/molecularDynamics/mdEquilibrationFoam/mdEquilibrationFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/discreteMethods/dsmc/dsmcFoam/dsmcFoam.C
    - heatTransfer:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/heatTransfer/thermoFoam/thermoFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/heatTransfer/chtMultiRegionFoam/chtMultiRegionFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/heatTransfer/buoyantSimpleFoam/buoyantSimpleFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/heatTransfer/buoyantPimpleFoam/buoyantPimpleFoam.C
    - combustion:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/combustion/reactingFoam/reactingFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/combustion/reactingFoam/rhoReactingFoam/rhoReactingFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/combustion/reactingFoam/rhoReactingBuoyantFoam/rhoReactingBuoyantFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/combustion/fireFoam/fireFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/combustion/XiFoam/XiFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/combustion/PDRFoam/PDRFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/combustion/chemFoam/chemFoam.C
    - DNS:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/DNS/dnsFoam/dnsFoam.C
    - incompressible:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/nonNewtonianIcoFoam/nonNewtonianIcoFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/adjointShapeOptimizationFoam/adjointShapeOptimizationFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/shallowWaterFoam/shallowWaterFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/boundaryFoam/boundaryFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/pimpleFoam/pimpleFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/pimpleFoam/SRFPimpleFoam/SRFPimpleFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/pisoFoam/pisoFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/simpleFoam/simpleFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/simpleFoam/SRFSimpleFoam/SRFSimpleFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/simpleFoam/porousSimpleFoam/porousSimpleFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/incompressible/icoFoam/icoFoam.C
    - electromagnetics:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/electromagnetics/mhdFoam/mhdFoam.C
    - lagrangian:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/lagrangian/reactingParcelFoam/reactingParcelFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/lagrangian/reactingParcelFoam/simpleReactingParcelFoam/simpleReactingParcelFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/lagrangian/coalChemistryFoam/coalChemistryFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/lagrangian/uncoupledKinematicParcelFoam/uncoupledKinematicParcelFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/lagrangian/DPMFoam/DPMFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/lagrangian/icoUncoupledKinematicParcelFoam/icoUncoupledKinematicParcelFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/lagrangian/sprayFoam/sprayFoam.C
    - compressible:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/compressible/rhoPimpleFoam/rhoPimpleFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/compressible/rhoCentralFoam/rhoCentralFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/compressible/rhoSimpleFoam/rhoSimpleFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/compressible/rhoSimpleFoam/rhoPorousSimpleFoam/rhoPorousSimpleFoam.C
    - basic:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/basic/laplacianFoam/laplacianFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/basic/scalarTransportFoam/scalarTransportFoam.C
    '''
    def now(self, line):
        line = line.strip()
        if line.startswith(b'Time = '):
            return float(line[7:])

class FoamByIterationI(FoamBase):
    '''
    - electromagnetics:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/electromagnetics/electrostaticFoam/electrostaticFoam.C
    '''
    def now(self, line):
        line = line.strip()
        if line.startswith(b'Iteration = '):
            return float(line[12:])

class FoamByIterationII(FoamBase):
    '''
    - stressAnalysis:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/stressAnalysis/solidEquilibriumDisplacementFoam/solidEquilibriumDisplacementFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/stressAnalysis/solidDisplacementFoam/solidDisplacementFoam.C
    '''
    def now(self, line):
        line = line.strip()
        if line.startswith(b'Iteration: '):
            return float(line[11:])

class FoamByOther(FoamBase):
    '''
    - combustion:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/combustion/XiFoam/XiEngineFoam/XiEngineFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/combustion/coldEngineFoam/coldEngineFoam.C
    - electromagnetics:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/electromagnetics/magneticFoam/magneticFoam.C
    - lagrangian:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/lagrangian/DPMFoam/MPPICFoam/MPPICFoam.C
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/lagrangian/sprayFoam/engineFoam/engineFoam.C
    - financial:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/financial/financialFoam/financialFoam.C
    - basic:
        - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/basic/potentialFoam/potentialFoam.C
    '''
    def now(self, line):
        raise NotImplementedError


Apps = {}
pattern = re.compile(r'\w+Foam(?=\.C)')
for Class in [FoamByTime, FoamByIterationI, FoamByIterationII]:
    for key in pattern.findall(Class.__doc__):
        Apps[key] = Class
