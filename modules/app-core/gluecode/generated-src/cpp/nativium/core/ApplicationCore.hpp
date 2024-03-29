// AUTOGENERATED FILE - DO NOT MODIFY!
// This file was generated by Djinni from proj.djinni

#pragma once

#include <memory>
#include <string>

namespace nativium::core {

class ApplicationCore {
public:
    virtual ~ApplicationCore() = default;

    static /*not-null*/ std::shared_ptr<ApplicationCore> shared();

    virtual double multiply(double value1, double value2) = 0;

    virtual std::string getVersion() = 0;
};

} // namespace nativium::core
