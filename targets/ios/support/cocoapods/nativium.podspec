Pod::Spec.new do |s|
  s.name             = '{PROJECT_NAME}'
  s.version          = '{VERSION}'
  s.summary          = '{PRODUCT_NAME} Pod'

  s.homepage         = 'https://github.com/nativium/nativium'
  s.license          = { :type => 'MIT', :text => 'Free' }
  s.author           = { 'Paulo Coutinho' => 'paulo@prsolucoes.com' }
  s.source           = { :http => 'https://nativium.s3.amazonaws.com/dist/ios/{VERSION}/dist.tar.gz' }

  s.vendored_frameworks = 'Release/{PROJECT_NAME}.xcframework'

  s.ios.deployment_target = '9.0'
  s.watchos.deployment_target = '5.0'
  s.tvos.deployment_target = '11.0'

  s.public_header_files = 'Release/{PROJECT_NAME}.xcframework/{XCFRAMEWORK_RELEASE_GROUP_DIR}/{PROJECT_NAME}.framework/Headers/**/*.h'
  s.source_files = 'Release/{PROJECT_NAME}.xcframework/{XCFRAMEWORK_RELEASE_GROUP_DIR}/{PROJECT_NAME}.framework/Headers/**/*.h'

  s.requires_arc = true

  s.user_target_xcconfig = {
    'USER_HEADER_SEARCH_PATHS' => '"$(PODS_ROOT)/{PROJECT_NAME}/Release" "$(PODS_ROOT)/{PROJECT_NAME}/Release/{PROJECT_NAME}.xcframework/{XCFRAMEWORK_RELEASE_GROUP_DIR}/{PROJECT_NAME}.framework/Headers"',
    'FRAMEWORK_SEARCH_PATHS' => '"$(PODS_ROOT)/{PROJECT_NAME}/Release"'
  }
end
