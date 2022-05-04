from conans import ConanFile


# -----------------------------------------------------------------------------
def configure(params={}):
    pass


# -----------------------------------------------------------------------------
def requirements(params={}):
    conanfile: ConanFile = params["conanfile"]

    conanfile.requires("gtest/1.11.0")
