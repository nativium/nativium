#pragma once

#include "nativium/core/ApplicationCore.hpp"

#include <memory>

namespace nativium
{
namespace core
{

class ApplicationCoreImpl : public ApplicationCore
{
public:
    ApplicationCoreImpl();
    virtual ~ApplicationCoreImpl() {}

    static std::shared_ptr<ApplicationCoreImpl> internalSharedInstance();

    double multiply(double value1, double value2) override;
    std::string getVersion() override;

private:
    static std::shared_ptr<ApplicationCoreImpl> instance;
};

} // namespace core
} // namespace nativium
