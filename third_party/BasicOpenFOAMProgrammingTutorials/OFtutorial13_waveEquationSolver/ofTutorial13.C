#include "fvCFD.H"

int main(int argc, char *argv[]) {
    // additional message that will be displayed in the help options
    // i.e. when running "waveFoam -help"
    argList::addNote(
     "this application solves the wave equation over given mesh"
    );

    // Set up the case, parse command line options and create the grid
    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"

    // reading amplitude field "h" data and wave speed "C"
    #include "createFields.H"

    // starting time loop
    Info << nl << "Starting time loop..." << endl;

    // wave equation has no steady state solution, i.e. always transient in
    // nature. Hence looping through runTime.

    while(runTime.loop()) {
        // printing current run time on to screen
        Info << nl << "Time = " << runTime.timeName() << endl;

        Info << "Solving h field" << endl;

        // defining the wave equation in OpenFOAM's format
        fvScalarMatrix hEqn (
           fvm::d2dt2(h) // second order temporal discretization of amplitude
           == fvm::laplacian(sqr(C), h) // laplacian operation on amplitude, in implicit way.
        );

        // solving the wave equation for current time step.
        hEqn.solve();

        // saving the current timestep solution and writing it to file when
        // insisted by "writeControl" and "writeInterval" on controlDict
        runTime.write();

        // printing execution time information i.e. how much physical time it
        // took to solve the equation
        Info << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << endl;
    }

    Info << nl << "End." << endl;

    return 0;
}
