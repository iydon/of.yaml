/*
    Description
        myCustomScheme differencing scheme class.
*/

#include "OFtutorial15.H"
#include "fvMesh.H"

namespace Foam {
    // Call compiler macro defined in surfaceInterpolationScheme.H in order to
    //  add the constructor of the new scheme to the runtime selection tables.
    makeSurfaceInterpolationScheme(myCustomScheme)
}
