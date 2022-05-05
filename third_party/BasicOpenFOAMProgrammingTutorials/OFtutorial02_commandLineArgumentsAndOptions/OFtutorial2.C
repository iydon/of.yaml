#include "fvCFD.H"

int main(int argc, char *argv[]) {
    // ===
    // Define the help message for this application
    argList::addNote (
        "Demonstrates how to handle command line options.\n"
        "\n"
        "Input arguments:\n"
        "----------------\n"
        "  someWord - does stuff\n"
        "  someScalar - does more things\n"
    );

    // prepare argument list
    argList::noParallel();
    argList::validArgs.append("someWord");
    argList::validArgs.append("someScalar");

    // prepare options
    argList::addOption ( // string variable
        "dict",
        "word",
        "Path to an additional dictionary (not really used now)"
    );

    argList::addBoolOption ( // on/off depending on whether option is given or not
        "someSwitch",
        "Switches from A to B"
    );

    argList::addOption ( // integer variable
        "someInt",
        "label",
        "Optional integer"
    );

    // ===
    // create argument list
    // This is normally defined inside setRootCase.H
    // #include "setRootCase.H"
    Foam::argList args(argc, argv);
    if (!args.checkRootCase()) {
        Foam::FatalError.exit();
    }

    // ===
    // read arguments
    const word someWord = args[1];
    // NOTE: the built-in method for converting strings to other data types
    const scalar someScalar = args.argRead<scalar>(2);

    Info << "Got argument word " << someWord << " and scalar " << someScalar << endl;

    // ===
    // read options
    // default path to some dictionary
    fileName dictPath("./system/defaultDict");

    // conditional execution based on an option being passed
    if (args.optionFound("dict")) {
        args.optionReadIfPresent("dict", dictPath);
        Info << "Got an override flag for dictionary path" << endl;
    }
    Info << "Would read dict from " << dictPath << endl;

    // switch option
    const bool someConstBool = args.optionFound("someSwitch");
    Info << "Boolean switch set to " << someConstBool << endl;

    // numeric value option - same as string variables really
    label someInt(0);
    args.optionReadIfPresent("someInt", someInt);
    Info << "Integer option value " << someInt << endl;

    Info << "End\n" << endl;

    return 0;
}
