#include "ApplicationCoreImpl.hpp"

#include <memory>
#include <string>

namespace nativium
{
namespace core
{

std::shared_ptr<ApplicationCoreImpl> ApplicationCoreImpl::instance = nullptr;

ApplicationCoreImpl::ApplicationCoreImpl()
{
    // ignore
}

std::shared_ptr<ApplicationCore> ApplicationCore::shared()
{
    return ApplicationCoreImpl::internalSharedInstance();
}

std::shared_ptr<ApplicationCoreImpl> ApplicationCoreImpl::internalSharedInstance()
{
    if (instance == nullptr)
    {
        instance = std::make_shared<ApplicationCoreImpl>();
    }

    return instance;
}

double ApplicationCoreImpl::multiply(double value1, double value2)
{
    return (value1 * value2);
}

std::string ApplicationCoreImpl::getVersion()
{
#ifdef NATIVIUM_VERSION
#define NATIVIUM_VERSION_STR NATIVIUM_VERSION
#else
#define NATIVIUM_VERSION_STR "1.0.0"
#endif

#ifdef NATIVIUM_VERSION_CODE
#define NATIVIUM_VERSION_CODE_STR NATIVIUM_VERSION_CODE
#else
#define NATIVIUM_VERSION_CODE_STR "1"
#endif

    return std::string(NATIVIUM_VERSION_STR) + " (" + std::string(NATIVIUM_VERSION_CODE_STR) + ")";
}

} // namespace core
} // namespace nativium
