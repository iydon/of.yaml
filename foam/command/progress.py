__all__ = ['Default', 'Apps']


import re
import typing as t

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

class AppBase(Default):
    def __init__(self, foam: 'Foam') -> None:
        import tqdm

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

class AppByTime(AppBase):
    '''
    - solver:
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

class AppByIterationI(AppBase):
    '''
    - solver:
        - electromagnetics:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/electromagnetics/electrostaticFoam/electrostaticFoam.C
    '''
    def now(self, line):
        line = line.strip()
        if line.startswith(b'Iteration = '):
            return float(line[12:])

class AppByIterationII(AppBase):
    '''
    - solver:
        - stressAnalysis:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/stressAnalysis/solidEquilibriumDisplacementFoam/solidEquilibriumDisplacementFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/solvers/stressAnalysis/solidDisplacementFoam/solidDisplacementFoam.C
    '''
    def now(self, line):
        line = line.strip()
        if line.startswith(b'Iteration: '):
            return float(line[11:])

class AppByOther(AppBase):
    '''
    - solver:
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
    - utility:
        - postProcessing:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/postProcess/postProcess.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/lagrangian/steadyParticleTracks/steadyParticleTracks.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/lagrangian/particleTracks/particleTracks.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/miscellaneous/engineCompRatio/engineCompRatio.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/miscellaneous/temporalInterpolate/temporalInterpolate.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/miscellaneous/pdfPlot/pdfPlot.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/miscellaneous/postChannel/postChannel.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/graphics/PVReaders/vtkPVFoam/vtkPVFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/graphics/PVReaders/vtkPVblockMesh/vtkPVblockMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/noise/noise.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/dataConversion/foamToTecplot360/foamToTecplot360.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/dataConversion/smapToFoam/smapToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/dataConversion/foamToGMV/foamToGMV.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/dataConversion/foamToTetDualMesh/foamToTetDualMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/dataConversion/foamDataToFluent/foamDataToFluent.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/dataConversion/foamToEnsight/foamToEnsight.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/postProcessing/dataConversion/foamToEnsightParts/foamToEnsightParts.C
        - mesh:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/removeFaces/removeFaces.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/modifyMesh/modifyMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/collapseEdges/collapseEdges.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/splitCells/splitCells.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/PDRMesh/PDRMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/refineWallLayer/refineWallLayer.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/refinementLevel/refinementLevel.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/autoRefineMesh/autoRefineMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/selectCells/selectCells.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/combinePatchFaces/combinePatchFaces.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/advanced/refineHexMesh/refineHexMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/foamToStarMesh/foamToStarMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/fluent3DMeshToFoam/fluent3DMeshToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/vtkUnstructuredToFoam/vtkUnstructuredToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/Optional/ccm26ToFoam/ccm26ToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/foamToSurface/foamToSurface.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/ideasUnvToFoam/ideasUnvToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/netgenNeutralToFoam/netgenNeutralToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/gmshToFoam/gmshToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/writeMeshObj/writeMeshObj.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/mshToFoam/mshToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/ansysToFoam/ansysToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/foamMeshToFluent/foamMeshToFluent.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/gambitToFoam/gambitToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/plot3dToFoam/plot3dToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/fluentMeshToFoam/fluentMeshToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/star4ToFoam/star4ToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/datToFoam/datToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/tetgenToFoam/tetgenToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/cfx4ToFoam/cfx4ToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/sammToFoam/sammToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/star3ToFoam/star3ToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/conversion/kivaToFoam/kivaToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/splitMeshRegions/splitMeshRegions.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/stitchMesh/stitchMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/createPatch/createPatch.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/polyDualMesh/polyDualMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/moveEngineMesh/moveEngineMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/moveMesh/moveMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/moveDynamicMesh/moveDynamicMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/renumberMesh/renumberMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/rotateMesh/rotateMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/deformedGeom/deformedGeom.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/objToVTK/objToVTK.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/zipUpMesh/zipUpMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/transformPoints/transformPoints.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/mergeOrSplitBaffles/mergeOrSplitBaffles.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/attachMesh/attachMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/setsToZones/setsToZones.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/singleCellMesh/singleCellMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/orientFaceZone/orientFaceZone.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/topoSet/topoSet.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/mergeMeshes/mergeMeshes.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/setSet/setSet.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/createBaffles/createBaffles.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/checkMesh/checkMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/autoPatch/autoPatch.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/refineMesh/refineMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/insideCells/insideCells.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/mirrorMesh/mirrorMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/splitMesh/splitMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/flattenMesh/flattenMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/manipulation/subsetMesh/subsetMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/extrude/extrudeMesh/extrudeMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/extrude/extrudeToRegionMesh/extrudeToRegionMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/snappyHexMesh/snappyHexMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/extrude2DMesh/extrude2DMesh/extrude2DMesh/extrude2DMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/blockMesh/blockMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/foamyMesh/foamyHexMeshSurfaceSimplify/foamyHexMeshSurfaceSimplify.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/foamyMesh/foamyHexMesh/foamyHexMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/foamyMesh/foamyQuadMesh/foamyQuadMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/foamyMesh/foamyHexMeshBackgroundMesh/foamyHexMeshBackgroundMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/mesh/generation/foamyMesh/cellSizeAndAlignmentGrid/cellSizeAndAlignmentGrid.C
        - miscellaneous:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/miscellaneous/foamDictionary/foamDictionary.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/miscellaneous/foamListTimes/foamListTimes.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/miscellaneous/foamFormatConvert/foamFormatConvert.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/miscellaneous/patchSummary/patchSummary.C
        - parallelProcessing:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/parallelProcessing/reconstructParMesh/reconstructParMesh.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/parallelProcessing/decomposePar/decomposePar.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/parallelProcessing/reconstructPar/reconstructPar.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/parallelProcessing/redistributePar/redistributePar.C
        - thermophysical:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/thermophysical/chemkinToFoam/chemkinToFoam.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/thermophysical/equilibriumFlameT/equilibriumFlameT.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/thermophysical/mixtureAdiabaticFlameT/mixtureAdiabaticFlameT.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/thermophysical/equilibriumCO/equilibriumCO.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/thermophysical/adiabaticFlameT/adiabaticFlameT.C
        - preProcessing:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/createExternalCoupledPatchGeometry/createExternalCoupledPatchGeometry.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/changeDictionary/changeDictionary.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/applyBoundaryLayer/applyBoundaryLayer.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/mdInitialise/mdInitialise.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/faceAgglomerate/faceAgglomerate.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/wallFunctionTable/wallFunctionTable.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/engineSwirl/engineSwirl.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/mapFieldsPar/mapFieldsPar.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/setWaves/setWaves.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/dsmcInitialise/dsmcInitialise.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/foamSetupCHT/foamSetupCHT.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/setFields/setFields.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/viewFactorsGen/viewFactorsGen.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/mapFields/mapFields.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/boxTurb/boxTurb.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/preProcessing/foamUpgradeCyclics/foamUpgradeCyclics.C
        - surface:
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceConvert/surfaceConvert.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceAutoPatch/surfaceAutoPatch.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceTransformPoints/surfaceTransformPoints.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceMeshExport/surfaceMeshExport.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceOrient/surfaceOrient.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceMeshConvertTesting/surfaceMeshConvertTesting.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceMeshConvert/surfaceMeshConvert.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceSplitByTopology/surfaceSplitByTopology.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceSplitNonManifolds/surfaceSplitNonManifolds.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceFeatureExtract/surfaceFeatureExtract.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceFeatures/surfaceFeatures.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceToPatch/surfaceToPatch.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceCheck/surfaceCheck.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceRedistributePar/surfaceRedistributePar.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceRefineRedGreen/surfaceRefineRedGreen.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceLambdaMuSmooth/surfaceLambdaMuSmooth.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceSplitByPatch/surfaceSplitByPatch.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceMeshInfo/surfaceMeshInfo.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceAdd/surfaceAdd.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceMeshImport/surfaceMeshImport.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceHookUp/surfaceHookUp.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceSubset/surfaceSubset.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceFeatureConvert/surfaceFeatureConvert.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceClean/surfaceClean.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceCoarsen/surfaceCoarsen.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfacePointMerge/surfacePointMerge.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceBooleanFeatures/surfaceBooleanFeatures.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceInertia/surfaceInertia.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceFind/surfaceFind.C
            - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/surface/surfaceMeshTriangulate/surfaceMeshTriangulate.C
    '''
    def now(self, _):
        raise NotImplementedError


Apps = {}
pattern = re.compile(r'\w+(?=\.C)')
for App in [AppByTime, AppByIterationI, AppByIterationII]:
    for name in pattern.findall(App.__doc__):
        Apps[name] = App
