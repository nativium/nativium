// AUTOGENERATED FILE - DO NOT MODIFY!
// This file was generated by Djinni from proj.djinni

#pragma once

#include "djinni/jni/djinni_support.hpp"
#include "nativium/core/ApplicationCore.hpp"

namespace djinni_generated {

class NTVCoreApplicationCore final : ::djinni::JniInterface<::nativium::core::ApplicationCore, NTVCoreApplicationCore> {
public:
    using CppType = std::shared_ptr<::nativium::core::ApplicationCore>;
    using CppOptType = std::shared_ptr<::nativium::core::ApplicationCore>;
    using JniType = jobject;

    using Boxed = NTVCoreApplicationCore;

    ~NTVCoreApplicationCore();

    static CppType toCpp(JNIEnv* jniEnv, JniType j) { return ::djinni::JniClass<NTVCoreApplicationCore>::get()._fromJava(jniEnv, j); }
    static ::djinni::LocalRef<JniType> fromCppOpt(JNIEnv* jniEnv, const CppOptType& c) { return {jniEnv, ::djinni::JniClass<NTVCoreApplicationCore>::get()._toJava(jniEnv, c)}; }
    static ::djinni::LocalRef<JniType> fromCpp(JNIEnv* jniEnv, const CppType& c) { return fromCppOpt(jniEnv, c); }

private:
    NTVCoreApplicationCore();
    friend ::djinni::JniClass<NTVCoreApplicationCore>;
    friend ::djinni::JniInterface<::nativium::core::ApplicationCore, NTVCoreApplicationCore>;

};

} // namespace djinni_generated
