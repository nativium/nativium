Pod::Spec.new do |s|
  s.name             = '{PROJECT_NAME}'
  s.version          = '{VERSION}'
  s.summary          = '{PRODUCT_NAME} Pod'

  s.homepage         = 'https://github.com/nativium/nativium'
  s.license          = { :type => 'MIT', :text => 'Free' }
  s.author           = { 'Paulo Coutinho' => 'paulocoutinhox@gmail.com' }
  s.source           = { :http => 'https://nativium.s3.amazonaws.com/dist/ios/{VERSION}/dist.tar.gz' }

  s.vendored_frameworks = '{BUILD_TYPE}/{PROJECT_NAME}.{PACKAGE_EXTENSION}'

  s.ios.deployment_target = '9.0'
  s.watchos.deployment_target = '5.0'
  s.tvos.deployment_target = '11.0'

  s.public_header_files = '{BUILD_TYPE}/{PROJECT_NAME}.{PACKAGE_EXTENSION}/{XCFRAMEWORK_GROUP_DIR}/{PROJECT_NAME}.framework/Headers/**/*.h'
  s.source_files = '{BUILD_TYPE}/{PROJECT_NAME}.{PACKAGE_EXTENSION}/{XCFRAMEWORK_GROUP_DIR}/{PROJECT_NAME}.framework/Headers/**/*.h'

  s.requires_arc = true

  s.user_target_xcconfig = {
    'USER_HEADER_SEARCH_PATHS' => '"$(PODS_ROOT)/{PROJECT_NAME}/{BUILD_TYPE}" "$(PODS_ROOT)/{PROJECT_NAME}/{BUILD_TYPE}/{PROJECT_NAME}.{PACKAGE_EXTENSION}/{XCFRAMEWORK_GROUP_DIR}/{PROJECT_NAME}.framework/Headers"',
    'FRAMEWORK_SEARCH_PATHS' => '"$(PODS_ROOT)/{PROJECT_NAME}/{BUILD_TYPE}"'
  }
end
