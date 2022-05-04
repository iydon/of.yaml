#include "fvCFD.H"

int main(int argc, char *argv[]) {
    // Checks the basic folder structure, verifies there is a control dict present, etc.;
    // also deals with parsing command line arguments and options.
    // It works by taking an external piece of code, written in $FOAM_SRC/OpenFOAM/include.
    // The contents of the include file actually look like this:
    /*
        - deciphers the arguments passed to the program:
            ```
            Foam::argList args(argc, argv);
            ```
        - verifies the folder structure:
            ```
            if (!args.checkRootCase()) {
                Foam::FatalError.exit();
            }
            ```
    */
    #include "setRootCase.H"

    // OpenFOAM screen output is very similar to rudimentary C++ with its std::cout, std::nl and std::endl
    // being replaced with Foam::Info, Foam::nl, and Foam::endl.
    Info << "Hello there, I'm an OpenFOAM program!" << nl
         << "You don't need a mesh or anything to run it, just a bare OpenFOAM case will do." << nl
         << tab << "This is me again, just creating a tabulated new line, move along." << nl << endl;

    Info << "End\n" << endl;

    return 0;
}
