#include "fvCFD.H"

// Include the headers for the custom library.
// The library can implement anything from a simple function to several different
// classes. The main advantage of libraries is that they allow the same code to be
// compiled once and used by many other pieces of code later on.
// NOTE: check how the Make/options changed to make sure the additional code gets
// linked to the current utility.
#include "customLibrary.H"

int main(int argc, char *argv[]) {
    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"
    #include "createFields.H"

    const dimensionedVector originVector("x0", dimLength, vector(0.05, 0.05, 0.005));
    scalar f (1.);
    // NOTE: initialise the radius field with zero values and dimensions
    volScalarField r (
        IOobject (
            "r",
            runTime.timeName(),
            mesh,
            IOobject::NO_READ,
            IOobject::NO_WRITE
        ),
        mesh,
        dimensionedScalar("r0", dimLength, 0.)
    );
    // NOTE: use the method implemented in the library to calculate r and rFarCell
    const scalar rFarCell = computeR(mesh, r, originVector);

    Info << "\nStarting time loop\n" << endl;

    while (runTime.loop()) {
        Info << "Time = " << runTime.timeName() << nl << endl;

        p = Foam::sin(2.*constant::mathematical::pi*f*runTime.time().value())
            / (r/rFarCell + dimensionedScalar("small", dimLength, 1e-12))
            * dimensionedScalar("tmp", dimensionSet(0, 3, -2, 0, 0), 1.);
        p.correctBoundaryConditions();

        // NOTE: call the library method to calculate U
        computeU(mesh, U);

        runTime.write();
    }

    Info << "End\n" << endl;

    return 0;
}
